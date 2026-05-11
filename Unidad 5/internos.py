# internos.py

# --- ADA 1 ---
def burbuja(lista):
    arr = lista.copy()
    n = len(arr)
    print(f"\n--- [1. Burbuja] ---")
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                print(f"Intercambio: {arr[j]} por {arr[j+1]}")
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                print(f"  Estado: {arr}")
    return arr

def insercion(lista):
    arr = lista.copy()
    print(f"\n--- [2. Inserción] ---")
    for i in range(1, len(arr)):
        clave = arr[i]
        j = i - 1
        print(f"Tomando el valor {clave} para comparar")
        while j >= 0 and clave < arr[j]:
            print(f"  Moviendo {arr[j]} a la derecha")
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = clave
        print(f"Insertado {clave} en posición {j+1} -> {arr}")
    return arr

def seleccion(lista):
    arr = lista.copy()
    print(f"\n--- [3. Selección] ---")
    for i in range(len(arr)):
        m = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[m]: 
                m = j
        if m != i:
            print(f"Intercambio: {arr[i]} por el mínimo {arr[m]}")
            arr[i], arr[m] = arr[m], arr[i]
        print(f"Paso {i+1}: {arr}")
    return arr

# --- ADA 2 ---
def shell_sort(lista):
    arr = lista.copy()
    n = len(arr)
    gap = n // 2
    print(f"\n--- [4. ShellSort] ---")
    while gap > 0:
        print(f"Probando con Gap: {gap}")
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                print(f"  Moviendo {arr[j-gap]} (distancia {gap})")
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        print(f"Estado con gap {gap}: {arr}")
        gap //= 2
    return arr

def quick_sort(arr, nivel=0):
    if nivel == 0: print(f"\n--- [5. QuickSort] ---")
    if len(arr) <= 1: return arr
    piv = arr[len(arr)//2]
    print(f"Nivel {nivel}: Usando pivote {piv}")
    izq = [x for x in arr if x < piv]
    cen = [x for x in arr if x == piv]
    der = [x for x in arr if x > piv]
    res = quick_sort(izq, nivel+1) + cen + quick_sort(der, nivel+1)
    print(f"Fusión Nivel {nivel}: {izq} + {cen} + {der} -> {res}")
    return res

def heap_sort(lista):
    import heapq
    arr = lista.copy()
    print(f"\n--- [6. HeapSort] ---")
    print("Convirtiendo lista en un Montículo (Heap)...")
    heapq.heapify(arr)
    print(f"Estructura inicial: {arr}")
    res = []
    while arr:
        v = heapq.heappop(arr)
        print(f"Extrayendo raíz (el más pequeño): {v}")
        res.append(v)
        print(f"  Lista ordenada: {res} | Heap restante: {arr}")
    return res

def radix_sort(lista):
    if not lista: return lista
    arr = lista.copy()
    m = max(arr)
    exp = 1
    print(f"\n--- [7. RadixSort] ---")
    while m // exp > 0:
        print(f"Ordenando por el dígito en posición: {exp}")
        buckets = [[] for _ in range(10)]
        for x in arr: 
            digito = (x // exp) % 10
            buckets[digito].append(x)
        arr = [item for sub in buckets for item in sub]
        print(f"  Resultado de esta pasada: {arr}")
        exp *= 10
    return arr