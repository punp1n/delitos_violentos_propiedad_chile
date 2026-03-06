# Referencia API — Fiscalía de Chile (Power BI)

Documentación completa del endpoint de descarga del dashboard de estadísticas interactivas de la Fiscalía de Chile:  
**https://www.fiscaliadechile.cl/estadisticas-interactivas**

---

## 1. Endpoint de descarga

```
GET https://app-backend-reportabilidad-est-dev-eastus-001.azurewebsites.net/Descarga/GenerarDocumento
```

- **Sin autenticación** — acceso público
- **Respuesta**: archivo `.xlsx` (Excel con openpyxl)
- **Timeout recomendado**: 120-180 segundos
- **Rate limiting**: no detectado, pero se recomienda pausar 2s entre descargas

> **IMPORTANTE:** Este endpoint NO es el frontend. El frontend (`app-frontend-reportabilidad-...`) redirige las peticiones al backend. Siempre usar el backend directamente.

---

## 2. Parámetros (25 en total)

### Filtros principales

| Parámetro | Tipo | Valores | Descripción |
|---|---|---|---|
| `ANNO` | int/ALL | `2014`-`2025`, `ALL` | Año |
| `MES_NOMBRE` | int/ALL | `1`-`12`, `ALL` | Mes |
| `COD_REGION` | str/ALL | Códigos internos, `ALL` | Región de la Fiscalía |
| `COD_FISCALIA` | str/ALL | Códigos internos, `ALL` | Fiscalía Local |
| `COD_MATERIA` | int/ALL | `804`, `702`, etc., `ALL` | **Código del delito (CUM)** |
| `COD_COMUNA` | str/ALL | `318-1370`, `ALL` | **Código interno de comuna** |
| `COD_FAMILIADEL` | str/ALL | Códigos internos, `ALL` | Familia de delito |
| `COD_REGION_OCURRENCIA` | str/ALL | Códigos internos, `ALL` | Región de ocurrencia |

### Filtros secundarios

| Parámetro | Tipo | Valores |
|---|---|---|
| `GLS_TIPO_IMPUTADO` | str/ALL | Conocido / Desconocido |
| `COD_MARCA_VIF` | str/ALL | SI / NO (Violencia Intrafamiliar) |
| `MARCA_RPA` | str/ALL | Responsabilidad Penal Adolescente |
| `COD_MARCA_ACD` | str/ALL | Acuerdo Complementario |
| `COD_MARCA_ACD_FLAGRANCIA` | str/ALL | ACD Flagrancia |
| `GLS_FAMILIADELVIF` | str/ALL | Familia delito VIF |
| `TIPO_TERMINO` | str/ALL | Tipo de término |
| `TIPO_GRUPO` | str/ALL | Tipo de grupo |
| `MENOR_DE_EDAD` | str/ALL | Menor de edad |
| `TIP_SEXO` | str/ALL | Sexo |
| `TIP_PERSONA` | str/ALL | Natural / Jurídica |
| `COD_PAIS` | str/ALL | Nacionalidad |
| `COD_PARENTESCO` | str/ALL | Parentesco |
| `GLS_PROCEDIMIENTO` | str/ALL | Procedimiento |

### Estructura de salida

| Parámetro | Descripción |
|---|---|
| `Tabular_Columna` | Qué va en las columnas del Excel |
| `Tabular_Fila` | Qué va en las filas del Excel |
| `Tematica` | Métrica a descargar |

---

## 3. Tabular_Fila — Dimensiones disponibles

Estos valores usan **referencias DAX** del modelo Power BI:

| Dimensión | Valor de `Tabular_Fila` |
|---|---|
| Total (agregado) | `TOTAL` |
| Comuna | `'GOLD DIM_COMUNA'[GLS_COMUNA]` |
| Delito | `'GOLD DIM_MATERIA'[GLS_MATERIA]` |
| Familia de delitos | `'GOLD DIM_FAMILIADELITO'[GLS_FAMILIADEL]` |
| Fiscalía Regional | `'GOLD DIM_FISCALIA'[GLS_FISCALIA_NORM]` |
| Región de ocurrencia | `'GOLD DIM_REGION'[GLS_REGION]` |

