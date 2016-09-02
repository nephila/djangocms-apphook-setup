# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from aldryn_apphooks_config.app_base import CMSConfigApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

from djangocms_apphook_setup.base import AutoCMSAppMixin

from .cms_appconfig import App4Config


class App4(AutoCMSAppMixin, CMSConfigApp):
    name = _('App4')
    urls = ['sample_app_4.urls']
    app_name = 'app4'
    app_config = App4Config
    auto_setup = {
        'enabled': True,
        'home title': 'home title',
        'page title': 'page 4 title',
        'namespace': 'namespace',
        'config_fields': {'random_option': True},
        'config_translated_fields': {'app_title': 'app title', 'object_name': 'name'},
    }

apphook_pool.register(App4)
App4.setup()
