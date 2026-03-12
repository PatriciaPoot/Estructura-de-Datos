class Order:
    def __init__(self, qtty, customer):
        self.qtty = qtty
        self.customer = customer

    def print_order(self):
        print(f" Cliente: {self.customer.ljust(15)} | Cantidad: {self.qtty}")

class Node:
    def __init__(self, info):
        self.info = info
        self.next = None

class Queue:
    def __init__(self, limit):
        self.top = None
        self.tail = None
        self._size = 0
        self.max_size = limit

    def is_empty(self):
        return self.top is None

    def is_full(self):
        return self._size >= self.max_size

    def enqueue(self, info):
        if self.is_full():
            return False
        
        new_node = Node(info)
        if self.is_empty():
            self.top = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1
        return True

    def dequeue(self):
        if self.is_empty():
            return None
        extracted_info = self.top.info
        self.top = self.top.next
        if self.top is None:
            self.tail = None
        self._size -= 1
        return extracted_info

    def print_info(self):
        print("\n" + "=" * 45)
        print(f"LISTADO DE PEDIDOS ACTUALES ({self._size}/{self.max_size})")
        print("-" * 45)
        if self.is_empty():
            print("La cola esta vacia.")
        else:
            current = self.top
            index = 1
            while current:
                print(f" [{index}]", end="")
                current.info.print_order()
                current = current.next
                index += 1
        print("=" * 45)

# --- INICIO DEL PROGRAMA ---
if __name__ == "__main__":
    print("-" * 40)
    print("CONFIGURACIÓN DEL SISTEMA")
    try:
        limite_input = int(input("Ingrese cuántos elementos desea agregar: "))
    except ValueError:
        print("Dato invalido. Se usara un limite de 5 por defecto.")
        limite_input = 5
    
    cola_pedidos = Queue(limite_input)
    print(f"Sistema configurado para un maximo de {limite_input} elementos.")
    print("-" * 40)

    while True:
        print("\n" + "x" + "-" * 38 + "x")
        print("|      PANEL DE CONTROL DE VENTAS      |")
        print("|" + "-" * 38 + "|")
        capacidad_str = f"| Capacidad: {cola_pedidos._size}/{cola_pedidos.max_size}"
        print(capacidad_str.ljust(39) + "|")
        print("|" + "-" * 38 + "|")
        print("| 1. Registrar nuevo pedido            |")
        print("| 2. Eliminar pedido                   |")
        print("| 3. Ver estado de la cola             |")
        print("| 4. Salir del sistema                 |")
        print("x" + "-" * 38 + "x")
        
        opcion = input(" > Seleccione una opcion: ")

        if opcion == "1":
            if cola_pedidos.is_full():
                print(f"\nERROR: La cola esta llena. Limite: {cola_pedidos.max_size}")
            else:
                print("\n--- DATOS DEL NUEVO PEDIDO ---")
                nombre = input("   Nombre del cliente: ")
                try:
                    cantidad = int(input("   Cantidad de producto: "))
                    if cola_pedidos.enqueue(Order(cantidad, nombre)):
                        print("\nPedido guardado exitosamente.")
                except ValueError:
                    print("\nERROR: La cantidad debe ser un numero entero.")

        elif opcion == "2":
            atendido = cola_pedidos.dequeue()
            if atendido:
                print(f"\nDESPACHANDO A: {atendido.customer}")
                print(f"Cantidad retirada: {atendido.qtty}")
            else:
                print("\nNo hay pedidos pendientes para eliminar.")

        elif opcion == "3":
            cola_pedidos.print_info()

        elif opcion == "4":
            print("\nCerrando sistema...")
            break
        else:
            print("\nOpcion invalida. Intente de nuevo.")