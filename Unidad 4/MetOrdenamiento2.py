import tkinter as tk
from tkinter import messagebox
import math

# Configuración Estética
BG = "#1e1e2f"
TEXT = "#ffffff" 
PRIMARY = "#cf87e7"
GOLD = "#f9e45b"

# Estado Global
paso = [0]
modo = {"tipo": "manual"}
corriendo = {"activo": False}
esperando_inicio = [True] 
continuar = None
cantidad_esperada = [0]
copia_max_heap = [] 
lista_final = []    

def establecer_cantidad():
    try:
        n = int(entrada_cant.get())
        if n <= 0: raise ValueError
        cantidad_esperada[0] = n
        entrada_cant.config(state="disabled")
        btn_fijar.config(state="disabled")
        entrada_nums.config(state="normal")
        entrada_nums.focus()
        limpiar_historial()
    except ValueError:
        messagebox.showwarning("Error", "Ingresa una cantidad válida.")

def obtener_lista():
    txt = sv_nums.get().strip()
    try:
        nums = list(map(int, txt.split()))
        # VALIDACIÓN ESTRICTA DE CANTIDAD
        if len(nums) < cantidad_esperada[0]:
            messagebox.showwarning("Atención", f"Faltan números. Ingresaste {len(nums)} de {cantidad_esperada[0]}.")
            return None
        if len(nums) > cantidad_esperada[0]:
            messagebox.showwarning("Atención", f"Exceso de números. Ingresaste {len(nums)} pero fijaste {cantidad_esperada[0]}.")
            return None
        return nums
    except ValueError:
        messagebox.showerror("Error", "Formato incorrecto. Usa solo números y espacios.")
        return None

def esperar():
    if not corriendo["activo"]: raise StopIteration
    if esperando_inicio[0]:
        esperando_inicio[0] = False
        continuar.set(False)
        root.wait_variable(continuar)
    
    if modo["tipo"] == "auto":
        root.after(500); root.update()
    else:
        continuar.set(False)
        root.wait_variable(continuar)

def siguiente(event=None):
    if corriendo["activo"]: continuar.set(True)

def reset_interfaz():
    extra_tree_controls.pack_forget()
    tree.delete("all")
    canvas.delete("all")
    paso[0] = 0

def limpiar_historial():
    hist.delete(1.0, tk.END)

def detener_y_limpiar():
    corriendo["activo"] = False
    continuar.set(True) 
    entrada_cant.config(state="normal")
    entrada_cant.delete(0, tk.END)
    btn_fijar.config(state="normal")
    sv_nums.set("")
    entrada_nums.config(state="disabled")
    modo["tipo"] = "manual"
    limpiar_historial()
    reset_interfaz()
    mostrar_paneles(False)

def agregar_historial(texto):
    hist.insert(tk.END, texto + "\n", "centrado")
    hist.see(tk.END)

