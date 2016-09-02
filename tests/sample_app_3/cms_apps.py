# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

from djangocms_apphook_setup.base import AutoCMSAppMixin


class App3(AutoCMSAppMixin, CMSApp):
    name = _('App3')
    urls = ['sample_app_3.urls']
    auto_setup = {
        'enabled': True,
        'home title': 'home title',
        'page title': 'page 3 title',
    }

apphook_pool.register(App3)
App3.setup()
