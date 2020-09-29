import plotly.graph_objs as go
import plotly.offline as opy
import networkx as nx
import random

#G = nx.random_geometric_graph(200, 0.125)
G = nx.Graph()

G.add_edge('First', 'Second', weight=10)
G.add_edge('Second', 'Third', weight=5)
G.add_edge('Third', 'Fourth', weight=15)
G.add_edge('Fourth', 'First', weight=1)
G.add_edge('One', 'Two', weight=2)

edge_weights = nx.get_edge_attributes(G,'weight')

labels = [] # names of the nodes to plot
group = [] # id of the communities
group_cnt = 0

for node in G.nodes():
    labels.append(node)

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
    plot_weights.append((edge_weights[(e[0], e[1])], ax, ay))

annotations_list = [
                    dict(
                        x=plot_weight[1],
                        y=plot_weight[2],
                        xref='x',
                        yref='y',
                        text=plot_weight[0],
                        showarrow=True,
                        arrowhead=7,
                        ax=plot_weight[1],
                        ay=plot_weight[2]
                        ) 
                    for plot_weight in plot_weights
                    ]

edge_trace = go.Scatter(
    x=Xe,
    y=Ye,
    mode='lines',
    line=dict(color='rgb(90, 90, 90)', width=1),
    hoverinfo='none'
    )

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
    text=labels,
    textposition='top center',
    hoverinfo='none'
    )

xaxis = dict(
    backgroundcolor="rgb(200, 200, 230)",
    #gridcolor="rgb(255, 255, 255)",
    showbackground=True,
    showgrid=False,
    zerolinecolor="rgb(255, 255, 255)"
    )
yaxis = dict(
    backgroundcolor="rgb(230, 200,230)",
    #gridcolor="rgb(255, 255, 255)",
    showbackground=True,
    showgrid=False,
    zerolinecolor="rgb(255, 255, 255)"
    )

"""layout=go.Layout(
            title=,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
            )"""

layout = go.Layout(
        title="Тут будет граф",
        showlegend=False,
        plot_bgcolor="rgb(230, 230, 200)",
        scene=dict(
            xaxis=dict(xaxis),
            yaxis=dict(yaxis)
        ),
        margin=dict(
            t=100
        ),
        hovermode='closest',
        annotations=annotations_list
        , )

data = [edge_trace, node_trace]
figure=go.Figure(data=data,layout=layout)
net_div = opy.plot(figure, auto_open=False, output_type='div')
