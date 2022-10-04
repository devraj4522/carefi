from django.urls import path

from .views import current_price, get_price_list_details

urlpatterns = [
    path('current_price/', current_price, name="current_price"),
    path('list/', get_price_list_details, name="get_price_list_details"),
]
