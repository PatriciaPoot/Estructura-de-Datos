import tkinter as tk
from tkinter import messagebox
import time
import threading

class Pila:
    def __init__(self, nombre):
        self.items = []
        self.nombre = nombre
    
    def esta_vacia(self):
        return len(self.items) == 0
    
    def apilar(self, item):
        if not self.esta_vacia() and item > self.ver_tope():
            return False
        self.items.append(item)
        return True
    
    def desapilar(self):
        if not self.esta_vacia():
            return self.items.pop()
        return None
    
    def ver_tope(self):
        if not self.esta_vacia():
            return self.items[-1]
        return float('inf')

class TorresHanoiCompleto:
    def __init__(self, root):
        self.root = root
        self.root.title("Torres de Hanoi - 3 Discos")
        self.root.geometry("750x600")
        self.root.resizable(False, False)
        self.root.configure(bg='#1a2634')
        
        # Variables del juego
        self.num_discos = 3
        self.torres = {
            'A': Pila('A'),
            'B': Pila('B'),
            'C': Pila('C')
        }
        self.torre_seleccionada = None
        self.disco_seleccionado = None
        self.movimientos = 0
        self.modo_actual = "manual"
        self.animando = False
        self.animacion_detener = False
        
        # Posiciones en el canvas
        self.base_x = 190
        self.base_y = 280
        self.alto_torre = 150
        self.alto_disco = 28
        self.separacion_torres = 175
        
        self.crear_interfaz()
        self.inicializar_juego()
    
    def crear_interfaz(self):
        # Título
        titulo = tk.Label(self.root, text="TORRES DE HANOI - 3 DISCOS", 
                          font=('Arial', 16, 'bold'), bg='#1a2634', fg='#e8eef2')
        titulo.pack(pady=5)
        
        # Canvas con AZUL MUY SUAVE (intermedio)
        self.canvas = tk.Canvas(self.root, width=700, height=350, bg='#f2f6fc',
                                highlightbackground='#3a4a5a', highlightthickness=2)
        self.canvas.pack(pady=2)
        self.canvas.bind("<Button-1>", self.clic_en_canvas)
        
        # Frame para selector de modo
        frame_modo = tk.Frame(self.root, bg='#1a2634')
        frame_modo.pack(pady=2)
        
        tk.Label(frame_modo, text="MODO DE JUEGO:", font=('Arial', 11, 'bold'),
                 bg='#1a2634', fg='#c0d0e0').pack(side=tk.LEFT, padx=10)
        
        self.modo_var = tk.StringVar(value="manual")
        
        self.radio_manual = tk.Radiobutton(frame_modo, text="✋ MANUAL", variable=self.modo_var,
                                           value="manual", command=self.cambiar_modo,
                                           font=('Arial', 11), bg='#1a2634', fg='#a1c9d7',
                                           selectcolor='#1a2634', activebackground='#1a2634')
        self.radio_manual.pack(side=tk.LEFT, padx=10)
        
        self.radio_auto = tk.Radiobutton(frame_modo, text="🤖 AUTOMÁTICO", variable=self.modo_var,
                                         value="auto", command=self.cambiar_modo,
                                         font=('Arial', 11), bg='#1a2634', fg='#e8c1c7',
                                         selectcolor='#1a2634', activebackground='#1a2634')
        self.radio_auto.pack(side=tk.LEFT, padx=10)
        
        # Frame de botones de acción
        frame_accion = tk.Frame(self.root, bg='#1a2634')
        frame_accion.pack(pady=3)
        
        # Botones
        self.boton_reiniciar = tk.Button(frame_accion, text="🔄 REINICIAR JUEGO", 
                                          command=self.reiniciar_juego,
                                          font=('Arial', 11, 'bold'), bg='#e8c1c7',
                                          fg='#1a2634', padx=12, pady=4, cursor='hand2',
                                          activebackground='#d9b1b7')
        self.boton_reiniciar.pack(side=tk.LEFT, padx=5)
        
        self.boton_iniciar_auto = tk.Button(frame_accion, text="▶️ INICIAR AUTOMÁTICO", 
                                            command=self.iniciar_automatico,
                                            font=('Arial', 11, 'bold'), bg='#b5d6d6',
                                            fg='#1a2634', padx=12, pady=4, cursor='hand2',
                                            activebackground='#a4c5c5')
        self.boton_iniciar_auto.pack(side=tk.LEFT, padx=5)
        
        self.boton_detener = tk.Button(frame_accion, text="⏹️ DETENER", 
                                       command=self.detener_animacion,
                                       font=('Arial', 11, 'bold'), bg='#f5d0b8',
                                       fg='#1a2634', padx=12, pady=4, cursor='hand2',
                                       activebackground='#e5c0a8')
        self.boton_detener.pack_forget()
        
        # Frame de información
        frame_info_superior = tk.Frame(self.root, bg='#1a2634')
        frame_info_superior.pack(pady=1)
        
        # Contador de movimientos
        self.movimientos_var = tk.StringVar()
        self.movimientos_var.set("Movimientos: 0")
        
        self.movimientos_label = tk.Label(frame_info_superior, textvariable=self.movimientos_var,
                                          font=('Arial', 14, 'bold'), bg='#1a2634', fg='#f5e5b3')
        self.movimientos_label.pack()
        
        # Frame para el estado
        frame_estado = tk.Frame(self.root, bg='#1a2634')
        frame_estado.pack(pady=1)
        
        # Estado del juego
        self.estado_var = tk.StringVar()
        self.estado_var.set("✋ MODO MANUAL - Haz clic en un disco para comenzar")
        
        self.estado_label = tk.Label(frame_estado, textvariable=self.estado_var,
                                      font=('Arial', 11), bg='#1a2634', fg='#b5d6d6',
                                      width=60, anchor='center')
        self.estado_label.pack()
        
        # Frame de instrucciones
        self.frame_instrucciones = tk.Frame(self.root, bg='#1a2634')
        self.frame_instrucciones.pack(pady=5)
        
        self.instrucciones_text = tk.Text(self.frame_instrucciones, height=5, width=75,
                                          font=('Arial', 9), bg='#2a3645', fg='#c0d0e0',
                                          wrap=tk.WORD, state=tk.DISABLED)
        self.instrucciones_text.pack()
        
        self.actualizar_instrucciones()
    
    def actualizar_instrucciones(self):
        self.instrucciones_text.config(state=tk.NORMAL)
        self.instrucciones_text.delete(1.0, tk.END)
        
        if self.modo_actual == "manual":
            instrucciones = """✋ MODO MANUAL:
1. Haz clic en un disco para seleccionarlo (se pondrá amarillo pastel)
2. Haz clic en otra torre para mover el disco seleccionado
3. No puedes colocar un disco grande sobre uno pequeño"""
        else:
            instrucciones = """🤖 MODO AUTOMÁTICO:
1. Presiona 'INICIAR AUTOMÁTICO' para ver la solución
2. El programa resolverá el juego en 7 movimientos
3. Puedes detener la animación en cualquier momento"""
        
        self.instrucciones_text.insert(1.0, instrucciones)
        self.instrucciones_text.config(state=tk.DISABLED)
    
    def cambiar_modo(self):
        self.modo_actual = self.modo_var.get()
        self.actualizar_instrucciones()
        
        if self.modo_actual == "manual":
            self.estado_var.set("✋ MODO MANUAL - Haz clic en un disco para comenzar")
            self.boton_iniciar_auto.pack(side=tk.LEFT, padx=5)
            self.boton_detener.pack_forget()
        else:
            self.estado_var.set("🤖 MODO AUTOMÁTICO - Presiona 'INICIAR AUTOMÁTICO' para comenzar")
            self.boton_iniciar_auto.pack(side=tk.LEFT, padx=5)
            self.boton_detener.pack_forget()
        
        self.reiniciar_juego()
    
    def inicializar_juego(self):
        for torre in self.torres.values():
            torre.items.clear()
        
        for i in range(self.num_discos, 0, -1):
            self.torres['A'].apilar(i)
        
        self.torre_seleccionada = None
        self.disco_seleccionado = None
        self.movimientos = 0
        self.movimientos_var.set("Movimientos: 0")
        self.dibujar_torres()
    
    def dibujar_torres(self):
        self.canvas.delete("all")
        
        # Dibujar base
        self.canvas.create_rectangle(40, self.base_y, 660, self.base_y + 18, 
                                      fill='#d9c8b4', outline='#b8a38f', width=2)
        
        # Dibujar torres
        for i, letra in enumerate(['A', 'B', 'C']):
            x = self.base_x + i * self.separacion_torres
            
            # Base de la torre
            self.canvas.create_rectangle(x - 35, self.base_y + 3, x + 35, self.base_y + 13,
                                          fill='#e5d5c0', outline='#b8a38f')
            
            # Poste
            self.canvas.create_rectangle(x - 4, self.base_y - self.alto_torre, 
                                         x + 4, self.base_y, 
                                         fill='#c0b3a3', outline='#9b8b7a', width=2)
            
            # Etiqueta de la torre
            self.canvas.create_text(x, self.base_y + 35, text=letra, 
                                     font=('Arial', 14, 'bold'), fill='#9b8b7a')
        
        # Dibujar discos
        for i, letra in enumerate(['A', 'B', 'C']):
            x = self.base_x + i * self.separacion_torres
            discos_torre = self.torres[letra].items
            
            for j, disco in enumerate(discos_torre):
                ancho = 45 + (disco * 18)
                y = self.base_y - (j + 1) * self.alto_disco
                
                if (self.modo_actual == "manual" and 
                    self.torre_seleccionada == letra and 
                    self.disco_seleccionado == disco and 
                    j == len(discos_torre)-1):
                    color = '#faf0c7'
                    borde = '#e5d5a0'
                else:
                    colores_pastel = ['#c7e0e8', '#fad5d0', '#e3d2f0']
                    color = colores_pastel[disco - 1]
                    borde = '#d4c2b0'
                
                self.canvas.create_rectangle(x - ancho//2, y - self.alto_disco + 5,
                                             x + ancho//2, y,
                                             fill=color, outline=borde, width=2)
                
                self.canvas.create_text(x, y - self.alto_disco//2 + 2,
                                         text=str(disco), font=('Arial', 10, 'bold'),
                                         fill='#2c3e50')
    
    def clic_en_canvas(self, event):
        if self.modo_actual != "manual" or self.animando:
            return
        
        x, y = event.x, event.y
        
        torre_clic = None
        for i, letra in enumerate(['A', 'B', 'C']):
            torre_x = self.base_x + i * self.separacion_torres
            if abs(x - torre_x) < 50:
                torre_clic = letra
                break
        
        if not torre_clic:
            return
        
        if self.torre_seleccionada is None:
            self.seleccionar_disco(torre_clic)
        else:
            self.mover_disco_seleccionado(torre_clic)
    
    def seleccionar_disco(self, torre):
        if not self.torres[torre].esta_vacia():
            self.torre_seleccionada = torre
            self.disco_seleccionado = self.torres[torre].ver_tope()
            self.estado_var.set(f"✨ Disco {self.disco_seleccionado} seleccionado - Haz clic en torre destino")
            self.dibujar_torres()
    
    def mover_disco_seleccionado(self, torre_destino):
        if torre_destino == self.torre_seleccionada:
            self.torre_seleccionada = None
            self.disco_seleccionado = None
            self.estado_var.set("✋ Selección cancelada - Elige un disco")
            self.dibujar_torres()
            return
        
        disco = self.torres[self.torre_seleccionada].desapilar()
        
        if self.torres[torre_destino].apilar(disco):
            self.movimientos += 1
            self.movimientos_var.set(f"Movimientos: {self.movimientos}")
            self.estado_var.set(f"✅ Disco movido de {self.torre_seleccionada} a {torre_destino}")
            
            if len(self.torres['C'].items) == 3:
                messagebox.showinfo("¡Felicidades!", f"¡Has ganado!\nTotal de movimientos: {self.movimientos}")
                self.estado_var.set("🎉 ¡JUEGO COMPLETADO!")
        else:
            self.torres[self.torre_seleccionada].apilar(disco)
            self.estado_var.set("❌ Movimiento inválido - No puedes poner un disco grande sobre uno pequeño")
        
        self.torre_seleccionada = None
        self.disco_seleccionado = None
        self.dibujar_torres()
    
    def reiniciar_juego(self):
        self.animando = False
        self.animacion_detener = True
        self.inicializar_juego()
        self.estado_var.set("✋ Juego reiniciado")
        
        if self.modo_actual == "auto":
            self.boton_detener.pack_forget()
            self.boton_iniciar_auto.pack(side=tk.LEFT, padx=5)
    
    def iniciar_automatico(self):
        if self.modo_actual != "auto":
            return
        
        self.reiniciar_juego()
        self.animando = True
        self.animacion_detener = False
        
        self.boton_iniciar_auto.pack_forget()
        self.boton_detener.pack(side=tk.LEFT, padx=5)
        self.estado_var.set("🤖 Resolviendo automáticamente...")
        
        thread = threading.Thread(target=self.resolver_automatico)
        thread.daemon = True
        thread.start()
    
    def detener_animacion(self):
        self.animacion_detener = True
        self.estado_var.set("⏸️ Animación detenida")
        
        self.boton_detener.pack_forget()
        self.boton_iniciar_auto.pack(side=tk.LEFT, padx=5)
    
    def resolver_automatico(self):
        def hanoi(n, origen, destino, auxiliar):
            if self.animacion_detener:
                return
            if n == 1:
                self.root.after(0, lambda: self.mover_disco_auto(origen, destino))
                time.sleep(0.8)
            else:
                hanoi(n-1, origen, auxiliar, destino)
                if self.animacion_detener:
                    return
                self.root.after(0, lambda: self.mover_disco_auto(origen, destino))
                time.sleep(0.8)
                hanoi(n-1, auxiliar, destino, origen)
        
        hanoi(3, 'A', 'C', 'B')
        
        if not self.animacion_detener:
            self.root.after(0, self.automatico_completado)
    
    def mover_disco_auto(self, origen, destino):
        if self.animacion_detener:
            return
        
        disco = self.torres[origen].desapilar()
        self.torres[destino].apilar(disco)
        self.movimientos += 1
        self.movimientos_var.set(f"Movimientos: {self.movimientos}")
        self.dibujar_torres()
    
    def automatico_completado(self):
        self.animando = False
        self.estado_var.set("🎉 ¡Resolución automática completada!")
        messagebox.showinfo("Completado", f"¡Torres de Hanoi resuelto!\nTotal de movimientos: {self.movimientos}")
        
        self.boton_detener.pack_forget()
        self.boton_iniciar_auto.pack(side=tk.LEFT, padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = TorresHanoiCompleto(root)
    root.mainloop()
