# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import sys

from cms.api import create_page, create_title
from cms.models import Page, Site, warnings
from cms.utils import get_language_list
from django.utils.translation import override

from .base import BaseTest
from .sample_app_1.cms_appconfig import AppConfig
from .sample_app_4.cms_appconfig import App4Config
from .sample_app_6.cms_appconfig import App6Config


class SetupAppBaseTest(BaseTest):
    config = None
    module = None
    app_name = None

    def setUp(self):
        super(SetupAppBaseTest, self).setUp()
        Page.objects.all().delete()
        if self.config:
            self.config.objects.all().delete()
        self._delete_modules()

    def _delete_modules(self):
        from cms.apphook_pool import apphook_pool
        delete = [
            'tests.sample_app_1',
            'tests.sample_app_1.cms_apps',
            'tests.sample_app_2',
            'tests.sample_app_2.cms_apps',
            'tests.sample_app_3',
            'tests.sample_app_3.cms_apps',
            'tests.sample_app_4',
            'tests.sample_app_4.cms_apps',
            'tests.sample_app_5',
            'tests.sample_app_5.cms_apps',
            'tests.sample_app_6',
            'tests.sample_app_6.cms_apps',
        ]
        for module in delete:
            if module in sys.modules:
                del sys.modules[module]
        if self.config:
            self.config.cmsapp = None
        apphook_pool.clear()

    def _setup_from_cmsapp(self, site_id=1, home_final=4, blog_final=2, configs_final=1, configs_init=0, pages_init=0):

        # Tests starts with a set of pages / configs
        self.assertEqual(Page.objects.count(), pages_init)
        if self.config:
            self.assertEqual(self.config.objects.count(), configs_init)
        self.assertEqual(Page.objects.filter(application_urls=self.app_name).count(), configs_init * 2)

        # importing cms_app triggers the auto setup
        __import__(self.module, fromlist=(str('cms_apps'),))

        # Final set of pages / configs
        self.assertEqual(Page.objects.count(), home_final)
        if self.config:
            self.assertEqual(self.config.objects.count(), configs_final)
        self.assertEqual(Page.objects.filter(application_urls=self.app_name).count(), blog_final)

    def _setup_filled(self, site_id=1, home_final=4, blog_final=2, configs_final=1, configs_init=0, pages_init=0):
        site = Site.objects.get(pk=site_id)
        set_home = hasattr(Page, 'set_as_homepage')
        # Tests starts with a set of pages / configs
        self.assertEqual(Page.objects.count(), pages_init)
        if self.config:
            self.assertEqual(self.config.objects.count(), configs_init)
        self.assertEqual(Page.objects.filter(application_urls=self.app_name).count(), configs_init * 2)

        langs = get_language_list()
        home = None
        for lang in langs:
            with override(lang):
                if not home:
                    home = create_page(
                        'a new home', language=lang, site=site,
                        template='page.html', in_navigation=True, published=True
                    )
                    if set_home:
                        home.set_as_homepage()
                else:
                    create_title(
                        language=lang, title='a new home', page=home
                    )
                    home.publish(lang)

        # importing cms_app triggers the auto setup
        __import__(self.module, fromlist=(str('cms_apps'),))

        # Final set of pages / configs
        self.assertEqual(Page.objects.count(), home_final)
        if self.config:
            self.assertEqual(self.config.objects.count(), configs_final)
        self.assertEqual(Page.objects.filter(application_urls=self.app_name).count(), blog_final)

        home = Page.objects.get_home(site)
        self.assertEqual(home.get_title(), 'a new home')


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
        __import__(self.module, fromlist=(str('cms_apps'),))
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
        __import__(self.module, fromlist=(str('cms_apps'),))
        config = self.config.objects.first()
        self.assertEqual(set(config.get_available_languages()), set(('en', 'it', 'fr')))
        self.assertTrue(config.random_option)
        config.set_current_language('en')
        self.assertEqual(config.object_name, 'name')


