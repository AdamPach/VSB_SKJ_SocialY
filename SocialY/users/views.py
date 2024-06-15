from django.shortcuts import render, redirect
from django.db.utils import IntegrityError
from .models import ApplicationUser
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.

def users(request):
    return render(request, 'base.html')


def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_check = request.POST.get("passwordCheck")

        if password_check != password or len(password) < 8:
            return render(request, "register.html", {"error_message": "Check if your password fits the rights"})

        try:
            user = ApplicationUser.objects.create_user(username, email=email, password=password)
            user.is_staff = False
        except IntegrityError:
            return render(request, "register.html", {"error_message": "This user name is already used"})

        validation_result = user.full_clean()

        if validation_result is not None:
            user.delete()
            return render(request, "register.html", {"error_message": "You provide a bad credentials, check if "
                                                                      "everything is correct"})

        user.save()
        return redirect("/users/auth/login")
    else:
        return render(request, "register.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/profile')

        return render(request, "login.html", {"error_message": "Auth failed, please check your credentials"})
    else:
        return render(request, "login.html")


@login_required
def logout_user(request):
    logout(request)
    return redirect('/index?message=Successfully%20logged%20out')
