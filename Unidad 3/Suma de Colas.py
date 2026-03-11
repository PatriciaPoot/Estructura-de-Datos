class Cola:
    def __init__(self):
        self.items = []
    
    def encolar(self, item):
        self.items.append(item)
    
    def desencolar(self):
        if not self.esta_vacia():
            return self.items.pop(0)
        return None
    
    def esta_vacia(self):
        return len(self.items) == 0
    
    def tamanio(self):
        return len(self.items)


def sumar_colas(cola1, cola2):
    """Suma los elementos de dos colas y devuelve una nueva cola con los resultados"""
    resultado = Cola()
    
    # Determinar cuántos elementos vamos a sumar (el tamaño de la cola más pequeña)
    minimo = min(cola1.tamanio(), cola2.tamanio())
    
    # Sumar elemento por elemento
    for i in range(minimo):
        # Desencolamos y guardamos temporalmente
        val1 = cola1.desencolar()
        val2 = cola2.desencolar()
        
        # Sumamos y encolamos en resultado
        resultado.encolar(val1 + val2)
        
        # Volvemos a encolar en las colas originales para no perderlos
        cola1.encolar(val1)
        cola2.encolar(val2)
    
    return resultado


def ingresar_numeros(mensaje):
    """Función para validar que solo se ingresen números (enteros o decimales)"""
    while True:
        print(mensaje)
        entrada = input().strip().split()
        numeros = []
        valido = True
        
        for item in entrada:
            try:
                numeros.append(float(item))
            except ValueError:
                print(f"Error: '{item}' no es un número válido. Intenta de nuevo.")
                valido = False
                break
        
        if valido:
            return numeros


# Programa principal
print("=== SUMADOR DE COLAS ===\n")

# Cola A
nums_a = ingresar_numeros("Ingresa números para Cola A (separados por espacios):")
cola_a = Cola()
for num in nums_a:
    cola_a.encolar(num)

# Cola B
nums_b = ingresar_numeros("Ingresa números para Cola B (separados por espacios):")
cola_b = Cola()
for num in nums_b:
    cola_b.encolar(num)

# Sumar colas
resultado = sumar_colas(cola_a, cola_b)

# Obtener resultados
resultados = []
while not resultado.esta_vacia():
    resultados.append(resultado.desencolar())

# Mostrar solo la tabla
print("\nTABLA DE SUMAS:")
print("-" * 45)
print("|  Cola A  |  Cola B  |   Suma   |")
print("-" * 45)
for i in range(len(resultados)):
    print(f"|   {nums_a[i]:6.2f} |   {nums_b[i]:6.2f} |   {resultados[i]:6.2f} |")
print("-" * 45)

# Mostrar sobrantes si los hay (formateados a 2 decimales)
if len(nums_a) > len(nums_b):
    sobrantes = [f"{x:.2f}" for x in nums_a[len(nums_b):]]
    print(f"\nSobrantes de Cola A: {sobrantes}")
elif len(nums_b) > len(nums_a):
    sobrantes = [f"{x:.2f}" for x in nums_b[len(nums_a):]]
    print(f"\nSobrantes de Cola B: {sobrantes}")
