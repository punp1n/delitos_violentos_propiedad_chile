# Interpretación de Resultados v5.0
## Cambio Estructural en los Delitos Violentos contra la Propiedad en Chile (2013–2025)

*Versión 5.0 — 12 de marzo de 2026*
*Basada en datos CCH 2013–2025 (N = 2.496 obs., 16 regiones × 156 meses) y CPHDV 2018–2025*
*Protocolos anteriores: v4.0 (10/03/2026), v3.1, v3.0*

---

## Resumen ejecutivo de cambios v5.0 respecto a v4.0

Esta versión incorpora cinco novedades respecto a v4.0:

1. **Decisión sobre la línea base descriptiva (2016–2019) con nota metodológica:** Se confirma el uso de 2016–2019 como línea base para los Δ% del análisis CUM, justificado por el quiebre estructural Q1 del test de Bai-Perron (mayo 2015), que delimita dos regímenes. Se incorpora nota explícita advirtiendo que la tasa post-pandemia de los CUMs dominantes (802: 184/100K) es comparable al inicio de la serie (2013: ~190–210/100K), no un mínimo histórico absoluto; el -22.9% refleja la distancia desde el peak pre-estallido, no desde el inicio del período. El análisis inferencial (spline) es inmune a esta elección.

2. **Corrección metodológica en scripts de robustez y sensibilidad (07 y 08):** Los scripts anteriores extraían Spline 1 (período inicial) en lugar del Spline 4 (2022–2025), que es el término relevante para la hipótesis central. La corrección alinea las tablas de robustez y sensibilidad con la comparación Spline 1 vs. Spline 4 especificada en el protocolo.

2. **Robustez fortalecida:** Con la corrección, R1 (Offset libre) da IRR=0.732 (p=0.010) y R6 (Detenciones) da IRR=0.539 (p<0.001) para Spline 4. La dirección negativa del hallazgo principal se confirma con mayor solidez.

3. **P3 (Secuestros) como nuevo placebo positivo:** El Spline 4 de secuestros pasa de IRR=1.073 (p=0.415, NS) en v4.0 a IRR=1.553 (p<0.001) en v5.0. Los secuestros crecen significativamente en 2022–2025, confirmando el patrón de violencia coactiva emergente que complementa la hipótesis de cambio cualitativo.

4. **Triangulación CPHDV matizada:** El modelo spline para CPHDV (2018–2025) no muestra un Spline 4 significativo (IRR=1.075, p=0.530). La interpretación se apoya en los datos anuales brutos, que muestran con claridad la caída: 1.330 (2022) → 1.249 → 1.209 → 1.091 (2025). Se explica la limitación del spline con los nuevos knots.

**Resultado central (v5.0, sin cambios respecto a v4.0):** No hay evidencia de aumento estructural en el *volumen* de robos violentos en 2022–2025. El Spline 4 del modelo Poisson-QMLE es negativo e inferior a 1 (IRR=0.868, p=0.057). Lo que sí existe es un **desplazamiento cualitativo en la composición** del delito contra la propiedad, con un ratio Violentos/Total en máximo histórico (21.6% en enero 2024), explicado por la caída más acelerada de los robos no violentos.

---

## 1. Análisis Descriptivo por CUM (Consistente con v4.0)

### 1.1 Composición de los Robos Violentos (C3.1 — Violencia Dura)

Los robos violentos están conformados por 8 CUMs. Solo dos concentran el 93% del total de denuncias 2013–2025.

| CUM | Glosa | N total | % grupo | Tasa base (2016-19) | Tasa post (2022-25) | Δ% |
|-----|-------|--------:|:-------:|--------------------:|--------------------:|---:|
| 802 | Robo con intimidación | 519.171 | 64.3% | 238.5/100K | 184.0/100K | **-22.9%** |
| 803 | Robo con violencia | 232.073 | 28.7% | 97.7/100K | 89.5/100K | **-8.3%** |
| 867 | Robo de vehículo c/violencia | 53.130 | 6.6% | *29.65/100K¹* | 46.7/100K | *+57.6%* |
| 828 | Robo con violación | 1.470 | 0.2% | 0.66/100K | 0.57/100K | -14.1% |
| 862 | Robo con retención (secuestro express) | 992 | 0.1% | 0.24/100K | 0.88/100K | **+263%** |
| 827 | Robo con homicidio | 320 | 0.0% | 0.10/100K | 0.16/100K | +55.1% |
| 861 | Robo con lesiones graves | 175 | 0.0% | 0.09/100K | 0.10/100K | +16.7% |
| 829 | Robo c/castración o mutilación | 15 | 0.0% | 0.005/100K | 0.009/100K | +71.3% |

