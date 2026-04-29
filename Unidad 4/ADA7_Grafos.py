import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SistemaRutasMexico:
    def __init__(self, root):
        self.root = root
        self.root.title("SISTEMA DE RUTAS MÉXICO - GRAFOS")
        self.root.geometry("1300x850")
        
        # Colores
        self.bg_vs_code = "#1e1e1e"      
        self.bg_sidebar = "#252526"      
        self.naranja_pastel = "#ffcc99"  
        self.morado_pastel = "#d8bfff"   
        self.rosa_pastel_suave = "#ffcce6"
        self.verde_ruta = "#baffc9" 
        
        self.colores_nodos = ["#baffc9", "#ff9aa2", "#bde0fe", "#ffffba", "#ffc8dd", "#cdb4db", "#e2ece9"]
        
        self.root.configure(bg=self.bg_vs_code)

        # --- CONFIGURACIÓN DEL GRAFO ---
        self.G = nx.Graph()
        self.estados = ['CDMX', 'Yucatán', 'Morelos', 'Querétaro', 'Guanajuato', 'Jalisco', 'Michoacán']
        self.conexiones = [
            ('CDMX', 'Yucatán', 50), ('CDMX', 'Morelos', 120),
            ('Yucatán', 'Querétaro', 250), ('Yucatán', 'Michoacán', 200),
            ('Querétaro', 'Guanajuato', 180), ('Guanajuato', 'Jalisco', 300),
            ('Jalisco', 'Michoacán', 220), ('Michoacán', 'Morelos', 150)
        ]
        self.G.add_weighted_edges_from(self.conexiones)

        # --- INTERFAZ (MENÚ) ---
        self.frame_menu = tk.Frame(self.root, width=320, bg=self.bg_sidebar, bd=0)
        self.frame_menu.pack(side=tk.LEFT, fill=tk.Y)
        self.frame_menu.pack_propagate(False)

        tk.Label(self.frame_menu, text="SISTEMA GAIA", font=("Impact", 26), 
                 bg=self.bg_sidebar, fg=self.naranja_pastel).pack(pady=(40, 5))

        # Comentario solicitado
        tk.Label(self.frame_menu, text="* Tablas ajustables para ver todo el contenido", 
                 font=("Arial", 9, "italic"), bg=self.bg_sidebar, fg="#aaaaaa").pack(pady=(0, 25))

        btn_style = {
            "font": ("Arial Black", 8), "bg": self.rosa_pastel_suave, "fg": "black",
            "activebackground": "#ffb3d9", "width": 32, "pady": 12, "bd": 0, "cursor": "hand2"
        }

        tk.Button(self.frame_menu, text="1. RECORRIDO SIN REPETIR", command=self.recorrido_sin_repetir, **btn_style).pack(pady=8)
        tk.Button(self.frame_menu, text="2. RECORRIDO CON REPETICIÓN", command=self.recorrido_con_repeticion, **btn_style).pack(pady=8)
        tk.Button(self.frame_menu, text="3. COSTOS DE LOS RECORRIDOS", command=self.mostrar_costos_totales, **btn_style).pack(pady=8)
        tk.Button(self.frame_menu, text="4. DIBUJAR GRAFO CON VALORES", command=self.dibujar_grafo, **btn_style).pack(pady=8)
        tk.Button(self.frame_menu, text="5. MOSTRAR ESTADOS Y RELACIONES", command=self.mostrar_tabla_relaciones, **btn_style).pack(pady=8)
        
        tk.Button(self.frame_menu, text="SALIR", command=self.root.quit, bg="#ff6b6b", 
                 font=("Arial Black", 9), bd=0, fg="white", width=15).pack(side=tk.BOTTOM, pady=30)

        self.area_visual = tk.Frame(self.root, bg=self.bg_vs_code)
        self.area_visual.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=40, pady=40)

        self.estilo_tablas()

    def estilo_tablas(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2d2d2d", foreground="white", 
                        fieldbackground="#2d2d2d", rowheight=45, font=("Arial", 11), borderwidth=0)
        style.configure("Treeview.Heading", background=self.morado_pastel, 
                        foreground="black", font=("Arial Black", 10))

    def limpiar_pantalla(self):
        for widget in self.area_visual.winfo_children():
            widget.destroy()

    def calcular_costo_ruta(self, ruta):
        costo = 0
        for i in range(len(ruta) - 1):
            costo += self.G[ruta[i]][ruta[i+1]]['weight']
        return costo

    # --- GENERADOR DE TABLAS CORREGIDO ---
    def generar_tabla_estetica(self, titulo, columnas, datos):
        self.limpiar_pantalla()
        
        tk.Label(self.area_visual, text=titulo.upper(), font=("Impact", 22), 
                 bg=self.bg_vs_code, fg=self.morado_pastel).pack(pady=20)
        
        tabla = ttk.Treeview(self.area_visual, columns=columnas, show="headings", height=len(datos))
        
        for col in columnas:
            tabla.heading(col, text=col, anchor=tk.CENTER)
            tabla.column(col, anchor=tk.CENTER, width=200, stretch=tk.YES)
        
        for fila in datos:
            tabla.insert("", tk.END, values=fila)
        
        tabla.pack(pady=10, fill=tk.X)

        # Buscar si hay una "Ruta" para mostrar el detalle extendido abajo
        for fila in datos:
            if "Ruta" in fila:
                # El valor de la ruta suele ser el segundo elemento de la fila
                valor_ruta = fila[1]
                tk.Label(self.area_visual, text="DETALLE DE RUTA COMPLETA:", 
                         font=("Arial Black", 10), bg=self.bg_vs_code, fg=self.naranja_pastel).pack(pady=10)
                
                lbl_ruta = tk.Label(self.area_visual, text=valor_ruta, font=("Consolas", 12, "bold"), 
                                   bg="#2d2d2d", fg=self.verde_ruta, wraplength=800, 
                                   justify=tk.CENTER, padx=20, pady=20)
                lbl_ruta.pack(pady=10)

    def recorrido_sin_repetir(self):
        ruta = ["Morelos", "CDMX", "Yucatán", "Querétaro", "Guanajuato", "Jalisco", "Michoacán"]
        costo = self.calcular_costo_ruta(ruta)
        self.generar_tabla_estetica("1. Recorrido Sin Repetir", ("CONCEPTO", "VALOR"), 
                                   [("Ruta", " → ".join(ruta)), ("Costo Total", f"${costo}")])

    def recorrido_con_repeticion(self):
        ruta = ["Yucatán", "CDMX", "Morelos", "Michoacán", "Morelos", "CDMX", "Yucatán", "Querétaro", "Guanajuato", "Jalisco"]
        costo = self.calcular_costo_ruta(ruta)
        self.generar_tabla_estetica("2. Recorrido Con Repetición", ("CONCEPTO", "VALOR"), 
                                   [("Ruta", " → ".join(ruta)), ("Costo Total", f"${costo}")])

    def mostrar_costos_totales(self):
        r1 = ["Morelos", "CDMX", "Yucatán", "Querétaro", "Guanajuato", "Jalisco", "Michoacán"]
        r2 = ["Yucatán", "CDMX", "Morelos", "Michoacán", "Morelos", "CDMX", "Yucatán", "Querétaro", "Guanajuato", "Jalisco"]
        datos = [
            ("Inciso A (Sin repetir)", f"${self.calcular_costo_ruta(r1)}"),
            ("Inciso B (Con repetición)", f"${self.calcular_costo_ruta(r2)}")
        ]
        self.generar_tabla_estetica("3. Costo Total del Recorrido", ("DESCRIPCIÓN", "TOTAL"), datos)

    def mostrar_tabla_relaciones(self):
        # Aquí enviamos 3 valores por fila: esto causaba el error antes
        datos = [(u, v, f"${d['weight']}") for u, v, d in self.G.edges(data=True)]
        self.generar_tabla_estetica("5. Estados y Relaciones", ("ORIGEN", "DESTINO", "COSTO"), datos)

    def dibujar_grafo(self):
        self.limpiar_pantalla()
        fig = plt.figure(figsize=(10, 7), facecolor=self.bg_vs_code)
        ax = fig.add_subplot(111)
        ax.set_facecolor(self.bg_vs_code)
        
        pos = nx.spring_layout(self.G, seed=42) 
        nx.draw_networkx_edges(self.G, pos, edge_color='#666666', width=2, ax=ax)
        for i, nodo in enumerate(self.estados):
            nx.draw_networkx_nodes(self.G, pos, nodelist=[nodo], 
                                   node_color=self.colores_nodos[i % len(self.colores_nodos)], 
                                   node_size=3800, ax=ax)
        nx.draw_networkx_labels(self.G, pos, font_size=9, font_weight='bold', ax=ax)
        labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=labels, font_color='white', 
                                     font_weight='bold', bbox=dict(facecolor='#333333', alpha=0.8, edgecolor='none'))
        ax.set_title("4. REPRESENTACIÓN GRÁFICA", color=self.morado_pastel, fontname="Impact", fontsize=22, pad=20)
        plt.axis('off')
        canvas = FigureCanvasTkAgg(fig, master=self.area_visual)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaRutasMexico(root)
    root.mainloop()
