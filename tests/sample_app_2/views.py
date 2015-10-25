# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.http import HttpResponse
from django.views.generic import View


class BaseView(View):

    def get(self, *args, **kwargs):
        return HttpResponse('app 2')
