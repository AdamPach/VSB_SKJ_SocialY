from django.urls import path
from . import views

urlpatterns = [
    path('<int:id_post>', views.get_post_detail),
]

