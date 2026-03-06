# Protocolo de Investigación v4.0: Cambio Estructural en los Delitos Violentos contra la Propiedad en Chile (2014-2024)

*Versión: 4.0 (rev.1) — 06 de marzo de 2026*
*Protocolos anteriores: `05032026_proyecto_v3.1.md` (v3.1), `05032026_proyecto_v3.0.md` (v3.0), `04032026_proyecto_v2.0.md` (v2.0), `02032026_proyecto.md` (v1.0)*

---

## Historial de cambios respecto a v3.1 (Resultado de Peer Review interno)

| Cambio | Justificación |
|--------|---------------|
| **Corrección de inferencia:** Se reemplaza `fepois()` + `boottest()` (incompatibles) por `glm(..., family=poisson)` con dummies regionales explícitas + `sandwich::vcovBS()` para Wild Cluster Bootstrap. | `fwildclusterboot::boottest()` no acepta objetos `fepois`. La combinación `glm()` + `vcovBS()` mantiene la consistencia Poisson-QMLE con inferencia WCB válida. |
| **Nodos del spline basados en percentiles** (P25, P50, P75 del trend) como especificación principal; nodos teóricos (2016, 2018, 2022) como robustez. | Evita circularidad: los nodos originales coincidían con la hipótesis de quiebre. |
| **Interpolación lineal mensual del denominador poblacional.** | Elimina saltos discretos enero-diciembre en el offset. |
| **Ampliación de placebos con CUM verificados en SQL:** Homicidios dolosos (CUM 702, 703, 705) como placebo positivo; cuasidelito vehicular (CUM 14020) como placebo negativo de movilidad. Se descarta estafas (CUM 816) por estar confundida con la digitalización. | La exploración de frecuencias confirma: homicidios (277→650) capturan violencia real con cifra negra ≈ 0; CUM 14020 tiene volumen adecuado (2K-4.6K/año) y rebota post-COVID como proxy de movilidad; CUM 816 muestra crecimiento exponencial (16K→62K) por digitalización, no movilidad, invalidándola como placebo. |
| **Degradación del Componente 1b:** La "Tasa de Denuncia Empírica" pasa de "demostración matemática" a "indicador descritivo-relativo" con bandas de incertidumbre. | El ratio incidencia (CCH) / prevalencia (ENUSC) mezcla unidades inconmensurables y no es interpretable como proporción de denuncia. |
| **Análisis de sensibilidad al denominador irregular:** Se añade tabla de robustez con factores de inflación demográfica k ∈ {1.00, 1.05, 1.10, 1.15, 1.20} para regiones de alta inmigración. | Formaliza el argumento de "cota inferior" con evidencia cuantitativa. |
| **Análisis complementario de potencia regional** para CUSUM-GLM. | Regiones con conteos bajos (Aysén, Magallanes) podrían no tener potencia suficiente para detectar quiebres. Se reporta potencia ex-post. |
| **Macrozona como nivel de interacción espacial** en modelo complementario. | Permite testear heterogeneidad espacial dentro del panel sin los problemas de potencia de las series regionales individuales. |
| **Comisaría Virtual declarada como limitación** (no disponible variable de canal). | Se confirma que CCH no contiene la variable de canal de denuncia (presencial vs. online). Se declara como limitación y se argumenta la dirección del sesgo. |
| **Extracción a nivel de comuna (CUT)** en ETL. | Permite filtrar denuncias CCH a las mismas 102 comunas ENUSC para comparabilidad directa en el Componente 1b. |
| **Perfil del infractor (Eje 2) reservado para paper independiente.** | Evita fragmentación narrativa. Los microdatos de detenidos se preservan para un segundo artículo. |

---

## 1. Pregunta de Investigación e Hipótesis

### 1.1 Pregunta Central

> ¿Han aumentado estructuralmente los delitos violentos contra la propiedad en Chile durante la última década (2014-2024), y este incremento se concentra en la "violencia dura" (alta lesividad), aportando evidencia empírica a la tesis de un cambio cualitativo ("crisis de seguridad") no atribuible exclusivamente a sesgos de reporte ciudadano o esfuerzo policial?

### 1.2 Hipótesis

**H₁ — Hipótesis de Cambio Estructural Heterogéneo:**
En el período post-COVID (2022-2024) existe un aumento significativo y estructural en la tasa regional de *denuncias* por delitos violentos contra la propiedad (específicamente violencia dura) en comparación con la línea base pre-estallido social (2016–2019). Este cambio no es uniforme a nivel nacional, concentrándose espacialmente en territorios específicos (ej. Macrozona Norte, RM).

**H₂ — Hipótesis de Convergencia Descriptiva:**
Las señales de quiebre estructural observadas en los registros administrativos policiales son cualitativamente convergentes con las tendencias de prevalencia en la ENUSC. Adicionalmente, un índice relativo de propensión a denunciar (normalizado a 2016) no muestra un salto abrupto que explique completamente el incremento observado, descartando que el motor *exclusivo* del alza sea un cambio en el comportamiento de reporte ciudadano.

---

## 2. Diseño General

El artículo aísla la demanda por seguridad ciudadana (denuncias) de la oferta policial (detenciones), estructurándose en dos componentes:

| Componente | Objetivo | Fuente primaria | Unidad de análisis |
|------------|----------|-----------------|---------------------|
| **1a: Panel de Denuncias** | Cuantificar la evolución de las tasas de reportes ciudadanos, aislando proactividad policial, e identificar quiebres regionales y por macrozona. | CCH (solo denuncias) | Región × Mes |
| **1b: Triangulación ENUSC** | Verificar convergencia con victimización auto-reportada. Calcular índice relativo de propensión a denunciar (no ratio absoluto). | ENUSC + CCH combinados | Región × Año |

---

## 3. Fuentes de Datos

### 3.A Registros Administrativos Policiales: Carabineros de Chile (CCH)

* **Acceso:** SQL Server (`SYJ_SCV_DEDS`). Credenciales en `data/SyJ/.env`.
* **Período:** 2014–2024 (11 años, 132 meses).
* **Cobertura geográfica:** Nacional exhaustiva (todas las comunas).
* **Tablas utilizadas:**

| Tabla | Rol | Variables clave |
|-------|-----|-----------------|
| `cch.denuncias` | Variable dependiente principal (ventana de victimización reportada) | `id_hecho`, `year`, `id_mes`, `comuna_ocurrencia_codigo`, `codigo_delito_carabineros` |
| `cch.detenciones` | Análisis de robustez (ventana de reacción policial) | Mismas variables que denuncias |

* **Definición de VD (Depurada v3.1+):** Solo `cch.denuncias`. Justificación: las detenciones reflejan proactividad estatal (operativos "Calles sin Violencia"), no victimización. Las detenciones se reservan para robustez (§7.2).
* **Mapeo comuna → región:** `region = comuna_ocurrencia_codigo // 1000`.
* **Extracción a nivel comunal (NUEVO v4.0 rev.1):** El ETL debe preservar `comuna_ocurrencia_codigo` en la tabla intermedia para permitir filtrado a las 102 comunas ENUSC en el Componente 1b y en la robustez R2.

