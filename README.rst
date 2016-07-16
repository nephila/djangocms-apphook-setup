=======================
djangocms-apphook-setup
=======================

.. image:: https://img.shields.io/pypi/v/djangocms-apphook-setup.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-apphook-setup
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/djangocms-apphook-setup.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-apphook-setup
    :alt: Monthly downloads

.. image:: https://img.shields.io/pypi/pyversions/djangocms-apphook-setup.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-apphook-setup
    :alt: Python versions

.. image:: https://img.shields.io/travis/nephila/djangocms-apphook-setup.svg?style=flat-square
    :target: https://travis-ci.org/nephila/djangocms-apphook-setup
    :alt: Latest Travis CI build status

.. image:: https://img.shields.io/coveralls/nephila/djangocms-apphook-setup/master.svg?style=flat-square
    :target: https://coveralls.io/r/nephila/djangocms-apphook-setup?branch=master
    :alt: Test coverage

.. image:: https://img.shields.io/codecov/c/github/nephila/djangocms-apphook-setup/develop.svg?style=flat-square
    :target: https://codecov.io/github/nephila/djangocms-apphook-setup
    :alt: Test coverage

.. image:: https://codeclimate.com/github/nephila/djangocms-apphook-setup/badges/gpa.svg?style=flat-square
   :target: https://codeclimate.com/github/nephila/djangocms-apphook-setup
   :alt: Code Climate

Utility function to auto setup apphooks on project startup.

Supported Django versions:

* Django 1.6
* Django 1.7
* Django 1.8

Supported django CMS versions:

* django CMS 3.x

Features
--------

The mixin included in this utility allows to automatically add an Apphook to a django CMS
project on the first access to the website.

This is intended for use by the django CMS application developers by extending their own
``CMSApp`` classes.

This behavior simplify the initial setup of a project and lower the barrier for the end user.

The setup function included here does the following:

* Check if the Apphook is already added to a CMS page
* If it is, it skips any further step
* If not:

  * Creates the home page (if not present)
  * Creates a sub page of the home
  * Adds the application Apphook to it

In case the application uses ``aldryn-apphooks-config``, a Apphook Config instance is created
and added to the application page together with the Apphook.

.. note:: To avoid issues with ``AldrynSearch`` during the creation of pages, the url of the
          pages is faked; this is normally not an issues as the pages will be reindexed
          whenever the content is updated.

Usage
-----

This utility can be used by extending the ``CMSApp`` class, adding the ``auto_setup`` attribute
with relevant configuration options and triggering setup at the end of ``cms_app.py``::


    class App4(AutoCMSAppMixin, CMSConfigApp):
        name = _('App4')
        urls = ['sample_app_4.urls']
        app_name = 'app4'
        app_config = App4Config
        # djangocms-apphook-setup attribute
        auto_setup = {
            'enabled': True,
            'home title': 'home title',
            'page title': 'page 4 title',
            'namespace': 'namespace',
            'config_fields': {'random_option': True},
            'config_translated_fields': {'app_title': 'app title', 'object_name': 'name'},
        }

    apphook_pool.register(App4)
    # trigger djangocms-apphook-setup function
    App4.setup()


Customizing ApphookConfig instances creation
--------------------------------------------

While ``config_fields`` and ``config_translated_fields`` should cover most use cases when it comes
to ApphookConfig instances creation, you may need more control over the process.

For this, it's possible to override ``AutoCMSAppMixin._create_config`` and
``AutoCMSAppMixin._create_config_translation``.

Default implementation::

    @classmethod
    def _create_config(cls):
        return cls.app_config.objects.create(
            namespace=cls.auto_setup['namespace'], **cls.auto_setup['config_fields']
        )

    @classmethod
    def _create_config_translation(cls, config, lang):
        config.set_current_language(lang, initialize=True)
        for field, data in cls.auto_setup['config_translated_fields'].items():
            setattr(config, field, data)
        config.save_translations()


You can completely redefine the methods, provided you return an ApphookConfig instance
in ``_create_config``.


Configuration options
---------------------

The behavior of the setup function can be customized by setting the following keys in the
``auto_setup`` attribute:

* ``enabled``: If ``True`` the setup is invoked; a good option is to use a setting to control this
  to allow application users to disable the behavior (default: ``True``)
* ``home title``: Title of the home page if created by the setup function; this **must** be set in
  the application ``CMSApp``, otherwise the setup function will exit with a warning.
* ``page title``: Title of the page created by the setup function; this **must** be set in
  the application ``CMSApp``, otherwise the setup function will exit with a warning.
* ``namespace``: Application instance name used when attaching the Apphook; this **must** be set in
  the application ``CMSApp`` if an ``app_name`` is defined, otherwise the setup function will exit
  with a warning.
* ``config_fields``: Fields used when creating the ApphookConfigModel instance; use this attribute
  for non-translated fields.
* ``config_translated_fields``: Fields used when creating the ApphookConfigModel instance;
  use this attribute for translated fields (currently only ``django-parler`` is supported).
* ``sites``: List of site ids for which to create the pages; if set to ``True`` (the default value)
  pages will be created for all sites. A single apphook config is created for all the sites;
  instance is created only on first page creation.


Notes on testing
----------------

As this utility works by triggering setup function at import time, extra steps must be taken
in the tests to unload the modules between the tests (this is only needed when testing the setup).

Example cleanup to be included in ``setUp`` method::

    def setUp(self):
        super(SetupAppBaseTest, self).setUp()
        from cms.apphook_pool import apphook_pool

        delete = [
            'my_app',
            'my_app.cms_app',
        ]
        for module in delete:
            if module in sys.modules:
                del sys.modules[module]
        MyApphoolConfigModel.cmsapp = None
        apphook_pool.clear()

