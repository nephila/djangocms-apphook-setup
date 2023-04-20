from aldryn_apphooks_config.models import AppHookConfig
from aldryn_apphooks_config.utils import setup_config
from app_data import AppDataForm
from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _


class AppConfig(AppHookConfig):
    app_title = models.CharField(_("application title"), max_length=234)


class AppConfigForm(AppDataForm):
    some_option = forms.BooleanField(required=False, initial=False)


setup_config(AppConfigForm, AppConfig)