* **Datos de placebo (CUM verificados en SQL):**

| Categoría Placebo | CUM confirmados | Volumen anual aprox. | Función |
|-------------------|----------------|---------------------|--------|
| Cuasidelito vehicular (Ley de Tránsito) | **14020** | 2,000–4,600/año | Placebo negativo: proxy de movilidad vehicular. Rebota post-COVID proporcionalmente a la actividad vial. |
| Homicidios dolosos | **702** (simple), **703** (calificado), **705** (en riña) | 265–650/año | Placebo positivo: cifra negra ≈ 0. Si la violencia real está aumentando, homicidios también deberían subir. |
| No dar cuenta de accidente (complemento) | **12077** | 200–1,450/año | Placebo negativo complementario: proxy de actividad vial con tendencia secular propia. |

> **Nota:** Se descartaron las **estafas (CUM 816)** como placebo. Aunque inicialmente parecían un buen control negativo, la exploración de datos revela un crecimiento exponencial de 16,057 (2014) a 61,669 (2024), impulsado por la digitalización y el comercio electrónico. Esta tendencia está *confundida* con la adopción tecnológica — exactamente la misma amenaza que queremos aislar con los placebos — por lo que su uso como control invalidaría la interpretación.

### 3.B Encuesta Nacional Urbana de Seguridad Ciudadana: ENUSC (INE)

* **Base utilizada:** `data/ENUSC/Interanual_2008_2024/base-de-datos---interanual-2008---2024.csv`.
* **Período utilizable:** 2016–2024 (9 olas). Cobertura de 102 comunas históricas (filtro `com102 == 1`).
* **Formato:** CSV con `sep=';', decimal=','`.

#### 3.B.1 Variables de victimización (dummies binarias)

| Variable | Descripción | Clasificación |
|----------|-------------|---------------|
| `rvi` | Víctima de robo con violencia o intimidación | Violento |
| `rps` | Víctima de robo por sorpresa | Violento (Oportunidad) |
| `rfv` | Víctima de robo con fuerza en vivienda | No violento |
| `hur` | Víctima de hurto | No violento |

* **Variable construida "víctima violenta":** `victim_violent = max(rvi, rps)` → 1 si fue víctima de al menos un delito violento.
* **Variable construida "víctima violencia dura":** `victim_hard = rvi` → 1 si fue víctima de robo con violencia/intimidación (análogo a "Violencia Dura" CCH).
* **Variable construida "víctima no violenta":** `victim_nonviolent = max(rfv, hur)`.

#### 3.B.2 Factores de expansión (hogares)

| Años | Factor de expansión | Justificación |
|------|---------------------|---------------|
| 2016–2018 | `fact_hog_2008_2019` | Calibrado para 102 comunas. |
| 2019 | `fact_hog_2019_2024` | Empalme prospectivo. Check de sensibilidad con `fact_hog_2008_2019` en nota al pie. |
| 2020–2022 | `fact_hog_2019_2024` | Único factor disponible. |
| 2023–2024 | `fact_hog_2023_2024` | Recalibrado para 136 comunas; combinado con filtro `com102 == 1`. |

#### 3.B.3 Variables de diseño muestral

| Variable | Uso |
|----------|-----|
| `varstrat` | Estratificación para `survey::svydesign()` |
| `conglomerado` | Unidad primaria de muestreo |
| `region16` | Región (16 regiones) |
| `año` | Año de la ola |

#### 3.B.4 Limitación de temporalidad (solapamiento)

**Advertencia:** La ENUSC pregunta por victimización en "los últimos 12 meses". El levantamiento se realiza entre agosto y diciembre de cada año. Esto genera solapamiento temporal entre olas consecutivas (e.g., la ola 2022 cubre ≈ agosto 2021 – diciembre 2022; la ola 2023 cubre ≈ agosto 2022 – diciembre 2023). Los meses agosto-diciembre 2022 aparecen en ambas olas, suavizando quiebres inter-anuales. Esto se declara explícitamente y se discute en limitaciones.

### 3.C Denominadores Poblacionales

#### 3.C.1 Proyecciones INE base Censo 2017

* **Fuente:** `data/Poblacion_base_2017/estimaciones-y-proyecciones-2002-2035-comunas.xlsx`.
* **Procesamiento:** Sumar por comuna → mapear a región (`// 1000`) → sumar por región → obtener `Pop_INE(r, t)` para cada región `r` y año `t`.

#### 3.C.2 Corrección migratoria: SERMIG

* **Fuente:** Servicio Nacional de Migraciones (SERMIG).
* **Archivos:**

| Archivo | Ubicación | Variables clave |
|---------|-----------|-----------------|
| RD Resueltas | `data/SERMIG/Residencias_definitivas/RD-Resueltas-2o-semestre-2025.xlsx` | `REGIÓN`, `AÑO`, `TIPO_RESUELTO`, `Total` |
| RT Resueltas | `data/SERMIG/Residencias_temporales/RT-Resueltas-2o-semestre-2025.xlsx` | `REGIÓN`, `AÑO`, `TIPO_RESUELTO`, `Total` |

* **Filtro:** Solo `TIPO_RESUELTO == 'Otorga'`.
* **Mapeo de regiones SERMIG → código numérico estándar.** Categorías `'Anonimizada'` y `'Sin Información'` se excluyen.

#### 3.C.3 Fórmula de corrección poblacional

$$\text{Pop}_{\text{corr}}(r, t) = \text{Pop}_{\text{INE}}(r, t) + \text{SERMIG}_{\text{cumul}}(r, t)$$

Donde:

$$\text{SERMIG}_{\text{cumul}}(r, t) = \begin{cases} \displaystyle\sum_{y=2018}^{t} \left[ \text{RD}_{\text{otorga}}(r, y) + \text{RT}_{\text{otorga}}(r, y) \right] & \text{si } t \geq 2018 \\ 0 & \text{si } t < 2018 \end{cases}$$

**Justificación del inicio en 2018:** Las proyecciones INE incorporan migración observada hasta el Censo 2017. Los flujos Post-2018 (oleada venezolana, haitiana, colombiana) no están reflejados.

**Justificación acumulativa:** Cada "Otorga" corresponde a un individuo que se suma al stock poblacional de forma permanente.

#### 3.C.4 Interpolación mensual del offset (NUEVO v4.0)

Las proyecciones INE son anuales. Para evitar saltos discretos diciembre-enero en el offset mensual:

$$\text{Pop}_{\text{month}}(r, y, m) = \text{Pop}_{\text{corr}}(r, y) + \frac{m - 6.5}{12} \times \left[\text{Pop}_{\text{corr}}(r, y+1) - \text{Pop}_{\text{corr}}(r, y)\right]$$

Donde $m$ es el mes del año (1-12). Para el último año (2024), se extrapola linealmente con la pendiente del año anterior.

```r
# Interpolación en R
panel <- panel %>%
  group_by(region) %>%
  arrange(year, month) %>%
  mutate(
    pop_next_year = lead(pop_corrected_annual, 12),
    pop_monthly = pop_corrected_annual + 
      (month - 6.5) / 12 * (coalesce(pop_next_year, pop_corrected_annual + 
        (pop_corrected_annual - lag(pop_corrected_annual, 12))) - pop_corrected_annual)
  ) %>%
  ungroup()
```

