#!/usr/bin/env python
import networkx as nx
import matplotlib.pyplot as plt
G = nx.DiGraph()
G.add_node("1511")
G.add_node("2521")
G.add_edge("1511","2521")
nx.draw(G,pos=nx.planar_layout(G))
nx.draw_networkx_labels(G,pos=nx.planar_layout(G))
plt.show()


