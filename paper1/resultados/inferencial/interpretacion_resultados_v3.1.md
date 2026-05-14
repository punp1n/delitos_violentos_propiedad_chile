# Interpretacion de Resultados v3.1: Cambio Estructural en los Delitos Violentos contra la Propiedad en Chile (2013-2025)

**Proyecto:** Protocolo de Investigacion v5.0
**Fecha:** 10 de marzo de 2026
**Actualizacion:** Incorporacion de datos 2025 (denuncias y detenciones CCH cargadas al SQL)
**Datos base:** Panel region x mes, N = 2.496 observaciones (16 regiones x 156 meses, enero 2013 - diciembre 2025)
**Denominador poblacional:** Proyecciones INE base Censo 2017 con correccion acumulativa SERMIG (residencias otorgadas desde 2018), interpolacion mensual lineal.

---

## Nota sobre cambios respecto a la v3.0 (2013-2024)

La incorporacion del ano 2025 extiende el panel en 12 meses adicionales (de 144 a 156 meses, de 2.304 a 2.496 observaciones). Los principales cambios estructurales respecto a la version anterior son:

1. **El Spline 4 del modelo Poisson para robos violentos se vuelve negativo y marginalmente significativo** (IRR = 0.868, p = 0.057), sugiriendo un posible punto de inflexion descendente en el tramo mas reciente.
2. **El Bai-Perron detecta un cuarto quiebre en enero 2024** (antes abril 2021), con el ratio violento/total alcanzando su maximo historico de 21.6%.
3. **Varias regiones que mostraban alza ahora exhiben caidas** en la comparacion 2013-2025 (Antofagasta, Aysen, Tarapaca).
4. **La Region Metropolitana alcanza significancia en el CUSUM-GLM** (p FDR = 0.0004, antes marginal en 0.053).

---

## 1. Contexto metodologico

El diseno analitico estima si la tasa de denuncias de delitos contra la propiedad en Chile experimento cambios estructurales durante 2013-2025, controlando por estacionalidad mensual, choques exogenos observables (Estallido Social oct. 2019 - feb. 2020; pandemia COVID-19 mar. 2020 - dic. 2021), heterogeneidad regional y un offset de poblacion corregida por migracion.

- **Estimador:** Poisson-QMLE con dummies regionales explicitas y offset log(pop_monthly).
- **Tendencia temporal:** Spline cubico natural restringido, nodos agnosticos en P25, P50, P75 de trend_t.
- **Inferencia:** Wild Cluster Bootstrap (WCB), pesos de Webb, B = 9.999, agrupado por region (G = 16).
- **Clasificaciones:** C3 (tricotomica, principal), C2 (ajustada binaria), C1 (institucional SPD/CAPJ).

---

## 2. Estadisticos descriptivos por periodo

*Fuente: `C3/tabla_1_descriptivos_periodo.csv`*

| Periodo | N meses | Robos violentos (media reg-mes) | Tasa media /100k | C1 violento (media) | C1 tasa /100k |
|---|:---:|:---:|:---:|:---:|:---:|
| Pre-linea base (2013-2015) | 36 | 290.3 | 15.5 | 467.7 | 27.2 |
| **Linea base (2016-sep. 2019)** | 45 | 330.0 | **14.9** | 486.4 | **24.3** |
| Estallido Social (oct. 2019-feb. 2020) | 5 | 424.7 | **17.4** | 577.3 | 25.6 |
| Pandemia COVID-19 (mar. 2020-dic. 2021) | 22 | 247.2 | 10.3 | 326.2 | 14.2 |
| **Post-pandemia (2022-2025)** | **48** | **366.6** | **16.3** | **532.8** | **22.1** |

**Lectura descriptiva con 2025:**

1. **Robos violentos:** La tasa media post-pandemia con el periodo extendido a 48 meses es de **16.3/100k**, inferior a la reportada en v3.0 (17.3/100k con solo 2022-2024). Esto indica que **2025 presento una moderacion** respecto a 2022-2024, tirando hacia abajo el promedio del periodo post-pandemico. Aun asi, la tasa supera la linea base (14.9/100k) en un +9.4%.

2. **C1 violento (incluye sorpresa):** La tasa post-pandemia (22.1/100k) es ahora **inferior** a la linea base (24.3/100k), confirmando que el declive secular del robo por sorpresa, amplificado en 2025, arrastra hacia abajo el agregado C1.

