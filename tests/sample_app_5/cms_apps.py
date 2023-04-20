from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import gettext_lazy as _

from djangocms_apphook_setup.base import AutoCMSAppMixin


@apphook_pool.register
class App5a(AutoCMSAppMixin, CMSApp):
    name = _("App5a")
    _urls = ["tests.sample_app_5.urls"]
    app_name = "app5a"
    auto_setup = {
        "enabled": True,
    }


App5a.setup()


@apphook_pool.register
class App5b(AutoCMSAppMixin, CMSApp):
    name = _("App5b")
    _urls = ["tests.sample_app_5.urls"]
    app_name = "app5b"
    auto_setup = {
        "enabled": True,
        "home title": "home title",
    }


App5b.setup()


@apphook_pool.register
class App5c(AutoCMSAppMixin, CMSApp):
    name = _("App5c")
    _urls = ["tests.sample_app_5.urls"]
    app_name = "app5c"
    auto_setup = {
        "enabled": True,
        "home title": "home title",
        "page title": "page 1 title",
    }


App5c.setup()