#### 3.C.5 Limitación del denominador: análisis de sensibilidad a población irregular (NUEVO v4.0)

El corrector SERMIG es una **cota inferior** que solo captura migrantes formalmente regularizados. La población irregular no aparece en el denominador.

**Fisura del argumento de "cota inferior":** El argumento asume que migrantes irregulares no generan denuncias. Sin embargo, delitos *contra* migrantes irregulares (no denunciados) no aparecen en el numerador, pero un delito *de* un migrante irregular sí genera denuncia de la víctima. La dirección neta del sesgo es empíricamente indeterminada.

**Solución:** Análisis de sensibilidad paramétrico con factor de inflación demográfica $k$:

$$\text{Pop}_{\text{sens}}(r, t; k_r) = \text{Pop}_{\text{corr}}(r, t) \times k_r$$

Donde $k_r \in \{1.00, 1.05, 1.10, 1.15, 1.20\}$ para regiones de alta inmigración (Tarapacá, Antofagasta, Arica-Parinacota, RM) y $k_r \in \{1.00, 1.02\}$ para el resto. Se reporta cómo cambia el IRR del trend bajo cada escenario.

---

## 4. Clasificación de Delitos (Variable Dependiente)

El universo de estudio se restringe a **delitos contra la propiedad**. Fuente: CNP, archivo `CNP_hist_2.0.xlsx`. Se evalúan tres esquemas de clasificación (C1, C2, C3) como parte integral del análisis de sensibilidad. Las tres clasificaciones se calculan como columnas paralelas en el ETL.

### 4.1 Tres esquemas de clasificación

#### C1 — Clasificación Institucional SPD/CAPJ (dummy binaria)

Clasificación oficial utilizada por la **Subsecretaría de Prevención del Delito (SPD)** y el **Centro de Análisis de Políticas de Justicia (CAPJ)**. Se obtiene directamente de la columna `delito_violento_propiedad` del catálogo CNP.

| Categoría | CUM incluidos | Variable |
|-----------|--------------|----------|
| **Violento** (=1) | 802, 803, **804**, 827, 828, 829, 861, 862, 867 | `C1_violento` |
| **No Violento** (=0) | 808, 809, 810, **812, 864, 869, 2009, 12053**, 821, 826, 846, 847, 848, 853, 13028, 831, 868, 858, 870, 871, 872, 891, 892 | `C1_violento` |

**Diferencias clave con C2/C3:**
- Incluye **CUM 804** (robo por sorpresa) como violento.
- Incluye **Receptación** (812, 864, 869, 2009, 12053) como no violento.

#### C2 — Clasificación Ajustada (dummy binaria, propia)

Clasificación propia que corrige dos problemas de C1: excluye receptación (delito de *enforcement* puro) y mantiene la misma estructura binaria para comparabilidad.

| Categoría | CUM incluidos | Variable |
|-----------|--------------|----------|
| **Violento** (=1) | 802, 803, **804**, 827, 828, 829, 861, 862, 867 | `C2_violento` |
| **No Violento** (=0) | 808, 809, 810, 821, 826, 846, 847, 848, 853, 13028, 831, 868, 858, 870, 871, 872, 891, 892 | `C2_violento` |
| **Excluido** | 812, 864, 869, 2009, 12053 (Receptación) | `NaN` |

**Diferencia con C1:** Receptación excluida (89,583 detenciones vs. 2,320 denuncias en el periodo — delito de enforcement puro).
**Diferencia con C3:** CUM 804 permanece como "Violento" (no se separa).

#### C3 — Clasificación Tricotómica (3 niveles, propia — especificación principal)

Clasificación principal del artículo. Desagrega el componente "Violento" en dos subcategorías con dinámicas empíricas distintas.

**C3.1 — Violencia Dura (Alta lesividad):**
*Fuerza directa sobre las personas, intimidación grave, resultado lesivo.*

| CUM | Glosa |
|-----|-------|
| 802 | Robo con intimidación |
| 803 | Robo con violencia |
| 827 | Robo con homicidio |
| 828 | Robo con violación |
| 829 | Robo con castración, mutilación o lesiones |
| 861 | Robo con lesiones graves |
| 862 | Robo con retención de víctimas |
| 867 | Robo de vehículo motorizado por sorpresa, violencia o intimidación *(ver S5)* |

**C3.2 — Oportunidad / Contacto Físico Leve (Sorpresa):**
*Depende de aglomeración urbana; cayó abruptamente en pandemia.*

| CUM | Glosa |
|-----|-------|
| 804 | Robo por sorpresa ("lanzazo") |

**C3.3 — No Violentos (Comparador Baseline):**
*Fuerza sobre cosas, sustracción simple, sin confrontación.*

| CUM | Glosa |
|-----|-------|
| 808, 809, 810 | Robos en lugar habitado / no habitado / uso público |
| 821, 826, 846, 847, 848, 853, 13028 | Hurtos simples y afines |
| 831, 868 | Robo de vehículo motorizado (sin violencia) |
| 858 | Robo con fuerza de cajeros automáticos |
| 870, 871 | Robo/hurto en ocasión de calamidad |
| 872 | Saqueo *(ver S5)* |
| 891, 892 | Sustracción de madera |

**Excluido en C2 y C3:** Receptación (CUM 812, 864, 869, 2009, 12053).

### 4.2 Tabla comparativa de clasificaciones

| CUM | Glosa | C1 (SPD/CAPJ) | C2 (Ajustada) | C3 (Tricotómica) |
|:---:|-------|:-:|:-:|:-:|
| 802 | Robo con intimidación | Violento | Violento | Violencia Dura |
| 803 | Robo con violencia | Violento | Violento | Violencia Dura |
| 804 | Robo por sorpresa | Violento | Violento | **Sorpresa** |
| 827 | Robo con homicidio | Violento | Violento | Violencia Dura |
| 828 | Robo con violación | Violento | Violento | Violencia Dura |
| 829 | Robo con castración/mutilación | Violento | Violento | Violencia Dura |
| 861 | Robo con lesiones graves | Violento | Violento | Violencia Dura |
| 862 | Robo con retención de víctimas | Violento | Violento | Violencia Dura |
| 867 | Robo vehículo (violencia) | Violento | Violento | Violencia Dura |
| 808 | Robo en lugar habitado | No Violento | No Violento | No Violento |
| 809 | Robo en lugar no habitado | No Violento | No Violento | No Violento |
| 810 | Robo en lugar de uso público | No Violento | No Violento | No Violento |
| 812 | Receptación | No Violento | **Excluido** | **Excluido** |
| 864 | Receptación persona jurídica | No Violento | **Excluido** | **Excluido** |
| 869 | Receptación vehículos | No Violento | **Excluido** | **Excluido** |
| 2009 | Receptación datos informáticos | No Violento | **Excluido** | **Excluido** |
| 12053 | Receptación aduanera | No Violento | **Excluido** | **Excluido** |
| *Resto* | Hurtos, robos s/v, cajeros, etc. | No Violento | No Violento | No Violento |

