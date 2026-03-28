import tkinter as tk
from tkinter import messagebox, ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ProgramaGrafosFinal:
    def __init__(self, root):
        self.root = root
        self.root.title("SISTEMA DE RUTAS MÉXICO")
        self.root.geometry("1200x850")
        
        # COLORES SOLICITADOS
        self.bg_vs_code = "#1e1e1e"      # Gris oscuro principal
        self.bg_sidebar = "#252526"      # Menú lateral
        self.naranja_pastel = "#ffcc99"  # Título MENÚ
        self.morado_pastel = "#d8bfff"   # Cabeceras Tablas y Título Grafo
        self.rosa_pastel_suave = "#ffcce6" # Botones rosado pastel
        
        # Colores diferentes para cada nodo (7 colores pastel)
        self.colores_nodos = [
            "#baffc9", "#ff9aa2", "#bde0fe", "#ffffba", 
            "#ffc8dd", "#cdb4db", "#e2ece9"
        ]
        
        self.root.configure(bg=self.bg_vs_code)

        # 1. Datos del Grafo (Yucatán en lugar de Edomex)
        self.G = nx.Graph()
        self.estados = ['CDMX', 'Yucatán', 'Morelos', 'Querétaro', 'Guanajuato', 'Jalisco', 'Michoacán']
        self.conexiones = [
            ('CDMX', 'Yucatán', 50), ('CDMX', 'Morelos', 120),
            ('Yucatán', 'Querétaro', 250), ('Yucatán', 'Michoacán', 200),
            ('Querétaro', 'Guanajuato', 180), ('Guanajuato', 'Jalisco', 300),
            ('Jalisco', 'Michoacán', 220)
        ]
        self.G.add_weighted_edges_from(self.conexiones)

        # 2. Menú Lateral
        self.frame_menu = tk.Frame(self.root, width=320, bg=self.bg_sidebar, bd=0)
        self.frame_menu.pack(side=tk.LEFT, fill=tk.Y)
        self.frame_menu.pack_propagate(False)

        tk.Label(self.frame_menu, text="MENÚ", font=("Impact", 24), 
                 bg=self.bg_sidebar, fg=self.naranja_pastel, pady=30).pack()

        btn_style = {
            "font": ("Arial Black", 8),
            "bg": self.rosa_pastel_suave,
            "fg": "black",
            "activebackground": "#ffb3d9",
            "width": 32,
            "pady": 12,
            "bd": 0,
            "cursor": "hand2"
        }

        tk.Button(self.frame_menu, text="RECORRER 7 ESTADOS SIN REPETIR", command=self.recorrido_sin_repetir, **btn_style).pack(pady=8)
        tk.Button(self.frame_menu, text="RECORRER 7 ESTADOS CON REPETICIÓN", command=self.recorrido_con_repeticion, **btn_style).pack(pady=8)
        tk.Button(self.frame_menu, text="COSTO TOTAL DE LOS RECORRIDOS", command=self.mostrar_costos_totales, **btn_style).pack(pady=8)
        tk.Button(self.frame_menu, text="DIBUJAR GRAFO CON VALORES", command=self.dibujar_grafo, **btn_style).pack(pady=8)
        tk.Button(self.frame_menu, text="MOSTRAR ESTADOS Y RELACIONES", command=self.mostrar_tabla, **btn_style).pack(pady=8)
        
        tk.Button(self.frame_menu, text="SALIR", command=self.root.quit, bg="#ff6b6b", font=("Arial Black", 9), bd=0, fg="white", width=15).pack(side=tk.BOTTOM, pady=30)

        # 3. Área de Visualización
        self.area_visual = tk.Frame(self.root, bg=self.bg_vs_code)
        self.area_visual.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=40, pady=40)

        self.estilo_tablas()

    def estilo_tablas(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2d2d2d", foreground="white", fieldbackground="#2d2d2d", rowheight=35, font=("Arial", 11), borderwidth=0)
        style.configure("Treeview.Heading", background=self.morado_pastel, foreground="black", font=("Arial Black", 10))
        style.map("Treeview", background=[('selected', '#3e3e42')])

    def limpiar_pantalla(self):
        for widget in self.area_visual.winfo_children():
            widget.destroy()

    def generar_tabla_simple(self, titulo, columnas, datos):
        self.limpiar_pantalla()
        tk.Label(self.area_visual, text=titulo.upper(), font=("Impact", 22), bg=self.bg_vs_code, fg=self.morado_pastel).pack(pady=(0,20))
        tabla = ttk.Treeview(self.area_visual, columns=columnas, show="headings", height=len(datos))
        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, anchor=tk.CENTER, width=300)
        for fila in datos:
            tabla.insert("", tk.END, values=fila)
        tabla.pack(pady=10, fill=tk.X)

    def recorrido_sin_repetir(self):
        ruta = ["Morelos", "CDMX", "Yucatán", "Querétaro", "Guanajuato", "Jalisco", "Michoacán"]
        self.generar_tabla_simple("RECORRIDO SIN REPETIR", ("RUTA COMPLETA",), [(" → ".join(ruta),)])

    def recorrido_con_repeticion(self):
        ruta = ["Morelos", "CDMX", "Yucatán", "Querétaro", "Guanajuato", "Jalisco", "Michoacán", "Jalisco", "Michoacán"]
        self.generar_tabla_simple("RECORRIDO CON REPETICIÓN", ("RUTA CON ESCALA",), [(" → ".join(ruta),)])

    def mostrar_costos_totales(self):
        datos = [("TOTAL SIN REPETIR", "$1120"), ("TOTAL CON REPETICIÓN", "$1560")]
        self.generar_tabla_simple("COSTO TOTAL DEL RECORRIDO", ("DESCRIPCIÓN", "TOTAL"), datos)

    def mostrar_tabla(self):
        datos = [(u, v, f"${d['weight']}") for u, v, d in self.G.edges(data=True)]
        self.generar_tabla_simple("ESTADOS Y SUS RELACIONES", ("ORIGEN", "DESTINO", "COSTO"), datos)

    def dibujar_grafo(self):
        self.limpiar_pantalla()
        # FIGURA CON FONDO OSCURO (Aumentada para acomodar la expansión)
        fig = plt.figure(figsize=(11, 8), facecolor=self.bg_vs_code)
        ax = fig.add_subplot(111)
        ax.set_facecolor(self.bg_vs_code)
        
        # POSICIONES CORREGIDAS: Morelos alejado de CDMX, Michoacán separado de Yucatán
        pos = {
            'Morelos': (-1, 1),      # Alejar Morelos hacia la izquierda (Y=1)
            'CDMX': (1, 0.8),         # Mantener CDMX (Y=0.8)
            'Yucatán': (2.5, 0.6),    # Yucatán central
            'Michoacán': (4.5, 0.6),  # Michoacán separado de Yucatán
            'Jalisco': (6, 0.3),      # Jalisco a la derecha
            'Querétaro': (2.5, 0.1),  # Querétaro debajo de Yucatán
            'Guanajuato': (4.5, 0)     # Guanajuato debajo de Michoacán
        }
        
        # Aristas oscuras
        nx.draw_networkx_edges(self.G, pos, edge_color='#444444', width=2.5, ax=ax)

        # Nodos con colores pastel individuales y texto NEGRO
        for i, nodo in enumerate(self.estados):
            # Asignación de colores basada en el orden de self.estados
            idx = self.estados.index(nodo)
            nx.draw_networkx_nodes(self.G, pos, nodelist=[nodo], 
                                   node_color=self.colores_nodos[idx % len(self.colores_nodos)], 
                                   node_size=4200, ax=ax)
        
        # Etiquetas de estados (fuente pequeña para que no se encime)
        nx.draw_networkx_labels(self.G, pos, font_size=8, font_weight='bold', 
                                font_color='black', ax=ax)
        
        # Etiquetas de costos (Números blancos, sin fondo, muy visibles)
        labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=labels, font_size=11, 
                                     font_weight='bold', font_color='white', 
                                     bbox=dict(facecolor='none', alpha=0), ax=ax)
        
        # TÍTULO EN MORADO PASTEL
        ax.set_title("MAPA DE ESTADOS Y COSTOS", color=self.morado_pastel, fontname="Impact", fontsize=20, pad=20)
        
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_xticks([]); ax.set_yticks([])
        plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1)

        canvas = FigureCanvasTkAgg(fig, master=self.area_visual)
        canvas.draw()
        canvas.get_tk_widget().configure(background=self.bg_vs_code, highlightthickness=0)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = ProgramaGrafosFinal(root)
    root.mainloop()