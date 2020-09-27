import plotly.graph_objs as go
import networkx as nx

G = nx.random_geometric_graph(200, 0.125)
x = [-2,0,4,6,7]
y = [q**2-q+3 for q in x]
trace1 = go.Scatter(x=x, y=y, marker={'color': 'red', 'symbol': 104, 'size': 10},
    mode="lines",  name='1st Trace')