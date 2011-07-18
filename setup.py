from setuptools import setup, find_packages
import os

version = '1.0a1'

setup(name='collective.tinymceportlets',
      version=version,
      description="And portlets into content with tiny mce",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFPlone',
          'plone.transformchain',
          'plone.formwidget.contenttree',
          'plone.app.z3cform',
          'lxml',
          'repoze.xmliter'
      ],
      extras_require={
        'test': ['plone.app.testing'],
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