### 4.3 Estrategia analítica con las tres clasificaciones

- **C3 (Tricotómica)** es la **especificación principal** del artículo. Los modelos Poisson-QMLE (§6.1) y CUSUM-GLM (§6.1.2) se estiman para cada categoría de C3.
- **C1 y C2** se usan como **análisis de sensibilidad**: se re-estima el modelo principal usando la dummy binaria violento/no-violento de C1 y C2. Los resultados se reportan en la tabla de robustez (§7.3).
- La comparación C1 vs. C2 cuantifica el efecto de incluir/excluir receptación.
- La comparación C2 vs. C3 cuantifica el efecto de agrupar vs. separar Sorpresa (CUM 804).

### 4.4 Análisis de sensibilidad adicional en la clasificación

| ID | Cambio | Clasificación afectada | Justificación |
|----|--------|:---:|---------------|
| **S1** | CUM 804 → No Violento en C3 | C3 | En ICCS-ONU, arrebatamiento = robo sin violencia directa. |
| **S2** | CUM 872 → Violencia Dura en C3 | C3 | Saqueos del estallido involucraron intimidación colectiva. |
| **S3** | CUM 808 → Violencia Dura en C3 | C3 | Robo en lugar habitado frecuentemente involucra confrontación. |
| **S4** | Receptación re-incluida como No Violento en C2/C3 | C2, C3 | Evaluar sensibilidad al excluir receptación. |
| **S5** | CUM 867 excluido de C3 | C3 | Delito híbrido con dinámica propia (mercados de autopartes). |

---

## 5. Tratamiento de Períodos Atípicos

### 5.1 Definición temporal precisa (nivel mensual)

| Período | Meses | YYYYMM | Justificación |
|---------|-------|--------|---------------|
| **Pre línea base** | Ene 2014 – Dic 2015 (24 meses) | 201401–201512 | Solo CCH. Uso descriptivo. |
| **Línea base** | Ene 2016 – Sep 2019 (45 meses) | 201601–201909 | Post-cambio metodológico ENUSC. |
| **Estallido social** | Oct 2019 – Feb 2020 (5 meses) | 201910–202002 | 18-O hasta pre-pandemia. |
| **Pandemia COVID-19** | Mar 2020 – Dic 2021 (22 meses) | 202003–202112 | Cuarentenas, restricciones. |
| **Período reciente** | Ene 2022 – Dic 2024 (36 meses) | 202201–202412 | "Nueva normalidad". |

### 5.2 Estrategia econométrica para los shocks

Variables dummy absorbentes:
- $D_{\text{estallido},m} = 1$ si $m \in \{\text{Oct 2019}, \ldots, \text{Feb 2020}\}$.
- $D_{\text{pandemia},m} = 1$ si $m \in \{\text{Mar 2020}, \ldots, \text{Dic 2021}\}$.

No se omiten del dataset para preservar la estructura temporal.

---

## 6. Estrategia Analítica y Especificaciones Econométricas

### 6.1 Componente 1a — Panel Regional de Denuncias

**Unidad de análisis:** Región × Mes.
**N observaciones:** 16 regiones × 132 meses = 2,112.
**Variable dependiente:** $Y_{rm}$ = conteo mensual de denuncias por tipo (violencia dura, sorpresa, no violento).

#### 6.1.1 Modelo Principal: Poisson-QMLE con WCB

**Especificación formal:**

$$\ln(\mu_{rm}) = \sum_{k=2}^{12} \alpha_k \cdot \mathbb{1}(\text{mes}=k) + \delta_1 \cdot D_{\text{estallido},m} + \delta_2 \cdot D_{\text{pandemia},m} + f(t) + \sum_{r=2}^{16} \lambda_r \cdot \mathbb{1}(\text{región}=r) + \ln(\text{Pop}_{\text{month},rt})$$

| Componente | Descripción |
|-----------|-------------|
| $\sum \alpha_k$ | 11 dummies mensuales de estacionalidad (ref: enero). |
| $D_{\text{estallido}}$, $D_{\text{pandemia}}$ | Dummies de shocks (§5.2). |
| $f(t)$ | **Spline cúbico restringido** con nodos en percentiles P25, P50, P75 de `trend_t` (especificación agnóstica). Captura tendencia sin imponer linealidad ni pre-suponer la ubicación del quiebre. |
| $\lambda_r$ | Efectos fijos regionales como dummies explícitas (necesario para `glm()`). |
| $\ln(\text{Pop}_{\text{month},rt})$ | Offset de población interpolada mensualmente (§3.C.4). |

**Estimación:** `glm(..., family = poisson)` en R con dummies regionales explícitas.

> **Nota técnica (v4.0):** Se usa `glm()` en lugar de `fixest::fepois()` porque `fwildclusterboot::boottest()` es incompatible con objetos `fepois`. Para verificar que los coeficientes son idénticos, se estima también con `fepois()` y se comparan punto a punto como check de control.

**Inferencia:** Wild Cluster Bootstrap vía `sandwich::vcovBS()` con pesos de Webb (distribución de 6 puntos), B=9,999 replicaciones.

```r
library(splines)
library(sandwich)
library(lmtest)

# Nodos agnósticos en percentiles
knots_main <- quantile(panel$trend_t, probs = c(0.25, 0.50, 0.75))

# Modelo principal con dummies regionales explícitas
mod_violent <- glm(
  n_violent_hard ~ factor(month_of_year) +
                   d_estallido + d_pandemia +
                   ns(trend_t, knots = knots_main) +
                   factor(region) +
                   offset(log(pop_monthly)),
  family = poisson,
  data = panel
)

# Wild Cluster Bootstrap para inferencia válida con G=16
vcov_wcb <- vcovBS(
  mod_violent,
  cluster = ~region,
  R = 9999,
  type = "webb"
)
coeftest(mod_violent, vcov = vcov_wcb)

# Check: comparar con fepois
library(fixest)
mod_check <- fepois(
  n_violent_hard ~ i(month_of_year, ref = 1) +
                   d_estallido + d_pandemia +
                   ns(trend_t, knots = knots_main) |
                   region,
  offset = ~log(pop_monthly),
  data = panel,
  cluster = ~region
)
# Verificar: coef(mod_violent) ≈ coef(mod_check)
```

**Reporte:** Incidence Rate Ratios (IRR = $e^\beta$), p-valores WCB, intervalos de confianza invertidos al 95%.

#### 6.1.2 Tests de Quiebre Estructural

**A) CUSUM-GLM Regional con corrección FDR (test principal):**

El proceso empírico de fluctuación se evalúa **región por región** para evitar falacia ecológica:

1. Ajustar un Poisson-GLM base por cada región $r$ (132 meses):
   $$\ln(\mu_m^r) = \alpha^r + \sum \alpha_k^r \cdot \mathbb{1}(\text{mes}=k) + \delta_1^r D_{\text{est}} + \delta_2^r D_{\text{pan}} + \ln(\text{Pop}_m^r)$$
