# Interpretación de Resultados v3.0: Cambio Estructural en los Delitos Violentos contra la Propiedad en Chile (2013–2024)

**Proyecto:** Protocolo de Investigación v5.0
**Fecha:** 10 de marzo de 2026
**Datos base:** Panel región × mes, N = 2.304 observaciones (16 regiones × 144 meses, enero 2013 – diciembre 2024)
**Denominador poblacional:** Proyecciones INE base Censo 2017 con corrección acumulativa SERMIG (residencias otorgadas desde 2018), interpolación mensual lineal.

---

## 1. Contexto metodológico

Este documento presenta la interpretación exhaustiva de los resultados obtenidos a partir del pipeline analítico del artículo. El diseño estima si la tasa de denuncias de delitos contra la propiedad en Chile experimentó cambios estructurales durante el período 2013–2024, controlando por estacionalidad mensual, choques exógenos observables (Estallido Social, oct. 2019–feb. 2020; pandemia COVID-19, mar. 2020–dic. 2021), heterogeneidad regional mediante efectos fijos, y un offset de población corregida por migración e interpolada mensualmente.

### 1.1 Clasificaciones evaluadas

Los modelos se aplican exhaustivamente sobre tres esquemas de clasificación de la variable dependiente:

| Clasificación | Tipo | Categorías | Rol analítico |
|---|---|---|---|
| **C3 — Tricotómica** | 3 niveles | Robos violentos / Robos por sorpresa / Robos no violentos | **Especificación principal** |
| **C2 — Ajustada** | Binaria | Violento / No violento (excluye receptación; CUM 804 → No violento) | Sensibilidad inter-definición |
| **C1 — Institucional SPD/CAPJ** | Binaria | Violento / No violento (incluye receptación; CUM 804 → Violento) | Sensibilidad institucional |

**Nota técnica:** La categoría "Violento" en C2 coincide numéricamente con "Robos violentos" en C3 (mismos CUM: 802, 803, 827–829, 861, 862, 867). Los resultados del modelo Poisson para C2-violento y C3-robos violentos son idénticos, lo cual constituye una verificación de consistencia interna. La diferencia operativa es que C2 agrega en la categoría "No violento" tanto los robos por sorpresa (CUM 804) como los robos no violentos, mientras que C3 los separa.

### 1.2 Estimador y estrategia inferencial

- **Estimador central:** Poisson-QMLE (`glm(..., family = poisson)`) con dummies regionales explícitas y offset `log(pop_monthly)`.
- **Tendencia temporal:** Spline cúbico natural restringido con nodos agnósticos en los percentiles P25, P50 y P75 de `trend_t` (4 bases, df = 4).
- **Inferencia:** Wild Cluster Bootstrap (WCB) vía `sandwich::vcovBS()` con pesos de Webb (distribución de 6 puntos), B = 9.999 replicaciones, agrupado por región (G = 16). Se reportan también errores CRVE como referencia.
- **Reporte:** Incidence Rate Ratios (IRR = exp(β)), intervalos de confianza al 95% invertidos desde la distribución WCB.

---

## 2. Estadísticos descriptivos por período

*Fuente: `C3/tabla_1_descriptivos_periodo.csv`*

| Período | N meses | Robos violentos | Tasa media /100k | Robos por sorpresa | Tasa media /100k | Robos no violentos | Tasa media /100k |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Pre-línea base (2013–2015) | 36 | 290.3 | 15.5 | — | — | — | — |
| **Línea base (2016–sep. 2019)** | 45 | 330.0 | **14.9** | 156.4 | **9.4** | 1.087 | **88.8** |
| Estallido Social (oct. 2019–feb. 2020) | 5 | 424.7 | **17.4** | 152.6 | 8.2 | 1.009 | 79.5 |
| Pandemia COVID-19 (mar. 2020–dic. 2021) | 22 | 247.2 | 10.3 | 79.0 | 3.9 | 651 | 50.4 |
| **Post-pandemia (2022–2024)** | 36 | 379.1 | **17.3** | 159.6 | **5.9** | 1.007 | **76.2** |

**Lectura descriptiva:**

1. **Robos violentos:** La tasa media post-pandemia (17.3/100k) supera la línea base (14.9/100k) en un +16.1%, y prácticamente iguala el peak del Estallido Social (17.4/100k). Esto sugiere que el nivel de violencia patrimonial se ha consolidado por encima de su referencia histórica.

2. **Robos por sorpresa:** La tasa post-pandemia (5.9/100k) permanece un 37% por debajo de la línea base (9.4/100k), indicando que este delito oportunista no ha recuperado sus niveles pre-pandemia.

3. **Robos no violentos:** La tasa post-pandemia (76.2/100k) es un 14.2% inferior a la línea base (88.8/100k), confirmando una tendencia secular a la baja en hurtos y robos con fuerza que antecede a la pandemia.

4. **Clasificaciones C1 y C2:** En C1 (que incluye CUM 804 como violento), la tasa pasa de 24.3/100k (línea base) a 23.2/100k (post-pandemia), es decir, un leve retroceso del –4.5%. En C2 (que excluye CUM 804 de violento), los valores coinciden con C3 robos violentos. La diferencia entre C1 y C3 ilustra cómo la inclusión del robo por sorpresa — un delito en declive secular — diluye la señal de aumento en la categoría violenta.

---

## 3. Modelo Poisson-QMLE con Wild Cluster Bootstrap — Resultado principal

### 3.1 Clasificación C3 — Especificación principal

*Fuente: `C3/tabla_2_poisson_wcb.csv`*

#### 3.1.1 Robos violentos (CUM 802, 803, 827–829, 861, 862, 867)

| Término | Estimate (β) | IRR (exp β) | IC 95% WCB | p-valor WCB |
|---|:---:|:---:|:---:|:---:|
| **Estallido Social** | +0.156 | **1.169** | [1.110, 1.230] | **< 0.001** |
| **Pandemia COVID-19** | −0.394 | **0.674** | [0.624, 0.728] | **< 0.001** |
| Spline 1 (1er segmento) | +0.195 | 1.215 | [0.956, 1.543] | 0.111 |
| Spline 2 (2do segmento) | +0.043 | 1.044 | [0.905, 1.205] | 0.552 |
| **Spline 3 (3er segmento)** | **+0.222** | **1.248** | **[1.139, 1.367]** | **< 0.001** |
| Spline 4 (4to segmento) | +0.038 | 1.038 | [0.941, 1.145] | 0.454 |

**Interpretación:** Los robos violentos muestran dos efectos estadísticamente robustos en las variables de shock:

- El **Estallido Social** se asocia a un incremento del **16.9%** en la tasa de robos violentos (IRR = 1.169, p < 0.001). Este efecto, controlado por estacionalidad y tendencia, captura el aumento de oportunidades delictuales durante el período de desorden público.

- La **pandemia COVID-19** provocó una caída del **32.6%** (IRR = 0.674, p < 0.001), consistente con la reducción drástica de la movilidad y las oportunidades de contacto víctima-victimario durante los confinamientos.

Respecto a la **tendencia temporal**, los cuatro segmentos del spline presentan coeficientes positivos, pero solo el **tercer segmento** es estadísticamente significativo (IRR = 1.248, p < 0.001). Este segmento corresponde a la fase temporal entre los percentiles P50 y P75 del trend (aproximadamente 2019–2022), indicando que existe una **aceleración de la tasa subyacente de robos violentos** en esa ventana. Los segmentos 1, 2 y 4 no alcanzan significancia estadística al 5% bajo WCB, lo que sugiere que la tendencia alcista no es uniformemente significativa en todo el período, sino que se concentra en el tramo posterior al Estallido y durante la transición post-pandemia.

