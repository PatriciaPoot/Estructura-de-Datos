from lib.MyLinkedList import LinkedList

# Crear instancia de la lista
mi_lista = LinkedList()

# Agregar datos
mi_lista.insert_at_end(10)
mi_lista.insert_at_end(20)
mi_lista.insert_at_start(5)

# Mostrar lista: 5 -> 10 -> 20 -> None
mi_lista.display()

# Eliminar un dato
mi_lista.delete_value(10)
mi_lista.display() # 5 -> 20 -> None