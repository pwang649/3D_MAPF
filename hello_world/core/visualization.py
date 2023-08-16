# %%
import plotly.express as px
import plotly.graph_objects as go
import os
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import pdb

def visualize_map():
    # %%
    map_prefix = "50_10_5_10_5_2"
    ndf = pd.read_csv("" + map_prefix + "_Nodes.csv")
    edf = pd.read_csv("" + map_prefix + "_Edges.csv")


    # %%
    ### Plotly
    newDf = []
    traces = []

    xLines, yLines, zLines = [], [], []
    for index, row in edf.iterrows():
        bidir = row['bidirectional']
        node1 = ndf.loc[ndf['NodeId'] == row['nodeFrom']]
        node2 = ndf.loc[ndf['NodeId'] == row['nodeTo']]
        xline = [node1['X'].iloc[0], node2['X'].iloc[0]]
        yline = [node1['Y'].iloc[0], node2['Y'].iloc[0]]
        zline = [node1['Z'].iloc[0], node2['Z'].iloc[0]]
        # aTrace = go.Scatter3d(x=xline, y=yline, z=zline, mode='lines', line=dict(color="blue"), hoverinfo='skip', showlegend=False)
        # traces.append(aTrace)
        vals = [xline[0], yline[0], zline[0], xline[1], yline[1], zline[1]]
        newDf.append([row["nodeFrom"], row["nodeFrom"], bidir, *vals])

        xLines.extend([*xline, None])
        yLines.extend([*yline, None])
        zLines.extend([*zline, None])
    aTrace = go.Scatter3d(x=xLines, y=yLines, z=zLines, mode='lines', line=dict(color="blue"), hoverinfo='skip', showlegend=False)
    traces.append(aTrace)
    # fig = go.Figure(data=traces)
    # fig.write_image("testPlotly.png")
    # plt.show()

    # %%
    fig = go.Figure(data=traces)
    # fig.write_image("../figs/maps/" + map_prefix + ".png")
    fig.write_html("hello_world/templates/" + map_prefix + ".html")

def animate_paths():
    map_prefix = "50_10_5_10_5_2"
    ndf = pd.read_csv("" + map_prefix + "_Nodes.csv")
    pdf = pd.read_csv("paths.csv")
    pdf = pdf.iloc[:, :-1] # Drop last empty column
    # %%
    ### Creating traces of
    pathTraces = []
    for index, row in pdf.iterrows():
        tmpdf = ndf.iloc[row[1:]]
        aTrace = go.Scatter3d(x=tmpdf["X"], y=tmpdf["Y"], z=tmpdf["Z"], mode='lines', hoverinfo="skip", showlegend=False)
        pathTraces.append(aTrace)

    # %%
    # fig = go.Figure(data=pathTraces)
    # fig.write_image("testPlotly.png")

    # %%
    ### Create animations
    numFrames = len(pdf.columns) - 1 # First columns is the string "Timesteps"
    numAgents = pdf.shape[0]
    agentColors = list(range(numAgents))

    def getSingleFrame(curT):
        curLocs = ndf.iloc[pdf[str(curT)]]
        return go.Frame(name=str(curT),
                        data = go.Scatter3d(x=curLocs["X"], y=curLocs["Y"], z=curLocs["Z"],
                            mode="markers", marker=dict(size=6, color=agentColors), showlegend=False, hoverinfo="skip"))
    allFrames = [getSingleFrame(t) for t in range(numFrames)]

    # %%
    ### https://plotly.com/python/visualizing-mri-volume-slices/?_ga=2.213007632.583970308.1664493502-1988171524.1656003349
    def sliderFrameArgs(duration):
        return {
                "frame": {"duration": duration},
                "mode": "immediate",
                "fromcurrent": True,
                "transition": {"duration": duration, "easing": "linear"},
            }

    sliders = [{
                "pad": {"b": 10, "t": 60},
                "len": 0.6,
                "x": 0.22,
                "y": 0,
                "steps": [
                    {
                        "args": [[f.name], sliderFrameArgs(300)],
                        "label": str(k),
                        "method": "animate",
                    }
                    for k, f in enumerate(allFrames)]
                }]

    fig = go.Figure(frames=allFrames,
        # data=traces, ## Show entire grid, significantly slows down animation
        # data=allFrames[0].data, ## First frame, no grid lines
        data=pathTraces,  ## Show path traces, animation works fine
        layout=go.Layout(
            title="3D MAPF Animation",
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="&#9654;", # play symbol
                              method="animate",
                              args=[None, sliderFrameArgs(300)]),
                        dict(label="&#9724;", # pause symbol
                            method="animate",
                            args=[[None], sliderFrameArgs(0)])
                ],
                direction="left",
                pad={"r": 10, "t": 70},
                x=0.22,
                y=0)],
            sliders=sliders)
        )
    # fig.update_layout(sliders=sliders)

    # %%
    fig.write_html("hello_world/templates/backAndForth.html")

    # %%



