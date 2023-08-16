from django.http import HttpResponse
from django.shortcuts import render

from hello_world.core.createWarehouse3D import create3D
from hello_world.core.visualization import *


def index(request):
    context = {
        "title": "Django example",
    }
    return render(request, "index.html", context)

def test1(request):
    create3D(50, 10, 5, 10, 5, 2)
    return HttpResponse("hello")

def test2(request):
    visualize_map()
    return render(request, "50_10_5_10_5_2.html", None)

def test3(request):
    animate_paths()
    return render(request, "backAndForth.html", None)
