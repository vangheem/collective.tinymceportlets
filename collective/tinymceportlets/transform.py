
from lxml import etree
from lxml.cssselect import CSSSelector
from lxml.html import fromstring

from repoze.xmliter.utils import getHTMLSerializer

from zope.interface import implements, Interface
from zope.component import adapts, getUtility, getMultiAdapter, queryMultiAdapter
from zope.site.hooks import getSite

from collective.tinymceportlets.interfaces import TinyMCEPortletsLayer
from collective.tinymceportlets import PORTLET_CLASS_IDENTIFIER
from collective.tinymceportlets.utils import decodeHash

from plone.transformchain.interfaces import ITransform
from plone.portlets.interfaces import IPortletRetriever, IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager, IPortletRenderer
from Products.CMFCore.utils import getToolByName

_portlet_selector = CSSSelector('img.' + PORTLET_CLASS_IDENTIFIER)

class TinyMCEPortletsTransform(object):
    implements(ITransform)
    adapts(Interface, TinyMCEPortletsLayer)
    
    order = 8100 # rather early off so other things, like xdv/diazo can leverage it

    def __init__(self, published, request):
        self.published = published
        self.request = request

    def transformString(self, result, encoding):
        return self.transformIterable([result], encoding)

    def transformUnicode(self, result, encoding):
        return self.transformIterable([result], encoding)

    def transformIterable(self, result, encoding):
        contentType = self.request.response.getHeader('Content-Type')
        if contentType is None or not contentType.startswith('text/html'):
            return None

        contentEncoding = self.request.response.getHeader('Content-Encoding')
        if contentEncoding and contentEncoding in ('zip', 'deflate', 'compress',):
            return None
            
        try:
            result = getHTMLSerializer(result, pretty_print=False)
        except (TypeError, etree.ParseError):
            return None

        portlets = _portlet_selector(result.tree)
        if len(portlets) > 0:
            site = getSite()
            ref_cat = getToolByName(site, 'reference_catalog')
            view = site.restrictedTraverse('@@plone')
            for tag in _portlet_selector(result.tree):
                klass = tag.attrib.get('class', '').replace(PORTLET_CLASS_IDENTIFIER, '').replace('mce-only ', '').strip()
                tag.attrib['class'] = tag.attrib.get('class', '').replace('mce-only ', '')
                manager, portletname, uid = decodeHash(klass)
                # get uid if object supports that.
                context = ref_cat.lookupObject(uid)
                if not context: # try traversing to it next
                    context = site.restrictedTraverse(uid)
                    if not context: # if not found, skip over it..
                        tag.getparent().remove(tag)
                        continue
                manager = getUtility(IPortletManager, name=manager, context=context)
                retriever = getMultiAdapter((context, manager), IPortletRetriever)
                portlet = None
                for portlet in retriever.getPortlets():
                    if portlet['name'] == portletname:
                        portlet = portlet['assignment']
                if not portlet:
                    # try and find it on the assignments
                    assignments = getMultiAdapter((context, manager), IPortletAssignmentMapping)
                    try:
                        portlet = assignments[portletname]
                    except KeyError:
                        tag.getparent().remove(tag)
                        continue
                renderer = queryMultiAdapter((context, self.request, view, manager, portlet), IPortletRenderer)
                if not renderer:
                    tag.getparent().remove(tag)
                    continue

                # Make sure we have working acquisition chain
                renderer = renderer.__of__(context)

                if not renderer:
                    return None

                renderer.update()
                html = renderer.render()
                style = tag.attrib.get('style', '')
                if style:
                    style = style.strip().strip(';') + ';'
                if tag.attrib.has_key('width'):
                    style += 'width:%spx;' % tag.attrib['width'].strip('px')
                if tag.attrib.has_key('height'):
                    style += 'height:%spx;' % tag.attrib['height'].strip('px')
                html = '<div class="tinymceportlet" style="' + style + '">' + html + '</div>'
                tag.addnext(fromstring(html))
                tag.getparent().remove(tag)
                
        return result
