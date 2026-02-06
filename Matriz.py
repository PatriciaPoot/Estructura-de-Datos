import random

# Cantidad de alumnos y materias
alumnos = 500
materias = 6

# Crear matriz con calificaciones aleatorias de 0 a 10
matriz = [[random.randint(0, 10) for _ in range(materias)] for _ in range(alumnos)]

# Imprimir encabezado
print("Alumno | M1  M2  M3  M4  M5  M6")
print("-" * 35)

# Imprimir los 500 alumnos
for i in range(alumnos):
    fila = "  ".join(f"{nota:>2}" for nota in matriz[i])
    print(f"{i+1:>6} | {fila}")

# ---- BUSCAR UNA POSICIÓN ----
print("\nBúsqueda de calificación")

alumno_buscar = int(input("Ingresa el número de alumno (1-500): "))
materia_buscar = int(input("Ingresa el número de materia (1-6): "))

# Ajustar a índices de Python
fila = alumno_buscar - 1
columna = materia_buscar - 1

if 0 <= fila < alumnos and 0 <= columna < materias:
    calificacion = matriz[fila][columna]
    print(f"\n Alumno {alumno_buscar}, Materia {materia_buscar}")
    print(f"Calificación: {calificacion}")
else:
    print("Posición fuera de rango")
