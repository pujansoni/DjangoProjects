from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def home_view(request, *args, **kwargs):
    print(request.user)
    return render(request, "home.html", {})


def contact_view(request, *args, **kwargs):
    return render(request, "contact.html", {})


def about_view(request, *args, **kwargs):
    # Here the my_text and my_number keys are directly accessible in about.html view
    my_context = {
        "my_text": "This is about us",
        "my_number": 123,
        "my_list": [123, 456, 789]
    }
    return render(request, "about.html", my_context)
