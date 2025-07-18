import networkx as nx
import random
import matplotlib.pyplot as plt

def cpp(n=6, p=0.4, weight_range=(1, 10), seed=None):
    G = nx.Graph()
    G.add_nodes_from(range(n))

    nodes = list(G.nodes())
    random.shuffle(nodes)
    for i in range(n - 1):
        w = random.randint(*weight_range)
        G.add_edge(nodes[i], nodes[i + 1], weight=w)

    for u in range(n):
        for v in range(u + 1, n):
            if not G.has_edge(u, v) and random.random() < p:
                w = random.randint(*weight_range)
                G.add_edge(u, v, weight=w)

    return G


def dcpp(n=6, p=0.4, weight_range=(1, 10), seed=None):
    G = nx.DiGraph()
    G.add_nodes_from(range(n))

    nodes = list(G.nodes())
    random.shuffle(nodes)
    for i in range(n - 1):
        w = random.randint(*weight_range)
        G.add_edge(nodes[i], nodes[i + 1], weight=w)

    for u in range(n):
        for v in range(n):
            if u != v and not G.has_edge(u, v) and random.random() < p:
                w = random.randint(*weight_range)
                G.add_edge(u, v, weight=w)
    return G


def draw_graph(G, title="Graph"):
    pos = nx.spring_layout(G, seed=42)
    edge_labels = nx.get_edge_attributes(G, 'weight')

    plt.figure(figsize=(6, 6))
    if G.is_directed():
        nx.draw_networkx(G, pos, arrows=True, node_color="#b4e0f5")
    else:
        nx.draw(G, pos, with_labels=True, node_color="#b4e0f5")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title(title)
    plt.axis("off")
    plt.show()

