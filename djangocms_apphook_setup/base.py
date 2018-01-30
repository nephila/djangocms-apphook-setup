# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import warnings

from django.contrib.sites.models import Site


class AutoCMSAppMixin(object):

    auto_setup = {
        'enabled': True,
        'home title': None,
        'page title': None,
        'namespace': None,
        'config_fields': {},
        'config_translated_fields': {},
        'sites': True
    }

    @classmethod
    def _create_page(cls, page, lang, auto_title, cms_app=None, parent=None, namespace=None,
                     site=None, set_home=False):
        """
        Create a single page or titles

        :param page: Page instance
        :param lang: language code
        :param auto_title: title text for the newly created title
        :param cms_app: Apphook Class to be attached to the page
        :param parent: parent page (None when creating the home page)
        :param namespace: application instance name (as provided to the ApphookConfig)
        :param set_home: mark as home page (on django CMS 3.5 only)

        :return: draft copy of the created page
        """
        from cms.api import create_page, create_title
        from cms.utils.conf import get_templates

        default_template = get_templates()[0][0]
        if page is None:
            page = create_page(
                auto_title, language=lang, parent=parent, site=site,
                template=default_template, in_navigation=True, published=True
            )
            page.application_urls = cms_app
            page.application_namespace = namespace
            page.save()
            page.publish(lang)
        elif lang not in page.get_languages():
            create_title(
                language=lang, title=auto_title, page=page
            )
            page.publish(lang)
        if set_home:
            page.set_as_homepage()
        return page.get_draft_object()

    @classmethod
    def _create_config(cls):
        """
        Creates an ApphookConfig instance

        ``AutoCMSAppMixin.auto_setup['config_fields']`` is used to fill in the data
        of the instance.

        :return: ApphookConfig instance
        """
        return cls.app_config.objects.create(
            namespace=cls.auto_setup['namespace'], **cls.auto_setup['config_fields']
        )

    @classmethod
    def _create_config_translation(cls, config, lang):
        """
        Creates a translation for the given ApphookConfig

        Only django-parler kind of models are currently supported.

        ``AutoCMSAppMixin.auto_setup['config_translated_fields']`` is used to fill in the data
        of the instance for all the languages.

        :param config: ApphookConfig instance
        :param lang: language code for the language to create
        """
        config.set_current_language(lang, initialize=True)
        for field, data in cls.auto_setup['config_translated_fields'].items():
            setattr(config, field, data)
        config.save_translations()

    @classmethod
    def _setup_pages(cls, config):
        """
        Create the page structure.

        It created a home page (if not exists) and a sub-page, and attach the Apphook to the
        sub-page.
        Pages titles are provided by ``AutoCMSAppMixin.auto_setup``

        :param setup_config: boolean to control whether creating the ApphookConfig instance
        """
        from cms.exceptions import NoHomeFound
        from cms.models import Page
        from cms.utils import get_language_list
        from django.conf import settings
        from django.utils.translation import override

        app_page = None
        get_url = False
        if getattr(settings, 'ALDRYN_SEARCH_CMS_PAGE', False):
            from aldryn_search.search_indexes import TitleIndex

            def fake_url(self, obj):
                return ''

            get_url = TitleIndex.get_url
            TitleIndex.get_url = fake_url
        site = Site.objects.get_current()
        auto_sites = cls.auto_setup.get('sites', True)
        if auto_sites is True or site.pk in auto_sites:
            if getattr(cls, 'app_config', False):
                configs = cls.app_config.objects.all()
                if not configs.exists():
                    config = cls._create_config()
                else:
                    config = configs.first()

            langs = get_language_list(site.pk)
            if not Page.objects.on_site(site.pk).filter(application_urls=cls.__name__).exists():
                for lang in langs:
                    with override(lang):
                        if config:
                            if cls.auto_setup['config_translated_fields']:
                                cls._create_config_translation(config, lang)
                            namespace = config.namespace
                        elif cls.app_name:
                            namespace = cls.app_name
                        else:
                            namespace = None
                        try:
                            home = Page.objects.get_home(site.pk).get_draft_object()
                        except NoHomeFound:
                            home = None
                        set_home = hasattr(Page, 'set_as_homepage')
                        home = cls._create_page(
                            home, lang, cls.auto_setup['home title'], site=site, set_home=set_home
                        )
                        app_page = cls._create_page(
                            app_page, lang, cls.auto_setup['page title'], cls.__name__, home,
                            namespace, site=site
                        )
        if get_url:
            TitleIndex.get_url = get_url

    @classmethod
    def setup(cls):
        """
        Main method to auto setup Apphook

        It must be called after the Apphook registration::

            apphook_pool.register(MyApp)
            MyApp.setup()
        """
        try:
            if cls.auto_setup and cls.auto_setup.get('enabled', False):
                if not cls.auto_setup.get('home title', False):
                    warnings.warn(
                        '"home title" is not set in {0}.auto_setup attribute'.format(cls)
                    )
                    return
                if not cls.auto_setup.get('page title', False):
                    warnings.warn(
                        '"page title" is not set in {0}.auto_setup attribute'.format(cls)
                    )
                    return
                if cls.app_name and not cls.auto_setup.get('namespace', False):
                    warnings.warn(
                        '"page title" is not set in {0}.auto_setup attribute'.format(cls)
                    )
                    return
                config = None
                cls._setup_pages(config)
        except Exception:
            # Ignore any error during setup. Worst case: pages are not created, but the instance
            # won't break
            pass
