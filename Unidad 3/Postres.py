POSTRES = {}


# ==================================
# SUBPROGRAMA: eliminar repetidos
# ==================================

def eliminar_repetidos():

    for postre in POSTRES:

        ingredientes_unicos = []

        for ing in POSTRES[postre]:

            if ing not in ingredientes_unicos:
                ingredientes_unicos.append(ing)

        POSTRES[postre] = ingredientes_unicos


# ==================================
# MOSTRAR LISTA DE POSTRES
# ==================================

def mostrar_postres():

    print("\n" + "-"*40)

    if not POSTRES:
        print("No hay postres registrados.")
        print("-"*40)
        return

    print("Lista de postres:\n")

    for p in POSTRES:
        print("•", p)

    print("-"*40)


# ==================================
# MOSTRAR INGREDIENTES
# ==================================

def mostrar_ingredientes():

    print("\n" + "-"*40)

    if not POSTRES:
        print("No hay postres registrados.")
        print("-"*40)
        return

    nombre = input("Nombre del postre: ").lower().strip()

    if nombre in POSTRES:

        print("\nIngredientes de", nombre)
        print("-"*40)

        for ing in POSTRES[nombre]:
            print(" -", ing)

    else:
        print("El postre no existe.")

    print("-"*40)


# ==================================
# AGREGAR INGREDIENTE
# ==================================

def agregar_ingrediente():

    print("\n" + "-"*40)

    if not POSTRES:
        print("No hay postres registrados.")
        print("-"*40)
        return

    nombre = input("Postre: ").lower().strip()

    if nombre in POSTRES:

        ing = input("Ingrediente a agregar: ").strip()

        if ing == "":
            return

        POSTRES[nombre].append(ing)

        eliminar_repetidos()

        print("\nIngrediente agregado correctamente.")

    else:
        print("El postre no existe.")

    print("-"*40)


# ==================================
# ELIMINAR INGREDIENTE
# ==================================

def eliminar_ingrediente():

    print("\n" + "-"*40)

    if not POSTRES:
        print("No hay postres registrados.")
        print("-"*40)
        return

    nombre = input("Postre: ").lower().strip()

    if nombre in POSTRES:

        ing = input("Ingrediente a eliminar: ").strip()

        if ing in POSTRES[nombre]:

            POSTRES[nombre].remove(ing)
            print("\nIngrediente eliminado.")

        else:
            print("Ingrediente no encontrado.")

    else:
        print("El postre no existe.")

    print("-"*40)


# ==================================
# ALTA DE POSTRE
# ==================================

def alta_postre():

    print("\n" + "-"*40)

    nombre = input("Nombre del nuevo postre: ").lower().strip()

    if nombre == "":
        return

    if nombre in POSTRES:
        print("Ese postre ya existe.")
        print("-"*40)
        return

    ingredientes = []

    print("\nIngrese los ingredientes")
    print("Escriba 0 para terminar")

    while True:

        ing = input("Ingrediente: ").strip()

        if ing == "0":
            break

        if ing == "":
            continue

        ingredientes.append(ing)

    POSTRES[nombre] = ingredientes

    eliminar_repetidos()

    # ordenar postres alfabéticamente
    POSTRES_ordenado = dict(sorted(POSTRES.items()))
    POSTRES.clear()
    POSTRES.update(POSTRES_ordenado)

    print("\nPostre agregado correctamente.")
    print("-"*40)


# ==================================
# BAJA DE POSTRE
# ==================================

def baja_postre():

    print("\n" + "-"*40)

    if not POSTRES:
        print("No hay postres registrados.")
        print("-"*40)
        return

    nombre = input("Postre a eliminar: ").lower().strip()

    if nombre in POSTRES:

        del POSTRES[nombre]
        print("\nPostre eliminado correctamente.")

    else:
        print("El postre no existe.")

    print("-"*40)


# ==================================
# MENU
# ==================================

def mostrar_menu():

    print("\n")
    print("="*40)
    print("        SISTEMA DE POSTRES")
    print("="*40)
    print(" 1. Alta de postre")
    print(" 2. Agregar ingrediente")
    print(" 3. Eliminar ingrediente")
    print(" 4. Mostrar ingredientes")
    print(" 5. Mostrar lista de postres")
    print(" 6. Baja de postre")
    print(" 7. Salir")
    print("="*40)


# ==================================
# PROGRAMA PRINCIPAL
# ==================================

while True:

    mostrar_menu()

    op = input("Seleccione una opción: ")

    if op == "1":
        alta_postre()

    elif op == "2":
        agregar_ingrediente()

    elif op == "3":
        eliminar_ingrediente()

    elif op == "4":
        mostrar_ingredientes()

    elif op == "5":
        mostrar_postres()

    elif op == "6":
        baja_postre()

    elif op == "7":
        print("\nCerrando el sistema de postres...")
        print("Programa finalizado.")
        break

    else:
        print("\nOpción inválida.")
