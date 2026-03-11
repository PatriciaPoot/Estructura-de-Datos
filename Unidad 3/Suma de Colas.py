import tkinter as tk
from tkinter import messagebox, ttk, simpledialog

class Cola:
    def __init__(self):
        self.items = []
    
    def encolar(self, item):
        self.items.append(item)
    
    def desencolar(self):
        if self.esta_vacia():
            return None
        return self.items.pop(0)
    
    def esta_vacia(self):
        return len(self.items) == 0
    
    def copia(self):
        nueva_cola = Cola()
        for item in self.items:
            nueva_cola.encolar(item)
        return nueva_cola
    
    def __len__(self):
        return len(self.items)

class SumadorColasGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sumador de Colas - Validación de Longitud")
        self.root.geometry("850x850")
        self.root.configure(bg="#1a252c")
        self.root.resizable(False, False)
        
        self.cola_a = Cola()
        self.cola_b = Cola()
        self.elemento_a = tk.StringVar()
        self.elemento_b = tk.StringVar()
        
        self.setup_ui()
    
    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        bg_dark = "#1a252c"
        mint_p = "#a8d8d8"
        lavender_p = "#b2a4d4"
        blue_p = "#a2c2e0"
        orange_p = "#f0b291"
        header_p = "#bce4d8"

        style.configure("TFrame", background=bg_dark)
        style.configure("TLabelframe", background=bg_dark, foreground="white", bordercolor="#3b4b54")
        style.configure("TLabelframe.Label", background=bg_dark, foreground="white", font=('Arial', 10, 'bold'))
        style.configure("TLabel", background=bg_dark, foreground="white")
        style.configure("Mint.TButton", background=mint_p)
        style.configure("Lavender.TButton", background=lavender_p)
        style.configure("Blue.TButton", background=blue_p)
        style.configure("Orange.TButton", background=orange_p)
        style.configure("Vertical.TScrollbar", background="#cccccc", troughcolor=bg_dark, bordercolor="#3b4b54", arrowcolor="#333333")

        style.configure("Treeview", background="white", fieldbackground="white", foreground="black", rowheight=25)
        style.configure("Treeview.Heading", background=header_p, font=('Arial', 10, 'bold'))

        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="SUMADOR DE COLAS", font=('Arial', 18, 'bold')).pack(pady=(0, 15))
        
        colas_frame = ttk.Frame(main_frame)
        colas_frame.pack(fill=tk.X)
        
        # Cola A
        cola_a_f = ttk.LabelFrame(colas_frame, text="Cola A", padding="10")
        cola_a_f.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ent_a = ttk.Entry(cola_a_f, textvariable=self.elemento_a)
        ent_a.pack(fill=tk.X, pady=2)
        ent_a.bind('<Return>', lambda e: self.agregar_a())
        ttk.Button(cola_a_f, text="Agregar a Cola A", style="Mint.TButton", command=self.agregar_a).pack(pady=5)
        
        cont_a = ttk.Frame(cola_a_f)
        cont_a.pack(fill=tk.X)
        self.lista_a = tk.Listbox(cont_a, height=7, font=('Courier', 11))
        sc_a = ttk.Scrollbar(cont_a, orient=tk.VERTICAL, command=self.lista_a.yview)
        self.lista_a.configure(yscrollcommand=sc_a.set)
        self.lista_a.pack(side=tk.LEFT, fill=tk.X, expand=True)
        sc_a.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Cola B
        cola_b_f = ttk.LabelFrame(colas_frame, text="Cola B", padding="10")
        cola_b_f.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        ent_b = ttk.Entry(cola_b_f, textvariable=self.elemento_b)
        ent_b.pack(fill=tk.X, pady=2)
        ent_b.bind('<Return>', lambda e: self.agregar_b())
        ttk.Button(cola_b_f, text="Agregar a Cola B", style="Lavender.TButton", command=self.agregar_b).pack(pady=5)
        
        cont_b = ttk.Frame(cola_b_f)
        cont_b.pack(fill=tk.X)
        self.lista_b = tk.Listbox(cont_b, height=7, font=('Courier', 11))
        sc_b = ttk.Scrollbar(cont_b, orient=tk.VERTICAL, command=self.lista_b.yview)
        self.lista_b.configure(yscrollcommand=sc_b.set)
        self.lista_b.pack(side=tk.LEFT, fill=tk.X, expand=True)
        sc_b.pack(side=tk.RIGHT, fill=tk.Y)
        
        acc_frame = ttk.Frame(main_frame)
        acc_frame.pack(fill=tk.X, pady=15)
        
        r1 = ttk.Frame(acc_frame); r1.pack()
        ttk.Button(r1, text="SUMAR COLAS", style="Blue.TButton", command=self.sumar_colas).pack(side=tk.LEFT, padx=5)
        ttk.Button(r1, text="Limpiar Todo", style="Orange.TButton", command=self.limpiar_todo).pack(side=tk.LEFT, padx=5)
        ttk.Button(r1, text="Ejemplo", style="Lavender.TButton", command=self.cargar_ejemplo).pack(side=tk.LEFT, padx=5)
        
        r2 = ttk.Frame(acc_frame); r2.pack(pady=5)
        ttk.Button(r2, text="Gestionar Cola A", style="Mint.TButton", command=lambda: self.abrir_selector_gestion('A')).pack(side=tk.LEFT, padx=5)
        ttk.Button(r2, text="Gestionar Cola B", style="Lavender.TButton", command=lambda: self.abrir_selector_gestion('B')).pack(side=tk.LEFT, padx=5)
        
        res_container = ttk.LabelFrame(main_frame, text="Resultado", padding="10")
        res_container.pack(fill=tk.X, pady=10)
        
        self.tabla_resultados = ttk.Treeview(res_container, 
                                             columns=('A', 'B', 'Resultado'),
                                             show='headings', height=8)
        
        self.tabla_resultados.heading('A', text='Cola A')
        self.tabla_resultados.heading('B', text='Cola B')
        self.tabla_resultados.heading('Resultado', text='Cola Resultado')
        
        self.tabla_resultados.column('A', width=200, anchor='center')
        self.tabla_resultados.column('B', width=200, anchor='center')
        self.tabla_resultados.column('Resultado', width=200, anchor='center')
        
        sc_r = ttk.Scrollbar(res_container, orient=tk.VERTICAL, command=self.tabla_resultados.yview)
        self.tabla_resultados.configure(yscrollcommand=sc_r.set)
        self.tabla_resultados.pack(side=tk.LEFT, fill=tk.X, expand=True)
        sc_r.pack(side=tk.RIGHT, fill=tk.Y)

    def agregar_a(self):
        try:
            val = int(self.elemento_a.get()); self.cola_a.encolar(val)
            self.elemento_a.set(""); self.actualizar_listas()
        except: messagebox.showerror("Error", "Ingrese número", parent=self.root)

    def agregar_b(self):
        try:
            val = int(self.elemento_b.get()); self.cola_b.encolar(val)
            self.elemento_b.set(""); self.actualizar_listas()
        except: messagebox.showerror("Error", "Ingrese número", parent=self.root)

    def abrir_selector_gestion(self, tipo):
        cola_obj = self.cola_a if tipo == 'A' else self.cola_b
        if not cola_obj.items: return
        
        v = tk.Toplevel(self.root)
        v.title("Gestión")
        v_width, v_height = 280, 130
        root_x, root_y = self.root.winfo_x(), self.root.winfo_y()
        root_w, root_h = self.root.winfo_width(), self.root.winfo_height()
        pos_x = root_x + (root_w // 2) - (v_width // 2)
        pos_y = root_y + (root_h // 2) - (v_height // 2)
        v.geometry(f"{v_width}x{v_height}+{pos_x}+{pos_y}")
        v.configure(bg="#1a252c")
        v.transient(self.root); v.grab_set() 
        
        tk.Label(v, text=f"Cola {tipo}", bg="#1a252c", fg="white", font=('Arial', 10, 'bold')).pack(pady=10)
        f = tk.Frame(v, bg="#1a252c"); f.pack()
        ttk.Button(f, text="ELIMINAR", style="Orange.TButton", command=lambda: [v.destroy(), self.ejecutar_gestion(tipo, 'eliminar')]).pack(side=tk.LEFT, padx=5)
        ttk.Button(f, text="CAMBIAR", style="Blue.TButton", command=lambda: [v.destroy(), self.ejecutar_gestion(tipo, 'cambiar')]).pack(side=tk.LEFT, padx=5)

    def ejecutar_gestion(self, tipo, accion):
        cola_obj = self.cola_a if tipo == 'A' else self.cola_b
        idx = simpledialog.askinteger("Fila", f"Fila (1-{len(cola_obj)}):", minvalue=1, maxvalue=len(cola_obj), parent=self.root)
        if idx:
            if accion == 'eliminar': cola_obj.items.pop(idx-1)
            else:
                nv = simpledialog.askinteger("Nuevo", "Valor:", parent=self.root)
                if nv is not None: cola_obj.items[idx-1] = nv
            self.actualizar_listas()

    def sumar_colas(self):
        # Limpiar tabla anterior
        for i in self.tabla_resultados.get_children(): self.tabla_resultados.delete(i)
        
        len_a = len(self.cola_a)
        len_b = len(self.cola_b)
        
        if len_a == 0 or len_b == 0:
            messagebox.showwarning("Aviso", "Ambas colas deben tener elementos.", parent=self.root)
            return

        # MENSAJE DE VALIDACIÓN: Si las colas son desiguales
        if len_a != len_b:
            menor = min(len_a, len_b)
            messagebox.showinfo("Aviso de Suma", 
                                f"Las colas tienen tamaños diferentes ({len_a} vs {len_b}).\n"
                                f"Solo se sumarán los primeros {menor} elementos.", 
                                parent=self.root)

        ta, tb = self.cola_a.copia(), self.cola_b.copia()
        # El ciclo while se detiene automáticamente cuando una de las dos colas se vacía
        while not ta.esta_vacia() and not tb.esta_vacia():
            va, vb = ta.desencolar(), tb.desencolar()
            self.tabla_resultados.insert('', 'end', values=(va, vb, va + vb))

    def limpiar_todo(self):
        self.cola_a = Cola(); self.cola_b = Cola()
        self.actualizar_listas()
        for i in self.tabla_resultados.get_children(): self.tabla_resultados.delete(i)

    def cargar_ejemplo(self):
        # Ejemplo desigual: Cola A (5 elementos), Cola B (3 elementos)
        self.cola_a.items = [10, 20, 30, 40, 50]
        self.cola_b.items = [5, 5, 5]
        self.actualizar_listas()

    def actualizar_listas(self):
        self.lista_a.delete(0, tk.END); self.lista_b.delete(0, tk.END)
        for i, v in enumerate(self.cola_a.items): self.lista_a.insert(tk.END, f"{i+1}. {v}")
        for i, v in enumerate(self.cola_b.items): self.lista_b.insert(tk.END, f"{i+1}. {v}")

if __name__ == "__main__":
    root = tk.Tk(); app = SumadorColasGUI(root); root.mainloop()