import networkx as nx

def build_entity_graph(records):
    G = nx.Graph()
    for r in records:
        G.add_node(r["vendor"], type="vendor")
        G.add_node(r["title"], type="item")
        G.add_edge(r["vendor"], r["title"])
    return G
