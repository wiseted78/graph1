import networkx as nx
import matplotlib.pyplot as plt

def draw_city_graph(graph_obj, path=None, mode='distance', blocked_edge=None):
    plt.clf() # Очистка текущей фигуры
    G = nx.Graph()
    
    # Построение NetworkX структуры
    for u in graph_obj.graph:
        for v, attrs in graph_obj.graph[u].items():
            G.add_edge(u, v, weight=attrs[mode])
            
    # Фиксированный лейаут для стабильности картинки
    pos = nx.spring_layout(G, seed=42)
    
    # Обычные ребра и узлы
    nx.draw_networkx_nodes(G, pos, node_color='#A0CBE2', node_size=600)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    
    # Отрисовка всех ребер базовым стилем
    edge_labels = {}
    for u, v, d in G.edges(data=True):
        edge_labels[(u, v)] = f"{d['weight']}"
    
    nx.draw_networkx_edges(G, pos, edge_color='gray', width=1.5, style='solid')
    
    # Если есть заблокированное ребро — подсвечиваем его пунктиром/красным
    if blocked_edge:
        u, v = blocked_edge
        if G.has_edge(u, v):
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color='red', width=2, style='dashed')
            
    # Если найден кратчайший путь — выделяем его толстой зеленой линией
    if path and len(path) > 1:
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='#2ca02c', width=4)
        
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)
    plt.title(f"Маршруттар жүйесі ({'Қашықтық' if mode=='distance' else 'Уақыт'} бойынша)")
    plt.axis('off')
    plt.tight_layout()
    plt.show(block=False)
