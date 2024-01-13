import plotly.graph_objects as go

def visualize(ndf, edf):
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

    fig = go.Figure(data=traces)
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), height=800)
    
    # fig.write_image("../figs/maps/" + map_prefix + ".png")
    # fig.write_html('test.html')
    return fig.to_html()
    # return plt_div
   
# if __name__ == "__main__":

#     parser = argparse.ArgumentParser(
#                 prog='visualize 3D warehosue',
#                 description='For creating visualizing 3D warehosue maps and solutions')

#     parser.add_argument('-n', '--nodes_path', type=str)
#     parser.add_argument('-e', '--edges_path', type=str)
#     parser.add_argument('-o', '--output_path', type=str)
#     parser.add_argument('-p', '--solution_paths', type=str, required=False, default=None)
#     parser.add_argument('-sp', '--solution_output_path', type=str, required=False, default=None)

#     args = parser.parse_args()

#     visualize(args.nodes_path, args.edges_path, args.output_path, args.solution_paths, args.solution_output_path)
