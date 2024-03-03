import pdb
import pandas as pd


def get_x_size(aisle_length, num_of_margin, margin_gap=0):
    # margin are defaulted to be on both sides
    margin_occupancy = 2 * (num_of_margin + num_of_margin * margin_gap)
    return margin_occupancy + aisle_length


def get_y_size(num_of_aisles, aisle_gap):
    return num_of_aisles + (num_of_aisles - 1) * aisle_gap


def get_z_size(num_of_levels, level_gap):
    return num_of_levels + (num_of_levels - 1) * level_gap


def get_margin_size(num_of_margin, margin_gap):
    return num_of_margin + (num_of_margin - 1) * margin_gap


def get_elevator_size(num_of_elevator, elevator_gap):
    return num_of_elevator + (num_of_elevator - 1) * elevator_gap


def get_node_id(x, y, z, x_size, y_size):
    return x + x_size * y + (x_size * y_size) * z


def create_incomplete_2D_level(z_level, aisle_length, num_of_aisles, aisle_gap, num_of_elevator, connect_level_below, num_of_margin=5, margin_gap=0, elevator_gap=0):

    nodes = []
    edges = []
    y_size = get_y_size(num_of_aisles, aisle_gap)
    x_size = get_x_size(aisle_length, num_of_margin, margin_gap)
    margin_size = get_margin_size(num_of_margin, margin_gap)
    elevator_size = get_elevator_size(num_of_elevator, elevator_gap)

    occupied_aisles = [y for y in range(y_size) if y % (1 + aisle_gap) == 0]
    occupied_columns = [x for x in range(x_size) if ((x >= margin_size and x < margin_size + elevator_size)
                                                     or (x < x_size - margin_size and x >= x_size - margin_size - elevator_size))
                        and (x % (1 + margin_gap) == 0)]

    for y in range(y_size):
        for x in range(x_size):
            if y not in occupied_aisles or x not in occupied_columns:
                continue
            nodes.append(
                [get_node_id(x, y, z_level, x_size, y_size), x, y, z_level])
            edges.append([get_node_id(x, y, z_level - 1, x_size,
                                      y_size), get_node_id(x, y, z_level, x_size, y_size)])
            if connect_level_below:
                edges.append([get_node_id(x, y, z_level, x_size,
                                      y_size), get_node_id(x, y, z_level + 1, x_size, y_size)])
    return nodes, edges


def create_complete_2D_level(z_level, aisle_length, num_of_aisles, aisle_gap, num_of_margin=5, margin_gap=0):

    nodes = []
    edges = []
    y_size = get_y_size(num_of_aisles, aisle_gap)
    x_size = get_x_size(aisle_length, num_of_margin, margin_gap)
    margin_size = get_margin_size(num_of_margin, margin_gap)

    occupied_aisles = [y for y in range(y_size) if y % (1 + aisle_gap) == 0]
    occupied_margins = [x for x in range(x_size) if (
        x <= margin_size or x >= x_size - margin_size - 1) and (x % (1 + margin_gap) == 0)]

    for y in range(y_size):
        for x in range(x_size):
            if y not in occupied_aisles and x not in occupied_margins:
                continue
            nodes.append(
                [get_node_id(x, y, z_level, x_size, y_size), x, y, z_level])
            if x > 0 and y in occupied_aisles:
                edges.append([get_node_id(x - 1, y, z_level, x_size,
                             y_size), get_node_id(x, y, z_level, x_size, y_size)])
            if y > 0 and x in occupied_margins:
                edges.append([get_node_id(x, y - 1, z_level, x_size,
                             y_size), get_node_id(x, y, z_level, x_size, y_size)])
    return nodes, edges


