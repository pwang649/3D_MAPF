from io import BytesIO
import os
import zipfile
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from django.views import View

from mapf.core.createWarehouse3D import create3D
from mapf.core.visualization import *


def index(request):
    return default(request)

def generate_map(request):
    global nodes, edges, input1, input2, input3, input4, input5, input6, input7, startGoal
    if request.method == 'POST':
        input1 = int(request.POST.get('input1'))
        input2 = int(request.POST.get('input2'))
        input3 = int(request.POST.get('input3'))
        input4 = int(request.POST.get('input4'))
        input5 = int(request.POST.get('input5'))
        input6 = int(request.POST.get('input6'))
        input7 = int(request.POST.get('input7'))

        nodes, edges, startGoal = create3D(input1, input2, input3, input4, input5, input6, input7)
        html = visualize(nodes, edges)
        context = {
            "map": html,
            "input1": input1,
            "input2": input2,
            "input3": input3,
            "input4": input4,
            "input5": input5,
            "input6": input6,
            "input7": input7,
        }

        return render(request, "index.html", context)

    return render(request, 'index.html')

def default(request):
    global nodes, edges, input1, input2, input3, input4, input5, input6, input7, startGoal
    input1 = 50
    input2 = 10
    input3 = 5
    input4 = 10
    input5 = 5
    input6 = 2
    input7 = 50
    nodes, edges, startGoal = create3D(input1, input2, input3, input4, input5, input6, input7)
    html = visualize(nodes, edges)
    context = {
        "map": html,
        "input1": input1,
        "input2": input2,
        "input3": input3,
        "input4": input4,
        "input5": input5,
        "input6": input6,
        "input7": input7,
    }
    return render(request, "index.html", context)

def download(request):
    global nodes, edges, input1, input2, input3, input4, input5, input6, startGoal
    file_name_nodes = '{}_{}_{}_{}_{}_{}_Nodes.csv'.format(input1, input2, input3, input4, input5, input6)
    file_name_edges = '{}_{}_{}_{}_{}_{}_Edges.csv'.format(input1, input2, input3, input4, input5, input6)
    file_name_start_goal = '{}_{}_{}_{}_{}_{}_StartGoalLocations.csv'.format(input1, input2, input3, input4, input5, input6)
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        zip_file.writestr(file_name_nodes, nodes.to_csv(index=False))
        zip_file.writestr(file_name_edges, edges.to_csv(index=False))
        zip_file.writestr(file_name_start_goal, startGoal.to_csv(index=False))

    zip_name = "nodes_and_edges.zip"

    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{zip_name}"'
    response.write(zip_buffer.getvalue())
    return response