### ⭐ Cruces multi-dimensión

Se pueden combinar dimensiones separadas con guión (`-`):

```
# Delito × Comuna (cada fila: "ROBO POR SORPRESA-SANTIAGO")
Tabular_Fila = 'GOLD DIM_MATERIA'[GLS_MATERIA]-'GOLD DIM_COMUNA'[GLS_COMUNA]

# Comuna × Fiscalía (cada fila: "SANTIAGO-Metropolitana Centro Norte")
Tabular_Fila = 'GOLD DIM_COMUNA'[GLS_COMUNA]-'GOLD DIM_FISCALIA'[GLS_FISCALIA_NORM]
```

> **Parseo:** El separador es `-`. Para separar, usar `rfind('-')` ya que las comunas son MAYÚSCULAS sin guiones y las fiscalías usan CamelCase. Los nombres de delitos SÍ pueden tener guiones internos.

---

## 4. Tabular_Columna — Dimensiones columna

| Dimensión | Valor probable |
|---|---|
| Total (solo 1 columna de conteo) | `TOTAL` |
| Año | `'GOLD DIM_PERIODO'[ANNO]` (no confirmado) |
| Mes | `'GOLD DIM_PERIODO'[MES_NOMBRE]` (no confirmado) |

> Usar `TOTAL` con iteración manual por `ANNO` y `MES_NOMBRE` es más confiable.

---

## 5. Tematica — Métricas disponibles

| Métrica | Valor |
|---|---|
| **Delitos Ingresados** | `'Tabla de medidas'[Delitos_Ingresados]` |
| Términos aplicados | `'Tabla de medidas'[Términos_Aplicados]` (probable) |
| Víctimas | `'Tabla de medidas'[Víctimas]` (probable) |
| Imputados | `'Tabla de medidas'[Imputados]` (probable) |

> Solo "Delitos Ingresados" fue testeado extensamente.

---

## 6. Códigos de comuna (`COD_COMUNA`)

El sistema de Fiscalía **NO usa el código CUT estándar** del INE.

| Propiedad | Detalle |
|---|---|
| Formato | `XXX-YYYY` (ej: `318-1370` para Concón) |
| Estructura | Probablemente `fiscalía_local-id_interno` |
| CUT estándar | **No funciona** (ej: CUT 5103 para Concón ≠ 318-1370) |

### Cómo descubrir códigos de comuna

1. Usar el dashboard web → seleccionar comuna → capturar URL generada
2. Para todas las comunas: usar `Tabular_Fila = 'GOLD DIM_COMUNA'[GLS_COMUNA]` que devuelve **nombres** (no códigos)
3. No es necesario conocer los códigos si se usa `COD_COMUNA=ALL` + cruce multidimensión

---

## 7. Códigos de delito (`COD_MATERIA`)

| Propiedad | Detalle |
|---|---|
| Formato | Numérico (ej: `804` = Robo por sorpresa) |
| Correspondencia | Corresponde al código **CUM** (Catálogo Único de Materias) del CAPJ |
| Catálogo | 565+ códigos únicos |

### Glosas de delito

Los nombres que retorna la API son **versiones abreviadas y truncadas** de las glosas CUM oficiales:

| API Fiscalía | CUM oficial |
|---|---|
| `CONDUC EBRIEDAD C/RESULT MUERTE ART196INC3 LEY TRANSITO` | `CONDUCCIÓN ESTADO DE EBRIEDAD CON RESULTADO DE MUERTE` (CUM 14006) |
| `ABUSO SEX C/CONTACTO CORP. A MENOR DE 14 AÑOS ART 366 BIS` | `ABUSO SEXUAL CON CONTACTO CORPORAL DE MENOR DE 14 AÑOS` (CUM 623) |
| `ROBO POR SORPRESA. ART. 436 INC. 2°` | `ROBO POR SORPRESA` (CUM 804) |

