import numpy as np

alumnos = 500
materias = 6

matriz = np.random.randint(0, 11, size=(alumnos, materias))
print("Alumno | M1  M2  M3  M4  M5  M6")
print("-" * 35)

for i in range(alumnos):
    fila = "  ".join(f"{nota:>2}" for nota in matriz[i])
    print(f"{i+1:>6} | {fila}")

print("\nBúsqueda de calificación")
alumno_buscar = int(input("Ingresa el número de alumno (1-500): "))
materia_buscar = int(input("Ingresa el número de materia (1-6): "))

fila = alumno_buscar - 1
columna = materia_buscar - 1

if 0 <= fila < alumnos and 0 <= columna < materias:
    calificacion = matriz[fila, columna]  
    print(f"\nAlumno {alumno_buscar}, Materia {materia_buscar}")
    print(f"Calificación: {calificacion}")
else:
    print("Posición fuera de rango")
