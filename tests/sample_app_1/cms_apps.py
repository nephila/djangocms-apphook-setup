# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from aldryn_apphooks_config.app_base import CMSConfigApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

from djangocms_apphook_setup.base import AutoCMSAppMixin

from .cms_appconfig import AppConfig


class App1(AutoCMSAppMixin, CMSConfigApp):
    name = _('App1')
    urls = ['sample_app_1.urls']
    app_name = 'app1'
    app_config = AppConfig
    auto_setup = {
        'enabled': True,
        'home title': 'home title',
        'page title': 'page 1 title',
        'namespace': 'namespace',
        'config_fields': {'app_title': 'app title'},
        'config_translated_fields': {},
    }

apphook_pool.register(App1)
App1.setup()
