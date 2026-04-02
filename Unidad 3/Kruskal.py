import tkinter as tk
from tkinter import messagebox, simpledialog
import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

class EditorGrafosKruskalStyle:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Grafos - Kruskal Interactivo")
        self.root.geometry("1200x850")
        self.root.configure(bg="#1e1e1e")
        self.label_carga = tk.Label(self.root, text="Cargando editor...", bg="#1e1e1e", fg="white", font=("Arial", 12))
        self.label_carga.place(relx=0.5, rely=0.5, anchor="center")
        self.root.update()
        self.root.after(50, self._iniciar_programa)
    def _iniciar_programa(self):
        self.G = nx.Graph()
        self.pos, self.nodo_seleccionado, self.aristas_resaltadas = {}, None, []
        self.drag_timer = None
        self.label_carga.destroy()
        self._crear_menu()
        self._crear_area_grafico()
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
        canvas.create_window((0, 0), window=menu, anchor="nw", width=300)
        def on_mousewheel(e): canvas.yview_scroll(int(-1*(e.delta/120)), "units")
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        tk.Label(menu, text="GRAFO NO DIRIGIDO", font=("Impact", 18), bg="#252526", fg="#ffcc99", pady=10).pack()
        self._crear_seccion(menu, "✚ NUEVO NODO")
        self.ent_nodo = tk.Entry(menu, justify='center', font=("Segoe UI", 10))
        self.ent_nodo.pack(pady=5, padx=20, fill=tk.X)
        tk.Button(menu, text="AGREGAR NODO", command=self.agregar_nodo, bg="#bde0fe").pack(pady=5, fill=tk.X, padx=20)
        self._crear_separador(menu)
        self._crear_seccion(menu, "🔗 CONEXIONES")
        tk.Label(menu, text="Origen:", bg="#252526", fg="white").pack()
        self.ent_orig = tk.Entry(menu, justify='center', font=("Segoe UI", 10))
        self.ent_orig.pack(pady=2, padx=20, fill=tk.X)
        tk.Label(menu, text="Destino:", bg="#252526", fg="white").pack()
        self.ent_dest = tk.Entry(menu, justify='center', font=("Segoe UI", 10))
        self.ent_dest.pack(pady=2, padx=20, fill=tk.X)
        tk.Label(menu, text="Peso:", bg="#252526", fg="white").pack()
        self.ent_peso = tk.Entry(menu, justify='center', font=("Segoe UI", 10))
        self.ent_peso.pack(pady=2, padx=20, fill=tk.X)
        tk.Button(menu, text="CONECTAR", command=self.agregar_arista, bg="#baffc9").pack(pady=5, fill=tk.X, padx=20)
        self._crear_separador(menu)
        self._crear_seccion(menu, "🌲 KRUSKAL (ÁRBOL DE EXPANSIÓN MÍNIMA)")
        tk.Button(menu, text="CALCULAR KRUSKAL", command=self.calcular_kruskal, bg="#e0bbff").pack(pady=5, fill=tk.X, padx=20)
        self._crear_separador(menu)
        self._crear_seccion(menu, "✎ EDICIÓN")
        tk.Button(menu, text="EDITAR NOMBRE", command=self.editar_nodo, bg="#ffffba").pack(pady=5, fill=tk.X, padx=20)
        tk.Button(menu, text="ELIMINAR NODO", command=self.eliminar_nodo, bg="#ff9aa2").pack(pady=5, fill=tk.X, padx=20)
        tk.Button(menu, text="ELIMINAR ARISTA", command=self.eliminar_arista, bg="#ffb3ba").pack(pady=5, fill=tk.X, padx=20)
        self._crear_separador(menu)
        self._crear_seccion(menu, "📊 INFORMACIÓN")
        tk.Button(menu, text="VACIAR PROGRAMA", command=self.vaciar_grafo, bg="#d8bfff").pack(pady=5, fill=tk.X, padx=20)
        tk.Button(menu, text="SALIR", command=self.root.quit, bg="#ff6b6b", fg="white").pack(pady=20, fill=tk.X, padx=20)
        menu.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
    def _crear_seccion(self, parent, texto):
        tk.Label(parent, text=texto, font=("Segoe UI", 10, "bold"), bg="#252526", fg="white").pack(pady=(10,0))
    def _crear_separador(self, parent):
        tk.Frame(parent, height=2, bg="#444444").pack(fill=tk.X, pady=10)
    def _crear_area_grafico(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 8), facecolor="#1e1e1e")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas.mpl_connect("button_press_event", self._on_press)
        self.canvas.mpl_connect("button_release_event", self._on_release)
        self.canvas.mpl_connect("motion_notify_event", self._on_motion)
        self.actualizar_dibujo()
    def _generar_posicion(self):
        n = len(self.pos)
        if n == 0:
            return [0.5, 0.5]
        angulo = 2 * math.pi * n / 8
        x = 0.5 + 0.35 * math.cos(angulo)
        y = 0.5 + 0.35 * math.sin(angulo)
        return [x, y]
    def agregar_nodo(self):
        nombre = self.ent_nodo.get().strip()
        if not nombre:
            messagebox.showwarning("Error", "Nombre vacío")
            return
        if nombre in self.G:
            messagebox.showwarning("Error", f"El nodo '{nombre}' ya existe")
            return
        self.G.add_node(nombre)
        self.pos[nombre] = self._generar_posicion()
        self.actualizar_dibujo()
        self.ent_nodo.delete(0, tk.END)
        self.ent_nodo.focus()
    def agregar_arista(self):
        u = self.ent_orig.get().strip()
        v = self.ent_dest.get().strip()
        p = self.ent_peso.get().strip()
        if not all([u, v, p]):
            messagebox.showwarning("Error", "Complete todos los campos")
            return
        if u not in self.G:
            messagebox.showwarning("Error", f"El nodo '{u}' no existe")
            return
        if v not in self.G:
            messagebox.showwarning("Error", f"El nodo '{v}' no existe")
            return
        if u == v:
            messagebox.showwarning("Error", "No se permiten bucles")
            return
        try:
            peso = int(p)
            if peso <= 0:
                messagebox.showwarning("Error", "El peso debe ser positivo")
                return
            self.G.add_edge(u, v, weight=peso)
            self.aristas_resaltadas = []
            self.actualizar_dibujo()
            for e in [self.ent_orig, self.ent_dest, self.ent_peso]:
                e.delete(0, tk.END)
            self.ent_orig.focus()
        except ValueError:
            messagebox.showerror("Error", "El peso debe ser un número entero")
    def eliminar_arista(self):
        u = simpledialog.askstring("Eliminar arista", "Origen:", parent=self.root)
        if not u or u not in self.G:
            return
        v = simpledialog.askstring("Eliminar arista", "Destino:", parent=self.root)
        if not v or v not in self.G:
            return
        if self.G.has_edge(u, v):
            self.G.remove_edge(u, v)
            self.aristas_resaltadas = []
            self.actualizar_dibujo()
            messagebox.showinfo("Éxito", f"Arista {u}—{v} eliminada")
        else:
            messagebox.showwarning("Advertencia", f"No existe arista entre {u} y {v}")
    def eliminar_nodo(self):
        nombre = simpledialog.askstring("Eliminar nodo", "Nombre del nodo:", parent=self.root)
        if nombre and nombre in self.G:
            self.G.remove_node(nombre)
            if nombre in self.pos:
                del self.pos[nombre]
            self.aristas_resaltadas = []
            self.actualizar_dibujo()
        elif nombre:
            messagebox.showwarning("Advertencia", f"El nodo '{nombre}' no existe")
    def editar_nodo(self):
        viejo = simpledialog.askstring("Editar nodo", "Nombre actual:", parent=self.root)
        if not viejo or viejo not in self.G:
            return
        nuevo = simpledialog.askstring("Editar nodo", "Nuevo nombre:", parent=self.root)
        if nuevo and nuevo not in self.G:
            nx.relabel_nodes(self.G, {viejo: nuevo}, copy=False)
            self.pos[nuevo] = self.pos.pop(viejo)
            self.actualizar_dibujo()
            messagebox.showinfo("Éxito", f"Nodo renombrado de '{viejo}' a '{nuevo}'")
    def vaciar_grafo(self):
        if messagebox.askyesno("Confirmar", "¿Vaciar grafo?"):
            self.G.clear()
            self.pos.clear()
            self.aristas_resaltadas.clear()
            self.actualizar_dibujo()
    def calcular_kruskal(self):
        if not self.G.nodes():
            messagebox.showinfo("Kruskal", "Grafo vacío")
            return
        try:
            aristas = [(d['weight'], u, v) for u, v, d in self.G.edges(data=True)]
            aristas.sort()
            parent = {nodo: nodo for nodo in self.G.nodes()}
            def find(x):
                while parent[x] != x:
                    parent[x] = parent[parent[x]]
                    x = parent[x]
                return x
            def union(x, y):
                rx, ry = find(x), find(y)
                if rx == ry:
                    return False
                parent[ry] = rx
                return True
            mst = []
            peso_total = 0
            for peso, u, v in aristas:
                if union(u, v):
                    mst.append((u, v, peso))
                    peso_total += peso
            if len(mst) != len(self.G.nodes()) - 1:
                messagebox.showinfo("Kruskal", "El grafo no es conexo. No se puede formar un árbol de expansión.")
                return
            self.aristas_resaltadas = [(u, v) for u, v, _ in mst]
            self.actualizar_dibujo()
            msg = "ÁRBOL DE EXPANSIÓN MÍNIMA (Kruskal)\n\n"
            msg += f"Peso total: {peso_total}\n\n"
            msg += "Aristas seleccionadas:\n"
            for u, v, peso in mst:
                msg += f"  {u} — {v} : {peso}\n"
            messagebox.showinfo("Kruskal - MST", msg)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo calcular: {e}")
    def actualizar_dibujo(self):
        self.ax.clear()
        self.ax.set_facecolor("#1e1e1e")
        radio = 0.05
        for u, v, d in self.G.edges(data=True):
            x1, y1 = self.pos[u]
            x2, y2 = self.pos[v]
            dx, dy = x2-x1, y2-y1
            dist = math.hypot(dx, dy)
            if dist == 0: continue
            xs = x1 + (dx/dist)*radio
            ys = y1 + (dy/dist)*radio
            xe = x2 - (dx/dist)*radio
            ye = y2 - (dy/dist)*radio
            es_mst = (u, v) in self.aristas_resaltadas or (v, u) in self.aristas_resaltadas
            color = "#c8a2ff" if es_mst else "#888888"
            ancho = 4 if es_mst else 1.5
            self.ax.plot([xs, xe], [ys, ye], color=color, linewidth=ancho)
            mx, my = (xs+xe)/2, (ys+ye)/2
            self.ax.text(mx - dy/dist*0.03, my + dx/dist*0.03, str(d['weight']), color="#ffcc99", fontsize=11, fontweight='bold', ha='center', va='center')
        if self.G.nodes():
            nx.draw_networkx_nodes(self.G, self.pos, ax=self.ax, node_color="#bde0fe", node_size=1800, edgecolors="white", linewidths=2)
            nx.draw_networkx_labels(self.G, self.pos, ax=self.ax, font_size=12, font_weight='bold')
        self.ax.set_xlim(-0.1, 1.1)
        self.ax.set_ylim(-0.1, 1.1)
        self.ax.axis('off')
        self.canvas.draw_idle()
    def _on_press(self, event):
        if event.inaxes:
            for n, p in self.pos.items():
                if abs(p[0]-event.xdata) < 0.08 and abs(p[1]-event.ydata) < 0.08:
                    self.nodo_seleccionado = n
                    break
    def _on_release(self, event):
        self.nodo_seleccionado = None
    def _on_motion(self, event):
        if self.nodo_seleccionado and event.inaxes:
            x = max(0.0, min(1.0, event.xdata))
            y = max(0.0, min(1.0, event.ydata))
            self.pos[self.nodo_seleccionado] = [x, y]
            if self.drag_timer:
                self.root.after_cancel(self.drag_timer)
            self.drag_timer = self.root.after(16, self.actualizar_dibujo)
if __name__ == "__main__":
    root = tk.Tk()
    app = EditorGrafosKruskalStyle(root)
    root.mainloop()