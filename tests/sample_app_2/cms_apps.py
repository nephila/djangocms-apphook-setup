from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

from djangocms_apphook_setup.base import AutoCMSAppMixin


@apphook_pool.register
class App2(AutoCMSAppMixin, CMSApp):
    name = _("App2")
    _urls = ["tests.sample_app_2.urls"]
    app_name = "app2"
    auto_setup = {
        "enabled": True,
        "home title": "home title",
        "page title": "page 2 title",
        "namespace": "namespace",
    }


App2.setup()