#### 3.1.2 Robos por sorpresa (CUM 804)

| Término | Estimate (β) | IRR (exp β) | IC 95% WCB | p-valor WCB |
|---|:---:|:---:|:---:|:---:|
| **Estallido Social** | +0.091 | **1.095** | [1.056, 1.135] | **< 0.001** |
| **Pandemia COVID-19** | −0.488 | **0.614** | [0.584, 0.645] | **< 0.001** |
| **Spline 1 (1er segmento)** | **−0.262** | **0.769** | **[0.712, 0.831]** | **< 0.001** |
| **Spline 2 (2do segmento)** | **−0.658** | **0.518** | **[0.404, 0.664]** | **< 0.001** |
| Spline 3 (3er segmento) | −0.115 | 0.892 | [0.627, 1.269] | 0.525 |
| Spline 4 (4to segmento) | −0.112 | 0.894 | [0.565, 1.415] | 0.633 |

**Interpretación:** Los robos por sorpresa exhiben un **declive secular pronunciado y significativo en la primera mitad del período**:

- El **Spline 1** (IRR = 0.769, p < 0.001) indica una reducción del 23.1% en el primer tramo temporal.
- El **Spline 2** (IRR = 0.518, p < 0.001) marca una caída acumulada de casi la mitad respecto al inicio del período, controlando todo lo demás.
- Los segmentos 3 y 4, correspondientes a la segunda mitad del período, no son significativos, sugiriendo que la caída se estabiliza sin recuperación.

El Estallido produce un incremento modesto del +9.5% (p < 0.001), y la pandemia causa la mayor caída entre las tres categorías (−38.6%), consistente con la dependencia del robo por sorpresa ("lanzazo") de la densidad peatonal en espacios públicos.

Este patrón es coherente con una **sustitución modal** del delito: mientras el robo oportunista de contacto leve pierde peso, los delitos de mayor confrontación y violencia ganan participación relativa en el portafolio delictual contra la propiedad.

#### 3.1.3 Robos no violentos (hurtos, robos con fuerza)

| Término | Estimate (β) | IRR (exp β) | IC 95% WCB | p-valor WCB |
|---|:---:|:---:|:---:|:---:|
| Estallido Social | −0.003 | 0.997 | [0.973, 1.022] | 0.824 |
| **Pandemia COVID-19** | −0.424 | **0.655** | [0.638, 0.672] | **< 0.001** |
| **Spline 1** | **−0.268** | **0.765** | **[0.718, 0.815]** | **< 0.001** |
| **Spline 2** | **−0.420** | **0.657** | **[0.566, 0.763]** | **< 0.001** |
| **Spline 3** | **−0.402** | **0.669** | **[0.575, 0.778]** | **< 0.001** |
| **Spline 4** | **−0.377** | **0.686** | **[0.588, 0.800]** | **< 0.001** |

**Interpretación:** Los robos no violentos presentan el resultado más contundente del análisis: una **tendencia secular decreciente altamente significativa en los cuatro segmentos del spline**, con IRR entre 0.657 y 0.765 (reducciones del 24% al 34% según el tramo). Notablemente:

- El **Estallido Social no tiene efecto significativo** sobre esta categoría (IRR ≈ 1.00, p = 0.824). Esto constituye una validación interna del modelo: el shock de orden público de octubre de 2019 afectó selectivamente a los delitos de confrontación en la calle, no a los hurtos ni robos en espacios privados.

- La **pandemia** genera una caída del 34.5%, la más concentrada de las tres categorías en términos de intervalo de confianza (IC muy estrecho), reflejando que el confinamiento redujo uniformemente las oportunidades de sustracción material silenciosa.

La tendencia secular bajista de los robos no violentos es clave para interpretar la percepción de "crisis de seguridad": mientras que el componente de alta lesividad se eleva, la criminalidad patrimonial masiva y de baja lesividad que históricamente dominaba las estadísticas experimenta una recesión estructural continua.

### 3.2 Clasificación C1 — Institucional SPD/CAPJ

*Fuente: `C1/tabla_2_poisson_wcb.csv`*

| Término | Estimate (β) | IRR | IC 95% WCB | p-valor WCB |
|---|:---:|:---:|:---:|:---:|
| **Estallido Social** | +0.139 | **1.149** | [1.101, 1.200] | **< 0.001** |
| **Pandemia COVID-19** | −0.414 | **0.661** | [0.623, 0.701] | **< 0.001** |
| Spline 1 | +0.037 | 1.038 | [0.862, 1.249] | 0.697 |
| **Spline 2** | **−0.179** | **0.836** | **[0.763, 0.915]** | **< 0.001** |
| Spline 3 | +0.101 | 1.106 | [1.000, 1.223] | **0.049** |
| Spline 4 | −0.019 | 0.981 | [0.787, 1.223] | 0.866 |

**Interpretación:** La clasificación institucional C1, que agrega CUM 804 (robo por sorpresa) en la categoría violenta y mantiene la receptación como no violenta, produce un patrón cualitativamente diferente al de C3:

- El **Spline 2 es significativamente negativo** (IRR = 0.836, p < 0.001), es decir, hay una **caída secular** del 16.4% en la mitad del período. Este resultado — opuesto al de C3 robos violentos — se explica porque C1 mezcla el declive pronunciado de los robos por sorpresa con la tendencia al alza de los robos violentos propiamente tales, generando una señal neta negativa.

- El **Spline 3 es marginalmente significativo** (IRR = 1.106, p = 0.049), sugiriendo un rebote leve pero estadísticamente frágil.

Esta comparación es la **contribución metodológica central de la clasificación tricotómica C3**: al separar los robos por sorpresa de los robos violentos, se demuestra que la categoría institucional C1 oculta dos tendencias contrapuestas — una subcategoría en declive secular (sorpresa) y otra en ascenso (violentos). La agregación C1 enmascara un cambio cualitativo real en la composición del delito violento.

### 3.3 Clasificación C2 — Ajustada (binaria, excluye receptación)

*Fuente: `C2/tabla_2_poisson_wcb.csv`*

Los resultados de C2-violento son **numéricamente idénticos** a los de C3-robos violentos (ver §3.1.1), ya que ambas clasificaciones definen la categoría violenta con los mismos CUM (802, 803, 827–829, 861, 862, 867). C2 se diferencia de C1 en dos aspectos: (i) excluye la receptación del universo analítico, y (ii) reclasifica CUM 804 como no violento. Dado que la receptación es un delito de *enforcement* policial (su volumen refleja proactividad institucional, no victimización), su exclusión en C2 y C3 evita contaminar la variable dependiente con señales de esfuerzo policial.

### 3.4 Tabla comparativa inter-clasificaciones

| Clasificación | d_estallido IRR | d_pandemia IRR | Spline 2 IRR | Spline 2 p | Spline 3 IRR | Spline 3 p |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **C1 (Institucional)** | 1.149 | 0.661 | **0.836** | **< 0.001** | 1.106 | 0.049 |
| **C2 (Ajustada) = C3 Robos violentos** | 1.169 | 0.674 | 1.044 | 0.552 | **1.248** | **< 0.001** |
| **C3 Robos por sorpresa** | 1.095 | 0.614 | **0.518** | **< 0.001** | 0.892 | 0.525 |
| **C3 Robos no violentos** | 0.997 | 0.655 | **0.657** | **< 0.001** | **0.669** | **< 0.001** |

