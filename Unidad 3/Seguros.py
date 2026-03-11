import os
import time

class Cola:
    def __init__(self):
        self.items = []
    
    def encolar(self, item):
        self.items.append(item)
    
    def desencolar(self):
        if self.esta_vacia():
            return None
        return self.items.pop(0)
    
    def esta_vacia(self):
        return len(self.items) == 0
    
    def tamano(self):
        return len(self.items)
    
    def ver_primero(self):
        if self.esta_vacia():
            return None
        return self.items[0]

class SistemaSeguros:
    def __init__(self):
        self.colas = {}
        self.contadores = {}
        
    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_encabezado(self):
        print("=" * 70)
        print("            SISTEMA DE COLAS - COMPANIA DE SEGUROS")
        print("=" * 70)
    
    def mostrar_estado(self):
        print("\nESTADO ACTUAL DE COLAS:")
        print("-" * 40)
        
        if not self.colas:
            print("  (Sin colas activas)")
        else:
            for servicio in sorted(self.colas.keys()):
                cola = self.colas[servicio]
                tam = cola.tamano()
                if tam > 0:
                    print(f"  Servicio {servicio}: [{tam} cliente(s)] - Siguiente: {cola.ver_primero()}")
                else:
                    print(f"  Servicio {servicio}: [Vacia]")
        print("-" * 40)
    
    def procesar_comando(self, comando):
        comando = comando.strip().upper()
        
        if len(comando) >= 2 and comando[0] in ['C', 'A']:
            if comando[1:].isdigit():
                cmd = comando[0]
                servicio = int(comando[1:])
            else:
                partes = comando.split()
                if len(partes) == 2 and partes[1].isdigit():
                    cmd = partes[0]
                    servicio = int(partes[1])
                else:
                    print("\nFormato invalido. Use: C [numero] o A [numero]")
                    return True
        else:
            if comando == 'S':
                return False
            elif comando == 'H':
                self.mostrar_ayuda()
                return True
            else:
                print("\nComando no valido")
                self.mostrar_ayuda()
                return True
        
        if cmd == 'C':
            if servicio not in self.colas:
                self.colas[servicio] = Cola()
                self.contadores[servicio] = 1
            
            num = self.contadores[servicio]
            self.contadores[servicio] += 1
            ticket = f"S{servicio}-{num:03d}"
            
            self.colas[servicio].encolar(ticket)
            
            print(f"\nCliente registrado en Servicio {servicio}")
            print(f"   Numero de atencion: {ticket}")
            print(f"   Posicion en cola: {self.colas[servicio].tamano()}")
            
        elif cmd == 'A':
            if servicio not in self.colas:
                print(f"\nNo hay cola para el Servicio {servicio}")
                return True
            
            cola = self.colas[servicio]
            
            if cola.esta_vacia():
                print(f"\nNo hay clientes en espera para Servicio {servicio}")
                return True
            
            ticket = cola.desencolar()
            print(f"\nLLAMANDO: {ticket} - Modulo {servicio}")
        
        return True
    
    def mostrar_ayuda(self):
        print("\nCOMANDOS DISPONIBLES:")
        print("   C [numero]  - Registrar llegada de cliente")
        print("   A [numero]  - Atender siguiente cliente")
        print("   S           - Salir del sistema")
    
    def ejecutar(self):
        self.limpiar_pantalla()
        self.mostrar_encabezado()
        print("\nSistema iniciado. Ingrese comandos:")
        self.mostrar_ayuda()
        
        ejecutando = True
        while ejecutando:
            try:
                print("\n" + "-" * 70)
                comando = input("Ingrese comando: ").strip()
                
                if comando:
                    self.limpiar_pantalla()
                    self.mostrar_encabezado()
                    ejecutando = self.procesar_comando(comando)
                    self.mostrar_estado()
                
            except KeyboardInterrupt:
                print("\n\nSaliendo del sistema...")
                break
            except Exception as e:
                print(f"\nError inesperado: {e}")
        
        print("\nGracias por usar el sistema!")

if __name__ == "__main__":
    sistema = SistemaSeguros()
    sistema.ejecutar()
