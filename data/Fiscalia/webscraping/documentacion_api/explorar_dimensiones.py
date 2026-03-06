"""
===========================================================
  Explorador de la API de Fiscalía de Chile
===========================================================

Descarga listados de referencia del dashboard Power BI:
- Comunas
- Delitos (materias)
- Familias de delito
- Fiscalías Regionales
- Regiones

Uso:
  py explorar_dimensiones.py              # Descarga todo
  py explorar_dimensiones.py --dimension comunas   # Solo comunas
"""

import requests
import os
import sys
import csv
import argparse

try:
    import openpyxl
except ImportError:
    os.system(f"{sys.executable} -m pip install openpyxl")
    import openpyxl

BASE_URL = "https://app-backend-reportabilidad-est-dev-eastus-001.azurewebsites.net/Descarga/GenerarDocumento"

FIXED_PARAMS = {
    "ANNO": "ALL", "MES_NOMBRE": "ALL",
    "COD_REGION": "ALL", "COD_FISCALIA": "ALL",
    "GLS_TIPO_IMPUTADO": "ALL", "COD_MARCA_VIF": "ALL",
    "MARCA_RPA": "ALL", "COD_MARCA_ACD": "ALL",
    "COD_MARCA_ACD_FLAGRANCIA": "ALL", "COD_FAMILIADEL": "ALL",
    "COD_MATERIA": "ALL", "GLS_FAMILIADELVIF": "ALL",
    "TIPO_TERMINO": "ALL", "TIPO_GRUPO": "ALL",
    "MENOR_DE_EDAD": "ALL", "TIP_SEXO": "ALL",
    "TIP_PERSONA": "ALL", "COD_PAIS": "ALL",
    "COD_PARENTESCO": "ALL", "COD_REGION_OCURRENCIA": "ALL",
    "COD_COMUNA": "ALL", "GLS_PROCEDIMIENTO": "ALL",
    "Tabular_Columna": "TOTAL",
    "Tematica": "'Tabla de medidas'[Delitos_Ingresados]"
}

DIMENSIONES = {
    "comunas": {
        "tabular_fila": "'GOLD DIM_COMUNA'[GLS_COMUNA]",
        "desc": "Comunas con delitos ingresados"
    },
    "delitos": {
        "tabular_fila": "'GOLD DIM_MATERIA'[GLS_MATERIA]",
        "desc": "Delitos (materias) - glosas abreviadas"
    },
    "familias": {
        "tabular_fila": "'GOLD DIM_FAMILIADELITO'[GLS_FAMILIADEL]",
        "desc": "Familias de delito (agrupaciones)"
    },
    "fiscalias": {
        "tabular_fila": "'GOLD DIM_FISCALIA'[GLS_FISCALIA_NORM]",
        "desc": "Fiscalías Regionales"
    },
    "regiones": {
        "tabular_fila": "'GOLD DIM_REGION'[GLS_REGION]",
        "desc": "Regiones de ocurrencia"
    }
}


def descargar_dimension(nombre, config, output_dir):
    """Descarga una dimensión y la guarda como CSV."""
    print(f"\n{'='*50}")
    print(f"  {nombre.upper()}: {config['desc']}")
    print(f"{'='*50}")

    params = FIXED_PARAMS.copy()
    params["Tabular_Fila"] = config["tabular_fila"]

    print(f"  Descargando...")
    try:
        r = requests.get(BASE_URL, params=params, timeout=120)
        if r.status_code != 200:
            print(f"  ✗ HTTP {r.status_code}")
            return
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return

    # Parsear Excel
    tmp = os.path.join(output_dir, f"_tmp_{nombre}.xlsx")
    with open(tmp, "wb") as f:
        f.write(r.content)

    wb = openpyxl.load_workbook(tmp, read_only=True)
    ws = wb.active
    header_found = False
    datos = []
    for row in ws.iter_rows(values_only=True):
        if row[0] is None and not header_found:
            continue
        if not header_found:
            header_found = True
            continue
        if row[0] is not None:
            nombre_val = str(row[0]).strip()
            try:
                conteo = int(row[1]) if row[1] is not None else 0
            except (ValueError, TypeError):
                conteo = 0
            datos.append((nombre_val, conteo))
    wb.close()
    os.remove(tmp)

    # Guardar CSV
    csv_path = os.path.join(output_dir, f"dim_{nombre}.csv")
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["nombre", "delitos_ingresados_total"])
        for n, c in sorted(datos):
            w.writerow([n, c])

    print(f"  ✓ {len(datos)} valores → {csv_path}")
    print(f"  Primeros 10:")
    for n, c in datos[:10]:
        print(f"    {n}: {c:,}")

    return datos


def main():
    parser = argparse.ArgumentParser(description="Explorar dimensiones de Fiscalía")
    parser.add_argument("--dimension", "-d",
                       choices=list(DIMENSIONES.keys()),
                       help="Dimensión específica a descargar")
    args = parser.parse_args()

    output_dir = os.path.dirname(os.path.abspath(__file__))

    print("╔" + "═"*50 + "╗")
    print("║  Explorador de Dimensiones — Fiscalía de Chile  ║")
    print("╚" + "═"*50 + "╝")

    if args.dimension:
        dims = {args.dimension: DIMENSIONES[args.dimension]}
    else:
        dims = DIMENSIONES

    for nombre, config in dims.items():
        descargar_dimension(nombre, config, output_dir)

    print(f"\n✓ Listo. Archivos CSV en: {output_dir}")


if __name__ == "__main__":
    main()