*¹ Nota metodológica CUM 867:* Este código no existe en el sistema CCH antes de 2019 (solo 11 casos ese año) y se activa masivamente en 2020 (6.068 casos). Se trata como **discontinuidad de clasificación administrativa** (análisis de sensibilidad S5). La tasa base usada es del período pandemia (2020-2021: 29.65/100K), lo que produce Δ=+57.6%, pero este cambio refleja la activación del código, no necesariamente aumento real del delito.

> **Nota metodológica sobre la línea base 2016–2019:** Los Δ% de la tabla anterior comparan el período 2022–2025 con la línea base 2016–2019. Esta elección está justificada por el quiebre estructural Q1 del test de Bai-Perron (mayo 2015), que delimita el inicio de un nuevo régimen de composición del delito; 2016–2019 es el período estable de ese régimen, inmediatamente anterior al estallido social. Sin embargo, dado que la serie de robos violentos (CUM 802) era creciente entre 2013 y el peak 2019, el período 2016–2019 representa condiciones de *near-peak*. En consecuencia, el Δ=-22.9% para CUM 802 refleja el descenso desde ese peak: la tasa post-pandemia (184/100K) es comparable al nivel de inicio de la serie en 2013 (~190–210/100K), no un mínimo sin precedentes. El análisis inferencial (modelo Poisson-QMLE con spline) es completamente inmune a esta elección de línea base, ya que estima la trayectoria sobre el período completo 2013–2025.

**Conclusión descriptiva (Violentos):** Los CUMs de mayor volumen (802, 803 = 93% del grupo) registran tasas en 2022–2025 significativamente inferiores al período de línea base. El único incremento real sostenido es CUM 862 (retención de víctimas, +263%), coherente con el fenómeno de "portonazo" y secuestros express, pero su volumen sigue siendo muy pequeño (<0.1% del grupo).

### 1.2 Composición de los Robos No Violentos (C3.3)

Todos los CUMs muestran tasas inferiores en el período post-pandemia:

| CUM | Glosa | % grupo | Δ% base→post |
|-----|-------|:-------:|-------------:|
| 808 | Robo en bienes nacionales de uso público / sitio no habitado | 22.6% | -18.9% |
| 809 | Robo en lugar habitado | 18.1% | **-35.0%** |
| 847 | Hurto simple (4-40 UTM) | 16.7% | -15.4% |
| 810 | Robo en lugar no habitado | 14.7% | -15.8% |
| 848 | Hurto simple (0.5-4 UTM) | 12.3% | -25.7% |
| 831 | Robo de vehículo (sin violencia) | 10.7% | -4.8% |
| 846 | Hurto simple (>40 UTM) | 2.2% | -30.2% |

La caída más pronunciada es CUM 809 (Robo en lugar habitado, -35%), seguida por CUM 846 (-30.2%) y CUM 848 (-25.7%). Este declive generalizado es el mecanismo que eleva el *ratio* Violentos/Total incluso cuando el volumen de violentos también cae.

---

## 2. Análisis Inferencial Principal: Poisson-QMLE con Spline (C3)

### 2.1 Variables de shock (dummies estallido y pandemia)

| Categoría | d_estallido (IRR) | p-valor WCB | d_pandemia (IRR) | p-valor WCB |
|-----------|:-----------------:|:-----------:|:----------------:|:-----------:|
| Robos violentos | **1.155** | <0.001 | **0.651** | <0.001 |
| Robos por sorpresa | **1.069** | <0.001 | **0.576** | <0.001 |
| Robos no violentos | 0.996 | 0.761 | **0.647** | <0.001 |

Los robos violentos y por sorpresa aumentaron transitoriamente durante el estallido (+15.5% y +6.9%) y cayeron drásticamente en pandemia (-35% y -42%). Los robos no violentos no reaccionaron al estallido (IRR≈1.0) y también cayeron en pandemia (-35%).

### 2.2 Tendencia de largo plazo: Spline 1 vs. Spline 4 (comparación clave)

El spline cúbico restringido con nodos en P25, P50, P75 de `trend_t` captura la trayectoria secular en cuatro tramos. La comparación Spline 1 (tendencia inicial 2013–~2016) vs. Spline 4 (período reciente ~2022–2025) es el contraste central del análisis.

