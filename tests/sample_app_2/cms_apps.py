# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

from djangocms_apphook_setup.base import AutoCMSAppMixin


class App2(AutoCMSAppMixin, CMSApp):
    name = _('App2')
    urls = ['sample_app_2.urls']
    app_name = 'app2'
    auto_setup = {
        'enabled': True,
        'home title': 'home title',
        'page title': 'page 2 title',
        'namespace': 'namespace',
    }

apphook_pool.register(App2)
App2.setup()