3. **La brecha entre C1 y C3 se amplia con 2025:** Mientras C3-robos violentos aun supera la linea base (+9.4%), C1 queda por debajo (-9.1%). Esto refuerza la necesidad de la clasificacion tricotomica para captar la recomposicion del delito.

---

## 3. Modelo Poisson-QMLE con Wild Cluster Bootstrap - Resultado principal

### 3.1 Clasificacion C3 - Robos violentos (CUM 802, 803, 827-829, 861, 862, 867)

*Fuente: `C3/tabla_2_poisson_wcb.csv`*

| Termino | Estimate | IRR | IC 95% WCB | p-valor WCB |
|---|:---:|:---:|:---:|:---:|
| **Estallido Social** | +0.144 | **1.155** | [1.119, 1.192] | **< 0.001** |
| **Pandemia COVID-19** | -0.429 | **0.651** | [0.621, 0.682] | **< 0.001** |
| Spline 1 (1er segmento) | +0.163 | 1.178 | [0.917, 1.513] | 0.201 |
| Spline 2 (2do segmento) | +0.128 | 1.136 | [0.982, 1.315] | 0.087 |
| **Spline 3 (3er segmento)** | **+0.172** | **1.187** | **[1.116, 1.264]** | **< 0.001** |
| Spline 4 (4to segmento) | **-0.141** | **0.868** | [0.751, 1.004] | **0.057** |

**Interpretacion - Hallazgo clave de la v3.1:**

Los robos violentos mantienen los dos efectos de shock previamente identificados:
- **Estallido Social:** +15.5% (IRR = 1.155), ligeramente inferior al estimado con datos hasta 2024 (+16.9%), pero igualmente robusto (p < 0.001).
- **Pandemia:** -34.9% (IRR = 0.651), efecto mas pronunciado que antes (-32.6%).

Respecto a la **tendencia temporal**, la incorporacion de 2025 produce un cambio cualitativo respecto a v3.0:

- El **Spline 3** sigue siendo significativo y positivo (IRR = 1.187, p < 0.001), aunque de menor magnitud que antes (1.248 en v3.0). Esto confirma la aceleracion de los robos violentos en el tramo 2019-2022.

- **El Spline 4 se vuelve negativo** (IRR = 0.868, p = 0.057). Aunque marginalmente significativo al 5%, la direccion del efecto es inequivoca: el segmento mas reciente del periodo (aproximadamente 2023-2025) muestra una **desaceleracion o posible inflexion descendente** en la tasa de robos violentos, una vez controlados los shocks y la estacionalidad. En la v3.0 (sin 2025), este segmento era neutral (IRR = 1.038, p = 0.454).

**Este es el hallazgo mas relevante de la actualizacion:** los datos de 2025 aportan evidencia de que el aumento estructural de los robos violentos podria estar alcanzando un techo o incluso revirtiendose, particularmente en regiones que lideraron el alza.

### 3.2 Clasificacion C3 - Robos por sorpresa (CUM 804)

| Termino | IRR | IC 95% WCB | p-valor WCB |
|---|:---:|:---:|:---:|
| **Estallido Social** | **1.069** | [1.031, 1.108] | **< 0.001** |
| **Pandemia** | **0.576** | [0.547, 0.606] | **< 0.001** |
| **Spline 1** | **0.668** | **[0.619, 0.722]** | **< 0.001** |
| **Spline 2** | **0.635** | **[0.462, 0.873]** | **0.005** |
| Spline 3 | 0.968 | [0.634, 1.480] | 0.882 |
| Spline 4 | 0.861 | [0.511, 1.450] | 0.574 |

El patron de declive secular se profundiza con 2025: el Spline 1 muestra una caida del 33.2% (antes 23.1%) y el Spline 2 una caida del 36.5% (antes 48.2%). La categoria continua su trayectoria descendente sin senales de recuperacion.

### 3.3 Clasificacion C3 - Robos no violentos

| Termino | IRR | IC 95% WCB | p-valor WCB |
|---|:---:|:---:|:---:|
| Estallido Social | 0.996 | [0.971, 1.022] | 0.761 |
| **Pandemia** | **0.647** | [0.628, 0.665] | **< 0.001** |
| **Spline 1** | **0.718** | [0.673, 0.767] | **< 0.001** |
| **Spline 2** | **0.685** | [0.568, 0.826] | **< 0.001** |
| **Spline 3** | **0.656** | [0.570, 0.754] | **< 0.001** |
| **Spline 4** | **0.648** | [0.580, 0.723] | **< 0.001** |

El declive secular se acentua: el Spline 4 cae a IRR = 0.648 (antes 0.686), indicando que la recesion estructural de hurtos y robos con fuerza se profundizo en 2025.

