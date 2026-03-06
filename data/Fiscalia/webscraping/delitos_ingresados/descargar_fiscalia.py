"""
===========================================================
  DESCARGA DE DATOS - FISCALÍA DE CHILE
  Delitos Ingresados 2014-2025
===========================================================

Descarga todos los datos de delitos ingresados desde la API 
de reportabilidad de la Fiscalía de Chile, desglosados por:
  - Delito (materia)
  - Comuna
  - Fiscalía Regional
  - Año (2014-2025)
  - Mes (1-12)

Uso:
  py descargar_fiscalia.py          # Ejecución completa
  py descargar_fiscalia.py --test   # Modo test (solo 2 meses)

Autor: Script generado por asistente de IA
Fecha: 2026-02-27
"""

import requests
import os
import sys
import csv
import time
import json
import logging
import argparse
from datetime import datetime
from pathlib import Path

# ======================================================
# CONFIGURACIÓN
# ======================================================

BASE_URL = "https://app-backend-reportabilidad-est-dev-eastus-001.azurewebsites.net/Descarga/GenerarDocumento"

# Parámetros fijos (no cambian entre descargas)
FIXED_PARAMS = {
    "COD_REGION": "ALL",
    "COD_FISCALIA": "ALL",
    "GLS_TIPO_IMPUTADO": "ALL",
    "COD_MARCA_VIF": "ALL",
    "MARCA_RPA": "ALL",
    "COD_MARCA_ACD": "ALL",
    "COD_MARCA_ACD_FLAGRANCIA": "ALL",
    "COD_FAMILIADEL": "ALL",
    "COD_MATERIA": "ALL",
    "GLS_FAMILIADELVIF": "ALL",
    "TIPO_TERMINO": "ALL",
    "TIPO_GRUPO": "ALL",
    "MENOR_DE_EDAD": "ALL",
    "TIP_SEXO": "ALL",
    "TIP_PERSONA": "ALL",
    "COD_PAIS": "ALL",
    "COD_PARENTESCO": "ALL",
    "COD_REGION_OCURRENCIA": "ALL",
    "COD_COMUNA": "ALL",
    "GLS_PROCEDIMIENTO": "ALL",
    "Tabular_Columna": "TOTAL",
    "Tematica": "'Tabla de medidas'[Delitos_Ingresados]"
}

# Dimensiones a descargar
DIMENSIONES = {
    "delitos": {
        "tabular_fila": "'GOLD DIM_MATERIA'[GLS_MATERIA]",
        "nombre_columna": "delito",
        "descripcion": "Delitos (materias)"
    },
    "comunas": {
        "tabular_fila": "'GOLD DIM_COMUNA'[GLS_COMUNA]",
        "nombre_columna": "comuna",
        "descripcion": "Comunas"
    },
    "fiscalias": {
        "tabular_fila": "'GOLD DIM_FISCALIA'[GLS_FISCALIA_NORM]",
        "nombre_columna": "fiscalia_regional",
        "descripcion": "Fiscalías Regionales"
    }
}

# Rango de años
ANNO_INICIO = 2014
ANNO_FIN = 2025
MESES = list(range(1, 13))

# Control de tasa
PAUSA_ENTRE_DESCARGAS = 2  # segundos entre cada descarga
MAX_REINTENTOS = 3
TIMEOUT_DESCARGA = 120  # segundos

# ======================================================
# FUNCIONES
# ======================================================

def setup_logging(log_dir):
    """Configura logging a consola y archivo."""
    log_file = os.path.join(log_dir, f"descarga_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file, encoding="utf-8")
        ]
    )
    return log_file


