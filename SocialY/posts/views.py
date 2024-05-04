from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Post


# Create your views here.

@login_required
def get_post_detail(request, id_post):
    try:
        post = Post.objects.get(id=id_post)
        return render(request, "post.html", {"post": post})
    except ObjectDoesNotExist:
        raise Http404()
