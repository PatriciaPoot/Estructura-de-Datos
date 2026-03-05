import tkinter as tk
from tkinter import simpledialog, messagebox

class PilaGrafica:

    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Pila")
        self.root.configure(bg="black")

        self.stack = []
        self.max_size = 6

        self.canvas = tk.Canvas(root, width=260, height=420, bg="black", highlightthickness=0)
        self.canvas.pack(pady=15)

        self.info = tk.Label(root, text="", fg="white", bg="black", font=("Arial", 12, "bold"))
        self.info.pack()

        frame = tk.Frame(root, bg="black")
        frame.pack(pady=10)

        tk.Button(frame, text="Agregar", command=self.push, bg="#CDB4DB", width=12).grid(row=0,column=0,padx=6)
        tk.Button(frame, text="Eliminar", command=self.pop, bg="#FFC8DD", width=12).grid(row=0,column=1,padx=6)
        tk.Button(frame, text="Eliminar disco", command=self.eliminar_disco, bg="#BDE0FE", width=14).grid(row=0,column=2,padx=6)
        tk.Button(frame, text="Vaciar pila", command=self.vaciar_pila, bg="#A0E7E5", width=12).grid(row=0,column=3,padx=6)

        self.dibujar()

    def dibujar(self):

        self.canvas.delete("all")
        y = 360

        colores = [
            "#FFB3BA",
            "#BAE1FF",
            "#BAFFC9",
            "#FFFFBA",
            "#E0BBE4",
            "#FFD6A5"
        ]

        for i, item in enumerate(self.stack):

            color = colores[i % len(colores)]

            self.canvas.create_rectangle(
                80, y-40, 180, y,
                fill=color,
                outline="white",
                width=2
            )

            self.canvas.create_text(
                130, y-20,
                text=str(item),
                fill="black",
                font=("Arial", 12, "bold")
            )

            y -= 45

        if self.stack:
            self.canvas.create_text(
                130, y+15,
                text="TOP",
                fill="white",
                font=("Arial", 11, "bold")
            )

        self.actualizar_info()

    def actualizar_info(self):

        cantidad = len(self.stack)

        if cantidad == 0:
            estado = "VACÍA"
            cima = "Ninguno"
        else:
            estado = "LLENA" if cantidad == self.max_size else "NO llena"
            cima = self.stack[-1]

        texto = f"Elementos: {cantidad} | Cima: {cima} | Estado: {estado}"
        self.info.config(text=texto)

    def push(self):

        if len(self.stack) >= self.max_size:
            messagebox.showwarning("Pila llena", "La pila está llena")
            return

        valor = simpledialog.askstring("Entrada", "Ingresa el valor del disco:")

        if valor:
            self.stack.append(valor)
            self.dibujar()

    def pop(self):

        if not self.stack:
            messagebox.showwarning("Pila vacía", "La pila está vacía")
            return

        self.stack.pop()
        self.dibujar()

    def eliminar_disco(self):

        if not self.stack:
            messagebox.showwarning("Pila vacía", "No hay discos en la pila")
            return

        objetivo = simpledialog.askstring("Eliminar disco", "¿Qué disco quieres eliminar?")

        if objetivo not in self.stack:
            messagebox.showinfo("No encontrado", "Ese disco no está en la pila")
            return

        discos_removidos = 0

        while self.stack and self.stack[-1] != objetivo:
            self.stack.pop()
            discos_removidos += 1

        if self.stack and self.stack[-1] == objetivo:
            self.stack.pop()
            discos_removidos += 1

        self.dibujar()

        messagebox.showinfo(
            "Proceso terminado",
            f"Disco eliminado: {objetivo}\n"
            f"Discos removidos: {discos_removidos}"
        )

    def vaciar_pila(self):

        if not self.stack:
            messagebox.showinfo("Pila", "La pila ya está vacía")
            return

        self.stack.clear()
        self.dibujar()
        messagebox.showinfo("Pila vaciada", "Todos los discos fueron eliminados")


root = tk.Tk()
app = PilaGrafica(root)

root.mainloop()
