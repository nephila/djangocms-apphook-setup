from aldryn_apphooks_config.app_base import CMSConfigApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import gettext_lazy as _

from djangocms_apphook_setup.base import AutoCMSAppMixin

from .cms_appconfig import AppConfig


@apphook_pool.register
class App1(AutoCMSAppMixin, CMSConfigApp):
    name = _("App1")
    _urls = ["tests.sample_app_1.urls"]
    app_name = "app1"
    app_config = AppConfig
    auto_setup = {
        "enabled": True,
        "home title": "home title",
        "page title": "page 1 title",
        "namespace": "namespace",
        "config_fields": {"app_title": "app title"},
        "config_translated_fields": {},
    }


App1.setup()
