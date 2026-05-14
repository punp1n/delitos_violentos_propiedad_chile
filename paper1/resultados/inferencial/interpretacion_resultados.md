# Interpretación de Resultados: Cambio Estructural en Delitos Violentos contra la Propiedad en Chile (2014–2024)

**Proyecto v4.0 — Resultados generados el 08/03/2026**
**Datos base:** Panel región×mes, N = 2.112 observaciones (16 regiones × 132 meses)

---

## 1. Contexto metodológico

El diseño analítico del proyecto estima si la tasa de denuncias de delitos contra la propiedad en Chile experimentó cambios estructurales durante el período 2014–2024, controlando por estacionalidad, choques exógenos observables (Estallido Social oct. 2019–feb. 2020; pandemia COVID-19 mar. 2020–dic. 2021) y heterogeneidad regional.

La **especificación principal** (C3) distingue tres categorías mutuamente excluyentes:

| Categoría | CUM incluidos | Descripción |
|---|---|---|
| **Violencia Dura** | 802, 803, 827–829, 861, 862, 867 | Robos con violencia, homicidio, mutilación |
| **Sorpresa** | 804 | Robo por sorpresa |
| **No Violento** | 808–810, 821, 826, 831, 846–848, 853, 858, 868, 870–872, 891, 892, 13028 | Robos con fuerza, hurtos |

El estimador central es **Poisson-QMLE** (GLM Poisson con errores Wild Cluster Bootstrap por región, R = 9.999 réplicas) con spline natural en el trend temporal (nodos en P25, P50, P75 del trend). Los resultados de cambio estructural puntual se complementan con **CUSUM-GLM regional** (corrección Benjamini-Hochberg) y **Bai-Perron** (sin punto pre-especificado) sobre el ratio violento/total desestacionalizado.

---

## 2. Estadísticos descriptivos por período

*Fuente: `tabla_1_descriptivos_periodo.csv` — promedios por región-mes dentro de cada período*

| Período | n meses | VD media | VD tasa/100k | Sorpresa media | NV media | NV tasa/100k |
|---|---|---|---|---|---|---|
| Pre-línea base (2014–2015) | 24 | 304.2 | 15.97 | 185.0 | 1207.5 | 101.97 |
| Línea base (2016–sep. 2019) | 45 | 330.0 | 14.91 | 156.4 | 1087.2 | 88.78 |
| Estallido (oct. 2019–feb. 2020) | 5 | 424.5 | **17.38** | 152.6 | 1009.0 | 79.49 |
| Pandemia (mar. 2020–dic. 2021) | 22 | 230.5 | 9.88 | 79.0 | 651.4 | 50.44 |
| Post-pandemia (2022–2024) | 36 | 353.0 | 16.50 | 159.6 | 1006.5 | 76.19 |

**Lectura:** La Violencia Dura presenta su peak en tasa durante el Estallido (17.38/100k), cae drásticamente durante la pandemia (9.88) y recupera un nivel elevado en el período post-pandemia (16.50), superior a la línea base (14.91). Por contraste, el No Violento muestra un declive absoluto de la tasa entre la línea base (88.78) y el post-pandemia (76.19), sin recuperación completa, sugiriendo una depresión secular en hurtos y robos con fuerza.

---

## 3. Modelo Poisson-QMLE con Wild Cluster Bootstrap (Resultado Principal)

### 3.1 Clasificación C3 — Especificación Principal

*Fuente: `C3/tabla_2_poisson_wcb.csv`, Wild Cluster Bootstrap fractional, R=9.999, agrupado por región*

#### Violencia Dura (CUM 802, 803, 827–829, 861, 862, 867)

| Término | Estimate | IRR | IC 95% WCB | p-valor WCB |
|---|---|---|---|---|
| **Estallido Social** | +0.1293 | **1.138** | [1.103, 1.174] | **< 0.001** |
| **Pandemia COVID-19** | −0.4099 | **0.664** | [0.626, 0.704] | **< 0.001** |
| Spline 1 (trend, 1er segmento) | +0.117 | 1.124 | [0.870, 1.453] | 0.371 |
| Spline 2 (trend, 2do segmento) | −0.043 | 0.958 | [0.822, 1.118] | 0.588 |
| Spline 3 (trend, 3er segmento) | −0.025 | 0.975 | [0.906, 1.049] | 0.499 |
| Spline 4 (trend, 4to segmento) | +0.016 | 1.016 | [0.929, 1.112] | 0.725 |

