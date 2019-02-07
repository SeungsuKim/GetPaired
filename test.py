import networkx as nx
import matplotlib.pyplot as plt

G = nx.complete_graph(5)

for node in G.nodes:
    print(type(node))