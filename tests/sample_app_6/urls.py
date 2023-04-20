from django.urls import path

from .views import BaseView

urlpatterns = [
    path("", BaseView.as_view(), name="base-view-6"),
]