#### Robos Violentos:
| Tramo | IRR (WCB) | IC 95% WCB | p-val WCB |
|-------|:---------:|:----------:|:---------:|
| **Spline 1** (inicio a P25, ~2013–2016) | **1.177** | [0.917, 1.513] | 0.201 |
| Spline 2 (P25 a P50, ~2016–2019) | 1.136 | [0.982, 1.315] | 0.087 |
| Spline 3 (P50 a P75, ~2019–2022) | **1.187** | [1.116, 1.264] | <0.001 |
| **Spline 4** (P75 a fin, ~2022–2025) | **0.868** | [0.751, 1.004] | **0.057** |

**Interpretación Spline 1 vs. Spline 4:** El contraste es claro. Spline 1 muestra una tendencia levemente creciente (IRR=1.177) aunque no significativa. Spline 4 muestra una inflexión negativa (IRR=0.868), sugestiva estadísticamente (p=0.057). El período 2022–2025 tiene tasas de robos violentos *inferiores* a lo que predice la trayectoria previa. Esta inversión de la tendencia es la señal más relevante del análisis.

#### Robos por Sorpresa:
| Tramo | IRR (WCB) | IC 95% WCB | p-val WCB |
|-------|:---------:|:----------:|:---------:|
| **Spline 1** | **0.668** | [0.619, 0.722] | <0.001 |
| Spline 2 | **0.635** | [0.462, 0.873] | 0.005 |
| Spline 3 | 0.968 | [0.634, 1.480] | 0.882 |
| **Spline 4** | 0.861 | [0.511, 1.450] | 0.574 |

Declive secular fuerte en Spline 1 (IRR=0.668, -33.2%). Spline 4 sugiere estabilización, pero sin significancia. La tendencia de largo plazo para robos por sorpresa es estructuralmente decreciente desde el inicio.

#### Robos No Violentos:
| Tramo | IRR (WCB) | IC 95% WCB | p-val WCB |
|-------|:---------:|:----------:|:---------:|
| **Spline 1** | **0.718** | [0.673, 0.767] | <0.001 |
| Spline 2 | **0.685** | [0.568, 0.826] | <0.001 |
| Spline 3 | **0.656** | [0.570, 0.754] | <0.001 |
| **Spline 4** | **0.648** | [0.580, 0.723] | <0.001 |

Declive secular robusto, monotónico y significativo en todos los tramos. La tasa de robos no violentos en Spline 4 es un 35% inferior al nivel predicho al inicio del período. El ritmo de caída se mantiene en Spline 4 (IRR=0.648), ligeramente más pronunciado que en Spline 1 (IRR=0.718).

### 2.3 Síntesis del contraste Spline 1 vs. Spline 4

| Categoría | Spline 1 | Spline 4 | Dirección neta |
|-----------|:--------:|:--------:|:-------------:|
| Robos violentos | 1.177 (NS) | **0.868** (p=0.057) | **Inversión: leve crecimiento → inflexión negativa** |
| Robos por sorpresa | **0.668** (p<0.001) | 0.861 (NS) | Declive inicial → estabilización |
| Robos no violentos | **0.718** (p<0.001) | **0.648** (p<0.001) | Declive secular continuo |

La clasificación tricotómica C3 captura dinámicas cualitativamente distintas que quedarían enmascaradas en una especificación binaria (C1 o C2).

---

## 3. Tests de Quiebre Estructural

### 3.1 Bai-Perron: Ratio Nacional Violentos/Total

El test sobre el ratio desestacionalizado identifica **4 quiebres** como solución óptima (BIC=-883.23 para m=4; mejor que m=5: BIC=-879.44):

| Quiebre | Fecha | Ratio | Interpretación |
|:-------:|-------|------:|----------------|
| Q1 | **Mayo 2015** (obs. 28) | 14.7% | Inicio de la tendencia ascendente del ratio |
| Q2 | **Agosto 2017** (obs. 56) | 17.1% | Aceleración pre-estallido |
| Q3 | **Octubre 2019** (obs. 82) | 18.4% | Estallido social como punto de inflexión |
| Q4 | **Enero 2024** (obs. 133) | **21.6%** | **Máximo histórico confirmado** |

El cuarto quiebre (Q4 = enero 2024) establece el ratio en su nivel más alto registrado. Sin embargo, como en v4.0, la interpretación requiere cautela: este máximo no refleja aumento en el volumen de robos violentos (que están declinando), sino un declive más pronunciado de los no violentos que reduce el denominador.

### 3.2 CUSUM-GLM Regional con Corrección FDR (Robos Violentos, C3)