class SetupApp4Site2Test(SetupAppBaseTest):
    config = App4Config
    module = 'tests.sample_app_4'
    app_name = 'App4'

    def setUp(self):
        super(SetupApp4Site2Test, self).setUp()
        Site.objects.create(name='domain2', domain='www.example2.com', id=2)

    def test_setup_from_cmsapp(self):
        with self.settings(SITE_ID=1):
            self._setup_from_cmsapp(site_id=1, home_final=4, blog_final=2)
        self._delete_modules()
        with self.settings(SITE_ID=2):
            self._setup_from_cmsapp(
                site_id=2, home_final=8, blog_final=4, configs_final=1, configs_init=1, pages_init=4
            )
        self.assertEqual(Page.objects.count(), 8)
        self.assertEqual(Page.objects.on_site(1).count(), 4)
        self.assertEqual(Page.objects.on_site(2).count(), 4)
        self.assertEqual(self.config.objects.count(), 1)
        self.assertEqual(Page.objects.filter(application_urls=self.app_name).count(), 4)
        self.assertEqual(Page.objects.on_site(1).filter(application_urls=self.app_name).count(), 2)
        self.assertEqual(Page.objects.on_site(2).filter(application_urls=self.app_name).count(), 2)

    def test_setup_filled(self):
        with self.settings(SITE_ID=1):
            self._setup_filled(site_id=1, home_final=4, blog_final=2)
        self._delete_modules()
        with self.settings(SITE_ID=2):
            self._setup_filled(
                site_id=2, home_final=8, blog_final=4, configs_final=1, configs_init=1, pages_init=4
            )
        self.assertEqual(Page.objects.count(), 8)
        self.assertEqual(Page.objects.on_site(1).count(), 4)
        self.assertEqual(Page.objects.on_site(2).count(), 4)
        self.assertEqual(self.config.objects.count(), 1)
        self.assertEqual(Page.objects.filter(application_urls=self.app_name).count(), 4)
        self.assertEqual(Page.objects.on_site(1).filter(application_urls=self.app_name).count(), 2)
        self.assertEqual(Page.objects.on_site(2).filter(application_urls=self.app_name).count(), 2)

    def test_config_values(self):
        # importing cms_app triggers the auto setup
        with self.settings(SITE_ID=1):
            __import__(self.module, fromlist=(str('cms_apps'),))
            config = self.config.objects.first()
            self.assertEqual(set(config.get_available_languages()), set(('en', 'it', 'fr')))
            self.assertTrue(config.random_option)
            config.set_current_language('en')
            self.assertEqual(config.object_name, 'name')
        self._delete_modules()
        with self.settings(SITE_ID=2):
            __import__(self.module, fromlist=(str('cms_apps'),))
            self.assertEqual(self.config.objects.count(), 1)
            config = self.config.objects.first()
            self.assertEqual(set(config.get_available_languages()), set(('en', 'it', 'fr')))
            self.assertTrue(config.random_option)
            config.set_current_language('en')
            self.assertEqual(config.object_name, 'name')


class SetupApp6Site2Test(SetupAppBaseTest):
    config = App6Config
    module = 'tests.sample_app_6'
    app_name = 'App6'

    def setUp(self):
        super(SetupApp6Site2Test, self).setUp()
        Site.objects.create(name='domain2', domain='www.example2.com', id=2)

    def test_setup_from_cmsapp(self):
        with self.settings(SITE_ID=1):
            self._setup_from_cmsapp(site_id=1, home_final=0, blog_final=0, configs_final=0)
        self._delete_modules()
        with self.settings(SITE_ID=2):
            self._setup_from_cmsapp(site_id=2, home_final=4, blog_final=2, configs_final=1)
        self.assertEqual(Page.objects.count(), 4)
        self.assertEqual(Page.objects.on_site(1).count(), 0)
        self.assertEqual(Page.objects.on_site(2).count(), 4)
        self.assertEqual(self.config.objects.count(), 1)
        self.assertEqual(Page.objects.filter(application_urls=self.app_name).count(), 2)
        self.assertEqual(Page.objects.on_site(1).filter(application_urls=self.app_name).count(), 0)
        self.assertEqual(Page.objects.on_site(2).filter(application_urls=self.app_name).count(), 2)

    def test_setup_filled(self):
        with self.settings(SITE_ID=1):
            self._setup_filled(site_id=1, home_final=2, blog_final=0, configs_final=0)
        self._delete_modules()
        with self.settings(SITE_ID=2):
            self._setup_filled(site_id=2, home_final=6, blog_final=2, configs_final=1, pages_init=2)
        self.assertEqual(Page.objects.count(), 6)
        self.assertEqual(Page.objects.on_site(1).count(), 2)
        self.assertEqual(Page.objects.on_site(2).count(), 4)
        self.assertEqual(self.config.objects.count(), 1)
        self.assertEqual(Page.objects.filter(application_urls=self.app_name).count(), 2)
        self.assertEqual(Page.objects.on_site(1).filter(application_urls=self.app_name).count(), 0)
        self.assertEqual(Page.objects.on_site(2).filter(application_urls=self.app_name).count(), 2)

    def test_config_values(self):
        # importing cms_app triggers the auto setup
        with self.settings(SITE_ID=1):
            __import__(self.module, fromlist=(str('cms_apps'),))
            self.assertEqual(self.config.objects.count(), 0)
        self._delete_modules()
        with self.settings(SITE_ID=2):
            __import__(self.module, fromlist=(str('cms_apps'),))
            self.assertEqual(self.config.objects.count(), 1)
            config = self.config.objects.first()
            self.assertEqual(set(config.get_available_languages()), set(('en',)))
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

        with warnings.catch_warnings(record=True) as w:
            __import__(self.module, fromlist=(str('cms_apps'),))

        # No setup is performed
        self.assertEqual(Page.objects.count(), 0)
        self.assertEqual(Page.objects.filter(application_urls=self.app_name).count(), 0)
