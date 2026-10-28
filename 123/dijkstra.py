import heapq
import time

def dijkstra(graph_data, start, end, mode='distance', blocked_edge=None):
    """
    Самостоятельная реализация алгоритма Дейкстра.
    mode: 'distance' или 'time'
    blocked_edge: кортеж (u, v) или (v, u) для временно заблокированного ребра
    """
    start_time = time.perf_counter()
    
    # Инициализация структур данных
    distances = {node: float('inf') for node in graph_data}
    previous = {node: None for node in graph_data}
    distances[start] = 0
    
    # Приоритетная очередь: (текущий_вес, текущая_вершина)
    priority_queue = [(0, start)]
    visited_count = 0
    
    while priority_queue:
        current_weight, u = heapq.heappop(priority_queue)
        
        # Если нашли вершину с большим весом, пропускаем (уже обработана оптимальнее)
        if current_weight > distances[u]:
            continue
            
        visited_count += 1
        
        if u == end and end is not None:
            break

        # Обход соседей
        for neighbor, edge_attrs in graph_data[u].items():
            # Проверка на заблокированное ребро
            if blocked_edge and ((u == blocked_edge[0] and neighbor == blocked_edge[1]) or 
                                 (u == blocked_edge[1] and neighbor == blocked_edge[0])):
                continue
                
            # Выбор метрики оптимизации
            weight = edge_attrs.get(mode, float('inf'))
            
            # Релаксация ребра
            distance = current_weight + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = u
                heapq.heappush(priority_queue, (distance, neighbor))
                
    execution_time = time.perf_counter() - start_time
    
    # Восстановление пути
    path = []
    if distances.get(end) != float('inf'):
        curr = end
        while curr is not None:
            path.append(curr)
            curr = previous[curr]
        path.reverse()
        
    return path, distances.get(end, float('inf')), visited_count, execution_time, distances
