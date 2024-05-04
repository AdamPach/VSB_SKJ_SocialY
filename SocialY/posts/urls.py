from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_post),
    path('list', views.list_posts),
    path('<int:id_post>', views.get_post_detail),
    path('<int:id_post>/comment', views.add_comment)
]

