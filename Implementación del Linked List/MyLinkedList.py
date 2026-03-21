class Node:
    """Clase que representa un elemento individual en la lista."""
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    """Clase principal para la gestión de la lista enlazada."""
    def __init__(self):
        self.head = None

    def insert_at_end(self, data):
        """Inserta un nuevo elemento al final de la lista."""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def insert_at_start(self, data):
        """Inserta un nuevo elemento al principio de la lista."""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete_value(self, value):
        """Elimina la primera ocurrencia de un valor específico."""
        if not self.head:
            return

        if self.head.data == value:
            self.head = self.head.next
            return

        current = self.head
        while current.next:
            if current.next.data == value:
                current.next = current.next.next
                return
            current = current.next

    def display(self):
        """Muestra los elementos de la lista en un formato visual."""
        elements = []
        current = self.head
        while current:
            elements.append(str(current.data))
            current = current.next
        print(" -> ".join(elements) + " -> None")

    def search(self, value):
        """Busca si un valor existe en la lista."""
        current = self.head
        while current:
            if current.data == value:
                return True
            current = current.next
        return False

if __name__ == "__main__":
    lista_test = LinkedList()
    lista_test.insert_at_end("Nodo A")
    lista_test.insert_at_end("Nodo B")
    print("Prueba de librería interna:")
    lista_test.display()
