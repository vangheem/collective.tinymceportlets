from zope.component import adapts
from zope.interface import Interface, implements
from zope.schema import Choice
from plone.formwidget.contenttree import ContentTreeFieldWidget
from plone.formwidget.contenttree import PathSourceBinder
from z3c.form import form, button, field
from zope.app.pagetemplate import ViewPageTemplateFile as Zope3PageTemplateFile


class IPortletSelectionForm(Interface):
    manager = Choice(
        title=u"Portlet Manager",
        vocabulary="collective.tinymceportlets.vocabularies.portletmanagers"
    )

    context = Choice(
        title=u"Content Item",
        source=PathSourceBinder()
    )

    portlet = Choice(
        title=u"Portlet",
        vocabulary="collective.tinymceportlets.vocabularies.contextportlets"
    )


class PortletSelectionAdapter(object):
    implements(IPortletSelectionForm)
    adapts(Interface)

    manager = ''
    context = ''
    portlet = ''

    def __init__(self, context):
        self.context = context


class PortletSelectionForm(form.Form):
    template = Zope3PageTemplateFile("templates/portlets-selection.pt")
    fields = field.Fields(IPortletSelectionForm)
    fields['context'].widgetFactory = ContentTreeFieldWidget

    @button.buttonAndHandler(u'Save')
    def handle_save(self, action):
        pass

    @button.buttonAndHandler(u'Cancel')
    def handle_cancel(self, action):
        pass

    @button.buttonAndHandler(u'Remove')
    def handle_remove(self, action):
        pass


PortletSelectionFormView = PortletSelectionForm