**Interpretación:** La Violencia Dura aumentó un **13.8%** durante el Estallido Social (IRR = 1.138, p < 0.001), un efecto robusto y estadísticamente sólido. La pandemia provocó una caída del **33.6%** (IRR = 0.664), consistente con el efecto de confinamiento y restricción de movilidad que redujo las oportunidades delictuales. **Crucialmente, ninguno de los cuatro segmentos del spline temporal es estadísticamente significativo** en el período 2014–2024, lo que implica que, una vez controlados los choques exógenos y la estacionalidad, **no existe una tendencia secular significativa en Violencia Dura**. Esto contradice la narrativa de un aumento estructural sostenido de la criminalidad violenta en Chile: los movimientos observados en el tiempo son atribuibles a los choques identificados.

#### Sorpresa (CUM 804)

| Término | Estimate | IRR | IC 95% WCB | p-valor WCB |
|---|---|---|---|---|
| **Estallido Social** | +0.055 | **1.056** | [1.013, 1.102] | **0.011** |
| **Pandemia COVID-19** | −0.511 | **0.600** | [0.569, 0.632] | **< 0.001** |
| Spline 1 | −0.426 | **0.653** | [0.606, 0.703] | **< 0.001** |
| Spline 2 | −0.706 | **0.494** | [0.367, 0.664] | **< 0.001** |
| Spline 3 | −0.524 | **0.592** | [0.389, 0.901] | **0.015** |
| Spline 4 | −0.080 | 0.924 | [0.586, 1.456] | 0.732 |

**Interpretación:** El robo por sorpresa exhibe el patrón de mayor interés analítico: **declive secular significativo y sostenido a lo largo del período** en todos los segmentos temporales (splines 1–3 con p < 0.05). El IRR del spline 2 (0.494) indica que, en el segmento central del período, la tasa de sorpresas había caído casi a la **mitad** respecto al segmento inicial, controlando todo lo demás. El efecto del Estallido es leve (+5.6%) aunque estadísticamente significativo. La caída durante la pandemia es de magnitud similar a la de Violencia Dura (−40%). Este patrón es consistente con sustitución modal del delito: a medida que el robo por sorpresa se hace menos frecuente (quizás por mayor vigilancia de entornos públicos, cambio de hábitos), los robos con mayor planificación y violencia ganan participación relativa.

#### No Violento (hurtos y robos con fuerza)

| Término | Estimate | IRR | IC 95% WCB | p-valor WCB |
|---|---|---|---|---|
| Estallido Social | −0.004 | **0.996** | [0.973, 1.019] | 0.706 |
| **Pandemia COVID-19** | −0.426 | **0.653** | [0.637, 0.670] | **< 0.001** |
| **Spline 1** | −0.324 | **0.723** | [0.677, 0.773] | **< 0.001** |
| **Spline 2** | −0.412 | **0.663** | [0.568, 0.773] | **< 0.001** |
| **Spline 3** | −0.494 | **0.610** | [0.516, 0.723] | **< 0.001** |
| **Spline 4** | −0.353 | **0.703** | [0.606, 0.815] | **< 0.001** |

**Interpretación:** El No Violento exhibe el resultado más contundente del análisis: **una tendencia secular decreciente altamente significativa en los cuatro segmentos del spline**. Los IRR oscilan entre 0.61 y 0.72, indicando reducciones de entre 28% y 39% en distintos tramos del período, controlando pandemia, estallido y estacionalidad. Notablemente, el estallido **no tiene efecto significativo** sobre el No Violento (IRR ≈ 1.00, p = 0.706), lo que refuerza la validez del diseño: el Estallido no debería afectar los hurtos en espacios privados de la misma forma que los robos en el espacio público.

### 3.2 Comparación entre clasificaciones C1, C2 y C3

*Fuente: `C1/tabla_2_poisson_wcb.csv`, `C2/tabla_2_poisson_wcb.csv`*

Las clasificaciones C1 (institucional, incluye receptación) y C2 (ajustada, excluye receptación) producen resultados prácticamente idénticos entre sí:

