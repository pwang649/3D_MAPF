import os
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from django.views import View

from mapf.core.createWarehouse3D import create3D
from mapf.core.visualization import *


def index(request):
    return default(request)

def generate_map(request):
    global nodes, edges, input1, input2, input3, input4, input5, input6
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
            "input1": input1,
            "input2": input2,
            "input3": input3,
            "input4": input4,
            "input5": input5,
            "input6": input6,
        }

        return render(request, "index.html", context)

    return render(request, 'index.html')

def default(request):
    nodes, edges = create3D(50, 10, 5, 10, 5, 2)
    html = visualize(nodes, edges)
    context = {
        "map": html,
        "input1": 50,
        "input2": 10,
        "input3": 5,
        "input4": 10,
        "input5": 5,
        "input6": 2,
    }
    return render(request, "index.html", context)

def download_nodes(request):
    global nodes, input1, input2, input3, input4, input5, input6
    file_name = '{}_{}_{}_{}_{}_{}_Nodes.csv'.format(input1, input2, input3, input4, input5, input6)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    nodes.to_csv(response, index=False)
    return response

def download_edges(request):
    global edges, input1, input2, input3, input4, input5, input6
    file_name = '{}_{}_{}_{}_{}_{}_Edges.csv'.format(input1, input2, input3, input4, input5, input6)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    edges.to_csv(response, index=False)
    return response
