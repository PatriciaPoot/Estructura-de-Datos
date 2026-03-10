import time

def fibonacci_recursivo(n):
    if n <= 1:
        return n
    else:
        return fibonacci_recursivo(n-1) + fibonacci_recursivo(n-2)

def fibonacci_iterativo(n):
    if n <= 1:
        return n
    
    a, b = 0, 1
    for i in range(2, n+1):
        a, b = b, a + b
    return b

numero = int(input("Ingresa un número para calcular Fibonacci: "))

inicio_rec = time.time()
resultado_rec = fibonacci_recursivo(numero)
fin_rec = time.time()

inicio_it = time.time()
resultado_it = fibonacci_iterativo(numero)
fin_it = time.time()

print("\nResultado Fibonacci de", numero)
print("Recursivo:", resultado_rec)
print("Iterativo:", resultado_it)

print("\nTiempo de ejecución:")
print("Recursivo:", fin_rec - inicio_rec, "segundos")
print("Iterativo:", fin_it - inicio_it, "segundos")

print("\nVentajas:")
print("- Recursivo: Código más simple y fácil de entender matemáticamente.")
print("- Iterativo: Mucho más rápido y eficiente en memoria.")
