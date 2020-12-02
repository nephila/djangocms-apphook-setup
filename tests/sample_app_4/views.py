from django.http import HttpResponse
from django.views.generic import View


class BaseView(View):
    def get(self, *args, **kwargs):
        return HttpResponse("app 1")
