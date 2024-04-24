from django.urls import path

from . import views

urlpatterns = [
    path('', views.show_current_profile),
    path('edit', views.edit_profile),
    path('user/<slug:username>', views.show_profile_by_username),
]