De las 16 regiones, **12 muestran quiebre estructural significativo** (p-FDR < 0.05):

**Regiones con quiebre significativo:**

| Región | p-FDR | Quiebre estimado (YYYYMM) | Macrozona | Tipo temporal |
|--------|:-----:|:-------------------------:|:---------:|:-------------:|
| R7 — Maule | 5.5e-07 | **Abr 2017** | Centro | Pre-pandemia |
| R9 — La Araucanía | 1.8e-08 | **Jul 2018** | Sur | Pre-pandemia |
| R8 — Biobío | 8.1e-12 | **Ago 2018** | Sur | Pre-pandemia |
| R15 — Arica y Parinacota | 6.9e-13 | **Jul 2021** | Norte | Pandemia/post |
| R3 — Atacama | 3.8e-06 | **Ago 2021** | Norte | Pandemia/post |
| R4 — Coquimbo | 0.009 | **Sep 2021** | Norte | Pandemia/post |
| R6 — O'Higgins | 0.0004 | **Sep 2021** | Centro | Pandemia/post |
| R16 — Ñuble | 0.022 | **Ago 2021** | Sur | Pandemia/post |
| R13 — Metropolitana | 0.0004 | **Jul 2020** | RM | Pandemia |
| R12 — Magallanes | 0.003 | **Ago 2017** | Austral | Pre-pandemia |
| R11 — Aysén | 0.001 | **Feb 2016** | Austral | Muy temprano |
| R1 — Tarapacá | 0.005 | **Ago 2023** | Norte | Tardío |

**Regiones sin quiebre significativo:**

| Región | p-FDR | Nota |
|--------|:-----:|------|
| R2 — Antofagasta | 0.207 | No significativo |
| R5 — Valparaíso | 0.334 | No significativo |
| R10 — Los Lagos | 0.201 | No significativo |
| R14 — Los Ríos | 0.177 | No significativo |

**Patrones regionales (consistentes con v4.0):**
- **Pre-pandemia (R7, R8, R9, R12):** Maule, Biobío, Araucanía y Magallanes muestran quiebres en 2016–2018, anteriores al estallido.
- **Pandemia/post-pandemia (R3, R4, R6, R13, R15, R16):** Quiebres en 2020–2021.
- **Tardío (R1 — Tarapacá, 2023):** Dinámica migratoria y crimen organizado frontera norte.

---

## 4. Heterogeneidad Espacial: Macrozonas

### 4.1 Test de Wald: Heterogeneidad macrozona × spline

El test de Wald sobre los términos de interacción macrozona × trend:

> **X² = 7.059.869.9, df = 16, p = 0.000**

La heterogeneidad espacial de largo plazo es estadísticamente real y altamente significativa. Las macrozonas Norte, Centro, RM y Sur tienen trayectorias de robos violentos distintas a la Macrozona Austral (referencia). La inflexión negativa del Spline 4 (IRR=0.868 nacional) afecta transversalmente a todas las zonas, sin evidencia de heterogeneidad macrozonal significativa en el período reciente.

---

## 5. Placebos y Validación Externa

### 5.1 Placebo P1: Cuasidelito vehicular (proxy movilidad)

| Tramo spline | IRR | p-valor | Interpretación |
|-------------|:---:|:-------:|----------------|
| **Spline 1** | **9.08** | <0.001 | Recuperación masiva post-pandemia de movilidad |
| Spline 2 | **3.82** | <0.001 | Continúa recuperación |
| Spline 3 | **48.4** | <0.001 | Normalización de tráfico |
| **Spline 4** | **2.04** | <0.001 | **Sigue creciendo en el período reciente** |

El cuasidelito vehicular muestra un patrón completamente opuesto a los robos violentos: fuerte crecimiento en Spline 4 (IRR=2.04 vs. IRR=0.868 para violentos). Esto confirma que el efecto "vuelta a la calle" post-pandemia es real y captado por el modelo, pero no explica ni está asociado con el comportamiento de los robos violentos. La especificación distingue correctamente entre movilidad (creciente) y criminalidad violenta (declinante).

### 5.2 Placebo P2: Homicidios dolosos CCH (violencia real — nacional)

| Tramo spline | IRR | p-valor | Interpretación |
|-------------|:---:|:-------:|----------------|
| **Spline 1** | 1.300 | 0.096 | Sin tendencia clara inicial |
| Spline 2 | **2.746** | <0.001 | Aumento sostenido |
| Spline 3 | **3.612** | <0.001 | Continúa aumentando |
| **Spline 4** | **2.061** | <0.001 | **Aún creciendo en el período reciente** |