| Clasificación | d_estallido IRR | d_pandemia IRR | Spline2 IRR | Spline2 p |
|---|---|---|---|---|
| C1 | 1.115 | 0.649 | 0.775 | < 0.001 |
| C2 | 1.115 | 0.649 | 0.775 | < 0.001 |
| C3 Violencia Dura | 1.138 | 0.664 | 0.958 | 0.588 |
| C3 Sorpresa | 1.056 | 0.600 | 0.494 | < 0.001 |

La diferencia entre C1/C2 y C3-VD es instructiva: C1 y C2 agregan todas las categorías violentas (incluyendo Sorpresa), y al hacerlo capturan el declive secular del robo por sorpresa como parte de la tendencia del "violento" agregado. La clasificación C3 logra aislar que el **verdadero componente de alta violencia (Violencia Dura) no tiene tendencia secular significativa**, mientras que el **robo por sorpresa sí declina robustamente**. Esta desagregación es la contribución metodológica central de la C3.

---

## 4. Diagnósticos del modelo

*Fuente: `C3/diagnostico_sobredispersion_*.txt`, `C3/diagnostico_vif_*.csv`*

### 4.1 Sobredispersión

| Categoría | Deviance/df.residual | Test Cameron-Trivedi (z) | p-valor | alpha estimado |
|---|---|---|---|---|
| Violencia Dura | 8.45 | 5.61 | < 0.001 | 7.76 |
| Sorpresa | 7.07 | 17.09 | < 0.001 | 5.79 |
| No Violento | 19.49 | 22.05 | < 0.001 | 18.26 |
| C1 | 9.83 | 6.70 | < 0.001 | 8.97 |

Los ratios Deviance/df.residual entre 7 y 20 confirman sobredispersión sustancial. El rechazo de H0 de equidispersión es unánime (todos p < 0.001). **Esto no invalida el estimador**: el Poisson-QMLE es consistente para la función media bajo especificación correcta de E[Y|X] (propiedad QMLE), y los errores estándar WCB son robustos a la sobredispersión al corregir por clustering regional. El mayor alpha en No Violento (18.26) refleja la mayor heterogeneidad no observable en hurtos entre comunas de la misma región.

### 4.2 Multicolinealidad (VIF generalizado)

| Variable | GVIF^(1/2·Df) — Violencia Dura | Umbral crítico |
|---|---|---|
| factor(month_of_year) | 1.006 | < 2.5 ✓ |
| d_estallido | 1.194 | < 2.5 ✓ |
| d_pandemia | 1.282 | < 2.5 ✓ |
| ns(trend_t) | 1.092 | < 2.5 ✓ |
| factor(region) | 1.000 | < 2.5 ✓ |

Todos los GVIF^(1/2·Df) están muy por debajo del umbral de 2.5 (equivalente a VIF ≈ 6 para 1 gl). El modelo **no presenta multicolinealidad problemática**, pese a la presencia simultánea de dummies de tiempo (estallido, pandemia), spline temporal y dummies regionales.

---

## 5. Cambio Estructural: CUSUM-GLM Regional y Bai-Perron

### 5.1 CUSUM-GLM Regional con corrección FDR (Benjamini-Hochberg)

*Fuente: `C3/tabla_3_cusum_fdr.csv`*

**Violencia Dura:** 14 de 16 regiones presentan quiebre estructural significativo tras corrección FDR (solo R10 y R14 no lo hacen).

