import json
import os

class CityGraph:
    def __init__(self):
        # Структура: { node_u: { node_v: {'distance': w1, 'time': w2}, ... }, ... }
        self.graph = {}

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = {}
            return True
        return False

    def remove_node(self, node):
        if node in self.graph:
            del self.graph[node]
            for u in self.graph:
                if node in self.graph[u]:
                    del self.graph[u][node]
            return True
        return False

    def add_edge(self, u, v, distance, travel_time):
        if distance < 0 or travel_time < 0:
            raise ValueError("Салмақ терс мән қабылдай алмайды!")
        
        self.add_node(u)
        self.add_node(v)
        
        self.graph[u][v] = {'distance': distance, 'time': travel_time}
        self.graph[v][u] = {'distance': distance, 'time': travel_time} # Бағытталмаған граф

    def remove_edge(self, u, v):
        if u in self.graph and v in self.graph[u]:
            del self.graph[u][v]
            if u in self.graph[v]:
                del self.graph[v][u]
            return True
        return False

    def save_to_json(self, filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.graph, f, indent=4, ensure_ascii=False)

    def load_from_json(self, filepath):
        if not os.path.exists(filepath):
            return False
        with open(filepath, 'r', encoding='utf-8') as f:
            self.graph = json.load(f)
        return True

    def load_default_dataset(self):
        self.graph = {}
        # Набор данных из пункта 5 задания. 
        # Добавлены дефолтные значения для 'time' (дистанция / коэффициент скорости)
        edges = [
            ('A', 'B', 4), ('A', 'C', 2), ('B', 'C', 1), ('B', 'D', 5),
            ('C', 'E', 7), ('C', 'F', 4), ('D', 'E', 2), ('D', 'G', 6),
            ('E', 'F', 1), ('E', 'H', 3), ('F', 'H', 5), ('F', 'I', 8),
            ('G', 'H', 2), ('G', 'J', 7), ('H', 'I', 2), ('H', 'K', 6),
            ('I', 'L', 4), ('I', 'M', 9), ('J', 'K', 1), ('J', 'N', 8),
            ('K', 'L', 3), ('K', 'N', 5), ('L', 'M', 2), ('L', 'O', 7),
            ('M', 'O', 3), ('N', 'O', 4), ('B', 'F', 9), ('E', 'K', 8),
            ('C', 'H', 10), ('G', 'N', 6)
        ]
        for u, v, d in edges:
            # Для демонстрации усложненного задания время немного отличается от расстояния
            t = max(1, int(d * 0.8 if (edges.index((u,v,d)) % 2 == 0) else d * 1.2))
            self.add_edge(u, v, d, t)
