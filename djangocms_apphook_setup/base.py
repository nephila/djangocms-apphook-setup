# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals


class AutoCMSAppMixin(object):

    auto_setup = {
        'enabled': True,
        'home title': None,
        'page title': None,
        'namespace': None,
        'config_fields': {},
        'config_translated_fields': {},
    }

    @classmethod
    def _create_page(cls, page, lang, auto_title, cms_app=None, parent=None, namespace=None):
        from cms.api import create_page, create_title
        from cms.utils.conf import get_templates

        default_template = get_templates()[0][0]
        if page is None:
            page = create_page(
                auto_title, language=lang, parent=parent,
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
        return page.get_draft_object()

    @classmethod
    def _setup_pages(cls, setup_config=False):
        from cms.exceptions import NoHomeFound
        from cms.models import Page
        from cms.utils import get_language_list
        from django.utils.translation import override

        config = None
        if setup_config:
            config = cls.app_config.objects.create(
                namespace=cls.auto_setup['namespace'], **cls.auto_setup['config_fields']
            )
        langs = get_language_list()
        app_page = None
        for lang in langs:
            with override(lang):
                if config:
                    if cls.auto_setup['config_translated_fields']:
                        config.set_current_language(lang, initialize=True)
                        for field, data in cls.auto_setup['config_translated_fields'].items():
                            setattr(config, field, data)
                        config.save_translations()
                    namespace = config.namespace
                elif cls.app_name:
                    namespace = cls.app_name
                else:
                    namespace = None
                try:
                    home = Page.objects.get_home().get_draft_object()
                except NoHomeFound:
                    home = None
                home = cls._create_page(home, lang, cls.auto_setup['home title'])
                app_page = cls._create_page(
                    app_page, lang, cls.auto_setup['page title'], cls.__name__, home, namespace
                )

    @classmethod
    def setup(cls):
        from cms.models import Page

        if cls.auto_setup and cls.auto_setup['enabled']:
            if getattr(cls, 'app_config', False):
                configs = cls.app_config.objects.all()
                if not configs.exists():
                    cls._setup_pages(setup_config=True)
            elif not Page.objects.filter(application_urls=cls.__name__).exists():
                cls._setup_pages(setup_config=False)