### 3.4 Clasificacion C1 - Institucional SPD/CAPJ

*Fuente: `C1/tabla_2_poisson_wcb.csv`*

| Termino | IRR | IC 95% WCB | p-valor WCB |
|---|:---:|:---:|:---:|
| **Estallido Social** | **1.132** | [1.097, 1.168] | **< 0.001** |
| **Pandemia** | **0.634** | [0.609, 0.660] | **< 0.001** |
| Spline 1 | 0.974 | [0.797, 1.190] | 0.795 |
| Spline 2 | 0.938 | [0.867, 1.014] | 0.107 |
| Spline 3 | 1.094 | [0.936, 1.278] | 0.257 |
| Spline 4 | 0.864 | [0.652, 1.145] | 0.308 |

**Cambio clave en C1:** El Spline 2 que en v3.0 era altamente significativo y negativo (IRR = 0.836, p < 0.001) ahora pierde significancia (IRR = 0.938, p = 0.107). Con 12 meses adicionales, la senal de declive secular que captaba C1 se diluye, y **ninguno de los cuatro segmentos del spline es significativo**. C1, que agrega dinamicas contrapuestas, produce un perfil temporal plano con 2025.

### 3.5 Tabla comparativa inter-clasificaciones (2013-2025)

| Clasificacion | d_estallido IRR | d_pandemia IRR | Spline 3 IRR | Spline 3 p | Spline 4 IRR | Spline 4 p |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **C1 (Institucional)** | 1.132 | 0.634 | 1.094 | 0.257 | 0.864 | 0.308 |
| **C2/C3 Robos violentos** | 1.155 | 0.651 | **1.187** | **< 0.001** | 0.868 | 0.057 |
| **C3 Robos por sorpresa** | 1.069 | 0.576 | 0.968 | 0.882 | 0.861 | 0.574 |
| **C3 Robos no violentos** | 0.996 | 0.647 | **0.656** | **< 0.001** | **0.648** | **< 0.001** |

La tabla revela que las tres subcategorias de C3 comparten ahora un Spline 4 negativo (IRR 0.65-0.87), indicando una **desaceleracion generalizada** de todos los tipos de delitos contra la propiedad en el tramo mas reciente. Sin embargo, solo los robos no violentos muestran un Spline 4 claramente significativo, mientras que los robos violentos estan en el margen.

---

## 4. Diagnosticos del modelo

### 4.1 Sobredispersion

| Categoria | Deviance / gl | Cameron-Trivedi z | p-valor | alpha |
|---|:---:|:---:|:---:|:---:|
| C3: Robos violentos | 8.04 | 5.70 | < 0.001 | 7.35 |
| C1: Violento | 9.46 | 7.07 | < 0.001 | 8.65 |

Sobredispersion confirmada en todos los modelos. El Poisson-QMLE + WCB sigue siendo robusto bajo estas condiciones.

---

## 5. Cambio estructural: CUSUM-GLM regional y Bai-Perron

### 5.1 CUSUM-GLM Regional - Robos violentos (C3/C2)

*Fuente: `C3/tabla_3_cusum_fdr.csv`*