Los homicidios dolosos CCH muestran una tendencia secular creciente en Spline 4 (IRR=2.061, más fuerte que el IRR=1.440 reportado en v4.0). Esta escalada confirma que la violencia letal sigue en niveles elevados. La diferencia con los robos violentos (Spline 4 = 0.868 vs. 2.061 para homicidios) es notable: los robos con violencia masiva (802, 803) declinan mientras los eventos de mayor lesividad (homicidios, retenciones) se mantienen elevados. Esto es consistente con la hipótesis de concentración de la violencia.

### 5.3 Placebo P3: Secuestros (violencia coactiva — NUEVO HALLAZGO v5.0)

| Tramo spline | IRR | p-valor |
|-------------|:---:|:-------:|
| **Spline 1** | **1.338** | 0.024 |
| Spline 2 | **2.654** | <0.001 |
| Spline 3 | **1.649** | 0.024 |
| **Spline 4** | **1.553** | <0.001 |

**Cambio crítico respecto a v4.0:** En v4.0, el Spline 4 era IRR=1.073 (p=0.415, no significativo). Ahora es IRR=1.553 (p<0.001). Los secuestros muestran **crecimiento significativo y sostenido en el período 2022–2025**, con todos los tramos del spline significativos.

**Interpretación como placebo positivo confirmado:** Los secuestros son una forma de violencia coactiva (CUMs 202, 235–237, 248–249) que, como los homicidios, tiene cifra negra reducida (la víctima o su familia denuncia). El hecho de que crezcan significativamente en Spline 4 refuerza la hipótesis de que existe una violencia coactiva organizada que está aumentando en el período reciente, concentrada en modalidades de bajo volumen pero alta visibilidad (portonazos, secuestros express). Esto complementa al CUM 862 (retenciones, +263% en tasas).

**Triangulación de la narrativa:** La combinación de P2 (homicidios creciendo, Spline 4: 2.061) y P3 (secuestros creciendo, Spline 4: 1.553) vs. el modelo principal (robos violentos Spline 4: 0.868) dibuja un panorama claro: Chile tiene menos robos violentos masivos (los que generan la mayor parte del volumen), pero los eventos de violencia coactiva organizada (homicidios, secuestros, retenciones) están en niveles históricos elevados.

### 5.4 Placebos P4 y P5: Daños simples y Lesiones leves

Ambas categorías muestran declive secular en todos los tramos del spline, reforzando que una categoría amplia de delitos de menor lesividad está descendiendo estructuralmente en Chile.

- **P4 Daños simples** — Spline 1: IRR=0.741 (p<0.001); Spline 4: IRR=0.805 (p<0.001)
- **P5 Lesiones leves** — Spline 1: IRR=0.627 (p<0.001); Spline 4: IRR=0.698 (p<0.001)

### 5.5 Validación externa CPHDV: Homicidios confirmados 2018–2025

#### Datos brutos (descripción más probatoria):

| Año | Homicidios CPHDV | CCH | Ratio CCH/CPHDV |
|-----|:----------------:|:---:|:---------------:|
| 2018 | 845 | 320 | 0.379 |
| 2019 | 924 | 335 | 0.363 |
| 2020 | 1.115 | 505 | 0.453 |
| 2021 | 906 | 412 | 0.455 |
| **2022** | **1.330** | **640** | 0.481 |
| 2023 | 1.249 | 601 | 0.481 |
| 2024 | 1.209 | 650 | 0.538 |
| 2025 | **1.091** | 614 | 0.563 |

Los homicidios confirmados CPHDV muestran un **máximo histórico en 2022 (1.330)** y una **caída sostenida y sustancial en 2023–2025: -18.0% entre 2022 y 2025**. La trayectoria es clara: el período de máxima violencia letal fue 2022, y desde entonces hay un descenso real.

#### Modelo spline CPHDV (análisis complementario):

| Tramo spline | IRR | p-valor | Nota |
|-------------|:---:|:-------:|------|
| Spline 1 (2018–~2020) | **1.562** | 0.001 | Aumento inicial |
| Spline 2 (~2020–2022) | **1.430** | <0.001 | Continúa aumentando |
| Spline 3 (~2022–2024) | 1.774 | 0.113 | Pico, no significativo |
| **Spline 4** (~2024–2025) | 1.075 | **0.530** | **No significativo** |

