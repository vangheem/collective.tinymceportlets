import unittest2 as unittest

import transaction
from plone.testing.z2 import Browser
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from collective.tinymceportlets.testing import TINYMCE_PORTLETS_FUNCTIONAL_TESTING, \
    browser_login
from collective.tinymceportlets.utils import portletHash, portletMarkup

from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from zope.component import getUtility
from zope.component import getMultiAdapter

from plone.portlet.static import static
from plone.portlets.interfaces import IPortletAssignmentSettings

class TinyMCEPortetsRendererTests(unittest.TestCase):
    layer = TINYMCE_PORTLETS_FUNCTIONAL_TESTING
    
    def setUp(self):
        self.portal = self.layer['portal']
        self.browser = Browser(self.layer['app'])
        browser_login(self.portal, self.browser)
        setRoles(self.portal, TEST_USER_ID, ('Member', 'Manager'))
    
    def test_portlet_renders_in_tiny_mce(self):
        portal = self.layer['portal']
        rightcol = getUtility(IPortletManager, name=u'plone.rightcolumn', context=portal)
        right = getMultiAdapter((portal, rightcol,), IPortletAssignmentMapping, context=portal)
        
        staticportlet = static.Assignment(header=u"Static Portlet", text=u"TEXT INPUT")
        right[u'staticportlet'] = staticportlet
        
        settings = IPortletAssignmentSettings(staticportlet)
        visible = settings.get('visible', True)
        settings['visible'] = False
        
        page = portal[portal.invokeFactory('Document', 'testpage')]
        hash = portletHash(rightcol, staticportlet, portal)
        field = page.getField('text')
        portletmarkup = portletMarkup(hash)
        field.set(page, portletmarkup, mimetype='text/html')
        page.setTitle('Blah')
        page.reindexObject()
        transaction.commit()
        
        self.browser.open('http://nohost/plone/testpage')
        
        self.failUnless("TEXT INPUT" in self.browser.contents)
        
    def test_should_remove_tag_if_portlet_can_not_be_found(self):
        pass
        
    def test_should_remove_tag_if_context_can_not_be_found(self):
        pass
        