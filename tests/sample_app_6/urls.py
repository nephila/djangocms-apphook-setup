# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import url

from .views import BaseView

urlpatterns = [
    url(r'^$', BaseView.as_view(), name='base-view-6'),
]