2. Calcular estadístico CUSUM con `strucchange::gefp()` sobre scores del GLM.
3. Test supremo de puente browniano (`sctest(., functional = maxBB)`).
4. Extraer 16 p-valores regionales.
5. **Corrección FDR** de Benjamini-Hochberg sobre los 16 p-valores.

```r
library(strucchange)

cusum_results <- lapply(1:16, function(reg) {
  data_r <- panel[panel$region == reg, ]
  glm_r <- glm(n_violent_hard ~ factor(month_of_year) + d_estallido + d_pandemia +
                offset(log(pop_monthly)),
                family = poisson, data = data_r)
  gefp_r <- gefp(glm_r, fit = NULL, order.by = data_r$trend_t)
  test_r <- sctest(gefp_r, functional = maxBB)
  list(region = reg, pvalue = test_r$p.value, gefp = gefp_r)
})

# Corrección FDR
pvals <- sapply(cusum_results, function(x) x$pvalue)
pvals_adj <- p.adjust(pvals, method = "BH")
significant_regions <- which(pvals_adj < 0.05)
```

**Análisis de potencia ex-post** (NUEVO v4.0): Para cada región, simular 1,000 series bajo $H_A$ (quiebre del 30% en $t=97$) y calcular la proporción de rechazos a $\alpha=0.05$. Regiones con potencia < 50% se reportan con advertencia y se sugiere agrupar en macrozonas.

**B) Modelo de panel con heterogeneidad espacial (NUEVO v4.0):**

```r
# Macrozona: Norte(15,1,2,3,4), Centro(5,6,7,13), RM(13), Sur(8,9,14,16,10), Austral(11,12)
panel$macrozona <- case_when(
  panel$region %in% c(15, 1, 2, 3, 4) ~ "Norte",
  panel$region == 13 ~ "RM",
  panel$region %in% c(5, 6, 7) ~ "Centro",
  panel$region %in% c(8, 9, 14, 16, 10) ~ "Sur",
  panel$region %in% c(11, 12) ~ "Austral"
)

mod_heterog <- glm(
  n_violent_hard ~ factor(month_of_year) + d_estallido + d_pandemia +
                   ns(trend_t, knots = knots_main) +
                   ns(trend_t, knots = knots_main):factor(macrozona) +
                   factor(region) +
                   offset(log(pop_monthly)),
  family = poisson, data = panel
)

# Test de Wald: ¿las interacciones macrozona × trend son significativas?
library(aod)
wald.test(b = coef(mod_heterog), Sigma = vcovBS(mod_heterog, cluster = ~region, R = 9999, type = "webb"),
          Terms = grep("macrozona", names(coef(mod_heterog))))
```

**C) Test de Chow en puntos pre-especificados (complementario):**

Dentro del modelo con dummies, interactuar la tendencia con dummy de quiebre en enero 2022: $\gamma \cdot \mathbb{1}(t \geq 97) \times f(t)$. Testear significancia conjunta.

**D) Bai-Perron (complemento descriptivo):**

Aplicado al ratio nacional desestacionalizado $\frac{Y^{\text{viol}}_m}{Y^{\text{viol}}_m + Y^{\text{no viol}}_m}$ con errores HAC. `strucchange::breakpoints()`. Se reporta como evidencia descriptiva.

### 6.2 Componente 1b — Triangulación con ENUSC

**Objetivo:** Verificar convergencia direccional entre registros policiales y victimización auto-reportada. Calcular índice relativo de propensión a denunciar.

**Unidad de análisis:** Región × Año (2016–2024). N = 144.

#### 6.2.1 Prevalencia ponderada con errores de diseño complejo

```r
library(survey)

des <- svydesign(
  ids = ~conglomerado,
  strata = ~varstrat,
  weights = ~weight,
  data = enusc_micro,
  nest = TRUE
)

prev_violent <- svyby(~victim_violent, ~region16 + ano, des, svymean, na.rm = TRUE)
prev_hard <- svyby(~victim_hard, ~region16 + ano, des, svymean, na.rm = TRUE)
```

#### 6.2.2 Índice Relativo de Propensión a Denunciar (NUEVO v4.0)

**Importante:** El ratio Denuncias_CCH / Víctimas_Expandidas_ENUSC mezcla **incidencia** (numerador, conteo de eventos) con **prevalencia** (denominador, conteo de hogares victimizados). Un hogar con 3 robos cuenta como 1 en la ENUSC pero genera 3 denuncias en CCH. Por tanto, $R_{rt}$ **no es** la proporción de víctimas que denuncian; es un índice compuesto.

Para que sea interpretable, se normaliza a un año base:

$$\text{Índice}_{rt} = \frac{R_{rt}}{R_{r, 2016}} \quad \text{donde} \quad R_{rt} = \frac{\text{Denuncias\_CCH}_{rt}}{\hat{V}_{\text{ENUSC},rt}}$$

**Restricción geográfica:** El numerador se filtra a las **102 comunas ENUSC** para comparabilidad:

```r
# Denuncias CCH restringidas a 102 comunas ENUSC
comunas_102 <- read.csv("data/ENUSC/comunas_102_historicas.csv")$codigo
denuncias_102 <- panel_comuna[panel_comuna$comuna %in% comunas_102, ] %>%
  group_by(region, year) %>%
  summarise(n_denuncias_102 = sum(n_denuncias_violent))

# Víctimas expandidas ENUSC (con errores de diseño)
victimas_exp <- svyby(~victim_violent, ~region16 + ano, des, svytotal, na.rm = TRUE)

# Índice relativo a 2016
indice <- merge(denuncias_102, victimas_exp, by = c("region", "year"))
indice$ratio <- indice$n_denuncias_102 / indice$victim_violent
indice <- indice %>%
  group_by(region) %>%
  mutate(indice_rel = ratio / ratio[year == 2016]) %>%
  ungroup()
```

**Bandas de incertidumbre del ratio:** El denominador es una estimación muestral. Varianza por Delta Method:

$$\text{Var}(\hat{R}) \approx \hat{R}^2 \cdot \frac{\text{Var}(\hat{V})}{\hat{V}^2}$$

```r
# CIs del ratio por Delta Method
indice$se_ratio <- indice$ratio * (indice$se.victim_violent / indice$victim_violent)
indice$ci_lower <- indice$ratio - 1.96 * indice$se_ratio
indice$ci_upper <- indice$ratio + 1.96 * indice$se_ratio
```

**Interpretación:** Si el índice relativo se mantiene estable (≈1.0) mientras las denuncias absolutas suben, eso indica que tanto las denuncias como la victimización real subieron proporcionalmente → el alza no es artefacto de denuncia. Si el índice sube (>1.0), parte del alza *podría* deberse a mayor propensión a denunciar.

#### 6.2.3 Tabla de convergencia cualitativa

Para cada región, comparar la dirección del cambio (promedio 2022-2024 vs. 2016-2019):

| Región | CCH Violentos | ENUSC Violentos | Convergencia |
|--------|---------------|-----------------|--------------|
| Arica  | ↑ / ↓ / →     | ↑ / ↓ / →       | Sí / No / Parcial |

**Criterio:** Cambio > +10% = ↑, < -10% = ↓, entre = →.