def create3D(aisle_length, num_of_aisles, aisle_gap, num_of_levels, level_gap, num_of_elevator, num_of_agents):

    z_size = get_z_size(num_of_levels, level_gap)
    occupied_levels = [z for z in range(z_size) if z % (1 + level_gap) == 0]

    all_nodes = []
    all_edges = []
    for z in range(z_size):
        if z in occupied_levels:
            nodes, edges = create_complete_2D_level(
                z, aisle_length, num_of_aisles, aisle_gap)
            all_nodes += nodes
            all_edges += edges
        else:
            nodes, edges = create_incomplete_2D_level(
                z, aisle_length, num_of_aisles, aisle_gap, num_of_elevator, z + 1 in occupied_levels)
            all_nodes += nodes
            all_edges += edges

    # print("Num Nodes: {}".format(len(all_nodes)))
    # print("Num Edges: {}".format(len(all_edges)))
    # pdb.set_trace()

    nodeDf = pd.DataFrame(all_nodes, columns=["NodeId", "X", "Y", "Z"])
    # nodeDf.to_csv("{}_{}_{}_{}_{}_{}_Nodes.csv".format(aisle_length, num_of_aisles, aisle_gap, num_of_levels, level_gap, num_of_elevator), index=False)

    edgeDf = pd.DataFrame(all_edges, columns=["nodeFrom", "nodeTo"])
    edgeDf["bidirectional"] = "true"
    # edgeDf.to_csv("{}_{}_{}_{}_{}_{}_Edges.csv".format(aisle_length, num_of_aisles, aisle_gap, num_of_levels, level_gap, num_of_elevator), index=False)
    seed = 1
    # for seed in range(10):
    startGoalLocations = pd.DataFrame({'agentId': range(1, num_of_agents+1)})
    startGoalLocations["startNodeId"] = nodeDf["NodeId"].sample(n=num_of_agents, replace=False, random_state=seed).reset_index(drop=True)
    startGoalLocations["goalNodeId"] = nodeDf["NodeId"].sample(n=num_of_agents, replace=False, random_state=seed).reset_index(drop=True)
        # startGoalLocations.to_csv("all_scens/{}_{}_{}_{}_{}_{}/{}_{}_{}_{}_{}_{}_StartGoalLocations_Seed{}.csv".format(aisle_length, num_of_aisles, aisle_gap, num_of_levels, level_gap, num_of_elevator, aisle_length, num_of_aisles, aisle_gap, num_of_levels, level_gap, num_of_elevator, seed), index=False)
    
    # pdb.set_trace()
    return nodeDf, edgeDf, startGoalLocations

# if __name__ == "__main__":
#     maps = [(50, 10, 5, 10, 5, 2, 2000),
#             (100, 10, 5, 10, 5, 2, 2000),
#             (25, 10, 5, 10, 5, 2, 2000),
#             (50, 20, 5, 10, 5, 2, 2000),
#             (50, 5, 5, 10, 5, 2, 2000),
#             (50, 10, 10, 10, 5, 2, 2000),
#             (50, 10, 2, 10, 5, 2, 2000),
#             (50, 10, 5, 20, 5, 2, 2000),
#             (50, 10, 5, 5, 5, 2, 2000),
#             (50, 10, 5, 10, 10, 2, 2000),
#             (50, 10, 5, 10, 2, 2, 2000),
#             (50, 10, 5, 10, 5, 4, 2000),
#             (50, 10, 5, 10, 5, 1, 2000),
#             (100, 20, 10, 20, 10, 4, 2000),
#             (25, 5, 2, 5, 2, 1, 1000)]
#     for aisle_length, num_of_aisles, aisle_gap, num_of_levels, level_gap, num_of_elevator, num_agents in maps:    
#         nodeDf, edgeDf, startGoalLocations = create3D(aisle_length, num_of_aisles, aisle_gap, num_of_levels, level_gap, num_of_elevator, num_agents)
#         nodeDf.to_csv("all_maps/{}_{}_{}_{}_{}_{}_Nodes.csv".format(aisle_length, num_of_aisles, aisle_gap, num_of_levels, level_gap, num_of_elevator), index=False)
#         edgeDf.to_csv("all_maps/{}_{}_{}_{}_{}_{}_Edges.csv".format(aisle_length, num_of_aisles, aisle_gap, num_of_levels, level_gap, num_of_elevator), index=False)
