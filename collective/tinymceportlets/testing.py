from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import applyProfile
from plone.app.testing.layers import FunctionalTesting
from plone.app.testing.layers import IntegrationTesting
from zope.configuration import xmlconfig

class TinyMCEPortletsLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # load ZCML
        import collective.tinymceportlets
        xmlconfig.file('configure.zcml', collective.tinymceportlets, context=configurationContext)

    def setUpPloneSite(self, portal):
        # install into the Plone site
        applyProfile(portal, 'collective.tinymceportlets:default')


TINYMCE_PORTLETS_FIXTURE = TinyMCEPortletsLayer()
TINYMCE_PORTLETS_INTEGRATION_TESTING = IntegrationTesting(bases=(TINYMCE_PORTLETS_FIXTURE,), name="TINYMCE_PORTLETS_FIXTURE:Integration")
TINYMCE_PORTLETS_FUNCTIONAL_TESTING = FunctionalTesting(bases=(TINYMCE_PORTLETS_FIXTURE,), name="TINYMCE_PORTLETS_FIXTURE:Functional")

def browser_login(portal, browser, username=None, password=None):
    browser.open(portal.absolute_url() + '/login_form')
    if username is None:
        username = TEST_USER_NAME
    if password is None:
        password = TEST_USER_PASSWORD
    browser.getControl(name='__ac_name').value = username
    browser.getControl(name='__ac_password').value = password
    browser.getControl(name='submit').click()