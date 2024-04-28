from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from users.models import ApplicationUser


# Create your views here.

@login_required
def show_current_profile(request):
    return render(request, "profile_template.html", {"user_profile": request.user, "is_current_user": True})


def show_profile_by_username(request, username):
    user = None

    if request.user is not None and request.user.username == username:
        user = request.user
    else:
        user = ApplicationUser.objects.filter(username=username).first()

    if user is None:
        raise Http404("Product does not exist")

    return render(request,
                  "profile_template.html",
                  {"user_profile": user, "is_current_user": True if username == request.user.username else False})


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
        return render(request, "edit_profile.html")