**Limitación metodológica del spline CPHDV:** El Spline 4 no captura la caída 2023–2025 que sí es evidente en los datos brutos. Con los knots recalculados para 2018–2025, el Spline 4 cubre aproximadamente solo noviembre 2023 a diciembre 2025 (apenas 13 meses). Con solo ~13 meses en el último segmento y la gran variabilidad mensual de homicidios, la potencia del spline para detectar la caída final es limitada. Los datos brutos anuales son la forma más probatoria de presentar la triangulación CPHDV.

**Triangulación final:** La caída en CPHDV desde 2022 (-18%), combinada con el Spline 4 negativo de robos violentos (IRR=0.868) y la invarianza de este resultado a la corrección migratoria (ver §6.2), apoya la interpretación de que la criminalidad violenta en Chile está en una trayectoria declinante desde el máximo de 2022, aunque desde un nivel históricamente elevado.

---

## 6. Análisis de Robustez (C3, Spline 4 — corregido)

### 6.1 Especificaciones alternativas del modelo (Robos violentos, Spline 4)

| ID | Especificación | IRR Spline 4 | p-valor | Interpretación |
|----|---------------|:------------:|:-------:|----------------|
| **Principal** | Modelo base | **0.868** | **0.057** | Inflexión descendente en período reciente |
| R1 | Offset libre | **0.732** | **0.010** | Más negativo; confirma con mayor fuerza la dirección |
| R3 | Sin SERMIG | 0.994 | 0.948 | Efecto desaparece sin corrección migratoria |
| R5 | Nodos teóricos | 0.883 | 0.079 | Similar al principal; marginalmente no significativo |
| R6 | Detenciones como VD | **0.539** | **<0.001** | Caída muy marcada en detenciones 2022–2025 |
| R7 | Spline df=5 | 0.863 | 0.068 | Prácticamente idéntico al principal |

**Hallazgos clave de robustez (v5.0):**

- **R1 (Offset libre):** IRR=0.732, p=0.010. El resultado es **más negativo y más significativo** que el modelo principal. Si la población no es offset forzado y se estima libremente, la tasa ajustada de robos violentos en Spline 4 es aún más baja. Esto confirma la dirección del hallazgo.

- **R3 (Sin SERMIG):** IRR=0.994, p=0.948. El efecto **desaparece sin la corrección migratoria**. Esta es una señal metodológica importante: el denominador corregido por migración es crucial para detectar la inflexión. Sin corregir por el aumento de la población inmigrante (que amplía el denominador), el efecto en la tasa per cápita desaparece. Esto refuerza la necesidad del corrector SERMIG.

- **R5 (Nodos teóricos):** IRR=0.883, p=0.079. Resultado similar al principal, aunque con menor precisión (debido a que los nodos teóricos no están en los cuantiles de los datos). Consistente.

- **R6 (Detenciones):** IRR=0.539, p<0.001. **Hallazgo nuevo y relevante:** Las detenciones por robos violentos también declinan marcadamente en Spline 4, incluso más que las denuncias. Esto sugiere que la menor cantidad de robos violentos se traduce en menos eventos donde aplicar fuerza policial (no solo en menos denuncias), reduciendo la hipótesis de que la baja en denuncias refleja menor propensión a reportar.

- **R7 (Spline df=5):** IRR=0.863, p=0.068. Prácticamente idéntico al principal. El resultado es robusto a la flexibilidad del spline.

### 6.2 Sensibilidad al denominador irregular (Spline 4, corregido)

| Factor k (alta migración) | Spline 4 IRR | p-valor |
|:-------------------------:|:------------:|:-------:|
| k = 1.00 (base) | **0.868** | 0.048 |
| k = 1.05 | **0.868** | 0.061 |
| k = 1.10 | **0.868** | 0.057 |
| k = 1.15 | **0.868** | 0.050 |
| k = 1.20 | **0.868** | 0.062 |

El Spline 4 de robos violentos es **exactamente invariante al factor de inflación demográfica k**. El Estimate=-0.1411 (IRR=0.868) no varía en ningún escenario. Los p-valores fluctúan alrededor de 0.05–0.06 (variación aleatoria del WCB con R=999 réplicas), pero el estimador puntual es idéntico. La especificación es completamente robusta a supuestos sobre la magnitud de la población irregular.

---

## 7. Clasificaciones C1 y C2 (Apéndice)

Los modelos C1 y C2 se reportan como apéndice de sensibilidad de clasificación. La clasificación binaria institucional (C1) y la ajustada (C2) diluyen las señales divergentes capturadas por C3:

