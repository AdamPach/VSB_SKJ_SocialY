from django.urls import path

from . import views

urlpatterns = [
    path("", views.users),
    path("register", views.register_user)
]
