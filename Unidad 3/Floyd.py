import tkinter as tk
from tkinter import messagebox, simpledialog
import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
from matplotlib.patches import FancyArrowPatch

class EditorGrafosFloydStyle:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Grafos - Floyd Interactivo")
        self.root.geometry("1200x850")
        self.root.configure(bg="#1e1e1e")
        
        self.label_carga = tk.Label(self.root, text="Cargando editor...", bg="#1e1e1e", fg="white", font=("Arial", 12))
        self.label_carga.place(relx=0.5, rely=0.5, anchor="center")
        self.root.update()
        
        self.root.after(50, self._iniciar_programa)
    
    def _iniciar_programa(self):
        self.es_dirigido = messagebox.askyesno("Tipo de grafo", "¿Deseas que el grafo sea DIRIGIDO?", parent=self.root)
        self.G = nx.DiGraph() if self.es_dirigido else nx.Graph()
        self.pos, self.nodo_seleccionado = {}, None
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
        
        tk.Label(menu, text=f"GRAFO {'DIRIGIDO' if self.es_dirigido else 'NO DIRIGIDO'}", 
                font=("Impact", 18), bg="#252526", fg="#ffcc99", pady=10).pack()
        
        self._crear_seccion(menu, "✚ NUEVO NODO")
        self.ent_nodo = tk.Entry(menu, justify='center')
        self.ent_nodo.pack(pady=5, padx=20, fill=tk.X)
        tk.Button(menu, text="AGREGAR NODO", command=self.agregar_nodo, bg="#bde0fe").pack(pady=5, fill=tk.X, padx=20)
        self._crear_separador(menu)
        
        self._crear_seccion(menu, "🔗 CONEXIONES")
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
        self._crear_separador(menu)
        
        self._crear_seccion(menu, "⚡ FLOYD")
        tk.Button(menu, text="CALCULAR FLOYD", command=self.calcular_floyd, bg="#e0bbff").pack(pady=5, fill=tk.X, padx=20)
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
        tk.Label(parent, text=texto, font=("Segoe UI", 10, "bold"),
                bg="#252526", fg="white").pack(pady=(10,0))
    
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
        return [0.5 + 0.35 * math.cos(angulo), 0.5 + 0.35 * math.sin(angulo)]
    
    def agregar_nodo(self):
        nombre = self.ent_nodo.get().strip()
        if not nombre:
            messagebox.showwarning("Error", "Nombre vacío", parent=self.root)
            return
        if nombre in self.G:
            messagebox.showwarning("Error", "Nodo ya existe", parent=self.root)
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
            messagebox.showwarning("Error", "Complete todos los campos", parent=self.root)
            return
        if u not in self.G or v not in self.G:
            messagebox.showwarning("Error", "Nodo no existe", parent=self.root)
            return
        
        try:
            peso = int(p)
            if peso <= 0:
                messagebox.showwarning("Error", "Peso inválido", parent=self.root)
                return
            
            self.G.add_edge(u, v, weight=peso)
            self.actualizar_dibujo()
            
            for e in [self.ent_orig, self.ent_dest, self.ent_peso]:
                e.delete(0, tk.END)
            self.ent_orig.focus()
        
        except:
            messagebox.showerror("Error", "Debe ser número", parent=self.root)
    
    def eliminar_arista(self):
        u = simpledialog.askstring("Eliminar arista", "Origen:", parent=self.root)
        if not u or u not in self.G:
            return
        
        v = simpledialog.askstring("Eliminar arista", "Destino:", parent=self.root)
        if not v or v not in self.G:
            return
        
        if self.G.has_edge(u, v):
            self.G.remove_edge(u, v)
            self.actualizar_dibujo()
    
    def eliminar_nodo(self):
        nombre = simpledialog.askstring("Eliminar nodo", "Nombre:", parent=self.root)
        if nombre in self.G:
            self.G.remove_node(nombre)
            self.pos.pop(nombre, None)
            self.actualizar_dibujo()
    
    def editar_nodo(self):
        viejo = simpledialog.askstring("Editar nodo", "Actual:", parent=self.root)
        if not viejo or viejo not in self.G:
            return
        
        nuevo = simpledialog.askstring("Editar nodo", "Nuevo:", parent=self.root)
        if nuevo and nuevo not in self.G:
            nx.relabel_nodes(self.G, {viejo: nuevo}, copy=False)
            self.pos[nuevo] = self.pos.pop(viejo)
            self.actualizar_dibujo()
    
    def vaciar_grafo(self):
        self.G.clear()
        self.pos.clear()
        self.actualizar_dibujo()
    
    def calcular_floyd(self):
        if not self.G.nodes():
            messagebox.showinfo("Error", "Grafo vacío", parent=self.root)
            return
        
        dist = dict(nx.floyd_warshall(self.G))
        
        msg = "DISTANCIAS MÍNIMAS:\n\n"
        for u in sorted(dist):
            for v in sorted(dist[u]):
                valor = dist[u][v]
                if valor == float('inf'):
                    msg += f"{u} → {v}: No hay camino\n"
                elif u == v:
                    msg += f"{u} → {v}: 0 \n"
                else:
                    msg += f"{u} → {v}: {round(valor, 2)}\n"
            msg += "\n"
        
        messagebox.showinfo("Floyd", msg, parent=self.root)
    
    def actualizar_dibujo(self):
        self.ax.clear()
        self.ax.set_facecolor("#1e1e1e")
        radio = 0.05
        
        for u, v, d in self.G.edges(data=True):
            x1, y1 = self.pos[u]
            x2, y2 = self.pos[v]
            dx, dy = x2-x1, y2-y1
            dist = math.hypot(dx, dy)
            if dist == 0:
                continue
            
            xs = x1 + (dx/dist)*radio
            ys = y1 + (dy/dist)*radio
            xe = x2 - (dx/dist)*radio
            ye = y2 - (dy/dist)*radio
            
            if self.es_dirigido:
                self.ax.add_patch(FancyArrowPatch((xs, ys), (xe, ye),
                                                  arrowstyle='-|>',
                                                  mutation_scale=15,
                                                  color="#888888"))
            else:
                self.ax.plot([xs, xe], [ys, ye], color="#888888")
            
            mx, my = (xs+xe)/2, (ys+ye)/2
            self.ax.text(mx - dy/dist*0.03, my + dx/dist*0.03,
                         str(d['weight']), color="#ffcc99",
                         ha='center', fontsize=11)
        
        nx.draw_networkx_nodes(self.G, self.pos, ax=self.ax,
                               node_color="#bde0fe", node_size=1800,
                               edgecolors="white")
        
        nx.draw_networkx_labels(self.G, self.pos, ax=self.ax,
                                font_weight='bold')
        
        self.ax.set_xlim(-0.1, 1.1)
        self.ax.set_ylim(-0.1, 1.1)
        self.ax.axis('off')
        self.canvas.draw_idle()
    
    def _on_press(self, event):
        if event.inaxes:
            for n, p in self.pos.items():
                if abs(p[0]-event.xdata) < 0.08 and abs(p[1]-event.ydata) < 0.08:
                    self.nodo_seleccionado = n
    
    def _on_release(self, event):
        self.nodo_seleccionado = None
    
    def _on_motion(self, event):
        if self.nodo_seleccionado and event.inaxes:
            self.pos[self.nodo_seleccionado] = [event.xdata, event.ydata]
            self.actualizar_dibujo()


if __name__ == "__main__":
    root = tk.Tk()
    app = EditorGrafosFloydStyle(root)
    root.mainloop()