from django.shortcuts import render
from .models import Foo


def index(request):
    return render(request, "index.html")

