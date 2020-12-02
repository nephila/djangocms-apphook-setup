from aldryn_apphooks_config.models import AppHookConfig
from aldryn_apphooks_config.utils import setup_config
from app_data import AppDataForm
from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields


class App4Config(TranslatableModel, AppHookConfig):
    """
    Adds some translatable, per-app-instance fields.
    """

    random_option = models.BooleanField(default=False)
    translations = TranslatedFields(
        app_title=models.CharField(_("application title"), max_length=234),
        object_name=models.CharField(_("object name"), max_length=234),
    )


class App4ConfigForm(AppDataForm):
    some_option = forms.BooleanField(required=False, initial=False)


setup_config(App4ConfigForm, App4Config)