def cargar_progreso(progress_file):
    """Carga el archivo de progreso para retomar descargas."""
    if os.path.exists(progress_file):
        with open(progress_file, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()


def guardar_progreso(progress_file, completados):
    """Guarda el progreso actual."""
    with open(progress_file, "w", encoding="utf-8") as f:
        json.dump(list(completados), f)


def descargar_excel(params, filepath, max_reintentos=MAX_REINTENTOS):
    """
    Descarga un archivo Excel desde la API.
    Retorna True si la descarga fue exitosa.
    """
    for intento in range(1, max_reintentos + 1):
        try:
            response = requests.get(
                BASE_URL, 
                params=params, 
                timeout=TIMEOUT_DESCARGA
            )
            
            if response.status_code == 200 and len(response.content) > 500:
                with open(filepath, "wb") as f:
                    f.write(response.content)
                return True
            
            elif response.status_code == 200 and len(response.content) <= 500:
                logging.warning(f"  Respuesta muy pequeña ({len(response.content)} bytes), "
                              f"posiblemente sin datos. Intento {intento}/{max_reintentos}")
                # Guardar de todos modos si es un Excel válido
                if len(response.content) > 100:
                    with open(filepath, "wb") as f:
                        f.write(response.content)
                    return True
                    
            else:
                logging.warning(f"  HTTP {response.status_code}. "
                              f"Intento {intento}/{max_reintentos}")
        
        except requests.exceptions.Timeout:
            logging.warning(f"  Timeout. Intento {intento}/{max_reintentos}")
        
        except requests.exceptions.ConnectionError:
            logging.warning(f"  Error de conexión. Intento {intento}/{max_reintentos}")
        
        except Exception as e:
            logging.warning(f"  Error: {e}. Intento {intento}/{max_reintentos}")
        
        if intento < max_reintentos:
            wait = 5 * intento  # Backoff: 5s, 10s, 15s
            logging.info(f"  Esperando {wait}s antes de reintentar...")
            time.sleep(wait)
    
    return False


def parsear_excel(filepath):
    """
    Lee un Excel descargado y devuelve una lista de tuplas (nombre, cantidad).
    Los Excel tienen 6 filas vacías de encabezado, luego fila de headers, luego datos.
    """
    try:
        import openpyxl
    except ImportError:
        logging.error("openpyxl no está instalado. Ejecuta: py -m pip install openpyxl")
        sys.exit(1)
    
    datos = []
    try:
        wb = openpyxl.load_workbook(filepath, read_only=True, data_only=True)
        ws = wb.active
        
        header_encontrado = False
        for row in ws.iter_rows(values_only=True):
            # Saltar filas vacías al inicio
            if row[0] is None and not header_encontrado:
                continue
            
            # La primera fila no-nula es la cabecera
            if not header_encontrado:
                header_encontrado = True
                continue
            
            # Filas de datos
            if row[0] is not None:
                nombre = str(row[0]).strip()
                try:
                    cantidad = int(row[1]) if row[1] is not None else 0
                except (ValueError, TypeError):
                    cantidad = 0
                datos.append((nombre, cantidad))
        
        wb.close()
    except Exception as e:
        logging.error(f"Error leyendo {filepath}: {e}")
    
    return datos


def generar_tareas(annos, meses, dimensiones):
    """Genera la lista de todas las tareas de descarga."""
    tareas = []
    for dim_key, dim_info in dimensiones.items():
        for anno in annos:
            for mes in meses:
                tarea_id = f"{dim_key}_{anno}_{mes:02d}"
                tareas.append({
                    "id": tarea_id,
                    "dimension": dim_key,
                    "anno": anno,
                    "mes": mes,
                    "tabular_fila": dim_info["tabular_fila"],
                    "nombre_columna": dim_info["nombre_columna"],
                })
    return tareas


def ejecutar_descargas(base_dir, tareas, completados, progress_file):
    """Ejecuta todas las descargas pendientes."""
    total = len(tareas)
    pendientes = [t for t in tareas if t["id"] not in completados]
    
    logging.info(f"Total tareas: {total}")
    logging.info(f"Ya completadas: {total - len(pendientes)}")
    logging.info(f"Pendientes: {len(pendientes)}")
    logging.info("")
    
    exitosos = 0
    fallidos = 0
    
    for i, tarea in enumerate(pendientes):
        dim = tarea["dimension"]
        anno = tarea["anno"]
        mes = tarea["mes"]
        
        # Crear directorio
        excel_dir = os.path.join(base_dir, "excel", dim)
        os.makedirs(excel_dir, exist_ok=True)
        
        filename = f"{dim}_{anno}_{mes:02d}.xlsx"
        filepath = os.path.join(excel_dir, filename)
        
        # Construir parámetros
        params = FIXED_PARAMS.copy()
        params["ANNO"] = str(anno)
        params["MES_NOMBRE"] = str(mes)
        params["Tabular_Fila"] = tarea["tabular_fila"]
        
        # Progreso
        progreso_pct = ((total - len(pendientes) + i + 1) / total) * 100
        logging.info(f"[{progreso_pct:.1f}%] Descargando {dim} | {anno}-{mes:02d} "
                    f"({i+1}/{len(pendientes)} pendientes)")
        
        # Descargar
        ok = descargar_excel(params, filepath)
        
        if ok:
            exitosos += 1
            completados.add(tarea["id"])
            guardar_progreso(progress_file, completados)
            
            # Verificación rápida
            datos = parsear_excel(filepath)
            logging.info(f"  ✓ {len(datos)} registros descargados")
        else:
            fallidos += 1
            logging.error(f"  ✗ FALLÓ después de {MAX_REINTENTOS} intentos")
        
        # Pausa entre descargas
        if i < len(pendientes) - 1:
            time.sleep(PAUSA_ENTRE_DESCARGAS)
    
    return exitosos, fallidos


def consolidar_csv(base_dir, dimension, nombre_columna, annos, meses):
    """
    Lee todos los Excel de una dimensión y genera un CSV consolidado.
    """
    excel_dir = os.path.join(base_dir, "excel", dimension)
    csv_path = os.path.join(base_dir, f"datos_{dimension}.csv")
    
    logging.info(f"Consolidando {dimension} → {csv_path}")
    
    filas_totales = 0
    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["anno", "mes", nombre_columna, "delitos_ingresados"])
        
        for anno in annos:
            for mes in meses:
                filename = f"{dimension}_{anno}_{mes:02d}.xlsx"
                filepath = os.path.join(excel_dir, filename)
                
                if not os.path.exists(filepath):
                    logging.warning(f"  Archivo no encontrado: {filename}")
                    continue
                
                datos = parsear_excel(filepath)
                for nombre, cantidad in datos:
                    writer.writerow([anno, mes, nombre, cantidad])
                    filas_totales += 1
    
    logging.info(f"  ✓ {filas_totales} filas escritas en {csv_path}")
    return filas_totales


