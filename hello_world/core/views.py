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

    return HttpResponse("heloi")

def test2(request):
    visualize_map()
    return render(request, "50_10_5_10_5_2.html", None)

def test3(request):
    animate_paths()
    return render(request, "backAndForth.html", None)
