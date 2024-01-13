from django.http import HttpResponse
from django.shortcuts import render

from mapf.core.createWarehouse3D import create3D
from mapf.core.visualization import *


def index(request):
    context = {
        "title": "Django example",
    }
    return render(request, "index.html", context)

def generate_map(request):
    if request.method == 'POST':
        input1 = int(request.POST.get('input1'))
        input2 = int(request.POST.get('input2'))
        input3 = int(request.POST.get('input3'))
        input4 = int(request.POST.get('input4'))
        input5 = int(request.POST.get('input5'))
        input6 = int(request.POST.get('input6'))

        nodes, edges = create3D(input1, input2, input3, input4, input5, input6)
        html = visualize(nodes, edges)
        context = {
            "map": html,
        }

        return render(request, "index.html", context)

    return render(request, 'index.html')

def test3(request):
    nodes, edges = create3D(50, 10, 5, 10, 5, 2)
    html = visualize(nodes, edges)
    context = {
        "map": html,
    }
    return render(request, "index.html", context)