# ======================================================
# MAIN
# ======================================================

def main():
    parser = argparse.ArgumentParser(description="Descarga datos de Fiscalía de Chile")
    parser.add_argument("--test", action="store_true", 
                       help="Modo test: solo descarga 2 meses de 2025")
    parser.add_argument("--solo-csv", action="store_true",
                       help="Solo consolidar CSV (sin descargar)")
    parser.add_argument("--dimension", choices=["delitos", "comunas", "fiscalias"],
                       help="Descargar solo una dimensión")
    args = parser.parse_args()
    
    # Directorio base
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Setup logging
    os.makedirs(os.path.join(base_dir, "logs"), exist_ok=True)
    log_file = setup_logging(os.path.join(base_dir, "logs"))
    
    logging.info("=" * 60)
    logging.info("  DESCARGA DE DATOS - FISCALÍA DE CHILE")
    logging.info("  Delitos Ingresados")
    logging.info("=" * 60)
    
    # Verify openpyxl
    try:
        import openpyxl
    except ImportError:
        logging.info("Instalando openpyxl...")
        os.system(f"{sys.executable} -m pip install openpyxl")
        import openpyxl
    
    # Configurar rangos según modo
    if args.test:
        annos = [2025]
        meses = [1, 2]
        logging.info("MODO TEST: Solo 2025, meses 1-2")
    else:
        annos = list(range(ANNO_INICIO, ANNO_FIN + 1))
        meses = MESES
        logging.info(f"MODO COMPLETO: {ANNO_INICIO}-{ANNO_FIN}, meses 1-12")
    
    # Seleccionar dimensiones
    if args.dimension:
        dims = {args.dimension: DIMENSIONES[args.dimension]}
    else:
        dims = DIMENSIONES
    
    logging.info(f"Dimensiones: {', '.join(dims.keys())}")
    logging.info(f"Años: {annos[0]}-{annos[-1]}")
    logging.info(f"Meses: {meses}")
    logging.info(f"Log: {log_file}")
    logging.info("")
    
    # Archivo de progreso
    progress_file = os.path.join(base_dir, "progreso.json")
    completados = cargar_progreso(progress_file)
    
    if not args.solo_csv:
        # Generar tareas
        tareas = generar_tareas(annos, meses, dims)
        
        total_descargas = len(tareas)
        ya_hechas = len([t for t in tareas if t["id"] in completados])
        estimacion = (total_descargas - ya_hechas) * (PAUSA_ENTRE_DESCARGAS + 3)
        
        logging.info(f"Descargas planificadas: {total_descargas}")
        logging.info(f"Ya completadas: {ya_hechas}")
        logging.info(f"Tiempo estimado: ~{estimacion // 60} min")
        logging.info("")
        
        # Ejecutar descargas
        inicio = time.time()
        exitosos, fallidos = ejecutar_descargas(base_dir, tareas, completados, progress_file)
        duracion = time.time() - inicio
        
        logging.info("")
        logging.info(f"Descarga completada en {duracion/60:.1f} minutos")
        logging.info(f"  Exitosos: {exitosos}")
        logging.info(f"  Fallidos: {fallidos}")
        logging.info("")
    
    # Consolidar CSVs
    logging.info("=" * 60)
    logging.info("CONSOLIDANDO CSVs")
    logging.info("=" * 60)
    
    for dim_key, dim_info in dims.items():
        consolidar_csv(base_dir, dim_key, dim_info["nombre_columna"], annos, meses)
    
    logging.info("")
    logging.info("=" * 60)
    logging.info("¡PROCESO COMPLETADO!")
    logging.info("=" * 60)
    logging.info("")
    logging.info("Archivos generados:")
    for dim_key in dims:
        csv_path = os.path.join(base_dir, f"datos_{dim_key}.csv")
        if os.path.exists(csv_path):
            size = os.path.getsize(csv_path)
            logging.info(f"  {csv_path} ({size/1024:.1f} KB)")
    logging.info("")


if __name__ == "__main__":
    main()