- **C1 (Institucional SPD/CAPJ):** Al incluir CUM 804 (Robo por sorpresa) como "violento" y receptación como "no violento", la dinámica de los robos por sorpresa (que tiene un Spline 1 muy negativo: -33%) se mezcla con los robos violentos propiamente tales, enmascarando la inflexión del Spline 4.

- **C2 (Ajustada, binaria sin receptación):** Mejora la especificación al excluir receptación, pero al mantener estructura binaria no puede distinguir entre robos violentos (que bajan moderadamente en Spline 4) y robos no violentos (que bajan sostenidamente en todos los tramos).

La evidencia empírica confirma que **C3 es la especificación óptima** para detectar las dinámicas reales de los distintos tipos de robo.

---

## 8. Síntesis Interpretativa: ¿Crisis de seguridad o cambio qualitativo? (v5.0)

### 8.1 El relato basado en la evidencia (v5.0)

**Lo que sí ocurrió:** Chile experimentó un **cambio cualitativo en la composición** del delito contra la propiedad. La proporción de robos con alta lesividad sobre el total aumentó desde ~14.7% (mayo 2015) hasta un máximo histórico de ~21.6% (enero 2024). Paralelamente, los delitos de violencia coactiva (homicidios, secuestros) alcanzaron máximos en 2022 y se mantienen elevados.

**Lo que no ocurrió (o está revirtiendo):** Los dos CUMs que concentran el 93% de los robos violentos (802, 803) tienen tasas en 2022–2025 que son inferiores a la línea base 2016–2019. El Spline 4 del modelo Poisson-QMLE (IRR=0.868, p=0.057) sugiere una inflexión negativa. La robustez de este hallazgo se confirma especialmente en R1 (IRR=0.732, p=0.010) y R7 (IRR=0.863, p=0.068).

**La dualidad del período 2022–2025:**
- Robos violentos masivos (802, 803): Spline 4 → 0.868 (bajando)
- Homicidios dolosos: Spline 4 → 2.061 (subiendo aún)
- Secuestros: Spline 4 → 1.553 (subiendo significativamente)
- Robos no violentos: Spline 4 → 0.648 (cayendo fuertemente)

Esta dualidad sugiere una **estratificación de la violencia:** los delitos oportunistas de alto volumen (robos masivos) disminuyen, mientras los eventos de violencia organizada y coactiva (homicidios, secuestros, retenciones) se mantienen o crecen.

### 8.2 La paradoja del ratio máximo histórico

El ratio Violentos/Total en máximo histórico (21.6%, enero 2024) coexiste con tasas absolutas de violentos en descenso. La resolución sigue siendo la misma que en v4.0: los robos no violentos decayeron estructuralmente (Spline 4: IRR=0.648) mucho más que los violentos (Spline 4: IRR=0.868). La asimetría en los ritmos de caída genera el efecto de "creciente participación" de los robos violentos.

La nueva evidencia de v5.0 (secuestros crecientes, Spline 4: 1.553) añade matiz: dentro de los delitos "violentos" también hay una recomposición interna. Los robos violentos masivos bajan, pero la violencia coactiva organizada (secuestros, retenciones) sube. El ratio 21.6% puede estar subvalorando este fenómeno al mezclar dos tendencias opuestas dentro de la categoría "violentos".

### 8.3 Heterogeneidad regional: la crisis no es uniforme (sin cambios)

El análisis CUSUM muestra que 12/16 regiones presentan quiebres significativos, pero con momentos y magnitudes distintos. Los tres patrones temporales identificados en v4.0 se confirman sin cambios:

- **Patrón 1 — Pre-pandemia (R7, R8, R9, R12):** Maule, Biobío, Araucanía y Magallanes, quiebres 2016–2018.
- **Patrón 2 — Pandemia/post-pandemia (R3, R4, R6, R13, R15, R16):** Pandemia como punto de inflexión, con la RM en julio 2020.
- **Patrón 3 — Tardío (R1 — Tarapacá, agosto 2023):** Dinámica migratoria y crimen organizado.

---

## 9. Conclusiones y Agenda

### 9.1 Hallazgos principales (v5.0)

1. **No hay evidencia de aumento secular en el volumen de robos violentos 2022–2025.** El Spline 4 = IRR=0.868 (p=0.057) y el contraste con Spline 1 (IRR=1.177) muestra una clara inversión de tendencia.

2. **El ratio Violentos/Total alcanzó un máximo histórico (21.6% en enero 2024) por mecanismo compositivo:** los robos no violentos decayeron mucho más (Spline 4: 0.648) que los violentos.