#### 6.2.4 Test de tendencia

```r
library(lmtest); library(sandwich)
mod_trend <- lm(prev_violent ~ ano * I(ano >= 2022), data = prev_panel)
coeftest(mod_trend, vcov = vcovCL(mod_trend, cluster = ~region16))
```

---

## 7. Análisis de Robustez y Falsificación

### 7.1 Placebo Tests (Falsificación del diseño)

| Placebo | Tipo | CUM | Vol. anual | Hipótesis |
|---------|------|-----|-----------|----------|
| **P1: Cuasidelito vehicular** | Negativo (movilidad) | 14020 | 2K-4.6K | NO debe mostrar quiebre 2022. Si lo muestra, el spline captura la "vuelta a la calle" post-COVID, no criminalidad. |
| **P2: Homicidios dolosos** | Positivo (violencia real) | 702, 703, 705 | 265-650 | SÍ debería mostrar quiebre convergente. Cifra negra ≈ 0 → si sube, la violencia real está aumentando. Dato preliminar: 277 (2014) → 650 (2024), tendencia consistente. |

> **Nota sobre frecuencia de homicidios:** Con ~350-650 denuncias/año a nivel nacional, la serie regional mensual tiene conteos muy bajos (muchas celdas con 0-3 eventos). El análisis de homicidios se realizará exclusivamente a **nivel nacional mensual** (no panel regional), usando un GLM de Poisson simple sin efectos fijos regionales. La comparabilidad con el modelo principal se garantiza porque la pregunta del placebo es temporal, no espacial.

```r
# Placebo P1: Cuasidelito vehicular (proxy movilidad)
mod_p1 <- glm(
  n_cuasidelito ~ factor(month_of_year) + d_estallido + d_pandemia +
                  ns(trend_t, knots = knots_main) +
                  factor(region) +
                  offset(log(pop_monthly)),
  family = poisson,
  data = panel_placebo_transito
)

# Placebo P2: Homicidios dolosos (nivel nacional)
mod_p2 <- glm(
  n_homicidios ~ factor(month_of_year) + d_estallido + d_pandemia +
                 ns(trend_t, knots = knots_main) +
                 offset(log(pop_monthly_nacional)),
  family = poisson,
  data = panel_homicidios_nacional
)
```

### 7.2 Robustez en estimación

| ID | Descripción | Qué cambia |
|----|-------------|------------|
| **R1** | Offset libre | `log(pop_monthly)` como regresor libre. Si $\hat{\beta}_{\text{pop}} \approx 1$, el offset unitario es adecuado. |
| **R2** | Panel restringido a 102 comunas ENUSC | Solo comunas del marco ENUSC, población restringida. Comparabilidad con Componente 1b. |
| **R3** | Denominador sin corrección SERMIG | `Pop_INE(r,t)` sin corrector migratorio. |
| **R4** | Sensibilidad al denominador irregular | Pop × k para k ∈ {1.05, 1.10, 1.15, 1.20} en regiones de alta inmigración. |
| **R5** | Nodos teóricos del spline | Nodos en meses 25, 49, 97 (≈ 2016, 2018, 2022) en lugar de percentiles. |
| **R6** | Flexibilidad del spline (df) | df=3 (2 nodos) y df=5 (4 nodos) además del principal (df=4, 3 nodos). |
| **R7** | Detenciones como VD | Modelo estimado sobre `cch.detenciones` en lugar de denuncias. Evalúa disociación entre victimización y reacción estatal. |
| **R8** | Errores Conley (HAC espacial) | Errores con dependencia espacial, centroides regionales, bandwidth 200 km. |

### 7.3 Robustez en clasificación (de §4.2)

| ID | Cambio |
|----|--------|
| **S1** | CUM 804 → No violento |
| **S2** | CUM 872 → Violento |
| **S3** | CUM 808 → Violento |
| **S4** | Receptación re-incluida |
| **S5** | CUM 867 excluido |

**Formato de reporte:** Tabla comparativa con IRR del trend, SE (WCB), y IC para cada especificación.

---

## 8. Componentes Visuales

### 8.1 Figuras de series temporales

| Figura | Contenido | Datos |
|--------|-----------|-------|
| **Fig. 1** | Serie mensual nacional: Violencia Dura (línea roja), Sorpresa (línea naranja), No Violentos (línea gris). Bandas sombreadas estallido/pandemia. | CCH panel agregado |
| **Fig. 2** | Tasas por 100K hab. anuales por categoría (Violencia Dura, Sorpresa, No Violentos), con línea horizontal de referencia 2016. | CCH + Pop |
| **Fig. 3** | Ratio mensual Violentos / Total contra la propiedad, con CUSUM-GLM superpuesto. | CCH agregado |
| **Fig. 4** | Panel de 16 gráficos CUSUM-GLM regionales con bandas al 95%. Regiones con p-valor FDR < 0.05 resaltadas. | Residuos GLM regional |
| **Fig. 5** | Prevalencia ENUSC anual (violentos y no violentos) con CIs, en panel dual con serie CCH anualizada. | ENUSC + CCH |
| **Fig. 6** | Índice relativo de propensión a denunciar (normalizado 2016=1) por región, con bandas Delta Method. | CCH₁₀₂ + ENUSC |
| **Fig. 7** | Panel de placebos: Cuasidelito vehicular + Homicidios dolosos — series temporales comparativas con VD principal. | CCH placebos |

### 8.2 Mapas coropléticos

| Mapa | Contenido |
|------|-----------|
| **Mapa 1** | Tasa de violencia dura por región (por 100K hab.), side-by-side: 2016 vs. 2024. |
| **Mapa 2** | Cambio porcentual en tasa 2024 vs. 2016 por región. |
| **Mapa 3** | **Mapa de Calor FDR:** Regiones con p-valor CUSUM ajustado < 0.05 en color sólido; p-valor < 0.10 en semitransparente; no significativo en gris. |

### 8.3 Tablas principales

| Tabla | Contenido |
|-------|-----------|
| **Tabla 1** | Estadísticos descriptivos por período y categoría: media, DE, mín, máx de conteos y tasas. |
| **Tabla 2** | Poisson-QMLE: IRR, SE (WCB-Webb), IC 95% — modelo principal y por categoría (Violencia Dura, Sorpresa, No Violentos). |
| **Tabla 3** | CUSUM-GLM regional: p-valores crudos y ajustados (BH), punto estimado de quiebre por región. Potencia ex-post. |
| **Tabla 4** | Prevalencia ENUSC por región y año, SE de diseño complejo. |
| **Tabla 5** | Tabla de convergencia cualitativa CCH₁₀₂ vs. ENUSC + Índice relativo de propensión. |
| **Tabla 6** | Robustez: IRR del trend para todas las especificaciones R1-R8 y S1-S5. |
| **Tabla 7** | Sensibilidad al denominador irregular: IRR bajo k ∈ {1.00, 1.05, 1.10, 1.15, 1.20}. |
| **Tabla 8** | Placebos: IRR del trend para Cuasidelito vehicular (movilidad) y Homicidios dolosos (violencia real). |

---

## 9. Arquitectura del Pipeline

