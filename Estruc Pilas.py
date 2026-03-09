import tkinter as tk
from tkinter import simpledialog, messagebox

class SimuladorPilas:

    def __init__(self, root):

        self.root = root
        self.root.title("Simulador de Pila")
        self.root.configure(bg="black")

        self.stack = []
        self.aux = []
        self.max_size = 8

        frame = tk.Frame(root,bg="black")
        frame.pack()

        self.canvas1 = tk.Canvas(frame,width=200,height=420,bg="black",highlightthickness=0)
        self.canvas1.grid(row=0,column=0,padx=30)

        self.canvas2 = tk.Canvas(frame,width=200,height=420,bg="black",highlightthickness=0)
        self.canvas2.grid(row=0,column=1,padx=30)

        self.info = tk.Label(root,text="",fg="white",bg="black",font=("Arial",12,"bold"))
        self.info.pack(pady=10)

        botones = tk.Frame(root,bg="black")
        botones.pack()

        tk.Button(botones,text="Ejecutar ejercicio",command=self.ejercicio,bg="#CDB4DB",width=18).grid(row=0,column=0,padx=6)
        tk.Button(botones,text="Eliminar valor",command=self.eliminar_valor,bg="#BDE0FE",width=18).grid(row=0,column=1,padx=6)

        self.dibujar()

    def dibujar(self):

        self.canvas1.delete("all")
        self.canvas2.delete("all")

        self.canvas1.create_text(100,20,text="PILA",fill="white",font=("Arial",14,"bold"))
        self.canvas2.create_text(100,20,text="AUX",fill="white",font=("Arial",14,"bold"))

        y = 380

        colores = [
            "#FFB3BA","#BAE1FF","#BAFFC9","#FFFFBA",
            "#E0BBE4","#FFD6A5","#B5EAD7","#C7CEEA"
        ]

        for i,item in enumerate(self.stack):

            color = colores[i%len(colores)]

            self.canvas1.create_rectangle(60,y-40,140,y,fill=color,outline="white",width=2)
            self.canvas1.create_text(100,y-20,text=item,font=("Arial",12,"bold"))

            y -= 45

        if self.stack:
            self.canvas1.create_text(100,y+15,text="TOP",fill="white",font=("Arial",10,"bold"))

        y = 380

        for i,item in enumerate(self.aux):

            color = colores[i%len(colores)]

            self.canvas2.create_rectangle(60,y-40,140,y,fill=color,outline="white",width=2)
            self.canvas2.create_text(100,y-20,text=item,font=("Arial",12,"bold"))

            y -= 45

        if self.aux:
            self.canvas2.create_text(100,y+15,text="TOP",fill="white",font=("Arial",10,"bold"))

        self.info.config(text=f"Pila: {self.stack} | Aux: {self.aux}")

    def push(self,valor):

        if len(self.stack) >= self.max_size:
            messagebox.showwarning("Overflow","Pila llena")
            return

        self.stack.append(valor)
        self.dibujar()

    def ejercicio(self):

        self.stack.clear()
        self.aux.clear()
        self.dibujar()

        operaciones = [
            ("push","X"),
            ("push","Y"),
            ("pop","Z"),
            ("pop","T"),
            ("pop","U"),
            ("push","V"),
            ("push","W"),
            ("pop","P"),
            ("push","R")
        ]

        self.ejecutar_ops(operaciones,0)

    def ejecutar_ops(self,ops,i):

        if i >= len(ops):
            messagebox.showinfo("Ejercicio terminado","Ahora puedes eliminar cualquier elemento")
            return

        op,valor = ops[i]

        if op == "push":

            self.push(valor)
            self.root.after(1000,lambda:self.ejecutar_ops(ops,i+1))

        elif op == "pop":

            if len(self.stack) < self.max_size:

                # agregar Z,T,U,P
                self.stack.append(valor)
                self.dibujar()

                # luego eliminarlo
                self.root.after(800,lambda:self.eliminar_temp(ops,i))

            else:
                messagebox.showwarning("Overflow","No se puede agregar")
                self.root.after(1000,lambda:self.ejecutar_ops(ops,i+1))

    def eliminar_temp(self,ops,i):

        if self.stack:
            self.stack.pop()
            self.dibujar()

        self.root.after(800,lambda:self.ejecutar_ops(ops,i+1))

    def eliminar_valor(self):

        if not self.stack:
            messagebox.showwarning("Pila vacía","No hay elementos")
            return

        objetivo = simpledialog.askstring("Eliminar","¿Qué valor eliminar?")

        if objetivo not in self.stack:
            messagebox.showinfo("No encontrado","Ese valor no está en la pila")
            return

        self.eliminar_animacion(objetivo)

    def eliminar_animacion(self,objetivo):

        if self.stack and self.stack[-1] != objetivo:

            self.aux.append(self.stack.pop())
            self.dibujar()

            self.root.after(700,lambda:self.eliminar_animacion(objetivo))

        elif self.stack and self.stack[-1] == objetivo:

            self.stack.pop()
            self.dibujar()

            self.root.after(700,self.regresar_aux)

    def regresar_aux(self):

        if self.aux:

            self.stack.append(self.aux.pop())
            self.dibujar()

            self.root.after(700,self.regresar_aux)


root = tk.Tk()
app = SimuladorPilas(root)

root.mainloop()