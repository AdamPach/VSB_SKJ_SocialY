from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from users.models import ApplicationUser
from posts.models import Post
from .models import Link, Follow


# Create your views here.

@login_required
def show_current_profile(request):
    return render(request, "profile_template.html", {"user_profile": request.user, "is_current_user": True})


def show_profile_by_username(request, username):
    user = None
    followed = False

    if request.user is not None and request.user.username == username:
        user = request.user
    else:
        user = ApplicationUser.objects.filter(username=username).prefetch_related('follow_source').first()
        if request.user is not None:
            followed = Follow.objects.filter(source_id=request.user.id, destination_id=user.id).exists()

    if user is None:
        raise Http404("Product does not exist")

    return render(request,
                  "profile_template.html",
                  {
                      "user_profile": user,
                      "is_current_user": True if username == request.user.username else False,
                      "followed": followed})


@login_required
def edit_profile(request):
    if request.method == "POST":
        new_quote = request.POST.get("quote")
        new_description = request.POST.get("description")

        request.user.quote = new_quote if new_quote is not None else ""
        request.user.user_description = new_description if new_description is not None else ""
        request.user.save()

        return redirect('/profile')
    else:
        return render(request, "edit_profile.html", {"user_profile": request.user})


@login_required
def add_link(request):
    if request.method == "POST":
        name = request.POST.get("link-name")
        destination = request.POST.get("destination")
        button = request.POST.get("button-text")
        try:
            new_link = Link(name=name, destination=destination, user=request.user)
            if button != "":
                new_link.button_text = new_link
            new_link.save()
        except ValidationError:
            return render(request, "profile_add_link.html", {"error_message": "Link is invalid"})
        except IntegrityError:
            return render(request, "profile_add_link.html", {"error_message": "This destination is already in use"})

        return redirect("/profile/edit")

    else:
        return render(request, "profile_add_link.html")


@login_required
def delete_link(request, link_id):
    try:
        link = Link.objects.get(id=link_id)
        if link.user_id != request.user.id:
            raise Http404("Link does not exists")
        link.delete()
    except ObjectDoesNotExist:
        raise Http404("Link does not exists")

    return redirect("/profile/edit")


def show_profile_posts(request, username):
    user = None

    if request.user is not None and request.user.username == username:
        user = request.user
    else:
        user = ApplicationUser.objects.filter(username=username).first()

    if user is None:
        raise Http404("Product does not exist")

    posts = Post.objects.select_related('author').order_by('-created_on').filter(author_id=user.id)

    likes = []

    if request.user is not None:
        liked_posts = posts.prefetch_related("like_set__user").filter(like__user_id=request.user.id)

        for liked_post in liked_posts:
            likes.append(liked_post.id)

    posts = posts.all()
    followed = Follow.objects.filter(source_id=request.user.id, destination_id=user.id).exists()

    return render(request,
                  "profile_posts.html",
                  {
                      "user_profile": user,
                      "is_current_user": True if username == request.user.username else False,
                      "posts": posts,
                      "likes": likes,
                      "followed": followed})


@login_required
def follow_profile(request, username):
    if request.method != "POST":
        return redirect(f'/profile/user/{username}')

    user = ApplicationUser.objects.prefetch_related("follow_destination").filter(username=username).first()

    if user is None or user.id == request.user.id:
        raise Http404()

    follow = Follow.objects.filter(destination_id=user.id, source_id=request.user.id).first()

    if follow is None:
        new_follow = Follow(source=request.user, destination=user)
        new_follow.save()
    else:
        follow.delete()

    redirect_utl = request.POST.get("redirect_url")

    return redirect(redirect_utl)


def show_profile_followers(request, username):
    user = None

    if request.user is not None and request.user.username == username:
        user = request.user
    else:
        user = ApplicationUser.objects.filter(username=username).prefetch_related('follow_source').first()

    if user is None:
        raise Http404("Product does not exist")

    return render(request, "profile_followers.html", {
        "user_profile": user,
        "is_current_user": True if username == request.user.username else False})


def show_profile_following(request, username):
    user = None

    if request.user is not None and request.user.username == username:
        user = request.user
    else:
        user = ApplicationUser.objects.filter(username=username).prefetch_related('follow_source').first()

    if user is None:
        raise Http404("Product does not exist")

    return render(request, "profile_following.html", {
        "user_profile": user,
        "is_current_user": True if username == request.user.username else False})


def search_profile(request):
    search_pattern = request.GET.get("profile_name")

    profiles = ApplicationUser.objects.filter(username__contains=search_pattern).all()

    return render(request, "profiles_search.html", {"profiles": profiles})