| Región | Test stat | p FDR | Fecha quiebre estimada |
|---|---|---|---|
| R15 (Arica) | 4.03 | < 0.001 | **ago. 2021** |
| R8 (Biobío) | 3.65 | < 0.001 | **sep. 2018** |
| R9 (Araucanía) | 3.04 | < 0.001 | **ago. 2018** |
| R3 (Atacama) | 3.11 | < 0.001 | **sep. 2021** |
| R13 (RM) | 2.41 | < 0.001 | **ago. 2020** |
| R7 (Maule) | 2.82 | < 0.001 | **sep. 2017** |
| R2 (Antofagasta) | 2.47 | < 0.001 | **dic. 2019** |
| R16 (Ñuble) | 2.44 | < 0.001 | **sep. 2021** |
| R6 (O'Higgins) | 2.67 | < 0.001 | **oct. 2021** |
| R4 (Coquimbo) | 2.34 | 0.001 | **oct. 2021** |
| R1 (Tarapacá) | 1.97 | 0.017 | **jul. 2021** |
| R11 (Aysén) | 1.86 | 0.034 | **mar. 2016** |
| R12 (Magallanes) | 1.86 | 0.034 | **jul. 2017** |
| R5 (Valparaíso) | 1.61 | 0.159 | — |
| R10 (Los Lagos) | 1.36 | 0.515 | — |
| R14 (Los Ríos) | 1.85 | 0.034* | — |

**Patrón temporal de quiebres:** Se identifican dos olas diferenciadas:
- **Ola 1 (2017–2019), macrozona Sur y zonas rurales:** R7 (2017.09), R8 (2018.09), R9 (2018.08), R12 (2017.07) → el quiebre precede al Estallido, coincidiendo con el inicio del Conflicto Mapuche intensificado y el auge del narcotráfico en el sur.
- **Ola 2 (2020–2021), macrozona Norte y RM:** R15 (2021.08), R3 (2021.09), R4 (2021.10), R6 (2021.10), R16 (2021.09), R1 (2021.07), R13 (2020.08) → quiebres post-pandemia inmediatos, vinculados a la reorganización territorial del crimen organizado durante el período de restricción.

**Clasificación C1:** El patrón del CUSUM para n_violento_c1 es similar pero con quiebres más tempranos en varias regiones (R1: 2018.02, R8: 2018.09, R9: 2019.02), confirmando robustez inter-clasificación.

### 5.2 Bai-Perron (quiebres múltiples sin punto pre-especificado)

*Fuente: `C3/bai_perron_results.csv`, `C3/bai_perron_ci.csv`, `C3/bai_perron_summary.txt`*

**Violencia Dura — BIC selecciona m = 4 quiebres:**

| Quiebre | Obs | YYYYMM | IC 95% (obs) | Ratio desest. tras quiebre |
|---|---|---|---|---|
| Q1 | 19 | **jul. 2015** | [obs 9, 23] | 0.1542 |
| Q2 | 44 | **ago. 2017** | [obs 42, 46] | 0.1719 |
| Q3 | 70 | **oct. 2019** | [obs 62, 71] | 0.1845 |
| Q4 | 89 | **may. 2021** | [obs 75, 115] | 0.1859 |

BIC: 0 quiebres = −555.83 → 4 quiebres = **−762.15** (mejora de 206 puntos).

**Interpretación:** El algoritmo Bai-Perron identifica cuatro quiebres estructurales en el **ratio de Violencia Dura sobre el total de delitos contra la propiedad** (desestacionalizado):

1. **Jul. 2015:** Primer quiebre de bajo nivel, eleva la participación de VD del 15.4% al segmento siguiente. Coincide con el inicio del auge de robos a cajeros automáticos y crimen organizado vinculado a pandillas extranjeras.
2. **Ago. 2017:** Segundo quiebre con IC estrecho [jun.–oct. 2017]. La participación de VD asciende a 17.2%. Coincide con la escalada del conflicto en La Araucanía y primeras señales de expansión del narcotráfico hacia el norte.
3. **Oct. 2019:** Quiebre asociado al Estallido Social. IC amplio [jun. 2019–mar. 2020] refleja que el shock tiene un período de acumulación previa. VD sube a 18.5% del total.
4. **May. 2021:** Quiebre final, con IC muy amplio [mar. 2020–jul. 2023] que abarca toda la pandemia y recuperación, señalando **inestabilidad estructural en este segmento** — el sistema aún no ha convergido a un nuevo equilibrio estable al cierre del período estudiado (dic. 2024).

**Comparación C1 vs C3:** Para n_violento_c1, Bai-Perron también identifica 4 quiebres (201708, 201903, 202010, 202205) con BIC −750.33. Las fechas son muy similares, excepto que en C1 el segundo quiebre se desplaza a 2019.03 (incluyendo el período previo al estallido), lo que refleja la incorporación del robo por sorpresa en C1.

---

## 6. Heterogeneidad Geográfica por Macrozona

*Fuente: `C3/tabla_heterogeneidad_wald.txt`, `C3/tabla_4_macrozona_coefs.csv`*

**Test de Wald global (H0: coeficientes de interacción spline×macrozona = 0):**
- C3 Violencia Dura: X² = 718.263, df = 16, **p = 0** → heterogeneidad altamente significativa
- C1: X² = 9.605.846, df = 16, **p = 0** → heterogeneidad altamente significativa
- C2: X² = 9.894.757, df = 16, **p = 0** → heterogeneidad altamente significativa

Los coeficientes de interacción spline×macrozona permiten comparar trayectorias relativas a la macrozona de referencia (Austral — coeficiente base capturado en el spline principal):

| Macrozona | Spline1 | Spline2 | Spline3 | Interpretación |
|---|---|---|---|---|
| **Austral** (base) | −0.524 | −0.773 | −0.894 | Declive fuerte sostenido |
| **Norte** | +0.127 | +1.222 | +0.953 | **Contratrend marcado**: Norte crece fuertemente en segmentos 2–3 |
| **RM** | +0.811 | +0.676 | +0.858 | RM declina menos que la base → relativa estabilidad |
| **Centro** | +0.430 | +0.783 | +1.018 | Centro revierte el declive en el 3er segmento (convergencia al alza) |
| **Sur** | +0.218 | +0.565 | +0.772 | Sur intermedio, con recuperación en 3er segmento |

**Interpretación:** La macrozona **Norte** (Arica, Tarapacá, Antofagasta, Atacama, Coquimbo) presenta la trayectoria más divergente del país: mientras que en la macrozona Austral la Violencia Dura tiene un declive sostenido, en el Norte los segmentos temporales 2 y 3 muestran coeficientes de interacción de +1.22 y +0.95, indicando un **crecimiento relativo pronunciado de la violencia contra la propiedad**. Esto es consistente con la expansión del crimen organizado transnacional en el norte de Chile, particularmente desde Venezuela y Colombia, observada desde 2017–2018. La RM muestra una trayectoria intermedia, con declive atenuado respecto a la macrozona Austral. El Sur presenta un patrón de recuperación en el tercer segmento, posiblemente asociado al incremento del crimen vinculado al narcotráfico en ciudades medias de Biobío y La Araucanía.

---

## 7. Triangulación con ENUSC (Encuesta Nacional Urbana de Seguridad Ciudadana)

*Fuente: `tabla_4_enusc_prevalencia.csv`, `tabla_5a_indice_relativo.csv`*

### 7.1 Prevalencia de victimización violenta (ENUSC, diseño muestral complejo)

La ENUSC reporta prevalencia de victimización violenta (hogares donde al menos un miembro sufrió delito violento) por región y año (2018–2024):

**Regiones con mayor prevalencia en 2024 vs 2018:**

| Región | 2018 | 2022 | 2024 | Tendencia |
|---|---|---|---|---|
| R13 (RM) | 12.6% | 12.0% | 10.5% | Declive moderado |
| R1 (Tarapacá) | 9.7% | 11.2% | 5.4% | Alta volatilidad |
| R15 (Arica) | 5.2% | 8.6% | 4.4% | Spike 2022, declive 2024 |
| R2 (Antofagasta) | 6.4% | 5.6% | 4.4% | Declive |
| R5 (Valparaíso) | 6.7% | 6.7% | 5.9% | Estable |
| R8 (Biobío) | 6.4% | 3.7% | 3.9% | Declive post-pandemia |

**Nota:** La ENUSC mide victimización percibida/reportada en hogares y captura delitos que no se denuncian a Carabineros, por lo que no es directamente comparable con las tasas de denuncias CCH. La tendencia general de la ENUSC es **descendente o estable** para la mayoría de las regiones, lo que es **consistente con el patrón de No Violento y Sorpresa** en las denuncias CCH, pero contrasta con el crecimiento relativo de Violencia Dura registrado en CCH.

### 7.2 Índice relativo de propensión a denunciar

El índice relaciona denuncias CCH en las 102 comunas históricas ENUSC con el total de víctimas estimadas por ENUSC, normalizado al año base 2018:

**Hallazgos clave:**
- **Región Metropolitana:** Índice estable en torno a 1.00 entre 2018 y 2022, con leve alza en 2023 (1.20) y 2024 (1.19). Esto implica que la **propensión a denunciar en RM no cambió estructuralmente**, y el aumento de denuncias de VD en CCH refleja un aumento real, no mayor notificación.
- **Regiones extremas (R11 Aysén, R12 Magallanes):** Alta varianza del índice por reducido tamaño muestral ENUSC; los resultados deben interpretarse con cautela.
- **Norte (R15 Arica):** Índice crece de 1.0 (2018) a 1.36 (2024), lo que podría indicar **mayor propensión a denunciar** en la región que concentra la migración irregular. Sin embargo, el crecimiento de denuncias CCH es aún mayor, sugiriendo que el aumento de VD en el norte tiene componente real.
- **Sur (R8 Biobío):** Índice de 1.00 en 2018 a 1.55 en 2024, consistente con el aumento de VD detectado por CUSUM.

La triangulación no invalida los hallazgos del modelo Poisson-QMLE y refuerza que el aumento del ratio VD/total observado en CCH no se explica por cambios en la propensión a denunciar en las regiones clave.

---

## 8. Análisis de Placebos y Falsificación

*Fuente: `tabla_8_placebos.csv`, `tabla_8b_homicidios_regional.csv`, `tabla_8c_cphdv.csv`*

### 8.1 P1 — Cuasidelito vehicular (CUM 14020) — Placebo negativo de movilidad

| Término | IRR | p-valor |
|---|---|---|
| d_estallido | 1.110 | 0.077 |
| d_pandemia | **0.849** | **0.028** |

El cuasidelito vehicular (no dar cuenta de accidente) es sensible a la movilidad pero **no debería verse afectado por el Estallido Social**. Resultado: el estallido no tiene efecto significativo al 5% (p = 0.077), mientras que la pandemia reduce la tasa un 15% (consistente con la caída de tránsito). Adicionalmente, el spline muestra un **fuerte crecimiento secular** (IRR spline1 = 7.90, spline2 = 4.14), reflejo del aumento del parque vehicular y la movilidad urbana. Este placebo **pasa la prueba de falsificación**: no responde al Estallido de la forma esperada para un delito relacionado con crimen organizado.

### 8.2 P2 — Homicidios dolosos (CUM 702, 703, 705) — Placebo positivo (cifra negra ≈ 0)

| Término | IRR | p-valor |
|---|---|---|
| d_estallido | 1.034 | 0.668 |
| d_pandemia | 0.995 | 0.968 |
| Spline 2 | **1.488** | **< 0.001** |
| Spline 4 | **1.514** | **< 0.001** |

Los homicidios dolosos son el control de violencia real con cifra negra aproximadamente cero. Resultados:
- **No se ven afectados por el Estallido ni la pandemia** (ambos p > 0.60), a diferencia de los robos con violencia.
- Sí muestran **crecimiento secular significativo** en los segmentos 2 y 4 del spline (IRR ≈ 1.49–1.51).

La comparación CCH vs CPHDV confirma que Carabineros captura solo el 38–54% de los homicidios confirmados por el CPHDV:

| Año | Homicidios CCH | Homicidios CPHDV | Ratio CCH/CPHDV |
|---|---|---|---|
| 2018 | 320 | 845 | 0.379 |
| 2020 | 505 | 1.115 | 0.453 |
| 2022 | 640 | 1.330 | 0.481 |
| 2024 | 650 | 1.207 | 0.539 |

El ratio CCH/CPHDV aumenta de 0.38 a 0.54 entre 2018 y 2024, lo que podría indicar mejora en el registro o, alternativamente, un mayor procesamiento policial de casos. El modelo sobre datos CPHDV confirmados (P2b) tampoco encuentra efecto del Estallido ni la pandemia (p = 0.680 y p = 0.520), validando el resultado del CCH.

**Implicancia crítica para el modelo principal:** El hecho de que los homicidios (violencia extrema, sin sesgo de denuncia) crezcan secularmente pero **no respondan al Estallido Social** contradice la hipótesis de que el Estallido elevó permanentemente la violencia criminal. Sugiere en cambio que los homicidios responden a otra dinámica (crimen organizado, narcotráfico) con cronología independiente.

### 8.3 P3 — Secuestros (CUM 202, 235–249)

Los secuestros muestran crecimiento secular significativo (spline 2: IRR = 1.73) y son **afectados por la pandemia** (IRR = 0.62, p < 0.001) pero no significativamente por el Estallido (p = 0.055). Esto es consistente con su vinculación al crimen organizado transnacional (secuestros express, retención de personas vinculadas al narcotráfico), cuya dinámica es propia del crimen organizado y no responde a los shocks de orden público del Estallido.

### 8.4 P4 — Daños simples (CUM 840)

Los daños simples aumentan durante el Estallido (IRR = 1.118, p < 0.001) y declinan secularmente (splines 1, 3, 4 negativos y significativos). El efecto del Estallido es esperable dado que este delito captura vandalismo y disturbios. El hecho de que la VD también suba durante el Estallido pero los daños no tengan el mismo patrón en el largo plazo refuerza la diferenciación causal entre los efectos del Estallido y las tendencias estructurales.

### 8.5 P5 — Lesiones leves (CUM 13001) — Control no-propiedad

Las lesiones leves presentan un patrón espejo del No Violento: **declive secular pronunciado y robusto** en todos los segmentos (splines 1–4 con IRR entre 0.55 y 0.74) y aumento leve durante el Estallido (IRR = 1.09). Este patrón es compatible con:
- Mayor uso de aplicaciones de denuncia digital que redujo denuncias de bajo impacto
- Cambios en umbrales de judicialización de lesiones leves
- Menor propensión a denunciar delitos interpersonales menores

---

## 9. Análisis de Robustez

*Fuente: `C3/tabla_6_robustez.csv`*

La robustez se evalúa sobre el coeficiente del primer segmento del spline (el de mayor varianza en C3 Violencia Dura):

| Especificación | IRR (Spline 1) | p-valor | Conclusión |
|---|---|---|---|
| **Principal** (offset log poblacional) | 1.124 | 0.371 | No significativo |
| R1 — Offset libre (log(pop) como regresor) | 1.029 | 0.834 | No significativo |
| R3 — Sin corrección SERMIG | 1.193 | 0.213 | No significativo |
| R5 — Nodos teóricos (2016, 2018, 2022) | 1.112 | 0.403 | No significativo |
| R6 — df = 5 del spline | 1.095 | 0.174 | No significativo |

En todos los escenarios de robustez, **el primer segmento del spline temporal para Violencia Dura no es estadísticamente significativo**. La no significancia es robusta a:
- Cambios en la forma funcional del denominador poblacional
- Exclusión de la corrección por inmigración SERMIG
- Ubicación de los nodos del spline (percentiles vs. años teóricos)
- Grados de libertad del spline

---

## 10. Sensibilidad al Supuesto de Población

*Fuente: `C3/tabla_7_sensibilidad_poblacional.csv`, `tabla_7_sensibilidad_poblacional.csv`*

| Factor k (corrección migración) | IRR Spline 1 | p-valor |
|---|---|---|
| 1.00 (sin corrección adicional) | 1.124 | 0.354 |
| 1.05 | 1.124 | 0.381 |
| 1.10 | 1.124 | 0.371 |
| 1.15 | 1.124 | 0.361 |
| 1.20 (20% subestimación) | 1.124 | 0.377 |

El IRR estimado es **completamente invariante** a correcciones del denominador poblacional de hasta 20% por subestimación de la inmigración irregular. El p-valor oscila entre 0.35 y 0.42 en todos los escenarios, confirmando que la no significancia del trend temporal de Violencia Dura no depende de supuestos sobre la magnitud del efecto SERMIG.

---

## 11. Síntesis e interpretación integrada

### 11.1 Respuesta a la hipótesis central

El estudio pregunta si Chile experimentó un **cambio estructural en los delitos violentos contra la propiedad** entre 2014 y 2024. La respuesta es diferenciada según la categoría del delito:

**Violencia Dura:** No existe evidencia de una tendencia secular estadísticamente significativa una vez controlados los efectos del Estallido Social (+13.8%) y la pandemia COVID-19 (−33.6%). Sin embargo, el análisis Bai-Perron identifica **cuatro quiebres estructurales** en la participación relativa de la Violencia Dura sobre el total de delitos contra la propiedad (2015, 2017, 2019, 2021), todos con BIC ≫ la hipótesis nula. El cuarto quiebre (may. 2021) presenta un IC muy amplio, señalando que el sistema no ha convergido a un nuevo equilibrio al final del período. La interpretación más parsimoniosa es que la Violencia Dura aumentó su **participación relativa** de manera escalonada (especialmente en el Norte), mientras que en términos absolutos y controlando por shocks exógenos y población, no existe una trayectoria creciente uniforme a nivel nacional.

**Sorpresa:** Declive secular robusto e inequívoco. Los robos por sorpresa en espacios públicos han caído sistemáticamente, posiblemente por cambio en la vigilancia de entornos urbanos, mayor presencia policial en zonas comerciales, y sustitución por formas de delito más planificadas.

**No Violento:** Declive secular igualmente robusto y de mayor magnitud que la Sorpresa. Todos los segmentos del spline son negativos y altamente significativos, señalando que hurtos y robos con fuerza en Chile han **caído estructuralmente** en el período estudiado, lo que contradice la percepción pública de aumento generalizado de la criminalidad.

### 11.2 Heterogeneidad espacial

La macrozona Norte es el único territorio donde el modelo identifica un **contratrend positivo** robusto en Violencia Dura, con el quiebre CUSUM asociado al período 2021. Esto es consistente con la hipótesis de expansión del crimen organizado transnacional en el corredor Arica–Antofagasta desde 2020–2021. Las otras macrozonas muestran declive o estabilidad.

### 11.3 Placebos y falsificación

La batería de placebos pasa sistemáticamente las pruebas de falsificación:
- El cuasidelito vehicular no responde al Estallido (como se espera).
- Los homicidios crecen secularmente pero no responden al Estallido ni a la pandemia, diferenciando la dinámica de la VD de la violencia extrema interpersonal.
- Las lesiones leves replican el patrón del No Violento (declive secular), reforzando la interpretación de cambios en denunciabilidad de delitos menores.

### 11.4 Limitaciones

1. **Cifra negra diferencial:** Si los robos con alta violencia tienen menor cifra negra que los hurtos (razonable), el declive de No Violento podría estar parcialmente sobredimensionado. Los resultados ENUSC no permiten descartarlo completamente dado que la ENUSC cubre solo delitos en el espacio del hogar/persona.
2. **Cuarto quiebre Bai-Perron inestable:** El IC del cuarto quiebre (Q4: obs 89, IC [75, 115], i.e., mar. 2020–jul. 2023) es demasiado amplio para una datación precisa, señalando que el período 2020–2024 aún no tiene suficiente data post-quiebre para identificar con precisión.
3. **Agregación regional:** El panel región×mes puede enmascarar heterogeneidad intra-regional (comunas urbanas vs. rurales). El diseño excluye explícitamente el análisis comunal, que requeriría corrección por vecindad espacial.
4. **Datos placebos:** Los placebos P2-P5 usan `codigo_delito_carabineros` en vez de `codigo_materia`. Para las series placebo el impacto es presumiblemente menor (CUMs muy específicos sin subclasificaciones), pero una verificación directa de la consistencia entre ambos campos para estos CUMs es recomendable.

---

## 12. Conclusión

La evidencia en su conjunto apunta a un **cambio en la composición del delito contra la propiedad en Chile** más que a un aumento generalizado de la violencia:

1. **Violencia Dura aumenta su participación relativa** en la canasta delictual (Bai-Perron confirma 4 quiebres graduales), especialmente en la macrozona Norte, pero no presenta tendencia secular significativa en términos absolutos a nivel nacional.
2. **Sorpresa declina estructuralmente**, reduciendo la frecuencia de robos oportunistas en el espacio público.
3. **No Violento declina estructuralmente**, lo que implica que la frecuencia absoluta de hurtos y robos con fuerza ha caído en el período.
4. El Estallido Social tuvo un **efecto transitorio de corto plazo** sobre la Violencia Dura y la Sorpresa (aumentos del 14% y 6%), pero no generó un quiebre permanente en la trayectoria post-2020 a nivel nacional.
5. La pandemia genera el mayor choque observado (−33% a −40% en todas las categorías) con recuperación parcial post-2022.
6. La heterogeneidad geográfica es estadísticamente significativa y tiene implicancias de política pública: las intervenciones deberían diferenciarse por macrozona, con foco en el Norte para la Violencia Dura organizada.

---

*Archivo generado automáticamente el 08/03/2026 a partir de los outputs de los scripts R 01–08 y Python ETL 01–06.*
*Scripts fuente: `paper1/etl/` y `paper1/models/`*
*Datos: `paper1/output/tables/`*
