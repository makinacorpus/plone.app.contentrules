from setuptools import setup, find_packages

version = '2.1.9'

setup(name='plone.app.contentrules',
      version=version,
      description="Plone integration for plone.contentrules",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES.txt").read(),
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Zope2",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
        ],
      keywords='',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://pypi.python.org/pypi/plone.app.contentrules',
      license='GPL version 2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages = ['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'five.formlib',
        'kss.core',
        'plone.contentrules',
        'plone.memoize',
        'plone.stringinterp',
        'plone.uuid',
        'plone.app.form',
        'plone.app.kss',
        'plone.app.vocabularies',
        'transaction',
        'zope.annotation',
        'zope.browser',
        'zope.component',
        'zope.container',
        'zope.event',
        'zope.formlib',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.lifecycleevent',
        'zope.publisher >= 3.11.0',
        'zope.schema',
        'zope.site',
        'zope.traversing',
        'Acquisition',
        'Products.CMFPlone',
        'Products.CMFCore',
        'Products.CMFDefault',
        'Products.GenericSetup',
        'Products.statusmessages',
        'ZODB3',
        'Zope2 >= 2.12.3',
      ],
      )
