from django.shortcuts import render


# Create your views here.

def get_index(request):
    message = request.GET.get("message")
    return render(request, 'index_page.html', {'message': message})