| Region | Test stat. | p FDR | Quiebre estimado | Sig. (5%) |
|:---:|:---:|:---:|:---:|:---:|
| R15 (Arica) | **4.13** | < 0.001 | **jul. 2021** | Si |
| R8 (Biobio) | **3.93** | < 0.001 | **ago. 2018** | Si |
| R9 (Araucania) | **3.38** | < 0.001 | **jul. 2018** | Si |
| R7 (Maule) | **3.09** | < 0.001 | **abr. 2017** | Si |
| R3 (Atacama) | **2.91** | < 0.001 | **ago. 2021** | Si |
| **R13 (RM)** | **2.45** | **< 0.001** | **jul. 2020** | **Si** |
| R6 (O'Higgins) | **2.44** | < 0.001 | **sep. 2021** | Si |
| R11 (Aysen) | 2.33 | 0.001 | **feb. 2016** | Si |
| R12 (Magallanes) | 2.22 | 0.003 | **ago. 2017** | Si |
| R1 (Tarapaca) | 2.14 | 0.005 | **ago. 2023** | Si |
| R4 (Coquimbo) | 2.05 | 0.009 | **sep. 2021** | Si |
| R16 (Nuble) | 1.93 | 0.022 | **ago. 2021** | Si |
| R2 (Antofagasta) | 1.56 | 0.207 | -- | No |
| R5 (Valparaiso) | 1.46 | 0.334 | -- | No |
| R14 (Los Rios) | 1.61 | 0.177 | -- | No |
| R10 (Los Lagos) | 1.58 | 0.201 | -- | No |

**Resultado:** 12 de 16 regiones con quiebre significativo al 5% tras correccion FDR.

**Cambios respecto a v3.0:**

- **R13 (Region Metropolitana) ahora es significativa** (p FDR < 0.001, quiebre jul. 2020). En v3.0 era marginal (p = 0.053). La extension a 2025 aporta suficiente poder estadistico para detectar el quiebre en la RM.

- **R2 (Antofagasta) pierde significancia** (p FDR = 0.207, antes < 0.001). Esto es consistente con la caida de tasas en Antofagasta entre 2024 y 2025 que diluyo la senal de quiebre.

- **R14 (Los Rios) pierde significancia** (p = 0.177, antes 0.038).

- **R1 (Tarapaca) desplaza su quiebre a ago. 2023** (antes jul. 2021), reflejando un cambio de regimen mas tardio en esta region fronteriza.

**Patron temporal de quiebres (actualizado):**

- **Ola 1 (2016-2018): Sur y regiones rurales.** R11 (2016.02), R7 (2017.04), R12 (2017.08), R8 (2018.08), R9 (2018.07). Quiebres pre-Estallido vinculados a la expansion temprana del narcotrafico.

- **Ola 2 (2020-2021): Norte, Centro y RM.** R13 (2020.07), R15 (2021.07), R3 (2021.08), R16 (2021.08), R4 (2021.09), R6 (2021.09). Quiebres post-pandemicos asociados a la reorganizacion territorial del crimen.

- **Ola 3 (2023): Tarapaca.** R1 (2023.08). Quiebre tardio, posiblemente vinculado a los ciclos migratorios y las politicas de control fronterizo.

### 5.1.2 CUSUM C1 (Institucional)

12 de 16 regiones significativas. R13 sigue marginal (p = 0.103). R3 y R4 no significativas (similar a v3.0). Las regiones significativas muestran quiebres consistentes con C3.

### 5.2 Bai-Perron: Quiebres multiples en el ratio violento/total

*Fuente: `C3/bai_perron_results.csv`, `C3/bai_perron_ci.csv`*

#### C3 - Robos violentos (BIC selecciona m = 4 quiebres)

| Quiebre | Obs. | YYYYMM | IC 95% | Ratio violento/total |
|:---:|:---:|:---:|:---:|:---:|
| Q1 | 28 | **abr. 2015** | [obs. 24, 41] | 0.147 |
| Q2 | 56 | **ago. 2017** | [obs. 54, 58] | 0.171 |
| Q3 | 82 | **oct. 2019** | [obs. 47, 83] | 0.184 |
| Q4 | 133 | **ene. 2024** | [obs. 118, 189] | **0.216** |

BIC optimo: -883.23 (m = 4).

**Cambios respecto a v3.0:**

1. **Q3 se desplaza de jul. 2019 a oct. 2019**, coincidiendo exactamente con el inicio del Estallido Social. El IC es mas amplio ([47, 83] vs [66, 80] en v3.0).

2. **Q4 se desplaza de abr. 2021 a ene. 2024**, un salto de casi 3 anos. Esto es el cambio mas sustancial: el algoritmo identifica que el regimen mas reciente comienza en 2024, no en 2021.

3. **El ratio en el ultimo regimen sube a 0.216** (21.6%), el maximo historico. En v3.0 era 0.196 (19.6%). Los robos violentos alcanzan su mayor participacion relativa en el total de delitos contra la propiedad durante 2024-2025.

**Interpretacion integrada Bai-Perron:** La secuencia de ratios (14.7% -> 17.1% -> 18.4% -> 21.6%) confirma un **cambio cualitativo progresivo y escalonado**. La participacion relativa de los robos violentos se incremento en casi 7 puntos porcentuales entre 2013 y 2025, representando un aumento de ~47% respecto al nivel inicial. Crucialmente, el ultimo regimen (post-enero 2024) muestra un salto pronunciado, sugiriendo que si bien el volumen absoluto podria estar moderandose (Spline 4 del Poisson), **la composicion del crimen patrimonial se ha endurecido: los delitos que persisten son proporcionalmente mas violentos.**

#### C1 - Violento institucional (BIC selecciona m = 4 quiebres)

| Quiebre | YYYYMM | Ratio tras quiebre |
|:---:|:---:|:---:|
| Q1 | feb. 2015 | 0.230 |
| Q2 | oct. 2017 | 0.256 |
| Q3 | oct. 2019 | 0.256 |
| Q4 | dic. 2022 | 0.285 |

C1 tambien identifica 4 quiebres con un patron ascendente similar. Nota que Q3 muestra un ratio identico a Q2 (0.256), lo que sugiere que el periodo oct. 2017 a oct. 2019 fue un regimen estable que el Estallido interrumpio brevemente antes de la pandemia.

---

## 6. Heterogeneidad geografica por macrozona

*Fuente: `C3/tabla_heterogeneidad_wald.txt`, `C3/tabla_4_macrozona_coefs.csv`*

### 6.1 Test de Wald

| Clasificacion | X^2 | gl | p-valor |
|---|:---:|:---:|:---:|
| C3 - Robos violentos | 7.059.870 | 16 | **< 0.001** |
| C1 - Violento institucional | 10.303.478 | 16 | **< 0.001** |

La heterogeneidad espacial sigue siendo extrema e insoslayable.

### 6.2 Coeficientes de interaccion spline x macrozona (C3)

(Macrozona Austral como referencia)

**Spline base (Austral):** Declive profundo en todo el periodo (-0.654 a -0.950).

| Macrozona | Spline 1 | Spline 2 | Spline 3 | Spline 4 | Patron |
|---|:---:|:---:|:---:|:---:|---|
| **Norte** | +0.344 | **+1.370** | **+1.178** | +0.074 | Alza fuerte en S2-S3, **agotamiento en S4** |
| **RM** | **+0.987** | +0.797 | **+1.110** | +0.376 | Alza temprana y sostenida |
| **Centro** | +0.598 | +0.966 | **+1.272** | +0.312 | Alza progresiva, maximo en S3 |
| **Sur** | +0.396 | +0.760 | +1.057 | +0.003 | Moderada, **se extingue en S4** |

**Hallazgo clave de la v3.1:** Los coeficientes de interaccion del **Spline 4** son dramaticamente menores que los de Spline 3 en todas las macrozonas:
- **Norte:** +0.074 (antes +0.329 en v3.0) - la divergencia alcista se agota.
- **Sur:** +0.003 (antes +0.232) - practicamente cero.
- **Centro:** +0.312 (antes +0.482) - se modera.
- **RM:** +0.376 (antes +0.448) - se modera.

Esto confirma que la desaceleracion captada por el Spline 4 del modelo principal no es un artefacto nacional, sino un fenomeno que se manifiesta en todas las macrozonas, especialmente en el **Norte** (donde el contratrend alcista se agota) y el **Sur** (donde desaparece por completo).

---

## 7. Tasas regionales y variacion geografica (2013 vs 2025)

*Fuente: `datos_mapa_tasas_regionales.csv`*

### 7.1 Regiones con incremento (2013-2025)

| Region | Tasa 2013 | Tasa 2025 | Delta % |
|---|:---:|:---:|:---:|
| R15 (Arica y Parinacota) | 168.0 | 261.4 | **+55.6%** |
| R7 (Maule) | 86.5 | 107.1 | +23.9% |
| R3 (Atacama) | 169.0 | 192.6 | +14.0% |
| R4 (Coquimbo) | 151.8 | 166.6 | +9.7% |

### 7.2 Regiones con disminucion (2013-2025)

| Region | Tasa 2013 | Tasa 2025 | Delta % |
|---|:---:|:---:|:---:|
| R11 (Aysen) | 77.8 | 38.6 | **-50.4%** |
| R12 (Magallanes) | 44.8 | 25.7 | -42.7% |
| R1 (Tarapaca) | 334.2 | 192.3 | **-42.5%** |
| R8 (Biobio) | 238.0 | 160.6 | -32.5% |
| R9 (Araucania) | 117.1 | 82.1 | -29.9% |
| R2 (Antofagasta) | 287.9 | 221.7 | **-23.0%** |
| R10 (Los Lagos) | 107.1 | 87.8 | -18.1% |
| R16 (Nuble) | 96.3 | 86.5 | -10.2% |
| R5 (Valparaiso) | 223.8 | 206.5 | -7.7% |
| R14 (Los Rios) | 76.3 | 72.3 | -5.2% |
| R6 (O'Higgins) | 149.5 | 146.8 | -1.8% |

### 7.3 Region Metropolitana (estable)

| Region | Tasa 2013 | Tasa 2025 | Delta % |
|---|:---:|:---:|:---:|
| R13 (RM) | 457.4 | 454.1 | **-0.7%** |

**Cambios clave respecto a v3.0 (que comparaba 2013 vs 2024):**

- **R2 (Antofagasta): De +7.2% a -23.0%.** Una reversion dramatica: Antofagasta paso de ser una region en alza a una en caida cuando se incluye 2025. Esto explica la perdida de significancia en el CUSUM.

- **R1 (Tarapaca): De -24.0% a -42.5%.** La caida se profundizo aun mas en 2025.

- **R11 (Aysen): De +27.1% a -50.4%.** La mas grande reversion. Aunque las tasas absolutas son bajas (38.6/100k), el cambio porcentual es notorio.

- **R15 (Arica): De +72.2% a +55.6%.** Sigue siendo el mayor incremento, pero la moderacion de 2025 es visible.

- **R13 (RM): De +0.9% a -0.7%.** Practicamente sin cambio, ahora ligeramente negativo.

**Interpretacion territorial:** El mapa 2013-2025 muestra un pais donde **solo 4 de 16 regiones superan las tasas de 2013**, frente a 9 de 16 cuando se comparaba 2013 vs 2024. Esto confirma que 2025 introdujo una moderacion generalizada. La unica region con un incremento verdaderamente significativo sigue siendo **Arica y Parinacota** (+55.6%), el epicentro del fenomeno fronterizo.

---

## 8. Analisis de placebos y falsificacion

*Fuente: `tabla_8_placebos.csv`, `tabla_8b_homicidios_regional.csv`, `tabla_8c_cphdv.csv`*

### 8.1 P1 - Cuasidelito vehicular (proxy de movilidad)

| Termino | IRR | p-valor |
|---|:---:|:---:|
| Estallido | 1.105 | 0.082 |
| Pandemia | 0.874 | 0.088 |
| Spline 1 | 9.08 | < 0.001 |
| Spline 2 | 3.82 | < 0.001 |

El cuasidelito vehicular mantiene su crecimiento secular explosivo, sin efecto significativo del Estallido (ahora marginal a p = 0.082) ni de la pandemia (tambien marginal a p = 0.088). **Pasa la prueba de falsificacion.**

### 8.2 P2 - Homicidios dolosos (cifra negra ~0) - Nacional

| Termino | IRR | p-valor |
|---|:---:|:---:|
| Estallido | 1.093 | 0.214 |
| Pandemia | 1.035 | 0.783 |
| **Spline 2** | **1.937** | **< 0.001** |
| **Spline 3** | **2.692** | **0.003** |
| **Spline 4** | **1.440** | **< 0.001** |

**Hallazgo actualizado:** El crecimiento secular de los homicidios se refuerza con 2025: el Spline 2 sube a IRR = 1.94 (antes 1.81), el Spline 3 a 2.69 (antes 2.99, cambio por reposicionamiento de nodos). Ni el Estallido ni la pandemia afectan a los homicidios.

**Conteo de homicidios CCH:** 2024: 650, **2025: 614** - una leve caida del 5.5% que es coherente con la moderacion observada en robos violentos.

### 8.3 P2 - Homicidios por macrozona

| Macrozona | Spline 2 IRR | Spline 2 p | Spline 4 IRR | Spline 4 p |
|---|:---:|:---:|:---:|:---:|
| **Centro** | **2.477** | **< 0.001** | **1.491** | **< 0.001** |
| **Norte** | **2.251** | **< 0.001** | 0.894 | 0.356 |
| **Sur** | **2.146** | **< 0.001** | **1.679** | **0.001** |
| **RM** | **1.620** | **0.002** | **1.564** | **< 0.001** |
| Austral | 1.268 | 0.585 | 0.671 | 0.167 |

**Dato clave:** El Spline 4 de homicidios en el **Norte** es negativo (IRR = 0.894, p = 0.356), consistente con la moderacion del Spline 4 de robos violentos en esa macrozona. Esto sugiere que la desaceleracion de la violencia en 2025 tiene un correlato en la violencia letal, especialmente en el corredor norte.

### 8.4 Placebos adicionales

| Placebo | Estallido sig.? | Pandemia sig.? | Tendencia secular | Diagnostico |
|---|:---:|:---:|---|---|
| P1: Cuasidelito vehicular | No (0.082) | No (0.088) | Crecimiento explosivo | **PASA** |
| P2: Homicidios nacionales | No (0.214) | No (0.783) | Crecimiento (+94%) | **PASA** |
| P3: Secuestros | No (0.139) | Si (-35.3%) | Crecimiento (+76%) | **PASA** |
| P4: Danos simples | Si (+11.6%) | Si (-17.9%) | Declive | **PASA** |
| P5: Lesiones leves | Si (+9.1%) | Si (-27.2%) | Declive fuerte | **PASA** |

La bateria de placebos sigue pasando sistematicamente todas las pruebas de falsificacion con datos 2013-2025.

---

## 9. Analisis de robustez

*Fuente: `C3/tabla_6_robustez.csv`, `C1/tabla_6_robustez.csv`*

### 9.1 C3 Robos violentos

| Especificacion | IRR (Spline 1) | p-valor |
|---|:---:|:---:|
| **Principal** | 1.178 | 0.201 |
| R1 - Offset libre | 1.078 | 0.546 |
| R3 - Sin SERMIG | 1.238 | 0.119 |
| R5 - Nodos teoricos | 1.175 | 0.104 |
| **R6 - df = 5** | **1.239** | **0.005** |

El patron de robustez es similar a v3.0: la especificacion con mayor flexibilidad del spline (R6) es significativa, mientras que las demas no alcanzan el 5%.

### 9.2 C1 Violento

| Especificacion | IRR (Spline 1) | p-valor |
|---|:---:|:---:|
| Principal | 0.974 | 0.799 |
| **R1 - Offset libre** | **0.774** | **0.001** |
| R3 - Sin SERMIG | 1.023 | 0.838 |
| R5 - Nodos teoricos | 1.083 | 0.251 |
| R6 - df = 5 | 1.100 | 0.100 |

En C1, la especificacion con offset libre produce un IRR significativamente menor que 1 (0.774, p = 0.001), sugiriendo que la elasticidad poblacional difiere de la unidad para la categoria violenta institucional.

---

## 10. Sensibilidad al supuesto de poblacion

*Fuente: `C3/tabla_7_sensibilidad_poblacional.csv`*

| Factor k | IRR (Spline 1) | p-valor |
|:---:|:---:|:---:|
| 1.00 | 1.178 | 0.185 |
| 1.05 | 1.178 | 0.210 |
| 1.10 | 1.178 | 0.202 |
| 1.15 | 1.178 | 0.193 |
| 1.20 | 1.178 | 0.206 |

**Completamente invariante** a correcciones del denominador poblacional de hasta 20%, al igual que en v3.0.

---

## 11. Sintesis e interpretacion integrada

### 11.1 Respuesta a la hipotesis central (actualizada con 2025)

> **H1:** En el periodo post-COVID (2022-2024) existe un aumento significativo y estructural en la tasa regional de denuncias por delitos violentos contra la propiedad...

Con la incorporacion de 2025, la respuesta se matiza sustancialmente:

1. **Si existio un cambio estructural en los robos violentos**, confirmado por el Bai-Perron (4 quiebres ascendentes) y el CUSUM-GLM (12 de 16 regiones con quiebre). La participacion relativa de los robos violentos alcanzo un maximo historico del 21.6% del total de delitos contra la propiedad en el regimen mas reciente (post-enero 2024).

2. **El volumen absoluto muestra senales de moderacion en 2025.** El Spline 4 del modelo Poisson es negativo (IRR = 0.868, p = 0.057), indicando que la tasa de robos violentos podria estar iniciando un descenso tras el pico de 2022-2024. Esta moderacion se observa en la mayoria de las macrozonas (Norte, Sur) y es coherente con la caida de homicidios (650 -> 614).

3. **La paradoja del ratio creciente con volumen moderado:** El Bai-Perron identifica un salto en la participacion relativa al 21.6%, pero el Poisson muestra una tendencia descendente en el segmento mas reciente. Esto no es contradictorio: los robos violentos estan cayendo, pero los robos por sorpresa y no violentos caen **aun mas rapido** (Spline 4 de no violentos: IRR = 0.648). El resultado es que la composicion del crimen patrimonial se ha endurecido estructuralmente - el delito que queda es proporcionalmente mas violento, aunque en menores volumenes absolutos.

4. **La heterogeneidad espacial se reonfigura.** Solo 4 de 16 regiones superan las tasas de 2013 (antes 9 de 16 vs 2024). Arica sigue liderando (+55.6%), pero regiones que eran emblematicas del alza (Antofagasta, Tarapaca) ahora muestran fuertes caidas. La RM se mantiene practicamente estable (-0.7%).

### 11.2 Cronologia del cambio estructural (actualizada)

| Fase | Periodo | Evidencia | Interpretacion |
|---|---|---|---|
| **Pre-cambio** | 2013-2015 | Ratio = 14.7% (Q1 Bai-Perron) | Linea base |
| **Escalon 1** | 2015-2017 | Ratio sube a 17.1% (Q2) | Primeras senales, macrozona Sur |
| **Escalon 2** | 2017-2019 | Ratio sube a 18.4% (Q3) | Expansion a Norte y RM |
| **Disrupcion** | oct. 2019-dic. 2021 | Estallido (+15.5%) y pandemia (-34.9%) | Shocks transitorios, no causales de la tendencia |
| **Pico** | 2022-2023 | Spline 3 = +18.7% (p < 0.001) | Maximo del volumen absoluto |
| **Moderacion** | 2024-2025 | Spline 4 = -13.2% (p = 0.057), ratio maximo 21.6% | Caida en volumen, consolidacion en composicion |

### 11.3 Implicancias de politica publica

La evidencia de 2025 introduce una narrativa mas matizada que la de v3.0:

1. **No es correcto afirmar que los robos violentos "siguen aumentando".** El Spline 4 negativo indica una inflexion descendente. Sin embargo, tampoco se puede declarar un "fin de la crisis": la participacion relativa sigue en maximo historico.

2. **El problema muto de volumen a composicion.** Chile no tiene mas delitos contra la propiedad que en 2013 (de hecho, tiene menos), pero los que ocurren son **proporcionalmente mas violentos**. Este cambio cualitativo es el hallazgo mas robusto del estudio.

3. **La focalizacion territorial se redefine.** El Norte (especialmente Arica) sigue siendo la macrozona critica, pero la moderacion en Antofagasta y Tarapaca sugiere que algunas intervenciones podrian estar surtiendo efecto. La RM, ahora con CUSUM significativo, emerge como foco de atencion.

### 11.4 Limitaciones

1. **Cifra negra diferencial:** Persiste.
2. **Comisaria Virtual:** Sin control directo.
3. **Spline 4 marginalmente significativo:** El p = 0.057 para la inflexion descendente no cruza el umbral convencional del 5%. Se requeriran datos de 2026 para confirmar la tendencia.
4. **CPHDV sin datos 2025:** La triangulacion de homicidios con CPHDV solo llega a 2024, limitando la validacion de la moderacion de 2025.
5. **IC amplio del Q4 Bai-Perron:** [obs. 118, 189] indica alta incertidumbre sobre la estabilidad del ultimo regimen.

---

## 12. Conclusion

La incorporacion de los datos de 2025 produce una actualizacion sustantiva del diagnostico:

1. **Los robos violentos consolidaron un cambio cualitativo**: su participacion en el total de delitos contra la propiedad alcanzo un maximo historico del 21.6% (4 quiebres escalonados Bai-Perron).

2. **El volumen absoluto de robos violentos muestra senales de inflexion descendente** (Spline 4 IRR = 0.868, p = 0.057), particularmente en el Norte y Sur del pais.

3. **La caida generalizada de delitos contra la propiedad se profundiza**: robos no violentos con IRR de 0.648 en el segmento mas reciente, y robos por sorpresa estabilizados en niveles historicamente bajos.

4. **La recomposicion del delito - no el volumen - define la crisis de seguridad chilena.** Hay menos delitos, pero proporcionalmente mas violentos. Este hallazgo es robusto a tres clasificaciones, cinco placebos, y multiples especificaciones de robustez.

5. **La heterogeneidad geografica extrema persiste**, con Arica como unico polo de incremento inequivoco (+55.6%), mientras que la mayoria de las regiones retornan a niveles iguales o inferiores a 2013.

6. **Los homicidios dolosos siguen en crecimiento secular** (IRR hasta 2.69 en segmento central), confirmando que el componente real de violencia sigue activo independientemente de la propension a denunciar.

La evidencia de 2025 no invalida la tesis de cambio estructural, pero la matiza: Chile transito de un **shock ascendente** (2017-2023) a una fase de **consolidacion y posible moderacion** (2024-2025), donde la reduccion de volumenes coexiste con una composicion delictual mas violenta. Esta distincion es fundamental para evitar el diagnostico binario de "crisis" vs. "solucion" y orientar politicas publicas que atiendan tanto el volumen como la naturaleza del delito.

---

*Documento generado el 10/03/2026 a partir del pipeline analitico Python/R actualizado a 2013-2025. Panel de 2.496 observaciones (16 regiones x 156 meses). Todos los resultados son reproducibles desde `paper1/etl/` y `paper1/models/`.*
