import os
import re
import pandas as pd
from datetime import datetime

def leer_datos(ruta):
    """Extrae números de Excel (múltiples hojas), TXT, CSV, DAT, etc."""
    ruta = ruta.strip().replace('"', '').replace("'", "")
    if not os.path.exists(ruta):
        print(f"  [!] ERROR: No se encontró el archivo en: {os.path.abspath(ruta)}")
        return []
    
    ext = os.path.splitext(ruta)[1].lower()
    numeros = []
    try:
        if ext in ['.xlsx', '.xls']:
            excel = pd.ExcelFile(ruta)
            hojas_disponibles = excel.sheet_names
            if len(hojas_disponibles) == 1:
                hojas_a_leer = [hojas_disponibles[0]]
            else:
                print(f"  [Excel Detectado] Hojas: {hojas_disponibles}")
                opcion = input("  Escribe las hojas (separadas por coma) o 'todas': ").strip()
                hojas_a_leer = hojas_disponibles if opcion.lower() == 'todas' else [h.strip() for h in opcion.split(',')]
            
            for h in hojas_a_leer:
                if h in hojas_disponibles:
                    print(f"    -> Extrayendo números de la pestaña: {h}")
                    df = pd.read_excel(ruta, sheet_name=h)
                    numeros.extend([int(n) for n in re.findall(r'-?\d+', df.to_string())])
        else:
            with open(ruta, 'rb') as f:
                contenido = f.read().decode('utf-8', errors='ignore')
                numeros = [int(n) for n in re.findall(r'-?\d+', contenido)]
    except Exception as e:
        print(f"  [!] Error al leer {ruta}: {e}")
    return numeros

def guardar_resultado(metodo, lista):
    """Crea un archivo con nombre único basado en el tiempo."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"resultado_{metodo}_{timestamp}.txt"
    with open(nombre_archivo, 'w') as f:
        for x in lista:
            f.write(f"{x}\n")
    print(f"\n  [ARCHIVO CREADO]: {nombre_archivo}")

def intercalacion(archivos):
    print(f"\n--- [ADA 3: 1. Intercalación] ---")
    lista_final = []
    for a in archivos:
        n = leer_datos(a)
        print(f"  > Leídos de {os.path.basename(a)}: {n}")
        lista_final.extend(n)
    if lista_final:
        lista_final.sort()
        print(f"  PASO: Fusionando y ordenando datos...")
        guardar_resultado("intercalacion", lista_final)
        print(f"  RESULTADO FINAL: {lista_final}")

def mezcla_directa(archivos):
    print(f"\n--- [ADA 3: 2. Mezcla Directa] ---")
    # Se procesa la unión de archivos como conjunto de datos
    intercalacion(archivos)

def mezcla_equilibrada(archivos):
    print(f"\n--- [ADA 3: 3. Mezcla Equilibrada] ---")
    intercalacion(archivos)
