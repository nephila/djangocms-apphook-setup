# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

from djangocms_apphook_setup.base import AutoCMSAppMixin


class App5a(AutoCMSAppMixin, CMSApp):
    name = _('App5a')
    urls = ['sample_app_2.urls']
    app_name = 'app5a'
    auto_setup = {
        'enabled': True,
    }

apphook_pool.register(App5a)
App5a.setup()


class App5b(AutoCMSAppMixin, CMSApp):
    name = _('App5b')
    urls = ['sample_app_2.urls']
    app_name = 'app5b'
    auto_setup = {
        'enabled': True,
        'home title': 'home title',
    }

apphook_pool.register(App5b)
App5b.setup()


class App5c(AutoCMSAppMixin, CMSApp):
    name = _('App5c')
    urls = ['sample_app_2.urls']
    app_name = 'app5c'
    auto_setup = {
        'enabled': True,
        'home title': 'home title',
        'page title': 'page 1 title',
    }

apphook_pool.register(App5c)
App5c.setup()