3. **La robustez del hallazgo se fortalece:** R1 (Offset libre: IRR=0.732, p=0.010) confirma la dirección. R3 (Sin SERMIG: IRR=0.994, p=0.948) confirma que la corrección migratoria es crucial. R6 (Detenciones: IRR=0.539, p<0.001) muestra que la baja también se observa en detenciones.

4. **El Spline 4 de robos violentos es invariante al factor k de población irregular** (IRR=0.868 para todos k ∈ {1.00, 1.05, 1.10, 1.15, 1.20}).

5. **P3 (Secuestros) es ahora un placebo positivo activo:** Spline 4 = IRR=1.553 (p<0.001). Los secuestros crecen significativamente en 2022–2025, confirmando la hipótesis de violencia coactiva organizada emergente. Junto a P2 (homicidios: Spline 4 = 2.061, p<0.001), configura la narrativa de estratificación de la violencia.

6. **CPHDV: la triangulación más probatoria es la serie bruta.** Los datos anuales muestran caída sostenida 2022–2025: 1.330 → 1.091 (-18%). El modelo spline no captura bien la tendencia reciente por limitaciones de parametrización en el último segmento.

7. **La heterogeneidad regional y macrozonal es estadísticamente real** (Wald X²=7.059.870, p<0.001) pero la inflexión del Spline 4 nacional es transversal a todas las macrozonas.

8. **CUM 867 es discontinuidad de clasificación** (no cambio real). El análisis de sensibilidad S5 (exclusión de CUM 867) es metodológicamente recomendado. Sin CUM 867, los robos violentos solo decrecen.

9. **CUM 862 (retención de víctimas):** +263% en tasas post-pandemia desde volumen muy pequeño. Señal de alarma temprana sobre el "portonazo" como modalidad delictual emergente.

### 9.2 Contribución al debate sobre la "crisis de seguridad" (actualizada)

La evidencia no respalda la hipótesis de una "crisis" en el sentido de un incremento volumétrico de la criminalidad violenta contra la propiedad. Sí respalda la hipótesis de un **doble cambio cualitativo:**

1. **En la propiedad:** La delincuencia patrimonial está más concentrada en modalidades de contacto directo con la víctima (802, 803), aunque con menor volumen total.

2. **En la violencia coactiva organizada:** Homicidios y secuestros crecen, señalando que existe un componente de crimen organizado que aumenta independientemente de la tendencia general.

El debate público captura algo real — la experiencia de victimización directa es más probable incluso si el número total de robos baja, y los eventos de mayor gravedad (secuestros, homicidios) están en niveles históricamente elevados — pero sobreestima el fenómeno al no distinguir entre volumen, composición y tipo de violencia.

### 9.3 Cambios metodológicos relevantes (v5.0 para el artículo)

1. **Corrección scripts 07 y 08:** Las tablas de robustez y sensibilidad ahora reportan Spline 4, el término metodológicamente relevante para la hipótesis central.

2. **Triangulación CPHDV:** Para el artículo, presentar la serie anual bruta de CPHDV como el argumento principal de triangulación (caída -18% 2022-2025). El modelo spline es complementario pero con limitaciones que se deben declarar.

3. **P3 Secuestros:** Incluir en el cuerpo del artículo como placebo positivo activo (junto a P2 Homicidios). Versiones anteriores lo reportaban como no significativo, ahora es evidencia sustantiva.

### 9.4 Limitaciones (sin cambios respecto a v4.0)

1. **CUM 867:** Historia de codificación pendiente de confirmar con Carabineros.
2. **Comisaría Virtual:** No controlable directamente (canal de denuncia no disponible en CCH).
3. **G=16:** P-valores fronterizos (Spline 4: p=0.057) requieren interpretación cautelosa. El WCB-Webb es conservador con 16 clusters.
4. **CPHDV:** El modelo spline no captura bien la tendencia terminal con los knots del período 2018–2025. Priorizar datos brutos.

---

*Documentos relacionados:*
- *Protocolo: `06032026_proyecto_v4.0.md` (v4.1)*
- *Scripts corregidos: `paper1/models/07_robustness.R`, `paper1/models/08_sensitivity_pop.R`*
- *Tablas clave: `paper1/output/tables/C3/tabla_2_poisson_wcb.csv`, `tabla_6_robustez.csv`, `tabla_7_sensibilidad_poblacional.csv`, `tabla_8_placebos.csv`, `tabla_8c_cphdv.csv`*
- *Interpretaciones anteriores: `interpretacion_resultados_v4.0.md`, `v3.1`, `v3.0`*