Patrones comunes en las abreviaciones:
- Truncamiento a ~60 caracteres
- Agregan artículos legales al final (`ART. 196`, `LEY 20.000`)
- Abrevian palabras (`CONDUC` → Conducción, `FUNC.` → Funciones)
- Quitan preposiciones (`O DE` → `O`)

---

## 8. Estructura del Excel descargado

```
Fila 1: vacía o metadata
Fila 2: header (nombre_dimension | conteo)
Fila 3+: datos
```

- Columna A: nombre de la dimensión (o combinación si es multi-dimensión)
- Columna B: conteo (int)
- Las filas vacías al inicio se ignoran
- La primera fila no vacía es el **header**

---

## 9. Fiscalías Regionales

Las Fiscalías Regionales usan nombres estilizados (primera mayúscula, sin tildes en algunos casos):

| Región | Nombre Fiscalía |
|---|---|
| Arica y Parinacota | Arica y Parinacota |
| Tarapacá | Tarapaca |
| Antofagasta | Antofagasta |
| Atacama | Atacama |
| Coquimbo | Coquimbo |
| Valparaíso | Valparaiso |
| O'Higgins | O Higgins |
| Maule | Maule |
| Ñuble | Ñuble |
| Biobío | Bio Bio |
| Araucanía | Araucania |
| Los Ríos | Los Rios |
| Los Lagos | Los Lagos |
| Aysén | Aysen |
| Magallanes | Magallanes |
| Metropolitana Centro Norte | Metropolitana Centro Norte |
| Metropolitana Occidente | Metropolitana Occidente |
| Metropolitana Oriente | Metropolitana Oriente |
| Metropolitana Sur | Metropolitana Sur |

> Nota: La RM tiene 4 fiscalías regionales. Una misma comuna puede tener datos en más de una fiscalía.

---

## 10. Modelo de datos (resumen)

```
┌──────────────────┐      ┌──────────────────┐
│  DIM_PERIODO     │      │  DIM_MATERIA     │
│  - ANNO          │      │  - COD_MATERIA   │
│  - MES_NOMBRE    │      │  - GLS_MATERIA   │
└────────┬─────────┘      │  - FAMILIADEL    │
         │                └────────┬─────────┘
         │                         │
   ┌─────┴─────────────────────────┴─────┐
   │           TABLA DE HECHOS           │
   │  - Delitos_Ingresados (conteo)      │
   │  - Términos_Aplicados               │
   │  - Víctimas                         │
   │  - Imputados                        │
   └─────┬─────────────────────────┬─────┘
         │                         │
┌────────┴─────────┐      ┌────────┴─────────┐
│  DIM_COMUNA      │      │  DIM_FISCALIA    │
│  - COD_COMUNA    │      │  - COD_FISCALIA  │
│  - GLS_COMUNA    │      │  - GLS_FISCALIA  │
└──────────────────┘      └──────────────────┘
```

---

## 11. Consejos de uso

1. **Siempre usar `Tabular_Columna=TOTAL`** e iterar `ANNO` y `MES_NOMBRE` manualmente
2. **Usar cruces multi-dimensión** (`delito-comuna`) para evitar descubrir códigos internos
3. **Parsear con `rfind('-')`** para separar el último guión de los cruces
4. **Pausar 2 segundos entre descargas** para evitar saturar el servidor
5. **Implementar reintentos** con backoff exponencial (3 intentos, 5-10-15s)
6. **Usar `COD_MATERIA=ALL`** y `COD_COMUNA=ALL`; los cruces ya dan el detalle necesario
7. **Resume capability**: guardar progreso en JSON para continuar descargas interrumpidas
