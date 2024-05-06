from django.urls import path

from . import views

urlpatterns = [
    path('', views.show_current_profile),
    path('edit', views.edit_profile),
    path('add-link', views.add_link),
    path('delete-link/<int:link_id>', views.delete_link),
    path('user/posts/<slug:username>', views.show_profile_posts),
    path('user/<slug:username>', views.show_profile_by_username),
]

