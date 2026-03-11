import tkinter as tk
from tkinter import ttk, messagebox

class Pila:
    def __init__(self):
        self.items = []
    
    def esta_vacia(self):
        return len(self.items) == 0
    
    def apilar(self, item):
        self.items.append(item)
    
    def desapilar(self):
        if not self.esta_vacia():
            return self.items.pop()
        return None
    
    def ver_tope(self):
        if not self.esta_vacia():
            return self.items[-1]
        return None

class CalculadoraNotacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora - Notación Prefija/Posfija")
        self.root.geometry("650x550")
        self.root.resizable(False, False)
        self.root.configure(bg='#2c3e50')
        
        # Estilo
        self.estilo_label = {'bg': '#2c3e50', 'fg': 'white', 'font': ('Arial', 12)}
        self.estilo_entry = {'font': ('Arial', 14), 'bg': '#ecf0f1'}
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Título
        titulo = tk.Label(self.root, text="CALCULADORA DE NOTACION", 
                          font=('Arial', 18, 'bold'), bg='#2c3e50', fg='#3498db')
        titulo.pack(pady=15)
        
        # Frame para entrada
        frame_entrada = tk.Frame(self.root, bg='#2c3e50')
        frame_entrada.pack(pady=10)
        
        tk.Label(frame_entrada, text="Expresion:", **self.estilo_label).pack(side=tk.LEFT, padx=5)
        
        self.entrada = tk.Entry(frame_entrada, width=30, **self.estilo_entry)
        self.entrada.pack(side=tk.LEFT, padx=5)
        self.entrada.bind('<Return>', lambda e: self.evaluar())
        self.entrada.bind('<Button-1>', self.limpiar_para_nueva_operacion)  # Nuevo evento
        
        # Frame para tipo de notación
        frame_tipo = tk.Frame(self.root, bg='#2c3e50')
        frame_tipo.pack(pady=10)
        
        tk.Label(frame_tipo, text="Tipo de notacion:", **self.estilo_label).pack(side=tk.LEFT, padx=5)
        
        self.tipo = ttk.Combobox(frame_tipo, values=["Prefija", "Posfija"], 
                                  state="readonly", font=('Arial', 12), width=15)
        self.tipo.set("Prefija")
        self.tipo.pack(side=tk.LEFT, padx=5)
        self.tipo.bind('<<ComboboxSelected>>', self.limpiar_campos)  # Nuevo evento
        
        # Frame para resultado
        frame_resultado = tk.Frame(self.root, bg='#2c3e50')
        frame_resultado.pack(pady=15)
        
        tk.Label(frame_resultado, text="Resultado:", **self.estilo_label).pack(side=tk.LEFT, padx=5)
        
        self.resultado_var = tk.StringVar()
        self.resultado_var.set("---")
        
        self.resultado_label = tk.Label(frame_resultado, textvariable=self.resultado_var,
                                        font=('Arial', 16, 'bold'), bg='#34495e', 
                                        fg='#2ecc71', width=15, height=2, relief=tk.SUNKEN)
        self.resultado_label.pack(side=tk.LEFT, padx=5)
        
        # Botón calcular
        self.boton_calcular = tk.Button(self.root, text="CALCULAR", command=self.evaluar,
                                         font=('Arial', 14, 'bold'), bg='#3498db', 
                                         fg='white', padx=30, pady=8, cursor='hand2')
        self.boton_calcular.pack(pady=15)
        
        # Frame para ejemplos
        frame_ejemplos = tk.Frame(self.root, bg='#2c3e50')
        frame_ejemplos.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        tk.Label(frame_ejemplos, text="EJEMPLOS", font=('Arial', 12, 'bold'), 
                 bg='#2c3e50', fg='#f1c40f').pack(pady=5)
        
        # Frame para los dos tipos de notación en columnas
        frame_columnas = tk.Frame(frame_ejemplos, bg='#2c3e50')
        frame_columnas.pack(fill=tk.BOTH, expand=True)
        
        # Columna izquierda - Prefija
        frame_prefija = tk.Frame(frame_columnas, bg='#34495e', relief=tk.RIDGE, bd=2)
        frame_prefija.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        tk.Label(frame_prefija, text="PREFIJA", font=('Arial', 11, 'bold'), 
                 bg='#34495e', fg='#3498db').pack(pady=5)
        
        ejemplos_prefija = tk.Frame(frame_prefija, bg='#34495e')
        ejemplos_prefija.pack(pady=5, padx=10, anchor='w')
        
        # Ejemplos prefija (3)
        tk.Label(ejemplos_prefija, text="+ 10 5        = 15", 
                 font=('Courier', 11), bg='#34495e', fg='white', anchor='w').pack(fill='x', pady=2)
        tk.Label(ejemplos_prefija, text="* + 5 3 - 2 1 = 8", 
                 font=('Courier', 11), bg='#34495e', fg='white', anchor='w').pack(fill='x', pady=2)
        tk.Label(ejemplos_prefija, text="+ * 2 3 * 4 5 = 26", 
                 font=('Courier', 11), bg='#34495e', fg='white', anchor='w').pack(fill='x', pady=2)
        
        # Columna derecha - Posfija
        frame_posfija = tk.Frame(frame_columnas, bg='#34495e', relief=tk.RIDGE, bd=2)
        frame_posfija.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        tk.Label(frame_posfija, text="POSFIJA", font=('Arial', 11, 'bold'), 
                 bg='#34495e', fg='#e74c3c').pack(pady=5)
        
        ejemplos_posfija = tk.Frame(frame_posfija, bg='#34495e')
        ejemplos_posfija.pack(pady=5, padx=10, anchor='w')
        
        # Ejemplos posfija (3)
        tk.Label(ejemplos_posfija, text="10 5 +        = 15", 
                 font=('Courier', 11), bg='#34495e', fg='white', anchor='w').pack(fill='x', pady=2)
        tk.Label(ejemplos_posfija, text="5 3 + 2 1 - * = 8", 
                 font=('Courier', 11), bg='#34495e', fg='white', anchor='w').pack(fill='x', pady=2)
        tk.Label(ejemplos_posfija, text="2 3 * 4 5 * + = 26", 
                 font=('Courier', 11), bg='#34495e', fg='white', anchor='w').pack(fill='x', pady=2)
    
    def limpiar_campos(self, event=None):
        """Limpia el campo de entrada y el resultado al cambiar el tipo de notación"""
        self.entrada.delete(0, tk.END)
        self.resultado_var.set("---")
    
    def limpiar_para_nueva_operacion(self, event=None):
        """Limpia el campo de entrada y resultado cuando se hace clic para escribir una nueva operación"""
        if self.resultado_var.get() != "---" or self.entrada.get():
            self.entrada.delete(0, tk.END)
            self.resultado_var.set("---")
    
    def es_numero(self, cadena):
        try:
            float(cadena)
            return True
        except ValueError:
            return False
    
    def evaluar_expresion_prefija(self, expresion):
        elementos = expresion.split()
        pila = Pila()
        
        for elemento in reversed(elementos):
            if self.es_numero(elemento):
                pila.apilar(float(elemento))
            else:
                if pila.esta_vacia():
                    raise ValueError("Expresion invalida: faltan operandos")
                
                op1 = pila.desapilar()
                
                if pila.esta_vacia():
                    raise ValueError("Expresion invalida: faltan operandos")
                    
                op2 = pila.desapilar()
                
                if elemento == '+':
                    pila.apilar(op1 + op2)
                elif elemento == '-':
                    pila.apilar(op1 - op2)
                elif elemento == '*':
                    pila.apilar(op1 * op2)
                elif elemento == '/':
                    if op2 == 0:
                        raise ValueError("Error: Division entre cero")
                    pila.apilar(op1 / op2)
                else:
                    raise ValueError(f"Operador no valido: {elemento}")
        
        if pila.esta_vacia():
            raise ValueError("Expresion invalida: resultado vacio")
        
        resultado = pila.desapilar()
        if not pila.esta_vacia():
            raise ValueError("Expresion invalida: sobran operandos")
        
        return resultado
    
    def evaluar_expresion_posfija(self, expresion):
        elementos = expresion.split()
        pila = Pila()
        
        for elemento in elementos:
            if self.es_numero(elemento):
                pila.apilar(float(elemento))
            else:
                if pila.esta_vacia():
                    raise ValueError("Expresion invalida: faltan operandos")
                
                op2 = pila.desapilar()
                
                if pila.esta_vacia():
                    raise ValueError("Expresion invalida: faltan operandos")
                    
                op1 = pila.desapilar()
                
                if elemento == '+':
                    pila.apilar(op1 + op2)
                elif elemento == '-':
                    pila.apilar(op1 - op2)
                elif elemento == '*':
                    pila.apilar(op1 * op2)
                elif elemento == '/':
                    if op2 == 0:
                        raise ValueError("Error: Division entre cero")
                    pila.apilar(op1 / op2)
                else:
                    raise ValueError(f"Operador no valido: {elemento}")
        
        if pila.esta_vacia():
            raise ValueError("Expresion invalida: resultado vacio")
        
        resultado = pila.desapilar()
        if not pila.esta_vacia():
            raise ValueError("Expresion invalida: sobran operandos")
        
        return resultado
    
    def evaluar(self):
        expresion = self.entrada.get().strip()
        if not expresion:
            messagebox.showwarning("Advertencia", "Por favor ingresa una expresion")
            return
        
        try:
            if self.tipo.get() == "Prefija":
                resultado = self.evaluar_expresion_prefija(expresion)
            else:
                resultado = self.evaluar_expresion_posfija(expresion)
            
            self.resultado_var.set(f"{resultado:.2f}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.resultado_var.set("Error")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
            self.resultado_var.set("Error")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraNotacion(root)
    root.mainloop()
