- Matriz: Al ejecutar este programa con datos muy grandes, el código no corre correctamente porque consume demasiada memoria de la computadora. Y si, si llega a ejecutarse, a primera vista la salida deja de verse como una tabla y aparece solo como una lista de números desordenados, lo que dificulta su lectura.

- Departamento: Este programa tiene como propósito insertar, consultar y eliminar algún elemento en particular de las ventas de tres departamentos (Ropa, Deportes y Juguetería) durante los doce meses del año, y para ello se necesitó de 5 métodos:
     - "mostrar_tabla()" muestra todas las ventas en forma de tabla en la que se observan los meses y los montos de cada departamento.
     - "modificar_venta()" permite cambiar una venta; el usuario indica el mes y el departamento, y el programa actualiza el monto correspondiente.
     - "buscar_mes_departamento()" sirve para consultar una venta en específico, en donde al usuario se le pide el mes y el departamento, y luego el programa le muestra el valor guardado.
     - "eliminar_venta()" pone en 0 una venta después de que el usuario confirma su la eliminacion.
     - "menu()" muestra las opciones y ejecuta cada función según lo que el usuario elija.

- Programa Recursivo -> Fibonacci: Este programa implementa dos enfoques para calcular la secuencia de Fibonacci:
     - Ventajas del Enfoque Iterativo:
        - Más eficiente: Utiliza un solo bucle, complejidad O(n)
	    -  Menor uso de memoria: No crea nuevas llamadas en la pila de ejecución
		-  Más rápido: Especialmente para valores grandes de n
		-  Evita el desbordamiento de pila: No hay límite de recursión
		-  Predecible: El tiempo de ejecución crece linealmente
	 - Ventajas del Enfoque Recursivo:
		-  Código más limpio y elegante: Refleja directamente la definición matemática
		-  Más fácil de entender: Sigue la lógica natural de la secuencia
		-  Ideal para problemas divisibles: Útil cuando un problema puede dividirse en subproblemas similares
		-  Menos líneas de código: Solución más concisa
		-  Demuestra el concepto de recursividad: Excelente para aprendizaje y comprensión
		