def dibujar(lista, highlight=[]):
    canvas.delete("all")
    if not lista: return
    ancho_celda = min(70, 700 // len(lista))
    total_ancho = ancho_celda * len(lista)
    inicio_x = (800 - total_ancho) // 2 + ancho_celda//2
    for i, n in enumerate(lista):
        x = inicio_x + i * ancho_celda
        color = "#ff6b6b" if i in highlight else TEXT
        canvas.create_text(x, 80, text=str(n), fill=color, font=("Consolas", 22, "bold"))
    canvas.create_text(400, 20, text=f"Paso {paso[0]} - Modo: {modo['tipo'].upper()}", fill=PRIMARY, font=("Arial", 11, "bold"))
    root.update()

# =========================
# ALGORITMOS
# =========================
def shell(a):
    mostrar_paneles(False)
    esperar() 
    agregar_historial(f"=== INICIANDO SHELL ===")
    gap = len(a)//2
    while gap > 0:
        agregar_historial(f"--- GAP {gap} ---")
        for i in range(gap, len(a)):
            j = i
            while j >= gap:
                paso[0] += 1
                agregar_historial(f"¿{a[j-gap]} > {a[j]}?")
                dibujar(a, [j, j-gap]); esperar()
                if a[j-gap] > a[j]:
                    agregar_historial(f"Cambio: {a[j-gap]} ↔ {a[j]}")
                    a[j], a[j-gap] = a[j-gap], a[j]
                    dibujar(a, [j, j-gap]); esperar()
                j -= gap
        gap //= 2
    agregar_historial("☑ Finalizado")

def quick(a, l, h):
    if l == 0 and h == len(a)-1:
        esperar() 
        agregar_historial(f"=== INICIANDO QUICK ===")
    if l < h:
        piv = a[h]; i = l-1
        agregar_historial(f"Pivote: {piv}")
        for j in range(l, h):
            paso[0] += 1
            agregar_historial(f"¿{a[j]} < {piv}?")
            dibujar(a, [j, h]); esperar()
            if a[j] < piv:
                i += 1
                a[i], a[j] = a[j], a[i]
                dibujar(a, [i, j]); esperar()
        a[i+1], a[h] = a[h], a[i+1]
        dibujar(a, [i+1, h]); esperar()
        quick(a, l, i); quick(a, i+2, h)
    if l == 0 and h == len(a)-1: agregar_historial("☑ Finalizado")

def heapify_max(a, n, i):
    mayor = i
    izq, der = 2*i + 1, 2*i + 2
    if izq < n:
        agregar_historial(f"Hijo Izq {a[izq]} vs Padre {a[mayor]}")
        if a[izq] > a[mayor]: mayor = izq
    if der < n:
        agregar_historial(f"Hijo Der {a[der]} vs Padre {a[mayor]}")
        if a[der] > a[mayor]: mayor = der
    if mayor != i:
        a[i], a[mayor] = a[mayor], a[i]
        paso[0] += 1
        dibujar(a, [i, mayor])
        arbol(a, n, f"Ajuste", True); esperar()
        heapify_max(a, n, mayor)

def heap(a):
    global copia_max_heap, lista_final
    esperar() 
    agregar_historial(f"=== INICIANDO HEAP ===")
    n = len(a)
    agregar_historial("Construyendo Max-Heap")
    for i in range(n//2 - 1, -1, -1): heapify_max(a, n, i)
    copia_max_heap = list(a)
    arbol(a, n, "Heap Listo", True); esperar()
    for i in range(n-1, 0, -1):
        agregar_historial(f"Extrayendo raíz")
        a[i], a[0] = a[0], a[i]
        paso[0] += 1
        dibujar(a, [0, i])
        arbol(a, i, f"Reduciendo", True); esperar()
        heapify_max(a, i, 0)
    lista_final = list(a)
    tree.delete("all"); dibujar(a)
    agregar_historial("☑ Finalizado")
    extra_tree_controls.pack(side=tk.TOP, pady=5)

def radix(a):
    mostrar_paneles(False)
    esperar() 
    agregar_historial(f"=== INICIANDO RADIX ===")
    m = max(a); exp = 1
    while m // exp > 0:
        agregar_historial(f"Dígito: {exp}")
        buckets = [[] for _ in range(10)]
        for x in a:
            dig = (x // exp) % 10
            buckets[dig].append(x)
        a.clear()
        for b in buckets: a.extend(b)
        paso[0] += 1; dibujar(a); esperar(); exp *= 10
    agregar_historial("☑ Finalizado")

def iniciar_metodo(tipo):
    if corriendo["activo"]: return
    a = obtener_lista()
    if not a: return
    
    limpiar_historial()
    reset_interfaz()
    dibujar(a) 
    
    esperando_inicio[0] = True 
    corriendo["activo"] = True
    try:
        if tipo == "Shell": shell(a)
        elif tipo == "Quick": quick(a, 0, len(a)-1)
        elif tipo == "Heap": heap(a)
        elif tipo == "Radix": radix(a)
    except StopIteration: pass
    finally: 
        corriendo["activo"] = False
        modo["tipo"] = "manual"

# =========================
# GUI
# =========================
def arbol(lista, n_activos, msg="", resaltar_raiz=False, limpiar_primero=True):
    mostrar_paneles(True)
    if limpiar_primero: tree.delete("all")
    if n_activos <= 0: return
    niveles = int(math.log2(n_activos)) + 1
    ancho_canvas = tree.winfo_width() if tree.winfo_width() > 100 else 400
    ancho_necesario = max(ancho_canvas, (2 ** (niveles - 1)) * 60)
    tree.configure(scrollregion=(0, 0, ancho_necesario, niveles * 80 + 50))
    for i in range(1, n_activos):
        padre = (i-1)//2
        x1, y1 = calcular_pos(i, n_activos, ancho_necesario)
        x2, y2 = calcular_pos(padre, n_activos, ancho_necesario)
        tree.create_line(x1, y1, x2, y2, fill=TEXT, width=2)
    for i in range(n_activos):
        x, y = calcular_pos(i, n_activos, ancho_necesario)
        color = GOLD if (resaltar_raiz and i == 0) else PRIMARY
        tree.create_oval(x-18, y-18, x+18, y+18, fill=color, outline=BG, width=2)
        tree.create_text(x, y, text=str(lista[i]), fill="black", font=("Arial", 10, "bold"))
    if msg: agregar_historial(msg)
    root.update()

def calcular_pos(i, total, ancho_canvas):
    nivel = int(math.log2(i+1)); pos_en_nivel = i - (2**nivel - 1)
    nodos_en_nivel = 2**nivel
    x = ancho_canvas // (nodos_en_nivel + 1) * (pos_en_nivel + 1)
    y = 50 + nivel * 70
    return x, y

def mostrar_paneles(ver_arbol):
    if ver_arbol: tree_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    else: tree_frame.pack_forget()

root = tk.Tk()
root.title("Visualizador de Estructuras")
root.configure(bg=BG)
root.geometry("1100x850")

sv_nums = tk.StringVar()
top_frame = tk.Frame(root, bg=BG)
top_frame.pack(pady=10)

tk.Label(top_frame, text="Cantidad:", bg=BG, fg=TEXT).grid(row=0, column=0, padx=5)
entrada_cant = tk.Entry(top_frame, width=5, bg="#313244", fg=TEXT)
entrada_cant.grid(row=0, column=1, padx=5)
btn_fijar = tk.Button(top_frame, text="Fijar", command=establecer_cantidad, bg="#89b4fa")
btn_fijar.grid(row=0, column=2, padx=5)

tk.Label(top_frame, text="Números:", bg=BG, fg=TEXT).grid(row=0, column=3, padx=15)
entrada_nums = tk.Entry(top_frame, textvariable=sv_nums, width=40, bg="#313244", fg=TEXT, state="disabled")
entrada_nums.grid(row=0, column=4, padx=5)

btn_frame = tk.Frame(root, bg=BG)
btn_frame.pack(pady=10)
ops = [("Shell", "#f7a8a8"), ("Quick", "#a8d8f7"), ("Heap", "#a8f7c5"), ("Radix", "#f7e6a8"),
       ("MANUAL", "#d1a8f7"), ("AUTO", "#f7cfa8"), ("LIMPIAR", "#a8f7f1"), ("SALIR", "#f7a8e5")]

for i, (txt, col) in enumerate(ops):
    if txt == "MANUAL": cmd = lambda: modo.update(tipo="manual")
    elif txt == "AUTO": cmd = lambda: modo.update(tipo="auto")
    elif txt == "LIMPIAR": cmd = detener_y_limpiar
    elif txt == "SALIR": cmd = root.destroy
    else: cmd = lambda t=txt: iniciar_metodo(t)
    tk.Button(btn_frame, text=txt, command=cmd, width=12, height=2, bg=col).grid(row=i//4, column=i%4, padx=5, pady=5)

canvas = tk.Canvas(root, width=850, height=150, bg=BG, highlightthickness=1, highlightbackground="#444")
canvas.pack(pady=10)

panel_bottom = tk.Frame(root, bg=BG)
panel_bottom.pack(fill=tk.BOTH, expand=True, padx=20)

hist_frame = tk.Frame(panel_bottom, bg=BG)
hist_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
hist = tk.Text(hist_frame, bg="#000000", fg="#ffffff", font=("Consolas", 10))
hist.tag_configure("centrado", justify='center')
hist.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

tree_frame = tk.Frame(panel_bottom, bg=BG)
extra_tree_controls = tk.Frame(tree_frame, bg=BG)
tk.Button(extra_tree_controls, text="Ver Max-Heap Inicial", command=lambda: arbol(copia_max_heap, len(copia_max_heap), "", True), bg=GOLD).pack(side=tk.LEFT, padx=5)
tk.Button(extra_tree_controls, text="Ver Árbol Final", command=lambda: arbol(lista_final, len(lista_final), "", True), bg=PRIMARY).pack(side=tk.LEFT, padx=5)

tree = tk.Canvas(tree_frame, bg=BG, highlightthickness=0)
tree.pack(fill=tk.BOTH, expand=True)

continuar = tk.BooleanVar()
root.bind("<Return>", siguiente)
root.mainloop()
