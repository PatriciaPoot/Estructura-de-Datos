import tkinter as tk
from tkinter import simpledialog, messagebox
import math

class Grafo:
    def __init__(self, dirigido=False):
        self.dirigido = dirigido
        self.vertices = {}
        self.aristas = []

    def numVertices(self): return len(self.vertices)
    def numAristas(self): return len(self.aristas)
    def vertices_lista(self): return list(self.vertices.keys())
    def aristas_lista(self): return self.aristas

    def grado(self, v):
        return sum(1 for a in self.aristas if v in a)

    def verticesAdyacentes(self, v):
        return [d for o, d in self.aristas if o == v] + \
               ([o for o, d in self.aristas if d == v] if not self.dirigido else [])

    def aristasIncidentes(self, v):
        return [a for a in self.aristas if v in a]

    def opuesto(self, v, e):
        return e[1] if e[0] == v else e[0]

    def verticesFinales(self, e):
        return e

    def esAdyacente(self, v, w):
        return (v, w) in self.aristas or (not self.dirigido and (w, v) in self.aristas)

    def gradoEntrada(self, v):
        return sum(1 for o, d in self.aristas if d == v)

    def gradoSalida(self, v):
        return sum(1 for o, d in self.aristas if o == v)

    def aristasIncidentesEnt(self, v):
        return [a for a in self.aristas if a[1] == v]

    def aristasIncidentesSal(self, v):
        return [a for a in self.aristas if a[0] == v]

    def verticesAdyacentesEnt(self, v):
        return [o for o, d in self.aristas if d == v]

    def verticesAdyacentesSal(self, v):
        return [d for o, d in self.aristas if o == v]

    def origen(self, e): return e[0]
    def destino(self, e): return e[1]

    def invierteDireccion(self, e):
        if e in self.aristas:
            self.aristas.remove(e)
            self.aristas.append((e[1], e[0]))

    def insertarVertice(self, v, x, y):
        self.vertices[v] = (x, y)

    def insertarArista(self, o, d):
        self.aristas.append((o, d))

    def eliminarVertice(self, v):
        if v in self.vertices:
            del self.vertices[v]
            self.aristas = [a for a in self.aristas if v not in a]

    def eliminarArista(self, o, d):
        if (o, d) in self.aristas:
            self.aristas.remove((o, d))


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Grafo PRO FINAL")

        dirigido = messagebox.askyesno("Tipo", "¿Grafo dirigido?")
        self.grafo = Grafo(dirigido)

        self.canvas = tk.Canvas(root, width=900, height=500, bg="white")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.release)

        self.sel = None
        self.menu()

    def menu(self):
        m = tk.Menu(self.root)

        gen = tk.Menu(m, tearoff=0)
        gen.add_command(label="numVertices", command=lambda: self.mostrar(self.grafo.numVertices()))
        gen.add_command(label="numAristas", command=lambda: self.mostrar(self.grafo.numAristas()))
        gen.add_command(label="vertices", command=lambda: self.mostrar(self.grafo.vertices_lista()))
        gen.add_command(label="aristas", command=lambda: self.mostrar(self.grafo.aristas_lista()))
        gen.add_command(label="grado(v)", command=self.grado)
        gen.add_command(label="adyacentes(v)", command=self.ady)
        gen.add_command(label="incidentes(v)", command=self.inc)
        gen.add_command(label="opuesto(v,e)", command=self.opuesto)
        gen.add_command(label="finales(e)", command=self.finales)
        m.add_cascade(label="Generales", menu=gen)

        dirg = tk.Menu(m, tearoff=0)
        dirg.add_command(label="entrada(v)", command=self.ent)
        dirg.add_command(label="salida(v)", command=self.sal)
        dirg.add_command(label="invertir arista", command=self.invertir)
        m.add_cascade(label="Dirigidas", menu=dirg)

        act = tk.Menu(m, tearoff=0)
        act.add_command(label="Agregar arista", command=self.addA)
        act.add_command(label="Eliminar vértice", command=self.delV)
        act.add_command(label="Eliminar arista", command=self.delA)
        m.add_cascade(label="Actualizar", menu=act)

        self.root.config(menu=m)

    # -------- INTERACCIÓN --------
    def click(self, e):
        for v,(x,y) in self.grafo.vertices.items():
            if (x-e.x)**2+(y-e.y)**2<225:
                self.sel=v
                return
        n=simpledialog.askstring("Vertice","Nombre")
        if n:
            self.grafo.insertarVertice(n,e.x,e.y)
            self.draw()

    def drag(self,e):
        if self.sel:
            self.grafo.vertices[self.sel]=(e.x,e.y)
            self.draw()

    def release(self,e):
        self.sel=None

    # -------- FUNCIONES --------
    def mostrar(self,x):
        messagebox.showinfo("Resultado",x)

    def grado(self):
        v=simpledialog.askstring("v","v")
        self.mostrar(self.grafo.grado(v))

    def ady(self):
        v=simpledialog.askstring("v","v")
        self.mostrar(self.grafo.verticesAdyacentes(v))

    def inc(self):
        v=simpledialog.askstring("v","v")
        self.mostrar(self.grafo.aristasIncidentes(v))

    def opuesto(self):
        v=simpledialog.askstring("v","v")
        e=eval(simpledialog.askstring("e","(a,b)"))
        self.mostrar(self.grafo.opuesto(v,e))

    def finales(self):
        e=eval(simpledialog.askstring("e","(a,b)"))
        self.mostrar(self.grafo.verticesFinales(e))

    def ent(self):
        v=simpledialog.askstring("v","v")
        self.mostrar(self.grafo.gradoEntrada(v))

    def sal(self):
        v=simpledialog.askstring("v","v")
        self.mostrar(self.grafo.gradoSalida(v))

    def invertir(self):
        e=eval(simpledialog.askstring("e","(a,b)"))
        self.grafo.invierteDireccion(e)
        self.draw()

    def addA(self):
        o=simpledialog.askstring("o","o")
        d=simpledialog.askstring("d","d")
        if o in self.grafo.vertices and d in self.grafo.vertices:
            self.grafo.insertarArista(o,d)
            self.draw()

    def delV(self):
        v=simpledialog.askstring("v","v")
        self.grafo.eliminarVertice(v)
        self.draw()

    def delA(self):
        o=simpledialog.askstring("o","o")
        d=simpledialog.askstring("d","d")
        self.grafo.eliminarArista(o,d)
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        radio = 15

        for o,d in self.grafo.aristas:
            x1,y1=self.grafo.vertices[o]
            x2,y2=self.grafo.vertices[d]

            dx = x2 - x1
            dy = y2 - y1
            dist = (dx**2 + dy**2)**0.5

            if dist == 0:
                continue

            x_inicio = x1 + (dx/dist)*radio
            y_inicio = y1 + (dy/dist)*radio

            x_fin = x2 - (dx/dist)*radio
            y_fin = y2 - (dy/dist)*radio

            self.canvas.create_line(x_inicio, y_inicio, x_fin, y_fin, width=2)

            if self.grafo.dirigido:
                angle = math.atan2(y_fin - y_inicio, x_fin - x_inicio)

                length = 12
                offset = 0.5

                x3 = x_fin - length * math.cos(angle - offset)
                y3 = y_fin - length * math.sin(angle - offset)

                x4 = x_fin - length * math.cos(angle + offset)
                y4 = y_fin - length * math.sin(angle + offset)

                self.canvas.create_polygon(x_fin,y_fin,x3,y3,x4,y4, fill="black")

        for v,(x,y) in self.grafo.vertices.items():
            self.canvas.create_oval(x-radio,y-radio,x+radio,y+radio,fill="lightblue")
            self.canvas.create_text(x,y,text=v)


root = tk.Tk()
App(root)
root.mainloop()
