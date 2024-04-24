from django.urls import path

from . import views

urlpatterns = [
    path("", views.users),
    path("auth/login", views.login_user),
    path("auth/register", views.register_user),
    path("auth/logout", views.logout_user)
]
