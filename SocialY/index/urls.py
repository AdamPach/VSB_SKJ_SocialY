from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_index),
    path('index', views.get_index),
]
