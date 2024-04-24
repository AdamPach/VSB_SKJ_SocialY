from django.shortcuts import render
from django.http import HttpResponse
from django.db.utils import IntegrityError
from django.contrib.auth.models import User


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
            user = User.objects.create_user(username, email=email, password=password)
            user.is_staff = False
        except IntegrityError:
            return render(request, "register.html", {"error_message": "This user name is already used"})

        validation_result = user.full_clean()

        if validation_result is not None:
            user.delete()
            return render(request, "register.html", {"error_message": "You provide a bad credentials, check if "
                                                                      "everything is correct"})

        user.save()
        return HttpResponse("Registration successfully")
    else:
        return render(request, "register.html")