### 9.1 Estructura de directorio

```text
paper1/
├── config.py                        # Constantes compartidas
├── etl/
│   ├── 01_extract_cch.py            # SQL → parquet (denuncias + detenciones + comunas CUT)
│   ├── 02_extract_placebos.py       # SQL → parquet (CUM 14020, 702, 703, 705)
│   ├── 03_build_population.py       # Excel INE → csv (con interpolación mensual)
│   ├── 04_build_sermig.py           # Excel SERMIG → csv
│   ├── 05_build_enusc.py            # CSV interanual → parquet
│   └── 06_assemble_panel.py         # Merge → panel final parquet
├── models/
│   ├── 01_descriptive.R             # Tablas descriptivas + series temporales
│   ├── 02_main_poisson_wcb.R        # Modelo principal con glm() + vcovBS()
│   ├── 03_regional_cusum_fdr.R      # CUSUM-GLM × 16 regiones + BH + potencia
│   ├── 04_macrozona_interaction.R   # Modelo con heterogeneidad espacial
│   ├── 05_enusc_triangulation.R     # Prevalencia + índice relativo (filtrado 102 comunas)
│   ├── 06_placebos.R                # Modelos placebo (CUM 14020 + homicidios)
│   ├── 07_robustness.R              # Todas las robusteces R1-R8, S1-S5
│   ├── 08_sensitivity_pop.R         # Sensibilidad al denominador irregular
│   └── 09_maps_figures.R            # Mapas + figuras de publicación
└── output/
    ├── data/                        # Intermedios (.parquet, .csv)
    ├── tables/                      # Tablas (.tex, .csv)
    └── figures/                     # Figuras (.pdf, .png)
```

### 9.2 DAG de ejecución

```text
FASE 1 — ETL (Python):
  01_extract_cch.py ──────────────┐
  02_extract_placebos.py ─────────┤
  03_build_population.py ─────────┼──→ 06_assemble_panel.py ──→ panel_region_month.parquet
  04_build_sermig.py ─────────────┘
  05_build_enusc.py ───────────────────────────────────→ enusc_microdata_filtered.parquet

FASE 2 — Modelos (R):
  panel_region_month.parquet ──→ 01_descriptive.R
                               ──→ 02_main_poisson_wcb.R
                               ──→ 03_regional_cusum_fdr.R
                               ──→ 04_macrozona_interaction.R
                               ──→ 06_placebos.R
                               ──→ 07_robustness.R (depende de 02)
                               ──→ 08_sensitivity_pop.R
                               ──→ 09_maps_figures.R
  enusc_microdata_filtered.parquet ──→ 05_enusc_triangulation.R
```

### 9.3 Outputs intermedios

| Archivo | Generado por | Schema |
|---------|-------------|--------|
| `cch_panel_region_month.parquet` | `01_extract_cch.py` | `comuna, region, year, month, cum, n_denuncias, n_detenciones, violento_dura_v31` |
| `placebo_panel.parquet` | `02_extract_placebos.py` | `region, year, month, tipo_placebo (cuasidelito_vehicular \| homicidio), n_eventos` |
| `poblacion_regional_mensual.csv` | `03_build_population.py` | `region, year, month, pop_ine, sermig_cumul, pop_corrected, pop_monthly` |
| `sermig_correction.csv` | `04_build_sermig.py` | `region, year, rd_otorga_cumul, rt_otorga_cumul, sermig_cumul` |
| `enusc_microdata_filtered.parquet` | `05_build_enusc.py` | `region16, año, victim_violent, victim_hard, victim_nonviolent, weight, varstrat, conglomerado` |
| `panel_region_month.parquet` | `06_assemble_panel.py` | `region, year, month, yyyymm, n_violent_hard, n_sorpresa, n_nonviolent, pop_monthly, d_estallido, d_pandemia, month_of_year, trend_t, period_cat, macrozona` |

---

## 10. Amenazas a la Validez Interna

### 10.1 Comisaría Virtual y digitalización de la denuncia

La plataforma Comisaría Virtual de Carabineros permite realizar denuncias online desde ~2016, con adopción masiva post-COVID. Esto **reduce la fricción** para denunciar, potencialmente inflando el numerador para delitos de baja lesividad.

**Estado de los datos:** Se confirma que los registros CCH **no contienen** la variable de canal de denuncia (presencial vs. Comisaría Virtual). No es posible controlar directamente por este efecto.

**Mitigación primaria:** La desagregación Violencia Dura / Sorpresa atenúa este problema: los delitos de alta lesividad (robos con violencia, secuestros) son menos susceptibles al efecto de conveniencia (la víctima denuncia independientemente del canal). Frente a un robo con violencia, la gravedad del hecho motiva la denuncia presencial; la Comisaría Virtual facilita más bien denuncias de menor lesividad.

**Mitigación por placebo positivo:** Si los homicidios dolosos (CUM 702, 703, 705) — que no pueden denunciarse online — muestran una tendencia convergente con la Violencia Dura, la hipótesis de que el alza es puramente un artefacto de accesibilidad digital pierde fuerza.

**Dirección declarada del sesgo:** Conservadora para Violencia Dura (la gravedad motiva denuncia independientemente del canal), potencialmente inflacionaria para Sorpresa (lanzazos, arrebatamientos de menor lesividad que podrían no haberse denunciado antes de la digitalización).

### 10.2 Otras amenazas declaradas

1. **Criminalidad aparente, no real:** El Componente 1a mide criminalidad denunciada. La ENUSC se usa para triangulación descriptiva.
2. **Denominadores poblacionales:** Corrección SERMIG es cota inferior. Análisis de sensibilidad paramétrico en R4/Tabla 7.
3. **Granularidad temporal ENUSC:** Solo anual, con solapamiento temporal entre olas. Impide sincronización fina.
4. **Clusters escasos (G=16):** Resuelto con WCB (Webb). Potencia regional reportada.
5. **Spline cúbico restringido:** Nodos agnósticos como principal; nodos teóricos como R5. Flexibilidad alternativa: R6.
6. **ENUSC cobertura urbana:** 102 comunas. No generalizable a zonas rurales.
7. **Solapamiento temporal ENUSC:** Las ventanas de referencia entre olas consecutivas comparten ~5 meses, suavizando quiebres.

---

## 11. Estructura Propuesta del Artículo

**Extensión objetivo:** 6,000–8,000 palabras (sin apéndices).

