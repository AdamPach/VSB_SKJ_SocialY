from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Like


# Create your views here.

@login_required
def get_post_detail(request, id_post):
    try:
        post = Post.objects.get(id=id_post)
        liked_by_user = post.like_set.filter(user_id=request.user.id).exists()
        likes = [post.id] if liked_by_user else []
        return render(request, "post.html", {"post": post, "likes": likes})
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
    posts = Post.objects.select_related('author').order_by('-created_on')

    likes = []

    if request.user is not None:
        liked_posts = posts.prefetch_related("like_set__user").filter(like__user_id=request.user.id)

        for liked_post in liked_posts:
            likes.append(liked_post.id)

    posts = posts.all()

    return render(request, "list_posts.html", {"posts": posts, "likes": likes})


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


@login_required
def like_post(request, id_post):
    if request.method != "POST":
        return redirect(f"/posts/{id_post}")

    like = Like.objects.filter(post_id=id_post, user_id=request.user.id).first()

    if like is None:
        new_like = Like(post_id=id_post, user_id=request.user.id)
        new_like.save()
    else:
        like.delete()

    redirect_url = request.POST.get("redirect_url")
    return redirect(redirect_url)


@login_required
def list_followed_posts(request):
    posts = Post.objects.select_related('author').filter(
        author__follow_destination__source_id=request.user.id).order_by('-created_on')
    likes = []

    if request.user is not None:
        liked_posts = posts.prefetch_related("like_set__user").filter(like__user_id=request.user.id)

        for liked_post in liked_posts:
            likes.append(liked_post.id)

    posts = posts.all()

    return render(request, "list_following_posts.html", {"posts": posts, "likes": likes})
