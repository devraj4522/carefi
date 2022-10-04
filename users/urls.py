from django.urls import path

from .views import user_login, user_signup

urlpatterns = [
    path('user_signup/', user_signup, name="user_signup"),
    path('user_login/', user_login, name="user_login"),
]
