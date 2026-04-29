import tkinter as tk
import math
import random

# Colores y Configuración
BG = "#1e1e2f"
TEXT = "#ffffff"
PRIMARY = "#cf87e7"
GOLD = "#f9e45b"

paso = [0]
modo = {"tipo": "manual"}
corriendo = {"activo": False}
continuar = None
copia_max_heap = [] 
lista_final = []    

# =========================
# CONTROL E INTERFAZ
# =========================
def esperar():
    if not corriendo["activo"]: 
        raise StopIteration
    if modo["tipo"] == "auto":
        root.after(500)
        root.update()
    else:
        continuar.set(False)
        root.wait_variable(continuar)

def siguiente(event=None):
    if corriendo["activo"]: 
        continuar.set(True)

def reset_interfaz():
    extra_tree_controls.pack_forget()
    tree.delete("all")
    canvas.delete("all")
    paso[0] = 0

def detener_y_limpiar():
    corriendo["activo"] = False
    continuar.set(True) 
    entrada.delete(0, tk.END)
    hist.delete(1.0, tk.END)
    reset_interfaz()
    mostrar_paneles(False)

def obtener():
    txt = entrada.get().replace(",", " ").strip()
    try:
        return list(map(int, txt.split()))
    except ValueError:
        return []

def generar_aleatorios():
    detener_y_limpiar()
    cantidad = random.randint(5, 8)
    numeros = [random.randint(1, 99) for _ in range(cantidad)]
    entrada.insert(0, " ".join(map(str, numeros)))

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
    
    canvas.create_text(400, 20, text=f"Paso {paso[0]} - Modo: {modo['tipo'].upper()}", 
                       fill=PRIMARY, font=("Arial", 11, "bold"))
    root.update()

# =========================
# ÁRBOL DINÁMICO
# =========================
def arbol(lista, n_activos, msg="", resaltar_raiz=False, limpiar_primero=True):
    mostrar_paneles(True)
    if limpiar_primero: tree.delete("all")
    
    # CORRECCIÓN: Si queda 1 o 0 nodos, limpiamos y no dibujamos más círculos
    if n_activos <= 1:
        if msg: agregar_historial(msg)
        root.update()
        return

    niveles = int(math.log2(n_activos)) + 1
    ancho_canvas = tree.winfo_width() if tree.winfo_width() > 100 else 400
    ancho_necesario = max(ancho_canvas, (2 ** (niveles - 1)) * 60)
    alto_necesario = niveles * 80 + 50
    tree.configure(scrollregion=(0, 0, ancho_necesario, alto_necesario))
    
    for i in range(1, n_activos):
        padre = (i-1)//2
        x1, y1 = calcular_pos(i, n_activos, ancho_necesario)
        x2, y2 = calcular_pos(padre, n_activos, ancho_necesario)
        tree.create_line(x1, y1, x2, y2, fill=TEXT, width=2)
    
    for i in range(n_activos):
        x, y = calcular_pos(i, n_activos, ancho_necesario)
        color = GOLD if (resaltar_raiz and i == 0) else PRIMARY
        tree.create_oval(x-20, y-20, x+20, y+20, fill=color, outline=BG, width=2)
        tree.create_text(x, y, text=str(lista[i]), fill="black", font=("Arial", 11, "bold"))
    
    if msg: agregar_historial(msg)
    root.update()

def calcular_pos(i, total, ancho_canvas):
    nivel = int(math.log2(i+1))
    pos_en_nivel = i - (2**nivel - 1)
    nodos_en_nivel = 2**nivel
    x = ancho_canvas // (nodos_en_nivel + 1) * (pos_en_nivel + 1)
    y = 50 + nivel * 70
    return x, y

def mostrar_paneles(ver_arbol):
    if ver_arbol: tree_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    else: tree_frame.pack_forget()

