import networkx as nx

def build_keyword_graph(texts):
    graph = nx.Graph()
    for text in texts:
        words = text.split()
        for i in range(len(words) - 1):
            graph.add_edge(words[i], words[i + 1])
    return graph
