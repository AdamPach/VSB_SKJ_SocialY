from django.urls import path

from . import views

urlpatterns = [
    path("", views.users),
    path("login", views.login_user),
    path("register", views.register_user)
    path("auth/login", views.login_user),
    path("auth/register", views.register_user),
]