# =========================
# ALGORITMOS
# =========================
def heapify_max(a, n, i):
    mayor = i
    izq, der = 2*i + 1, 2*i + 2
    if izq < n:
        agregar_historial(f"¿Hijo izq {a[izq]} > {a[mayor]}?")
        if a[izq] > a[mayor]: mayor = izq
    if der < n:
        agregar_historial(f"¿Hijo der {a[der]} > {a[mayor]}?")
        if a[der] > a[mayor]: mayor = der
    if mayor != i:
        a[i], a[mayor] = a[mayor], a[i]
        paso[0] += 1
        dibujar(a, [i, mayor])
        arbol(a, n, f"Ajuste: {a[i]} sube", True)
        esperar()
        heapify_max(a, n, mayor)

def heap(a):
    global copia_max_heap, lista_final
    n = len(a)
    dibujar(a)
    agregar_historial("=== FASE: CONSTRUIR MAX-HEAP ===")
    for i in range(n//2 - 1, -1, -1):
        heapify_max(a, n, i)
    
    copia_max_heap = list(a)
    arbol(a, n, "Max-Heap Completo", True)
    esperar()
    
    agregar_historial("=== FASE: ORDENAMIENTO ===")
    for i in range(n-1, 0, -1):
        agregar_historial(f"Intercambio raíz {a[0]} con final {a[i]}")
        a[i], a[0] = a[0], a[i]
        paso[0] += 1
        dibujar(a, [0, i])
        arbol(a, i, f"Reduciendo árbol a {i} nodos", True)
        esperar()
        heapify_max(a, i, 0)
    
    lista_final = list(a)
    tree.delete("all") # Limpieza final del árbol residual
    dibujar(a) 
    agregar_historial("☑ Heap Sort Finalizado")
    extra_tree_controls.pack(pady=10)

def shell(a):
    mostrar_paneles(False)
    gap = len(a)//2
    while gap > 0:
        agregar_historial(f"--- GAP {gap} ---")
        for i in range(gap, len(a)):
            j = i
            while j >= gap:
                paso[0] += 1
                dibujar(a, [j, j-gap])
                if a[j-gap] > a[j]:
                    agregar_historial(f"Intercambio: {a[j-gap]} ↔ {a[j]}")
                    a[j], a[j-gap] = a[j-gap], a[j]
                    dibujar(a, [j, j-gap])
                esperar()
                j -= gap
        gap //= 2
    dibujar(a)
    agregar_historial("☑ Shell Sort Finalizado")

def quick(a, l, h):
    if l < h:
        p = particion(a, l, h)
        quick(a, l, p-1)
        quick(a, p+1, h)
    if l == 0 and h == len(a)-1: 
        dibujar(a)
        agregar_historial("☑ Quick Sort Finalizado")

def particion(a, l, h):
    piv = a[h]
    i = l-1
    agregar_historial(f"Partición - Pivote: {piv}")
    for j in range(l, h):
        paso[0] += 1
        dibujar(a, [j, h])
        if a[j] < piv:
            i += 1
            a[i], a[j] = a[j], a[i]
            dibujar(a, [i, j])
        esperar()
    a[i+1], a[h] = a[h], a[i+1]
    dibujar(a, [i+1, h])
    esperar()
    return i+1

def radix(a):
    mostrar_paneles(False)
    m = max(a)
    exp = 1
    while m // exp > 0:
        agregar_historial(f"--- Analizando dígito: {exp} ---")
        buckets = [[] for _ in range(10)]
        for x in a:
            digito = (x // exp) % 10
            buckets[digito].append(x)
        
        a.clear()
        for b in buckets: a.extend(b)
        paso[0] += 1
        dibujar(a)
        esperar()
        exp *= 10
    agregar_historial("☑ Radix Sort Finalizado")

# =========================
# ACCIONES DE VISTA
# =========================
def run(tipo):
    if corriendo["activo"]: return
    a = obtener()
    if not a: return
    
    # REGLA: Forzar modo MANUAL al iniciar cualquier método
    modo["tipo"] = "manual" 
    
    reset_interfaz()
    hist.delete(1.0, tk.END)
    corriendo["activo"] = True
    try:
        if tipo == "Shell": shell(a)
        elif tipo == "Quick": quick(a, 0, len(a)-1)
        elif tipo == "Heap": heap(a)
        elif tipo == "Radix": radix(a)
    except StopIteration: pass
    finally: corriendo["activo"] = False

def ver_max():
    tree.delete("all")
    arbol(copia_max_heap, len(copia_max_heap), "VISTA: Max-Heap inicial", True, False)

def ver_min():
    tree.delete("all")
    arbol(lista_final, len(lista_final), "VISTA: Árbol Final", True, False)

# =========================
# GUI
# =========================
root = tk.Tk()
root.title("Visualizador de Estructuras")
root.configure(bg=BG)
root.geometry("1100x850")

input_frame = tk.Frame(root, bg=BG)
input_frame.pack(pady=20)
tk.Label(input_frame, text="Números:", bg=BG, fg=TEXT, font=("Arial", 11)).pack(side=tk.LEFT)
entrada = tk.Entry(input_frame, width=45, font=("Arial", 12), bg="#313244", fg=TEXT, insertbackground=TEXT)
entrada.pack(side=tk.LEFT, padx=10)
tk.Button(input_frame, text="Generar Aleatorio", command=generar_aleatorios, bg="#89b4fa").pack(side=tk.LEFT)

btn_frame = tk.Frame(root, bg=BG)
btn_frame.pack(pady=10)
ops = [("Shell", "#f7a8a8"), ("Quick", "#a8d8f7"), ("Heap", "#a8f7c5"), ("Radix", "#f7e6a8"),
       ("MANUAL", "#d1a8f7"), ("AUTO", "#f7cfa8"), ("LIMPIAR", "#a8f7f1"), ("SALIR", "#f7a8e5")]

for i, (txt, col) in enumerate(ops):
    if txt in ["MANUAL", "AUTO"]: c = lambda t=txt: modo.update(tipo=t.lower())
    elif txt == "LIMPIAR": c = detener_y_limpiar
    elif txt == "SALIR": c = root.destroy
    else: c = lambda t=txt: run(t)
    tk.Button(btn_frame, text=txt, command=c, width=12, height=2, bg=col).grid(row=i//4, column=i%4, padx=5, pady=5)

canvas = tk.Canvas(root, width=850, height=150, bg=BG, highlightthickness=1, highlightbackground="#444")
canvas.pack(pady=10)

panel_bottom = tk.Frame(root, bg=BG)
panel_bottom.pack(fill=tk.BOTH, expand=True, padx=20)

hist_frame = tk.Frame(panel_bottom, bg=BG, width=450)
hist_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
hist = tk.Text(hist_frame, bg="#000000", fg="#ffffff", font=("Consolas", 10), borderwidth=0)
hist.tag_configure("centrado", justify='center')
hist.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrolly = tk.Scrollbar(hist_frame, command=hist.yview)
scrolly.pack(side=tk.RIGHT, fill=tk.Y)
hist.config(yscrollcommand=scrolly.set)

tree_frame = tk.Frame(panel_bottom, bg=BG)
tree_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
tree = tk.Canvas(tree_frame, bg=BG, highlightthickness=0)
tree.pack(fill=tk.BOTH, expand=True)

extra_tree_controls = tk.Frame(tree_frame, bg=BG)
tk.Button(extra_tree_controls, text="Ver Max-Heap (Inicio)", command=ver_max, bg=GOLD, width=18).pack(side=tk.LEFT, padx=5)
tk.Button(extra_tree_controls, text="Ver Árbol Final", command=ver_min, bg=PRIMARY, width=18).pack(side=tk.LEFT, padx=5)

tree_frame.pack_forget()
continuar = tk.BooleanVar()
root.bind("<Return>", siguiente)
root.mainloop()