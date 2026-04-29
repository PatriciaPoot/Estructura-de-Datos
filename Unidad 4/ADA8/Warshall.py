import tkinter as tk
from tkinter import messagebox, simpledialog
import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
from matplotlib.patches import FancyArrowPatch
from collections import deque

class EditorGrafosWarshall:
    def __init__(self, root):
        self.root = root
        self.root.title("Warshall - Cierre Transitivo")
        self.root.geometry("1200x850")
        self.root.configure(bg="#1e1e1e")
        self.root.after(50, self._iniciar)
    def _iniciar(self):
        self.es_dirigido = messagebox.askyesno("Tipo de grafo", "¿Deseas que el grafo sea DIRIGIDO?")
        self.G = nx.DiGraph() if self.es_dirigido else nx.Graph()
        self.pos, self.nodo_seleccionado, self.camino_resaltado = {}, None, []
        self._crear_menu()
        self._crear_grafico()
    def _crear_menu(self):
        container = tk.Frame(self.root, width=300, bg="#252526")
        container.pack(side=tk.LEFT, fill=tk.Y)
        container.pack_propagate(False)
        canvas = tk.Canvas(container, bg="#252526", highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        menu = tk.Frame(canvas, bg="#252526")
        canvas.create_window((0, 0), window=menu, anchor="nw", width=280)
        def on_mousewheel(e): canvas.yview_scroll(int(-1*(e.delta/120)), "units")
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        tk.Label(menu, text=f"GRAFO {'DIRIGIDO' if self.es_dirigido else 'NO DIRIGIDO'}", 
                font=("Impact", 18), bg="#252526", fg="#ffcc99", pady=10).pack()
        tk.Label(menu, text="✚ NUEVO NODO", font=("Segoe UI", 10, "bold"), bg="#252526", fg="white").pack(pady=(10,0))
        self.ent_nodo = tk.Entry(menu, justify='center')
        self.ent_nodo.pack(pady=5, padx=20, fill=tk.X)
        tk.Button(menu, text="AGREGAR NODO", command=self.agregar_nodo, bg="#bde0fe").pack(pady=5, fill=tk.X, padx=20)
        tk.Frame(menu, height=2, bg="#444444").pack(fill=tk.X, pady=10)
        tk.Label(menu, text="🔗 CONEXIONES", font=("Segoe UI", 10, "bold"), bg="#252526", fg="white").pack(pady=(10,0))
        tk.Label(menu, text="Origen:", bg="#252526", fg="white").pack()
        self.ent_orig = tk.Entry(menu, justify='center')
        self.ent_orig.pack(pady=2, padx=20, fill=tk.X)
        tk.Label(menu, text="Destino:", bg="#252526", fg="white").pack()
        self.ent_dest = tk.Entry(menu, justify='center')
        self.ent_dest.pack(pady=2, padx=20, fill=tk.X)
        tk.Label(menu, text="Peso:", bg="#252526", fg="white").pack()
        self.ent_peso = tk.Entry(menu, justify='center')
        self.ent_peso.pack(pady=2, padx=20, fill=tk.X)
        tk.Button(menu, text="CONECTAR", command=self.agregar_arista, bg="#baffc9").pack(pady=5, fill=tk.X, padx=20)
        tk.Frame(menu, height=2, bg="#444444").pack(fill=tk.X, pady=10)
        tk.Label(menu, text="⚡ WARSHALL", font=("Segoe UI", 10, "bold"), bg="#252526", fg="white").pack(pady=(10,0))
        tk.Button(menu, text="CALCULAR WARSHALL", command=self.calcular_warshall, bg="#ffcc99").pack(pady=5, fill=tk.X, padx=20)
        tk.Label(menu, text="Desde:", bg="#252526", fg="white").pack(pady=(10,0))
        self.ent_desde = tk.Entry(menu, justify='center')
        self.ent_desde.pack(pady=2, padx=20, fill=tk.X)
        tk.Label(menu, text="Hasta:", bg="#252526", fg="white").pack()
        self.ent_hasta = tk.Entry(menu, justify='center')
        self.ent_hasta.pack(pady=2, padx=20, fill=tk.X)
        tk.Button(menu, text="BUSCAR CAMINO", command=self.buscar_camino, bg="#e0bbff").pack(pady=5, fill=tk.X, padx=20)
        tk.Frame(menu, height=2, bg="#444444").pack(fill=tk.X, pady=10)
        tk.Label(menu, text="✎ EDICIÓN", font=("Segoe UI", 10, "bold"), bg="#252526", fg="white").pack(pady=(10,0))
        tk.Button(menu, text="EDITAR NOMBRE", command=self.editar_nodo, bg="#ffffba").pack(pady=5, fill=tk.X, padx=20)
        tk.Button(menu, text="ELIMINAR NODO", command=self.eliminar_nodo, bg="#ff9aa2").pack(pady=5, fill=tk.X, padx=20)
        tk.Button(menu, text="ELIMINAR ARISTA", command=self.eliminar_arista, bg="#ffb3ba").pack(pady=5, fill=tk.X, padx=20)
        tk.Frame(menu, height=2, bg="#444444").pack(fill=tk.X, pady=10)
        tk.Label(menu, text="📊 INFORMACIÓN", font=("Segoe UI", 10, "bold"), bg="#252526", fg="white").pack(pady=(10,0))
        tk.Button(menu, text="VACIAR", command=self.vaciar, bg="#d8bfff").pack(pady=5, fill=tk.X, padx=20)
        tk.Button(menu, text="SALIR", command=self.root.quit, bg="#ff6b6b", fg="white").pack(pady=20, fill=tk.X, padx=20)
        menu.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
    def _crear_grafico(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 8), facecolor="#1e1e1e")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas.mpl_connect("button_press_event", self._on_press)
        self.canvas.mpl_connect("button_release_event", self._on_release)
        self.canvas.mpl_connect("motion_notify_event", self._on_motion)
        self.actualizar()
    def agregar_nodo(self):
        n = self.ent_nodo.get().strip()
        if n and n not in self.G:
            self.G.add_node(n)
            ang = 2 * math.pi * len(self.pos) / 8
            self.pos[n] = [0.5 + 0.35 * math.cos(ang), 0.5 + 0.35 * math.sin(ang)]
            self.actualizar()
            self.ent_nodo.delete(0, tk.END)
    def agregar_arista(self):
        u, v, p = self.ent_orig.get().strip(), self.ent_dest.get().strip(), self.ent_peso.get().strip()
        if u in self.G and v in self.G and p.isdigit() and int(p) > 0:
            self.G.add_edge(u, v, weight=int(p))
            self.camino_resaltado = []
            self.actualizar()
            for e in [self.ent_orig, self.ent_dest, self.ent_peso]:
                e.delete(0, tk.END)
    def eliminar_arista(self):
        u = simpledialog.askstring("Eliminar arista", "Origen:", parent=self.root)
        if u and u in self.G:
            v = simpledialog.askstring("Eliminar arista", "Destino:", parent=self.root)
            if v and v in self.G and self.G.has_edge(u, v):
                self.G.remove_edge(u, v)
                self.camino_resaltado = []
                self.actualizar()
    def eliminar_nodo(self):
        n = simpledialog.askstring("Eliminar nodo", "Nombre:", parent=self.root)
        if n and n in self.G:
            self.G.remove_node(n)
            if n in self.pos:
                del self.pos[n]
            self.camino_resaltado = []
            self.actualizar()
    def editar_nodo(self):
        v = simpledialog.askstring("Editar nodo", "Actual:", parent=self.root)
        if v and v in self.G:
            n = simpledialog.askstring("Editar nodo", "Nuevo nombre:", parent=self.root)
            if n and n not in self.G:
                nx.relabel_nodes(self.G, {v: n}, copy=False)
                self.pos[n] = self.pos.pop(v)
                self.actualizar()
    def vaciar(self):
        self.G.clear()
        self.pos.clear()
        self.camino_resaltado = []
        self.actualizar()
    def _warshall(self):
        nodos = list(self.G.nodes())
        n = len(nodos)
        idx = {n: i for i, n in enumerate(nodos)}
        m = [[i == j for j in range(n)] for i in range(n)]
        for u, v in self.G.edges():
            if u in idx and v in idx:
                m[idx[u]][idx[v]] = True
                if not self.es_dirigido:
                    m[idx[v]][idx[u]] = True
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if m[i][k] and m[k][j]:
                        m[i][j] = True
        return nodos, m
    def _bfs(self, inicio, fin):
        if inicio == fin:
            return [inicio]
        q = deque([(inicio, [inicio])])
        v = {inicio}
        while q:
            n, p = q.popleft()
            for vec in self.G.neighbors(n):
                if vec == fin:
                    return p + [fin]
                if vec not in v:
                    v.add(vec)
                    q.append((vec, p + [vec]))
        return None
    def calcular_warshall(self):
        if not self.G.nodes():
            messagebox.showinfo("Warshall", "Grafo vacío", parent=self.root)
            return
        nodos, m = self._warshall() 
        v = tk.Toplevel(self.root)
        v.title("Matriz de alcanzabilidad")
        v.configure(bg="#1e1e1e")
        frame = tk.Frame(v, bg="#1e1e1e")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  
        canvas = tk.Canvas(frame, bg="#1e1e1e", highlightthickness=0)
        sb_y = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        sb_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=canvas.xview)
        canvas.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)
        sb_y.pack(side=tk.RIGHT, fill=tk.Y)
        sb_x.pack(side=tk.BOTTOM, fill=tk.X)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)   
        cont = tk.Frame(canvas, bg="#1e1e1e")
        canvas.create_window((0, 0), window=cont, anchor="nw")  
        tk.Label(cont, text="CIERRE TRANSITIVO (Warshall)", font=("Segoe UI", 14, "bold"), bg="#1e1e1e", fg="#ffcc99").pack()
        tk.Label(cont, text="¿Existe algún camino?", font=("Segoe UI", 11), bg="#1e1e1e", fg="#aaa").pack(pady=(0,20)) 
        tabla = tk.Frame(cont, bg="#1e1e1e")
        tabla.pack()
        ancho = max(3, max(len(n) for n in nodos) + 1)
        tk.Label(tabla, text="", font=("Consolas", 11), bg="#1e1e1e", fg="#c8a2ff", width=ancho).grid(row=0, column=0)        
        for j, n in enumerate(nodos):
            tk.Label(tabla, text=n, font=("Consolas", 11, "bold"), bg="#1e1e1e", fg="#c8a2ff", width=ancho).grid(row=0, column=j+1)
        for i, u in enumerate(nodos):
            tk.Label(tabla, text=u, font=("Consolas", 11, "bold"), bg="#1e1e1e", fg="#c8a2ff", width=ancho).grid(row=i+1, column=0)
            for j in range(len(nodos)):
                simb = "✓" if m[i][j] else "✗"
                color = "#88ff88" if m[i][j] else "#ff8888"
                tk.Label(tabla, text=simb, font=("Consolas", 11, "bold"), bg="#1e1e1e", fg=color, width=ancho).grid(row=i+1, column=j+1)
        tk.Button(cont, text="ACEPTAR", command=v.destroy, bg="#764ba2", fg="white", font=("Segoe UI", 10, "bold"), padx=20, pady=5).pack(pady=20)
        cont.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        w = min(cont.winfo_reqwidth() + 40, v.winfo_screenwidth() - 100)
        h = min(cont.winfo_reqheight() + 40, v.winfo_screenheight() - 100)
        v.geometry(f"{w}x{h}")
        v.update_idletasks()
        x = (v.winfo_screenwidth() - v.winfo_width()) // 2
        y = (v.winfo_screenheight() - v.winfo_height()) // 2
        v.geometry(f"+{x}+{y}")
    def buscar_camino(self):
        u = self.ent_desde.get().strip()
        v = self.ent_hasta.get().strip()
        if u not in self.G:
            messagebox.showwarning("Error", f"El nodo '{u}' no existe", parent=self.root)
            return
        if v not in self.G:
            messagebox.showwarning("Error", f"El nodo '{v}' no existe", parent=self.root)
            return
        if u == v:
            self.camino_resaltado = []
            self.actualizar()
            messagebox.showinfo("Resultado", f"✓ SÍ hay camino\n\nDe '{u}' a '{v}': {u} ", parent=self.root)
            self.ent_desde.delete(0, tk.END)
            self.ent_hasta.delete(0, tk.END)
            return
        camino = self._bfs(u, v)
        if camino:
            self.camino_resaltado = list(zip(camino, camino[1:]))
            self.actualizar()
            messagebox.showinfo("Resultado", f"✓ SÍ hay camino\n\n{' → '.join(camino)}", parent=self.root)
        else:
            self.camino_resaltado = []
            self.actualizar()
            messagebox.showinfo("Resultado", f"✗ NO hay camino\n\nNo existe camino de '{u}' a '{v}'", parent=self.root)
        self.ent_desde.delete(0, tk.END)
        self.ent_hasta.delete(0, tk.END)
    def actualizar(self):
        self.ax.clear()
        self.ax.set_facecolor("#1e1e1e")
        r = 0.05
        for u, v, d in self.G.edges(data=True):
            x1, y1 = self.pos[u]
            x2, y2 = self.pos[v]
            dx, dy = x2 - x1, y2 - y1
            d1 = math.hypot(dx, dy)
            if d1 == 0:
                continue
            xs = x1 + (dx/d1) * r
            ys = y1 + (dy/d1) * r
            xe = x2 - (dx/d1) * r
            ye = y2 - (dy/d1) * r
            es_camino = (u, v) in self.camino_resaltado
            if not self.es_dirigido:
                es_camino = es_camino or (v, u) in self.camino_resaltado
            color = "#c8a2ff" if es_camino else "#888888"
            ancho = 4 if es_camino else 1.5
            if self.es_dirigido:
                self.ax.add_patch(FancyArrowPatch((xs, ys), (xe, ye), arrowstyle='-|>', mutation_scale=15, color=color, linewidth=ancho))
            else:
                self.ax.plot([xs, xe], [ys, ye], color=color, linewidth=ancho)
            mx, my = (xs + xe) / 2, (ys + ye) / 2
            offset = 0.03
            self.ax.text(mx - dy/d1 * offset, my + dx/d1 * offset, str(d['weight']), 
                        color="#ffcc99", ha='center', fontsize=11, fontweight='bold')
        if self.G.nodes():
            nx.draw_networkx_nodes(self.G, self.pos, ax=self.ax, node_color="#bde0fe", node_size=1800, edgecolors="white", linewidths=2)
            nx.draw_networkx_labels(self.G, self.pos, ax=self.ax, font_size=12, font_weight='bold')
        self.ax.set_xlim(-0.1, 1.1)
        self.ax.set_ylim(-0.1, 1.1)
        self.ax.axis('off')
        self.canvas.draw_idle()
    def _on_press(self, e):
        if e.inaxes:
            for n, p in self.pos.items():
                if abs(p[0] - e.xdata) < 0.08 and abs(p[1] - e.ydata) < 0.08:
                    self.nodo_seleccionado = n
                    break
    def _on_release(self, e):
        self.nodo_seleccionado = None
    def _on_motion(self, e):
        if self.nodo_seleccionado and e.inaxes:
            self.pos[self.nodo_seleccionado] = [max(0, min(1, e.xdata)), max(0, min(1, e.ydata))]
            self.actualizar()
if __name__ == "__main__":
    root = tk.Tk()
    app = EditorGrafosWarshall(root)
    root.mainloop()
