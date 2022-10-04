from django.urls import path

from . import permissions

urlpatterns = [
    path('', permissions.index, name='index'),
]