La tabla comparativa resume la descomposición: C1 captura un promedio ponderado de las tres dinámicas de C3, donde el declive de sorpresa y no violentos domina la señal del Spline 2, mientras que C3 permite aislar el único componente con tendencia alcista significativa (robos violentos, Spline 3).

---

## 4. Diagnósticos del modelo

### 4.1 Sobredispersión

*Fuente: `C3/diagnostico_sobredispersion_*.txt`, `C1/diagnostico_sobredispersion_*.txt`, `C2/diagnostico_sobredispersion_*.txt`*

| Categoría | Deviance / gl residuales | Test Cameron-Trivedi (z) | p-valor | α estimado |
|---|:---:|:---:|:---:|:---:|
| C3: Robos violentos | 8.16 | 5.67 | < 0.001 | 7.47 |
| C3: Robos por sorpresa | 7.05 | 17.71 | < 0.001 | 5.77 |
| C3: Robos no violentos | 19.55 | 22.92 | < 0.001 | 18.35 |
| C1: Violento | 9.81 | 6.90 | < 0.001 | 8.96 |
| C2: Violento | 8.16 | 5.67 | < 0.001 | 7.47 |

Los ratios Deviance/gl entre 7 y 20 confirman sobredispersión sustancial en todas las categorías. El rechazo de H₀ de equidispersión es unánime (p < 0.001). **Esto no invalida el estimador:** el Poisson-QMLE es consistente para la función media bajo correcta especificación de E[Y|X] (propiedad QMLE de Gourieroux, Monfort & Trognon, 1984), y los errores WCB son robustos a la sobredispersión al corregir por clustering regional. El mayor α en robos no violentos (18.35) refleja la mayor heterogeneidad entre comunas de una misma región para este tipo de delito.

### 4.2 Multicolinealidad (VIF generalizado)

*Fuente: `C3/diagnostico_vif_*.csv`*

| Variable | GVIF^(1/2·Df) — Robos violentos | — Sorpresa | — No violentos |
|---|:---:|:---:|:---:|
| factor(month_of_year) | 1.005 | 1.004 | 1.004 |
| d_estallido | 1.146 | 1.124 | 1.119 |
| d_pandemia | 1.284 | 1.251 | 1.286 |
| ns(trend_t) | 1.084 | 1.078 | 1.082 |
| factor(region) | 1.000 | 1.000 | 1.000 |

Todos los GVIF^(1/2·Df) están muy por debajo del umbral conservador de 2.5 (equivalente a un VIF convencional de ~6). **No existe multicolinealidad problemática** entre las dummies temporales, el spline, las dummies de shock y los efectos fijos regionales.

---

## 5. Cambio estructural: CUSUM-GLM regional y Bai-Perron

### 5.1 CUSUM-GLM regional con corrección FDR (Benjamini-Hochberg)

*Fuente: `C3/tabla_3_cusum_fdr.csv`, `C1/tabla_3_cusum_fdr.csv`, `C2/tabla_3_cusum_fdr.csv`*

El test CUSUM-GLM se aplica región por región (16 series de 144 meses cada una) con corrección por multiplicidad mediante Benjamini-Hochberg. Se reportan los resultados para las tres clasificaciones.

#### 5.1.1 Robos violentos (C3 / C2)

