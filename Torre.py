import time

def torre_hanoi(n, origen, auxiliar, destino):
    if n == 1:
        print(f"Mover disco 1 de {origen} a {destino}")
        return
    torre_hanoi(n-1, origen, destino, auxiliar)
    print(f"Mover disco {n} de {origen} a {destino}")
    torre_hanoi(n-1, auxiliar, origen, destino)


# Programa principal
n = int(input("Ingrese el número de discos: "))

inicio = time.time()

print("\nMovimientos:\n")
torre_hanoi(n, "A", "B", "C")

fin = time.time()

tiempo = fin - inicio

print("\nTiempo que tardó en resolver la Torre de Hanoi:", tiempo, "segundos")