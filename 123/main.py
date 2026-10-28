import tkinter as tk
from tkinter import messagebox, ttk
from graph import CityGraph
from dijkstra import dijkstra
from visualization import draw_city_graph

class SmartCityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ақылды қала: Ең тиімді маршрутты анықтау")
        self.root.geometry("450x650")
        
        self.city_graph = CityGraph()
        self.json_path = "data/city_graph.json"
        
        # Попытка загрузить данные из JSON, иначе загружаем дефолтный датасет
        if not self.city_graph.load_from_json(self.json_path):
            self.city_graph.load_default_dataset()
            self.city_graph.save_to_json(self.json_path)

        self.create_widgets()
        self.update_comboboxes()

    def create_widgets(self):
        # Панель выбора маршрута
        frame_route = ttk.LabelFrame(self.root, text=" Маршрутты есептеу ")
        frame_route.pack(fill="x", padx=15, pady=10)
        
        ttk.Label(frame_route, text="Бастапқы нүкте:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.cb_start = ttk.Combobox(frame_route, width=10, state="readonly")
        self.cb_start.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_route, text="Соңғы нүкте:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.cb_end = ttk.Combobox(frame_route, width=10, state="readonly")
        self.cb_end.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame_route, text="Режим:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.mode_var = tk.StringVar(value="distance")
        ttk.Radiobutton(frame_route, text="Қашықтық", variable=self.mode_var, value="distance").grid(row=2, column=1, sticky='w')
        ttk.Radiobutton(frame_route, text="Уақыт", variable=self.mode_var, value="time").grid(row=2, column=2, sticky='w')

        ttk.Label(frame_route, text="Жолды жабу (U->V):").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.cb_block_u = ttk.Combobox(frame_route, width=5, state="readonly")
        self.cb_block_u.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.cb_block_v = ttk.Combobox(frame_route, width=5, state="readonly")
        self.cb_block_v.grid(row=3, column=2, padx=5, pady=5, sticky='w')

        btn_calc = ttk.Button(frame_route, text="Есептеу және Көрсету", command=self.calculate_route)
        btn_calc.grid(row=4, column=0, columnspan=3, pady=10)

        # Панель управления элементами графа
        frame_manage = ttk.LabelFrame(self.root, text=" Графты басқару ")
        frame_manage.pack(fill="x", padx=15, pady=10)
        
        ttk.Label(frame_manage, text="Төбе (Қосу/Жою):").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.ent_node = ttk.Entry(frame_manage, width=10)
        self.ent_node.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(frame_manage, text="+", width=4, command=self.add_node).grid(row=0, column=2, padx=2)
        ttk.Button(frame_manage, text="-", width=4, command=self.del_node).grid(row=0, column=3, padx=2)

        # Результаты вычислений
        frame_res = ttk.LabelFrame(self.root, text=" Нәтиже ")
        frame_res.pack(fill="both", expand=True, padx=15, pady=10)
        
        self.txt_output = tk.Text(frame_res, height=12, wrap="word")
        self.txt_output.pack(fill="both", expand=True, padx=5, pady=5)

    def update_comboboxes(self):
        nodes = sorted(list(self.city_graph.graph.keys()))
        self.cb_start['values'] = nodes
        self.cb_end['values'] = nodes
        
        nodes_with_empty = [""] + nodes
        self.cb_block_u['values'] = nodes_with_empty
        self.cb_block_v['values'] = nodes_with_empty

    def add_node(self):
        node = self.ent_node.get().strip().upper()
        if node:
            if self.city_graph.add_node(node):
                self.city_graph.save_to_json(self.json_path)
                self.update_comboboxes()
                messagebox.showinfo("Сәтті", f"Төбе {node} қосылды.")
            else:
                messagebox.showwarning("Қате", "Төбе бұрыннан бар!")
                
    def del_node(self):
        node = self.ent_node.get().strip().upper()
        if node:
            if self.city_graph.remove_node(node):
                self.city_graph.save_to_json(self.json_path)
                self.update_comboboxes()
                messagebox.showinfo("Сәтті", f"Төбе {node} жойылды.")
            else:
                messagebox.showwarning("Қате", "Төбе табылмады!")

    def calculate_route(self):
        u_start = self.cb_start.get()
        v_end = self.cb_end.get()
        mode = self.mode_var.get()
        
        bu = self.cb_block_u.get()
        bv = self.cb_block_v.get()
        blocked = (bu, bv) if (bu and bv) else None

        # Валидация ошибок по ТЗ
        if not u_start or not v_end:
            messagebox.showerror("Қате", "Бастапқы және соңғы төбелерді таңдаңыз!")
            return
        if u_start == v_end:
            self.txt_output.delete("1.0", tk.END)
            self.txt_output.insert(tk.END, f"Бастапқы нүкте соңғы нүктеге тең.\nМаршрут ұзындығы: 0")
            draw_city_graph(self.city_graph, path=[u_start], mode=mode, blocked_edge=blocked)
            return

        # Запуск алгоритма
        path, total_weight, visited, exec_time, _ = dijkstra(
            self.city_graph.graph, u_start, v_end, mode=mode, blocked_edge=blocked
        )
        
        self.txt_output.delete("1.0", tk.END)
        if not path:
            self.txt_output.insert(tk.END, f"Маршрут табылмады! (Байланыс жоқ немесе жол жабылған)")
            draw_city_graph(self.city_graph, path=None, mode=mode, blocked_edge=blocked)
            return

        # Вывод статистики
        res_str = (
            f"Бағыт: {' -> '.join(path)}\n"
            f"Жалпы салмағы ({'қашықтық' if mode=='distance' else 'уақыт'}): {total_weight}\n"
            f"Қаралған төбелер саны: {visited}\n"
            f"Орындалу уақыты: {exec_time*1000:.4f} мс\n"
        )
        self.txt_output.insert(tk.END, res_str)
        
        # Интерактивное обновление окна Matplotlib
        draw_city_graph(self.city_graph, path=path, mode=mode, blocked_edge=blocked)

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartCityApp(root)
    root.mainloop()
