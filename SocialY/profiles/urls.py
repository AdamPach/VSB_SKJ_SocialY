from django.urls import path

from . import views

urlpatterns = [
    path('', views.show_current_profile),
    path('search', views.search_profile),
    path('edit', views.edit_profile),
    path('add-link', views.add_link),
    path('delete-link/<int:link_id>', views.delete_link),
    path('user/posts/<slug:username>', views.show_profile_posts),
    path('user/followed-by/<slug:username>', views.show_profile_followers),
    path('user/following/<slug:username>', views.show_profile_following),
    path('user/<slug:username>', views.show_profile_by_username),
    path('follow/<slug:username>', views.follow_profile)
]
