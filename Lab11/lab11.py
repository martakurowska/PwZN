import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

nodes = pd.read_csv("musae_ENGB_target.csv")
edges = pd.read_csv("musae_ENGB_edges.csv")

G = nx.MultiGraph()

G.add_nodes_from(nodes["new_id"])
G.add_edges_from(edges.values.tolist())

print(f'Czy graf jest spójny: {nx.is_connected(G)}')
print(f'Liczba spójnych składowych: {nx.number_connected_components(G)}')
print(f'Ilość węzłów z całym grafie: {len(nodes["new_id"])}')
print(f'Ilość węzłów w składowej 1.: {len(list(nx.connected_components(G))[0])}')
print(f"Średnia ścieżka: {nx.average_shortest_path_length(G)}")  # 3.6776157289097005

node_sizes = [len(G.edges(n)) for n in G.nodes()]
pos = nx.spring_layout(G)
nx.draw_networkx_labels(G, pos, font_size=6, alpha=0.4)
nx.draw_networkx_edges(G, pos, alpha=0.05)
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, alpha=0.3)
plt.show()

# degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
# plt.bar(*np.unique(degree_sequence, return_counts=True))
# plt.yscale('log')
# plt.xscale('log')
# plt.title("Degree histogram")
# plt.xlabel("Degree")
# plt.ylabel("# of Nodes")
# plt.show()