```text
1. Introducción (~1,500 palabras)
   - El debate público sobre la "crisis de seguridad" en Chile
   - Brecha entre percepción y evidencia empírica
   - Pregunta de investigación e hipótesis

2. Marco Conceptual (~800 palabras)
   - Criminalidad aparente vs. real
   - Cifra negra y propensión a denunciar
   - La violencia patrimonial como indicador de cambio cualitativo
   - Comisaría Virtual y la digitalización de la denuncia

3. Datos y Métodos (~2,000 palabras)
   3.1 Fuentes de datos (CCH, ENUSC, SERMIG)
   3.2 Clasificación tricotómica (Violencia Dura / Sorpresa / No Violentos)
   3.3 Corrección poblacional e interpolación mensual
   3.4 Poisson-QMLE: especificación formal + justificación inferencial (WCB)
   3.5 Tests de quiebre estructural (CUSUM-FDR + Macrozona)
   3.6 Triangulación ENUSC: índice relativo de propensión
   3.7 Placebos y falsificación

4. Resultados (~2,500 palabras)
   4.1 "¿Aumentaron los delitos de violencia dura?"
       → Serie temporal + Poisson-QMLE + Mapa FDR
       [Párrafo puente: "Pero ¿es esto un artefacto de denuncia?"]
   4.2 "¿Lo confirman las víctimas?"
       → Prevalencia ENUSC + Índice relativo + Tabla convergencia
   4.3 "¿Descartamos artefactos de movilidad?"
       → Placebos (tránsito, fraudes, homicidios)

5. Robustez y Sensibilidad (~800 palabras)
   - Tabla resumen R1-R8, S1-S5
   - Sensibilidad al denominador irregular (Tabla 7)
   - Discusión de resultados que cambian/no cambian

6. Discusión (~1,000 palabras)
   - Implicaciones para política pública
   - Limitaciones metodológicas (Comisaría Virtual, denominadores, clusters)
   - Contribución: ¿crisis real o percibida?
   - Agenda futura (perfil del infractor, embudo de judicialización)

7. Conclusión (~400 palabras)
```

**Hilo narrativo:** La Sección 4 se estructura como cadena de falsificación. Primero se establece si hay quiebre (4.1), luego se disocia de artefactos de reporte (4.2), y finalmente de artefactos de movilidad-post-COVID (4.3).

---

## 12. Consideraciones Éticas y de Reproducibilidad

1. **Datos sensibles:** Los microdatos CCH se acceden mediante credenciales institucionales (`.env`). No se difunden microdatos.
2. **Reproducibilidad:** Pipeline Python/R documentado en `paper1/`. Constantes centralizadas en `config.py`.
3. **Pre-registro de especificaciones:** Todos los análisis de sensibilidad (S1-S5), robusteces (R1-R8), placebos (P1-P2), y la elección de factores de expansión ENUSC se declaran ex ante.
4. **Preparación para ambos escenarios de resultado:** El protocolo está diseñado para acomodar tanto la detección de un quiebre estructural como la no-detección. La no-detección es un resultado bibliométricamente valioso ("la crisis de seguridad no tiene respaldo empírico en los agregados de criminalidad") y el framing del paper se adaptará al resultado.

---

## Apéndice Pre-analítico: Hallazgos Preliminares por Exploración de Datos

*Los siguientes hallazgos provienen de la exploración del parquet CCH ya extraído y de consultas SQL al catálogo CNP. Son descriptivos y previos al modelamiento formal.*

### A.1 Tasas nacionales por 100K hab. (denuncias, sin corrección SERMIG)

| Año | Violencia Dura | Sorpresa | No Violentos |
|-----|:-:|:-:|:-:|
| 2014 | 323.7 | 203.0 | 1,322.3 |
| 2016 | **318.5** (base) | **175.7** (base) | **1,179.3** (base) |
| 2019 | 370.8 (+16.4%) | 147.4 (-16.1%) | 1,057.0 (-10.4%) |
| 2020 | 291.8 (-8.4%) | 90.1 (-48.7%) | 689.9 (-41.5%) |
| 2021 | 202.3 (-36.5%) | 78.7 (-55.2%) | 644.9 (-45.3%) |
| 2022 | 327.2 (+2.7%) | 126.8 (-27.8%) | 945.2 (-19.9%) |
| 2023 | 348.8 (+9.5%) | 152.0 (-13.5%) | 986.2 (-16.4%) |
| 2024 | 342.7 (+7.6%) | 181.5 (+3.3%) | 973.3 (-17.5%) |

**Observaciones clave:**
1. La Violencia Dura tiene una **tendencia pre-existente al alza** (2016→2019: +16.4%), no un "salto" post-2022.
2. En 2024, la tasa de Violencia Dura (+7.6% vs. 2016) **no supera** el pico 2019 (+16.4%).
3. Los No Violentos muestran **tendencia secular a la baja** (-17.5% vs. 2016).
4. Sorpresa rebota fuertemente en 2024, superando el nivel 2016.

### A.2 Heterogeneidad regional (Violencia Dura, tasas por 100K)

| Región | 2016 | 2019 | 2022 | 2024 | Δ% (2024 vs. 2016) |
|:------:|:----:|:----:|:----:|:----:|:-------------------:|
| 15 (Arica) | 191.5 | 250.6 | 373.7 | 372.1 | **+94.3%** |
| 2 (Antofagasta) | 260.7 | 253.5 | 402.5 | 328.4 | **+26.0%** |
| 3 (Atacama) | 205.4 | 207.2 | 273.6 | 259.1 | **+26.1%** |
| 1 (Tarapacá) | 362.8 | 285.4 | 473.4 | 306.4 | -15.5% |
| 13 (RM) | 512.5 | 650.2 | 500.4 | 549.5 | +7.2% |
| 7 (Maule) | 104.7 | 135.5 | 130.3 | 125.9 | +20.2% |
| 6 (O'Higgins) | 139.3 | 148.4 | 159.4 | 175.2 | **+25.8%** |
| 16 (Ñuble) | 95.8 | 88.2 | 120.9 | 104.1 | +8.7% |
| 11 (Aysén) | 39.2 | 48.7 | 23.1 | 49.8 | +27.0% |
| 12 (Magallanes) | 46.6 | 30.7 | 31.5 | 27.3 | -41.4% |

**Patrones emergentes:**
- **Macrozona Norte** (Arica, Atacama, Antofagasta) muestra incrementos sostenidos +25–94%.
- **RM** tiene las tasas absolutas más altas (>500/100K) pero regresa a proximidad de 2016.
- **Tarapacá** muestra un pico en 2022 (+31% vs. 2016) seguido de caída, no un trend sostenido.
- **Magallanes** y **La Araucanía** muestran tasas en baja.

### A.3 Placebos: señales preliminares

| Año | Homicidios dolosos (702+703+705) | Cuasidelito vehicular (14020) | Estafas (816) — descartada |
|-----|:------:|:------:|:------:|
| 2014 | 277 | 0* | 16,057 |
| 2016 | 265 | 1,976 | 17,011 |
| 2019 | 335 | 4,618 | 25,634 |
| 2020 | 505 | 2,988 | 29,846 |
| 2022 | 640 | 3,660 | 29,510 |
| 2024 | 650 | 3,469 | 61,669 |

*CUM 14020 sin registros significativos en 2014 (inicio gradual del código).

**Interpretaciones preliminares:**
- **Homicidios dolosos** prácticamente se duplicaron (277→650). Esto es una señal fuerte de que la violencia real *sí* ha aumentado, no solo la propensión a denunciar.
- **Cuasidelito vehicular** rebota de 2,988 (2020) a 3,660 (2022) y se estabiliza — patrón de recuperación post-COVID sin quiebre estructural.
- **Estafas** muestran crecimiento exponencial desligado de la criminalidad física — confirmando su inadecuación como placebo.
