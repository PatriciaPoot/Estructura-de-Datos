calificaciones = [0] * 5  

for i in range(5):

    dato = input(f"Captura la calificación {i}: ")
    calificaciones[i] = int(dato)

print("Calificaciones finales:", calificaciones)
