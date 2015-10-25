# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import sys

from cms.api import create_page, create_title
from cms.models import Page
from cms.utils import get_language_list
from django.utils.translation import override

from .base import BaseTest
from .sample_app_1.cms_appconfig import AppConfig
from .sample_app_4.cms_appconfig import App4Config


class SetupAppBaseTest(BaseTest):
    config = None
    module = None
    app_name = None

    def setUp(self):
        super(SetupAppBaseTest, self).setUp()
        from cms.apphook_pool import apphook_pool

        delete = [
            'tests.sample_app_1',
            'tests.sample_app_1.cms_app',
            'tests.sample_app_2',
            'tests.sample_app_2.cms_app',
            'tests.sample_app_3',
            'tests.sample_app_3.cms_app',
            'tests.sample_app_4',
            'tests.sample_app_4.cms_app',
            'tests.sample_app_5',
            'tests.sample_app_5.cms_app',
        ]
        for module in delete:
            if module in sys.modules:
                del sys.modules[module]
        if self.config:
            self.config.cmsapp = None
        apphook_pool.clear()

    def _setup_from_cmsapp(self):

        # Tests starts with no page and no config
        self.assertFalse(Page.objects.exists())
        if self.config:
            self.assertFalse(self.config.objects.exists())
        self.assertEqual(Page.objects.filter(application_urls=self.app_name).count(), 0)

        # importing cms_app triggers the auto setup
        __import__(self.module, fromlist=(str('cms_app'),))

        # Home and blog, published and draft
        self.assertEqual(Page.objects.count(), 4)
        if self.config:
            self.assertEqual(self.config.objects.count(), 1)
        self.assertEqual(Page.objects.filter(application_urls=self.app_name).count(), 2)

    def _setup_filled(self):

        # Tests starts with no page and no config
        self.assertFalse(Page.objects.exists())
        if self.config:
            self.assertFalse(self.config.objects.exists())
        self.assertEqual(Page.objects.filter(application_urls=self.app_name).count(), 0)

        langs = get_language_list()
        home = None
        for lang in langs:
            with override(lang):
                if not home:
                    home = create_page(
                        'a new home', language=lang,
                        template='page.html', in_navigation=True, published=True
                    )
                else:
                    create_title(
                        language=lang, title='a new home', page=home
                    )
                    home.publish(lang)

        # importing cms_app triggers the auto setup
        __import__(self.module, fromlist=(str('cms_app'),))

        # Home and blog, published and draft
        self.assertEqual(Page.objects.count(), 4)
        if self.config:
            self.assertEqual(self.config.objects.count(), 1)
        self.assertEqual(Page.objects.filter(application_urls=self.app_name).count(), 2)

        home = Page.objects.get_home()
        for lang in langs:
            self.assertEqual(home.get_title(lang), 'a new home')


class SetupApp1Test(SetupAppBaseTest):
    config = AppConfig
    module = 'tests.sample_app_1'
    app_name = 'App1'

    def test_setup_from_cmsapp(self):
        self._setup_from_cmsapp()

    def test_setup_filled(self):
        self._setup_filled()

    def test_config_values(self):
        # importing cms_app triggers the auto setup
        __import__(self.module, fromlist=(str('cms_app'),))
        config = self.config.objects.first()
        self.assertEqual(config.app_title, 'app title')


class SetupApp2Test(SetupAppBaseTest):
    module = 'tests.sample_app_2'
    app_name = 'App2'

    def test_setup_from_cmsapp(self):
        self._setup_from_cmsapp()

    def test_setup_filled(self):
        self._setup_filled()


class SetupApp3Test(SetupAppBaseTest):
    module = 'tests.sample_app_3'
    app_name = 'App3'

    def test_setup_from_cmsapp(self):
        self._setup_from_cmsapp()

    def test_setup_filled(self):
        self._setup_filled()


class SetupApp4Test(SetupAppBaseTest):
    config = App4Config
    module = 'tests.sample_app_4'
    app_name = 'App4'

    def test_setup_from_cmsapp(self):
        self._setup_from_cmsapp()

    def test_setup_filled(self):
        self._setup_filled()

    def test_config_values(self):
        # importing cms_app triggers the auto setup
        __import__(self.module, fromlist=(str('cms_app'),))
        config = self.config.objects.first()
        self.assertEqual(set(config.get_available_languages()), set(('en', 'it', 'fr')))
        self.assertTrue(config.random_option)
        config.set_current_language('en')
        self.assertEqual(config.object_name, 'name')


class SetupApp5Test(SetupAppBaseTest):
    module = 'tests.sample_app_5'
    app_name = 'App5'

    def test_setup_empty(self):
        # Tests starts with no page and no config
        self.assertFalse(Page.objects.exists())
        self.assertEqual(Page.objects.filter(application_urls=self.app_name).count(), 0)

        # importing cms_app triggers the auto setup
        __import__(self.module, fromlist=(str('cms_app'),))

        # No setup is performed
        self.assertEqual(Page.objects.count(), 0)
        self.assertEqual(Page.objects.filter(application_urls=self.app_name).count(), 0)