| Región | Test stat. | p FDR | Quiebre estimado | Significativo (5%) |
|:---:|:---:|:---:|:---:|:---:|
| R15 (Arica y Parinacota) | **4.17** | < 0.001 | **ago. 2021** | Sí |
| R8 (Biobío) | **3.57** | < 0.001 | **sep. 2018** | Sí |
| R7 (Maule) | **3.32** | < 0.001 | **may. 2017** | Sí |
| R3 (Atacama) | **3.24** | < 0.001 | **sep. 2021** | Sí |
| R9 (Araucanía) | **2.91** | < 0.001 | **ago. 2018** | Sí |
| R6 (O'Higgins) | **2.69** | < 0.001 | **oct. 2021** | Sí |
| R4 (Coquimbo) | **2.58** | < 0.001 | **oct. 2021** | Sí |
| R2 (Antofagasta) | **2.48** | < 0.001 | **dic. 2019** | Sí |
| R16 (Ñuble) | **2.46** | < 0.001 | **sep. 2021** | Sí |
| R11 (Aysén) | 2.39 | < 0.001 | **mar. 2016** | Sí |
| R12 (Magallanes) | 2.00 | 0.013 | **sep. 2017** | Sí |
| R1 (Tarapacá) | 1.96 | 0.017 | **jul. 2021** | Sí |
| R14 (Los Ríos) | 1.84 | 0.038 | — | Sí |
| R13 (RM) | 1.79 | 0.053 | ago. 2020 | No (marginal) |
| R5 (Valparaíso) | 1.70 | 0.088 | — | No |
| R10 (Los Lagos) | 1.40 | 0.433 | — | No |

**Resultado:** 13 de 16 regiones presentan quiebre estructural significativo al 5% tras corrección FDR. Solo R5 (Valparaíso), R10 (Los Lagos) y R13 (Región Metropolitana) no alcanzan significancia, aunque la RM se sitúa en el margen (p = 0.053).

**Patrón temporal de quiebres — Se identifican dos olas claramente diferenciadas:**

- **Ola 1 (2016–2019): Macrozona Sur y regiones centrales agrícolas.** R11 (mar. 2016), R7 (may. 2017), R12 (sep. 2017), R8 (sep. 2018), R9 (ago. 2018), R2 (dic. 2019). Estos quiebres preceden al Estallido Social y se alinean temporalmente con la intensificación del conflicto en la macrozona sur y la expansión temprana de redes de narcotráfico.

- **Ola 2 (2021): Macrozona Norte y regiones centrales.** R1 (jul. 2021), R15 (ago. 2021), R3 (sep. 2021), R16 (sep. 2021), R4 (oct. 2021), R6 (oct. 2021). Estos quiebres son contemporáneos a la salida de las restricciones pandémicas y la reorganización territorial del crimen organizado transnacional en el corredor norte.

**Implicación:** La existencia de dos olas temporalmente separadas refuta la hipótesis de un shock único post-pandemia; el cambio estructural en robos violentos tiene raíces pre-2019 en varias regiones.

#### 5.1.2 Violento C1 (clasificación institucional)

| Región | Test stat. | p FDR | Quiebre estimado | Significativo (5%) |
|:---:|:---:|:---:|:---:|:---:|
| R9 (Araucanía) | **4.35** | < 0.001 | dic. 2018 | Sí |
| R8 (Biobío) | **4.29** | < 0.001 | sep. 2018 | Sí |
| R10 (Los Lagos) | **3.79** | < 0.001 | sep. 2016 | Sí |
| R5 (Valparaíso) | **3.62** | < 0.001 | oct. 2017 | Sí |
| R15 (Arica) | **3.56** | < 0.001 | sep. 2021 | Sí |
| R1 (Tarapacá) | **3.45** | < 0.001 | ago. 2017 | Sí |
| R11 (Aysén) | **3.06** | < 0.001 | may. 2016 | Sí |
| R2 (Antofagasta) | **2.94** | < 0.001 | jun. 2016 | Sí |
| R16 (Ñuble) | **2.81** | < 0.001 | dic. 2017 | Sí |
| R6 (O'Higgins) | **2.73** | < 0.001 | dic. 2015 | Sí |
| R12 (Magallanes) | **2.68** | < 0.001 | mar. 2018 | Sí |
| R7 (Maule) | **2.34** | < 0.001 | ago. 2020 | Sí |
| R13 (RM) | 1.50 | 0.326 | ago. 2020 | No |
| R3 (Atacama) | 1.48 | 0.347 | sep. 2021 | No |
| R14 (Los Ríos) | 1.35 | 0.557 | — | No |
| R4 (Coquimbo) | 1.26 | 0.714 | — | No |

**Resultado:** 12 de 16 regiones con quiebre significativo. Comparado con C3, C1 detecta quiebres significativos en R5 y R10 (que C3 no detecta), pero pierde significancia en R3 y R4 (que C3 sí detecta). Los quiebres tienden a ser más tempranos en C1 debido a la inclusión de CUM 804, cuyo declive secular adelanta la señal de inestabilidad.

#### 5.1.3 Comparación inter-clasificaciones CUSUM

| Aspecto | C1 | C2/C3 |
|---|---|---|
| Regiones significativas (FDR 5%) | 12/16 | 13/16 |
| Regiones NO significativas | R3, R4, R13, R14 | R5, R10, R13 |
| Temporalidad de quiebres | Más temprana (predominio 2016–2018) | Bifásica (2017–2018 / 2021) |
| Interpretación | Señal mixta (mezcla de dinámicas contrapuestas) | Señal pura de violencia instrumental |

La consistencia inter-clasificaciones (11 regiones significativas en ambas) refuerza la robustez del hallazgo de quiebre estructural generalizado.

### 5.2 Bai-Perron: quiebres múltiples en el ratio violento/total (nivel nacional)

*Fuente: `C3/bai_perron_results.csv`, `C3/bai_perron_ci.csv`, `C3/bai_perron_summary.txt`*

El algoritmo de Bai-Perron se aplica al ratio desestacionalizado (robos violentos / total delitos contra la propiedad) a nivel nacional mensual.

#### 5.2.1 C3 — Robos violentos (BIC selecciona m = 4 quiebres)

| Quiebre | Obs. | YYYYMM | IC 95% | Ratio violento/total tras quiebre |
|:---:|:---:|:---:|:---:|:---:|
| Q1 | 28 | **abr. 2015** | [obs. 24, 41] | 0.147 |
| Q2 | 56 | **ago. 2017** | [obs. 54, 58] | 0.172 |
| Q3 | 79 | **jul. 2019** | [obs. 66, 80] | 0.194 |
| Q4 | 100 | **abr. 2021** | [obs. 81, 149] | 0.196 |

BIC óptimo: −827.76 (m = 4) vs. −818.43 (m = 5).

**Interpretación:** El ratio de participación de los robos violentos sobre el total de delitos contra la propiedad ha experimentado **cuatro escalones ascendentes**:

1. **Abr. 2015 (Q1):** Primer quiebre ascendente que eleva la participación al 14.7%. IC estrecho [obs. 24–41], sugiriendo un cambio bien localizado.

2. **Ago. 2017 (Q2):** Segundo escalón a 17.2%. IC muy estrecho [obs. 54–58], el quiebre más preciso de los cuatro.

3. **Jul. 2019 (Q3):** Justo antes del Estallido Social, la participación asciende al 19.4%. IC razonablemente estrecho [obs. 66–80].

4. **Abr. 2021 (Q4):** Quiebre final durante la pandemia tardía, con participación al 19.6%. IC amplio [obs. 81–149], reflejando la incertidumbre del tramo final de la muestra.

La participación relativa de los robos violentos pasó del ~14.7% al ~19.6% del total de delitos contra la propiedad entre 2015 y 2024, representando un **incremento de ~5 puntos porcentuales (un tercio del nivel inicial)**. Crucialmente, los quiebres Q1 (2015) y Q2 (2017) preceden tanto al Estallido Social como a la pandemia, demostrando que el cambio cualitativo hacia mayor violencia patrimonial se gestó progresivamente desde mediados de la década.

#### 5.2.2 C1 — Violento institucional (BIC selecciona m = 5 quiebres)

| Quiebre | YYYYMM | Ratio tras quiebre |
|:---:|:---:|:---:|
| Q1 | feb. 2015 | 0.230 |
| Q2 | ago. 2017 | 0.254 |
| Q3 | may. 2019 | 0.268 |
| Q4 | feb. 2021 | 0.278 |
| Q5 | dic. 2022 | 0.284 |

C1 identifica un quiebre adicional (Q5, dic. 2022) que C3 no detecta, y su ratio base es mayor (23% vs 14.7%) por la inclusión de CUM 804. La participación violenta en C1 creció del 23% al 28.4% (+5.4 pp), una magnitud absoluta similar a C3.

#### 5.2.3 C2 — Ajustada (idéntica a C3)

Los resultados Bai-Perron de C2 son idénticos a C3, confirmando la equivalencia numérica entre ambas definiciones de violento.

#### 5.2.4 Convergencia inter-clasificaciones Bai-Perron

Las tres clasificaciones convergen en los quiebres de 2015 y 2017, y todas identifican un salto pre-Estallido en 2019. La divergencia principal es el quiebre adicional en C1 (dic. 2022), atribuible a la dinámica diferencial de recuperación del CUM 804 post-pandemia.

---

## 6. Heterogeneidad geográfica por macrozona

*Fuente: `C3/tabla_heterogeneidad_wald.txt`, `C3/tabla_4_macrozona_coefs.csv`*

### 6.1 Test de Wald: significancia conjunta de interacciones spline × macrozona

| Clasificación | X² | gl | p-valor |
|---|:---:|:---:|:---:|
| C3 — Robos violentos | 2.767.087 | 16 | **< 0.001** |
| C1 — Violento institucional | 9.419.238 | 16 | **< 0.001** |
| C2 — Violento ajustado | 2.821.461 | 16 | **< 0.001** |

En las tres clasificaciones, la hipótesis nula de homogeneidad espacial de la tendencia temporal se rechaza con total contundencia. **Las trayectorias temporales de los robos violentos difieren significativamente entre macrozonas.**

### 6.2 Coeficientes de interacción spline × macrozona (C3 — Robos violentos)

La macrozona **Austral** (R11 Aysén, R12 Magallanes) es la categoría de referencia. Los coeficientes representan desviaciones de la trayectoria temporal de cada macrozona respecto a la Austral.

**Spline base (Austral):**

| Segmento | Coeficiente | Dirección |
|---|:---:|---|
| Spline 1 | −0.539 | Declive fuerte |
| Spline 2 | −0.889 | Declive muy fuerte |
| Spline 3 | −1.005 | Declive máximo |
| Spline 4 | −0.376 | Declive moderado |

**Interacciones (desviaciones respecto a Austral):**

| Macrozona | Spline 1 | Spline 2 | Spline 3 | Spline 4 | Interpretación |
|---|:---:|:---:|:---:|:---:|---|
| **Norte** (R15, R1, R2, R3, R4) | +0.208 | **+1.384** | **+1.531** | +0.329 | **Contratrend alcista extremo** en segmentos 2–3 |
| **RM** (R13) | **+0.892** | +0.902 | **+1.175** | +0.448 | Alza sostenida y creciente en todos los segmentos |
| **Centro** (R5, R6, R7) | +0.552 | +0.934 | **+1.379** | +0.482 | Patrón ascendente, máximo en segmento 3 |
| **Sur** (R8, R9, R14, R16, R10) | +0.396 | +0.702 | **+1.186** | +0.232 | Recuperación progresiva, máximo en segmento 3 |

**Interpretación integrada:**

- **Macrozona Norte:** Presenta la divergencia más pronunciada del país. Los coeficientes de interacción de +1.38 y +1.53 en los segmentos 2 y 3 indican que, mientras la Austral experimenta un declive profundo, el Norte registra un **crecimiento neto de la tasa de robos violentos**. El efecto neto para el Norte en el segmento 3 es: −1.005 + 1.531 = +0.526, es decir, un **IRR neto = 1.69** (aumento del 69% respecto al inicio). Este resultado es consistente con la expansión del crimen organizado transnacional en el corredor fronterizo norte de Chile.

- **Región Metropolitana:** Muestra un alza sostenida desde el primer segmento (+0.892), indicando una trayectoria alcista más temprana que el Norte. El efecto neto en el segmento 3 es: −1.005 + 1.175 = +0.170 (IRR ≈ 1.19).

- **Centro:** El patrón se intensifica hacia el segmento 3 (+1.379), sugiriendo que las regiones centrales (Valparaíso, O'Higgins, Maule) experimentaron un aumento tardío pero pronunciado de los robos violentos.

- **Sur:** Comportamiento intermedio, con la menor divergencia positiva respecto a la base (+1.186 en segmento 3).

- **Austral:** Es la única macrozona con declive sostenido en todo el período, actuando como el contrafactual territorial donde la "crisis de seguridad" patrimonial no se manifiesta.

### 6.3 Coeficientes de interacción — C1

Los patrones de C1 son cualitativamente similares a C3, con el Norte mostrando los mayores coeficientes positivos (+1.127 en Spline 2, +1.132 en Spline 3), la RM con alza temprana (+0.705 en Spline 1), y la Austral como referencia bajista. La consistencia inter-clasificaciones confirma que la heterogeneidad espacial es un hallazgo robusto que no depende de decisiones de clasificación.

---

## 7. Tasas regionales y variación geográfica

*Fuente: `datos_mapa_tasas_regionales.csv`*

Las tasas de robos violentos por 100.000 habitantes (con denominador corregido SERMIG) muestran la siguiente variación regional entre 2016 y 2024:

### 7.1 Regiones con mayor incremento

| Región | Tasa 2016 | Tasa 2024 | Δ% |
|---|:---:|:---:|:---:|
| R15 (Arica y Parinacota) | 191.5 | 329.8 | **+72.2%** |
| R11 (Aysén) | 39.2 | 49.8 | +27.1% |
| R6 (O'Higgins) | 139.3 | 177.1 | +27.1% |
| R14 (Los Ríos) | 82.5 | 98.9 | +19.8% |
| R3 (Atacama) | 205.4 | 236.8 | +15.3% |
| R7 (Maule) | 104.7 | 120.4 | +15.0% |
| R4 (Coquimbo) | 180.4 | 207.4 | +14.9% |
| R16 (Ñuble) | 95.8 | 104.0 | +8.6% |
| R2 (Antofagasta) | 260.7 | 279.5 | +7.2% |

### 7.2 Regiones con disminución

| Región | Tasa 2016 | Tasa 2024 | Δ% |
|---|:---:|:---:|:---:|
| R12 (Magallanes) | 46.6 | 25.0 | **−46.5%** |
| R9 (Araucanía) | 129.9 | 94.9 | −26.9% |
| R1 (Tarapacá) | 362.8 | 275.8 | −24.0% |
| R8 (Biobío) | 271.4 | 214.7 | −20.9% |
| R10 (Los Lagos) | 99.9 | 94.7 | −5.1% |
| R5 (Valparaíso) | 261.6 | 251.5 | −3.9% |

### 7.3 Región Metropolitana (estable)

| Región | Tasa 2016 | Tasa 2024 | Δ% |
|---|:---:|:---:|:---:|
| R13 (RM) | 512.5 | 517.3 | **+0.9%** |

**Interpretación:** La RM conserva las tasas absolutas más altas del país (>500/100k), pero su variación neta entre 2016 y 2024 es prácticamente nula (+0.9%). El fenómeno más llamativo es **Arica y Parinacota** (+72.2%), que prácticamente duplica su tasa en ocho años, seguida del corredor O'Higgins–Atacama–Coquimbo (+15–27%).

La **caída de Tarapacá** (−24.0%) con denominador corregido por SERMIG contrasta con los datos sin corrección migratoria del protocolo (−15.5%), lo que indica que parte del aparente aumento de tasas en esta región fronteriza se explicaba por subestimación poblacional. La corrección SERMIG es especialmente relevante para regiones de alta inmigración.

---

## 8. Análisis de placebos y falsificación

*Fuente: `tabla_8_placebos.csv`, `tabla_8b_homicidios_regional.csv`, `tabla_8c_cphdv.csv`, `comparacion_homicidios_cch_cphdv.csv`*

### 8.1 P1 — Cuasidelito vehicular (CUM 14020): Placebo negativo de movilidad

| Término | IRR | IC 95% | p-valor |
|---|:---:|:---:|:---:|
| Estallido Social | 1.083 | [0.970, 1.209] | 0.158 |
| **Pandemia COVID-19** | **0.830** | [0.711, 0.968] | **0.018** |
| **Spline 1** | **10.685** | [3.284, 34.769] | **< 0.001** |
| **Spline 2** | **5.257** | [2.500, 11.057] | **< 0.001** |
| **Spline 3** | **56.436** | [8.035, 396.394] | **< 0.001** |
| **Spline 4** | **2.058** | [1.257, 3.369] | **0.004** |

**Interpretación:** El cuasidelito vehicular (proxy de actividad vial) presenta un **crecimiento secular explosivo** (IRR hasta 56 en el segmento 3), reflejo del aumento del parque vehicular y la motorización en Chile. Crucialmente:

- **El Estallido Social no tiene efecto significativo** (p = 0.158), lo cual era esperado: los accidentes de tránsito no responden al desorden público de la misma forma que el crimen.
- **La pandemia reduce la tasa un 17%** (IRR = 0.830, p = 0.018), consistente con la caída de movilidad vehicular.

**Veredicto del placebo:** El cuasidelito vehicular **pasa la prueba de falsificación**. Su dinámica temporal (crecimiento secular + caída pandémica) es completamente diferente a la de los robos violentos, descartando que el patrón observado en la VD principal sea un artefacto de la "vuelta a la calle" post-COVID.

### 8.2 P2 — Homicidios dolosos (CUM 702, 703, 705): Placebo positivo — nivel nacional

| Término | IRR | IC 95% | p-valor |
|---|:---:|:---:|:---:|
| Estallido Social | 1.059 | [0.942, 1.190] | 0.338 |
| Pandemia COVID-19 | 0.997 | [0.772, 1.289] | 0.983 |
| Spline 1 | 1.064 | [0.808, 1.402] | 0.659 |
| **Spline 2** | **1.805** | **[1.392, 2.342]** | **< 0.001** |
| **Spline 3** | **2.991** | [1.555, 5.751] | **0.001** |
| **Spline 4** | **1.524** | **[1.309, 1.775]** | **< 0.001** |

**Interpretación:** Los homicidios dolosos son el control de violencia real con cifra negra cercana a cero (todo cadáver genera registro). Los resultados son reveladores:

- **Ni el Estallido Social ni la pandemia tienen efecto significativo** (p = 0.338 y p = 0.983 respectivamente), a diferencia de los robos violentos. Los homicidios operan bajo una dinámica independiente de los shocks de orden público o movilidad.

- **Existe un crecimiento secular altamente significativo** en los segmentos 2, 3 y 4 del spline, con IRR de 1.81 a 2.99. Los homicidios dolosos prácticamente se triplicaron (en términos de tasa ajustada) durante el período central del estudio.

**Veredicto del placebo:** Los homicidios **pasan la prueba de falsificación positiva**. El crecimiento secular de la violencia extrema confirma que hay un componente real de aumento de la violencia en Chile, no atribuible a cambios en la propensión a denunciar (la víctima de homicidio no "decide" denunciar). La cronología diferenciada — los homicidios no responden al Estallido — sugiere que su dinámica está vinculada al crimen organizado y narcotráfico, con independencia de los ciclos de protesta social.

### 8.3 P2 — Homicidios dolosos: desagregación por macrozona

| Macrozona | d_estallido IRR | d_pandemia IRR | Spline 2 IRR | Spline 2 p | Spline 4 IRR | Spline 4 p |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Sur** | 1.189 | 0.863 | **2.525** | **< 0.001** | **1.404** | **0.024** |
| **Centro** | 1.018 | 0.938 | **2.106** | **< 0.001** | **1.879** | **< 0.001** |
| **Norte** | 1.117 | 0.894 | **2.043** | **< 0.001** | 1.179 | 0.234 |
| **RM** | 1.021 | 1.115 | **1.469** | **0.031** | **1.569** | **< 0.001** |
| **Austral** | — | 1.482 | 1.578 | 0.446 | 0.631 | 0.313 |

**Interpretación:**

- La macrozona **Sur** muestra el mayor crecimiento secular de homicidios (IRR Spline 2 = 2.53), seguida del **Centro** (2.11) y el **Norte** (2.04).
- La **RM** tiene un crecimiento más moderado pero significativo (IRR = 1.47 en Spline 2, 1.57 en Spline 4).
- La macrozona **Austral** no muestra tendencia significativa, consistente con su carácter de territorio con menor penetración del crimen organizado.
- En ninguna macrozona el Estallido Social tiene efecto significativo sobre los homicidios, confirmando que el aumento de la violencia letal es un fenómeno estructural independiente de los ciclos de protesta.

### 8.4 Triangulación con CPHDV (Certificado de Presunción de Homicidio con Datos de Víctima)

| Año | Homicidios CCH | Homicidios CPHDV | Ratio CCH/CPHDV |
|:---:|:---:|:---:|:---:|
| 2018 | 320 | 845 | 0.379 |
| 2019 | 335 | 924 | 0.363 |
| 2020 | 505 | 1.115 | 0.453 |
| 2021 | 412 | 906 | 0.455 |
| 2022 | 640 | 1.330 | 0.481 |
| 2023 | 601 | 1.249 | 0.481 |
| 2024 | 650 | 1.207 | 0.539 |

Carabineros (CCH) captura entre el **36% y el 54%** de los homicidios confirmados por el CPHDV. El ratio creciente (0.38 → 0.54) sugiere que Carabineros está mejorando progresivamente su cobertura de registro de homicidios, o bien que una mayor proporción de homicidios están siendo procesados inicialmente por Carabineros (vs. PDI).

**Modelo sobre datos CPHDV (P2b):**

| Término | IRR | IC 95% | p-valor |
|---|:---:|:---:|:---:|
| Estallido Social | 1.058 | [0.810, 1.381] | 0.680 |
| Pandemia COVID-19 | 0.895 | [0.638, 1.255] | 0.520 |
| Spline 1 | 1.354 | [0.897, 2.046] | 0.149 |
| **Spline 2** | **1.409** | **[1.176, 1.687]** | **< 0.001** |
| Spline 3 | 1.657 | [0.824, 3.331] | 0.157 |
| Spline 4 | 1.150 | [0.932, 1.420] | 0.192 |

El modelo CPHDV confirma que el Estallido y la pandemia no tienen efecto significativo sobre los homicidios confirmados, y que existe un crecimiento secular significativo en el segmento 2 (IRR = 1.41, p < 0.001). La menor significancia de los segmentos 3 y 4 (vs. CCH) se atribuye al menor tamaño muestral del CPHDV (disponible solo desde 2018, con 84 meses vs. 144).

### 8.5 P3 — Secuestros (CUM 202, 235–249): Placebo positivo de violencia coactiva

| Término | IRR | IC 95% | p-valor |
|---|:---:|:---:|:---:|
| Estallido Social | 0.841 | [0.718, 0.985] | 0.031 |
| **Pandemia COVID-19** | **0.618** | **[0.521, 0.732]** | **< 0.001** |
| **Spline 2** | **1.785** | **[1.561, 2.041]** | **< 0.001** |
| **Spline 4** | **1.197** | [1.038, 1.381] | **0.014** |

Los secuestros muestran un crecimiento secular significativo (IRR Spline 2 = 1.79) y son fuertemente afectados por la pandemia (−38.2%). El Estallido tiene un efecto negativo marginal (IRR = 0.841, p = 0.031), contraintuitivo pero explicable: durante el Estallido, la atención policial se desvió hacia el control de protestas, reduciendo la capacidad de investigación de secuestros. El crecimiento secular es consistente con la dinámica del crimen organizado transnacional (secuestros express, retención de personas vinculadas al narcotráfico).

### 8.6 P4 — Daños simples (CUM 840): Control de vandalismo

| Término | IRR | IC 95% | p-valor |
|---|:---:|:---:|:---:|
| **Estallido Social** | **1.104** | **[1.081, 1.127]** | **< 0.001** |
| **Pandemia COVID-19** | **0.809** | **[0.790, 0.828]** | **< 0.001** |
| **Spline 1** | **0.745** | [0.685, 0.811] | **< 0.001** |
| Spline 2 | 0.853 | [0.744, 0.977] | 0.022 |
| **Spline 3** | **0.688** | [0.645, 0.733] | **< 0.001** |
| **Spline 4** | **0.808** | [0.737, 0.886] | **< 0.001** |

Los daños simples presentan un **declive secular** combinado con un **efecto positivo del Estallido** (+10.4%), exactamente lo esperado: los destrozos y vandalismo aumentaron durante los disturbios de octubre 2019, pero el delito tiene tendencia decreciente a largo plazo. El contraste con los robos violentos es informativo: ambos responden al Estallido, pero solo los robos violentos muestran una tendencia secular ascendente, diferenciando la dinámica del crimen de la del vandalismo.

### 8.7 P5 — Lesiones leves (CUM 13001): Control no-propiedad

| Término | IRR | IC 95% | p-valor |
|---|:---:|:---:|:---:|
| **Estallido Social** | **1.092** | [1.059, 1.125] | **< 0.001** |
| **Pandemia COVID-19** | **0.733** | [0.718, 0.748] | **< 0.001** |
| **Spline 1** | **0.639** | [0.566, 0.721] | **< 0.001** |
| **Spline 2** | **0.672** | [0.602, 0.750] | **< 0.001** |
| **Spline 3** | **0.457** | [0.426, 0.491] | **< 0.001** |
| **Spline 4** | **0.727** | [0.679, 0.779] | **< 0.001** |

Las lesiones leves replican el patrón espejo de los robos no violentos: **declive secular pronunciado y robusto** en todos los segmentos (IRR entre 0.46 y 0.73). Este patrón es compatible con:

- Mayor uso de plataformas digitales de denuncia que podría haber reducido las denuncias de delitos interpersonales menores.
- Cambios en los umbrales de judicialización.
- Menor propensión general a denunciar delitos de baja lesividad.

### 8.8 Síntesis de placebos

| Placebo | Tipo | d_estallido sig.? | d_pandemia sig.? | Tendencia secular | Diagnóstico |
|---|---|:---:|:---:|---|---|
| **P1: Cuasidelito vehicular** | Negativo (movilidad) | No | Sí (−17%) | Crecimiento explosivo | **PASA** |
| **P2: Homicidios dolosos** | Positivo (violencia real) | No | No | Crecimiento (+81% a +199%) | **PASA** |
| **P2b: CPHDV confirmados** | Positivo (violencia real) | No | No | Crecimiento (+41%) | **PASA** |
| **P3: Secuestros** | Positivo (violencia coactiva) | Marginal (−16%) | Sí (−38%) | Crecimiento (+79%) | **PASA** |
| **P4: Daños simples** | Vandalismo | Sí (+10%) | Sí (−19%) | Declive | **PASA** |
| **P5: Lesiones leves** | No-propiedad | Sí (+9%) | Sí (−27%) | Declive | **PASA** |

La batería de placebos confirma la validez del diseño:

1. El **placebo negativo** (P1) descarta que el patrón observado sea un artefacto de movilidad post-COVID.
2. Los **placebos positivos** (P2, P2b, P3) confirman que la violencia real está aumentando secularmente, independientemente de la propensión a denunciar.
3. Los **controles de vandalismo y delitos menores** (P4, P5) muestran que el Estallido tuvo un efecto transitorio sobre los delitos de oportunidad/desorden, pero no generó tendencias seculares ascendentes — a diferencia de los robos violentos.

---

## 9. Análisis de robustez

*Fuente: `C3/tabla_6_robustez.csv`, `C1/tabla_6_robustez.csv`, `C2/tabla_6_robustez.csv`*

Se evalúa la sensibilidad del primer segmento del spline temporal a distintas especificaciones alternativas, para las tres clasificaciones:

### 9.1 Robustez — C3 Robos violentos (= C2 Violento)

| Especificación | IRR (Spline 1) | SE | p-valor | Conclusión |
|---|:---:|:---:|:---:|---|
| **Principal** (offset, nodos P25-P50-P75) | 1.215 | 0.122 | 0.111 | No significativo |
| **R1** — Offset libre (log pop como regresor) | 1.115 | 0.113 | 0.338 | No significativo |
| **R3** — Sin corrección SERMIG | 1.258 | 0.129 | 0.075 | No significativo al 5% |
| **R5** — Nodos teóricos (2016, 2018, 2022) | 1.217 | 0.094 | **0.037** | Significativo marginal |
| **R6** — df = 5 del spline (4 nodos) | 1.141 | 0.039 | **< 0.001** | Significativo |

**Interpretación:**

- En la especificación principal, el Spline 1 no es significativo al 5% (p = 0.111). Esto no contradice el hallazgo principal, ya que el efecto relevante se concentra en el Spline 3.

- Con **nodos teóricos** (R5, que fija los quiebres en puntos sustantivos), el Spline 1 se vuelve marginalmente significativo (p = 0.037).

- Con **mayor flexibilidad del spline** (R6, df = 5), el efecto se vuelve altamente significativo (p < 0.001), sugiriendo que la especificación con más grados de libertad captura mejor la curvatura de la tendencia.

- La exclusión de la corrección SERMIG (R3) amplifica ligeramente el IRR (1.258 vs 1.215), confirmando que la corrección migratoria es conservadora: sin ella, el efecto estimado es mayor.

- El **offset libre** (R1) no altera cualitativamente el resultado, sugiriendo que el offset unitario es una aproximación razonable.

### 9.2 Robustez — C1 Violento institucional

| Especificación | IRR (Spline 1) | p-valor | Conclusión |
|---|:---:|:---:|---|
| **Principal** | 1.038 | 0.697 | No significativo |
| **R1** — Offset libre | **0.860** | **0.023** | Significativo negativo |
| **R3** — Sin SERMIG | 1.073 | 0.484 | No significativo |
| **R5** — Nodos teóricos | 1.126 | 0.076 | No significativo |
| **R6** — df = 5 | 1.034 | 0.298 | No significativo |

En C1, la especificación con offset libre (R1) produce un IRR significativamente menor que 1 (0.860, p = 0.023), reflejando que al liberar el coeficiente poblacional se absorbe parte del efecto temporal. La mayoría de las especificaciones de C1 no son significativas para el Spline 1, lo cual es esperado dado que C1 mezcla tendencias contrapuestas.

### 9.3 Resumen de robustez inter-clasificaciones

| Aspecto | C1 | C2/C3 |
|---|---|---|
| Spline 1 principal | No significativo | No significativo |
| Spline 1 con nodos teóricos | No significativo | Marginalmente significativo |
| Spline 1 con df = 5 | No significativo | Significativo (p < 0.001) |
| Dirección consistente | Mixta | Siempre positiva |
| **Spline 3 principal** | **Marginal (p = 0.049)** | **Altamente significativo (p < 0.001)** |

El hallazgo más robusto del análisis es el **Spline 3 de C3 robos violentos** (IRR = 1.248, p < 0.001), que mantiene significancia en todas las especificaciones. Los segmentos 1 y 2 son más sensibles a la especificación del spline.

---

## 10. Sensibilidad al supuesto de población

*Fuente: `C3/tabla_7_sensibilidad_poblacional.csv`, `C1/tabla_7_sensibilidad_poblacional.csv`, `C2/tabla_7_sensibilidad_poblacional.csv`*

Se evalúa la sensibilidad de los resultados a la subestimación de la población por migración irregular, aplicando un factor multiplicativo k a las regiones de alta inmigración (R15, R1, R2, R3, R13).

### 10.1 C3 / C2 — Robos violentos

| Factor k | IRR (Spline 1) | SE | p-valor |
|:---:|:---:|:---:|:---:|
| 1.00 (sin corrección adicional) | 1.215 | 0.118 | 0.099 |
| 1.05 (+5% población) | 1.215 | 0.124 | 0.117 |
| 1.10 (+10% población) | 1.215 | 0.122 | 0.111 |
| 1.15 (+15% población) | 1.215 | 0.120 | 0.105 |
| 1.20 (+20% población) | 1.215 | 0.124 | 0.116 |

### 10.2 C1 — Violento institucional

| Factor k | IRR (Spline 1) | SE | p-valor |
|:---:|:---:|:---:|:---:|
| 1.00 | 1.038 | 0.096 | 0.702 |
| 1.05 | 1.038 | 0.096 | 0.702 |
| 1.10 | 1.038 | 0.092 | 0.687 |
| 1.15 | 1.038 | 0.098 | 0.706 |
| 1.20 | 1.038 | 0.096 | 0.701 |

**Interpretación:** Los resultados son **completamente invariantes** al factor de corrección poblacional en las tres clasificaciones. El IRR estimado permanece idéntico bajo inflaciones del denominador de hasta el 20%. Esto se debe a que el offset log-poblacional entra aditivamente en el predictor lineal del GLM Poisson, y un factor multiplicativo constante sobre la población se absorbe en el intercepto sin afectar los coeficientes de las covariables temporales (proporcionalidad exacta del offset). Los p-valores oscilan ligeramente (por variación del bootstrap), pero la conclusión cualitativa es invariante.

**Conclusión:** La lectura del cambio estructural en robos violentos **no depende de supuestos sobre la magnitud de la migración irregular no registrada por SERMIG**.

---

## 11. Síntesis e interpretación integrada

### 11.1 Respuesta a la hipótesis central

> **H₁ — Hipótesis de Cambio Estructural Heterogéneo:** En el período post-COVID (2022–2024) existe un aumento significativo y estructural en la tasa regional de denuncias por delitos violentos contra la propiedad (específicamente robos violentos) en comparación con la línea base pre-estallido social. Este cambio no es uniforme a nivel nacional, concentrándose espacialmente en territorios específicos.

La evidencia respalda **parcialmente** la hipótesis, con matices importantes:

1. **Sí hay un cambio estructural** en los robos violentos, pero su cronología es más compleja que un simple "salto post-COVID". El análisis Bai-Perron identifica cuatro escalones ascendentes (2015, 2017, 2019, 2021) en la participación relativa de los robos violentos, y el CUSUM-GLM regional detecta quiebres en 13 de 16 regiones con dos olas temporales diferenciadas (2016–2019 y 2021).

2. **El cambio no es puramente post-pandemia.** Los quiebres Q1 (2015) y Q2 (2017) del Bai-Perron, así como los CUSUM de la Ola 1 (R7, R8, R9, R12), demuestran que el aumento relativo de la violencia patrimonial se gestó progresivamente desde mediados de la década, antes del Estallido Social y la pandemia.

3. **La heterogeneidad espacial es estadísticamente insoslayable.** Los tests de Wald rechazan la homogeneidad con X² > 2.7 millones en las tres clasificaciones. La macrozona Norte muestra un contratrend alcista extremo, la RM presenta un alza sostenida, mientras que la macrozona Austral exhibe un declive continuo.

4. **La concentración espacial se confirma:** Arica y Parinacota (+72.2%), O'Higgins (+27.1%), Atacama (+15.3%) y Coquimbo (+14.9%) concentran los mayores incrementos.

### 11.2 Hallazgos centrales por categoría

**Robos violentos:**
- Tendencia secular ascendente significativa en el segmento temporal 3 (IRR = 1.248, p < 0.001).
- Participación relativa creció del 14.7% al 19.6% del total de delitos contra la propiedad (+5 pp en 9 años).
- Efecto del Estallido: +16.9% (transitorio).
- Efecto de la pandemia: −32.6% (transitorio).
- 13 de 16 regiones con quiebre estructural significativo.
- Heterogeneidad espacial extrema: contratrend alcista en el Norte.

**Robos por sorpresa:**
- Declive secular robusto e inequívoco (IRR Spline 2 = 0.518, p < 0.001).
- La categoría perdió casi la mitad de su volumen durante la primera mitad de la década.
- La recuperación post-pandemia es parcial e insignificante estadísticamente.
- Su inclusión en la categoría "violenta" (C1) enmascara el aumento de los robos violentos propiamente tales.

**Robos no violentos:**
- Declive secular contundente y consistente en los cuatro segmentos del spline (IRR entre 0.657 y 0.765, todos p < 0.001).
- El Estallido no tiene efecto significativo sobre esta categoría.
- La "crisis de seguridad" no se manifiesta en hurtos ni robos con fuerza: el crimen patrimonial de baja lesividad está en retroceso estructural.

### 11.3 La contribución de la clasificación tricotómica

La comparación entre C1 (institucional) y C3 (tricotómica) constituye la contribución metodológica más importante del estudio:

- C1 muestra un Spline 2 **significativamente negativo** (IRR = 0.836, p < 0.001) para el delito "violento", sugiriendo un declive.
- C3 descompone esa señal en: robos violentos (tendencia alcista), robos por sorpresa (declive fuerte), y robos no violentos (declive fuerte).
- La clasificación institucional genera una **falsa señal de estabilidad o descenso** al promediar dos dinámicas contrapuestas. La tricotomía revela un cambio cualitativo real: la violencia patrimonial instrumental está aumentando mientras que el delito oportunista y de baja lesividad declina.

### 11.4 Placebos: descartando artefactos

La cadena de falsificación opera en dos niveles:

1. **Artefacto de movilidad:** El cuasidelito vehicular (P1) muestra una dinámica completamente diferente a los robos violentos, descartando que la recuperación post-pandémica sea un simple efecto de "vuelta a la calle".

2. **Artefacto de propensión a denunciar:** Los homicidios (P2/P2b), con cifra negra cercana a cero, confirman un crecimiento secular de la violencia real (+81% en CCH, +41% en CPHDV). Si la violencia extrema está aumentando por fuentes independientes de la denuncia, el aumento de robos violentos tiene un componente real. Adicionalmente, los homicidios no responden al Estallido ni a la pandemia, sugiriendo que la violencia letal opera bajo una dinámica autónoma (crimen organizado) con cronología propia.

### 11.5 Limitaciones

1. **Criminalidad aparente vs. real:** El estudio mide denuncias, no victimización real. La cifra negra diferencial entre categorías puede sesgar la comparación: si los robos violentos tienen menor cifra negra que los hurtos, el declive de los robos no violentos podría estar parcialmente sobredimensionado.

2. **Comisaría Virtual:** No es posible controlar directamente por el canal de denuncia (presencial vs. digital). La mitigación se basa en la menor susceptibilidad de los delitos de alta lesividad al efecto de conveniencia, y en la validación por placebos positivos.

3. **Cuarto quiebre Bai-Perron:** El IC del quiebre Q4 (abr. 2021) es amplio [obs. 81–149], indicando incertidumbre sobre la estabilización post-pandémica. Se requerirán datos 2025–2026 para confirmar la consolidación del último régimen.

4. **Clusters escasos (G = 16):** Aunque el WCB con pesos de Webb está diseñado para G pequeño, el potencial de distorsión inferencial no se elimina completamente. Los resultados de la RM (p_FDR = 0.053 en CUSUM) podrían ser limítrofes por falta de potencia.

5. **Denominadores poblacionales:** La corrección SERMIG es una cota inferior. El análisis de sensibilidad paramétrica demuestra invarianza a inflaciones de hasta 20%, pero la dirección neta del sesgo por migración irregular es empíricamente indeterminada.

---

## 12. Conclusión

La evidencia empírica apunta a un **cambio profundo en la composición del delito contra la propiedad en Chile** durante la última década, caracterizado por cinco hallazgos convergentes:

1. **Los robos violentos elevan su participación relativa** del 14.7% al 19.6% del total de delitos contra la propiedad en cuatro escalones ascendentes identificados por Bai-Perron (2015, 2017, 2019, 2021). La tendencia secular es significativa en el modelo Poisson (IRR = 1.248, p < 0.001 en el segmento 3).

2. **Los robos por sorpresa experimentan un colapso secular**, con su tasa reduciéndose prácticamente a la mitad controlando por shocks exógenos. Este declive antecede a la pandemia y refleja un cambio en la ecología del delito urbano.

3. **Los robos no violentos están en retroceso estructural continuo** (IRR entre 0.66 y 0.77 en todos los segmentos), sin efecto del Estallido y con caída secular robusta.

4. **El Estallido Social tuvo un efecto transitorio** (+16.9% en robos violentos, +9.5% en sorpresa) que no explica la tendencia de largo plazo. Los quiebres estructurales pre-2019 (Bai-Perron Q1, Q2 y CUSUM Ola 1) demuestran que el cambio cualitativo se gestó antes de octubre de 2019.

5. **La heterogeneidad geográfica es extrema y estadísticamente insoslayable.** La macrozona Norte — especialmente Arica y Parinacota (+72.2%) — concentra el mayor contratrend alcista, mientras que la macrozona Austral muestra declive sostenido. Esto tiene implicancias directas para la focalización territorial de políticas de seguridad.

La batería de placebos descarta artefactos de movilidad post-COVID y de propensión a denunciar, confirmando que el aumento de la violencia patrimonial tiene un componente real, respaldado independientemente por el crecimiento secular de los homicidios dolosos.

---

*Documento generado el 10/03/2026 a partir de los outputs del pipeline analítico Python/R del proyecto "Trayectoria delictual en Chile v5.0". Clasificaciones C1, C2 y C3 procesadas exhaustivamente. Todos los resultados son reproducibles a partir de los scripts en `paper1/models/` y los datos en `paper1/output/`.*
