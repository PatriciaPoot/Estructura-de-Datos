meses = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

departamentos = ["Ropa", "Deportes", "Juguetería"]

ventas = [
    [1200, 900, 1500],
    [1100, 850, 1400],
    [1300, 920, 1600],
    [1250, 980, 1550],
    [1400, 1000, 1700],
    [1500, 1100, 1800],
    [1600, 1200, 1900],
    [1550, 1150, 1850],
    [1450, 1050, 1750],
    [1500, 1100, 1800],
    [1650, 1250, 2000],
    [1800, 1400, 2200],
]

def mostrar_tabla():
    print("\nMes\t\tRopa\tDeportes\tJuguetería")
    for i in range(12):
        print(f"{meses[i]:<10}\t{ventas[i][0]}\t{ventas[i][1]}\t\t{ventas[i][2]}")

def modificar_venta():
    mes = input("¿Qué mes quieres modificar?: ").capitalize()
    dep = input("¿Qué departamento? (Ropa / Deportes / Juguetería): ").capitalize()

    if mes in meses and dep in departamentos:
        fila = meses.index(mes)
        col = departamentos.index(dep)

        print(f"Venta actual de {mes} en {dep}: {ventas[fila][col]}")
        nuevo = int(input("Ingresa el nuevo monto: "))
        ventas[fila][col] = nuevo
        print("Venta actualizada.")
    else:
        print("Mes o departamento inválido.")

def buscar_mes_departamento():
    mes = input("¿Qué mes quieres buscar?: ").capitalize()
    dep = input("¿Qué departamento? (Ropa / Deportes / Juguetería): ").capitalize()

    if mes in meses and dep in departamentos:
        fila = meses.index(mes)
        col = departamentos.index(dep)
        print(f"\nLa venta de {dep} en {mes} es: {ventas[fila][col]}")
    else:
        print("Mes o departamento inválido.")

def eliminar_venta():
    mes = input("¿Qué mes quieres eliminar?: ").capitalize()
    dep = input("¿Qué departamento? (Ropa / Deportes / Juguetería): ").capitalize()

    if mes in meses and dep in departamentos:
        fila = meses.index(mes)
        col = departamentos.index(dep)
        
        print(f"Venta actual de {mes} en {dep}: {ventas[fila][col]}")
        confirmar = input("¿Seguro que quieres eliminar este monto? (s/n): ").lower()

        if confirmar == "s":
            ventas[fila][col] = 0
            print("Monto eliminado (puesto en 0).")
        else:
            print("Operación cancelada.")
    else:
        print("Mes o departamento inválido.")

def menu():
    while True:
        print("\n=== MENÚ DE VENTAS ===")
        print("1. Mostrar tabla")
        print("2. Modificar una venta")
        print("3. Buscar venta por mes y departamento")
        print("4. Eliminar una venta")
        print("5. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            mostrar_tabla()
        elif opcion == "2":
            modificar_venta()
        elif opcion == "3":
            buscar_mes_departamento()
        elif opcion == "4":
            eliminar_venta()
        elif opcion == "5":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida.")

menu()
