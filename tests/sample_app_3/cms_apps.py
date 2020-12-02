from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

from djangocms_apphook_setup.base import AutoCMSAppMixin


@apphook_pool.register
class App3(AutoCMSAppMixin, CMSApp):
    name = _("App3")
    _urls = ["tests.sample_app_3.urls"]
    auto_setup = {
        "enabled": True,
        "home title": "home title",
        "page title": "page 3 title",
    }


App3.setup()
