from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment


# Create your views here.

@login_required
def get_post_detail(request, id_post):
    try:
        post = Post.objects.get(id=id_post)
        return render(request, "post.html", {"post": post})
    except ObjectDoesNotExist:
        raise Http404()


@login_required
def create_post(request):
    if request.method == "POST":
        post_content = request.POST.get("post_content")
        try:
            post = Post(post_content=post_content, author=request.user)
            post.save()
        except ValidationError:
            return render(request, "create_post.html", {"error_message": "Post is too long, max length is 1000 "
                                                                         "characters"})

        return redirect('/index?message=Post%20was%20created')
    else:
        return render(request, "create_post.html")


def list_posts(request):
    posts = Post.objects.select_related('author').order_by('-created_on').all()[:10]
    return render(request, "list_posts.html", {"posts": posts})


@login_required
def add_comment(request, id_post):
    if request.method != "POST":
        return redirect(f"/posts/{id_post}")

    comment_content = request.POST.get("comment_content")

    try:
        post = Comment(comment_content=comment_content, author=request.user, post_id=id_post)
        post.save()
    except ValidationError:
        return render(request, "create_post.html", {"error_message": "Post is too long, max length is 1000 "
                                                                     "characters"})
    return redirect(f"/posts/{id_post}")
