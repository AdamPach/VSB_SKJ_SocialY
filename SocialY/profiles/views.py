from django.shortcuts import render
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

    return render(request, "profile_template.html", {"user_profile": user, "is_current_user": True if username == request.user.username else False})
