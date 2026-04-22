import networkx as nx
from core.node import Node

def create_network(n):
    G = nx.complete_graph(n)
    nodes = {i: Node(i) for i in G.nodes()}
    return G, nodes