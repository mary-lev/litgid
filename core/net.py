import plotly.graph_objs as go
import networkx as nx
import random

#G = nx.random_geometric_graph(200, 0.125)
G = nx.Graph()

G.add_edge('First', 'Second', weight=1)
G.add_edge('Second', 'Third', weight=1)
G.add_edge('Third', 'Fourth', weight=1)
G.add_edge('Fourth', 'First', weight=1)
G.add_edge('One', 'Two', weight=2)

layt = nx.spring_layout(G, dim=2) # Generates the layout of the graph
Xn = [layt[k][0] for k in list(layt.keys())]  # x-coordinates of nodes
Yn = [layt[k][1] for k in list(layt.keys())]  # y-coordinates
Xe = []
Ye = []

plot_weights = []
for e in G.edges():
    Xe += [layt[e[0]][0], layt[e[1]][0], None]
    Ye += [layt[e[0]][1], layt[e[1]][1], None]
    ax = (layt[e[0]][0]+layt[e[1]][0])/2
    ay = (layt[e[0]][1]+layt[e[1]][1])/2
    plot_weights.append((random.randrange(3), ax, ay))

"""edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')"""

edge_trace = go.Scatter(
    x=Xe,
    y=Ye,
    mode='lines',
    line=dict(color='rgb(90, 90, 90)', width=1),
    hoverinfo='none'
    )

"""node_x = []
node_y = []
for node in G.nodes():
    x, y = G.nodes[node]['pos']
    node_x.append(x)
    node_y.append(y)"""

"""node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        # colorscale options
        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line_width=2))"""

node_trace = go.Scatter(
    x=Xn,
    y=Yn,
    mode='markers+text',
    name='Nodes',
    marker=dict(symbol='circle',
        size=8,
        #color=group,
        colorscale='Viridis',
        line=dict(color='rgb(255,255,255)', width=1)
        ),
    text="test",
    textposition='top center',
    hoverinfo='none'
    )


data = [edge_trace, node_trace]
