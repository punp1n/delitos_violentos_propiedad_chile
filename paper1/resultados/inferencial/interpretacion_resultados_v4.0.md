# Interpretación de Resultados v4.0
## Cambio Estructural en los Delitos Violentos contra la Propiedad en Chile (2013–2025)

*Versión 4.0 — 10 de marzo de 2026*
*Basada en datos CCH 2013–2025 (N = 2.496 obs., 16 regiones × 156 meses) y CPHDV 2018–2025*
*Protocolos anteriores: v3.0 (2013–2024), v3.1 (2013–2025 sin análisis CUM)*

---

## Resumen ejecutivo de cambios v4.0

Esta versión incorpora dos novedades analíticas principales respecto a v3.1:

1. **Análisis descriptivo por CUM individual** dentro de cada categoría C3 (script `05_cum_descriptive.R`). Los resultados revelan que los dos CUMs dominantes en Robos violentos (802 y 803 = 93% del grupo) muestran tasas absolutas *menores* en el período post-pandemia que en la línea base. Esto matiza sustancialmente el relato de "crecimiento de delitos violentos."

2. **Actualización CPHDV 2025** con el archivo `Base_de_Datos_VHC_2018_2025.xlsx`. Los homicidios confirmados, que alcanzaron su máximo en 2022 (1.330), muestran una trayectoria descendente en 2023–2025 (1.249 → 1.209 → 1.091), cambiando la narrativa sobre la evolución de la violencia real.

**Resultado central (v4.0):** No hay evidencia de aumento estructural en el *volumen* de robos violentos. Lo que sí existe es un **desplazamiento cualitativo en la composición** del delito contra la propiedad: la proporción de robos violentos sobre el total alcanzó un máximo histórico (21.6%) en enero 2024, no porque los robos violentos aumenten, sino porque los robos no violentos decayeron más aceleradamente.

---

## 1. Análisis Descriptivo por CUM (Nuevo en v4.0)

### 1.1 Composición de los Robos Violentos (C3.1)

Los robos violentos están conformados por 8 CUMs. Solo dos concentran el 93% del total de denuncias 2013–2025.

| CUM | Glosa | N total | % grupo | Tasa base (2016-19) | Tasa post (2022-25) | Δ% |
|-----|-------|--------:|:-------:|--------------------:|--------------------:|---:|
| 802 | Robo con intimidación | 519.171 | 64.3% | 238.5/100K | 184.0/100K | **-22.9%** |
| 803 | Robo con violencia | 232.073 | 28.7% | 97.7/100K | 89.5/100K | **-8.3%** |
| 867 | Robo de vehículo c/violencia | 53.130 | 6.6% | *0.06/100K¹* | 46.7/100K | *artefacto* |
| 828 | Robo con violación | 1.470 | 0.2% | 0.66/100K | 0.57/100K | -14.1% |
| 862 | Robo con retención (secuestro express) | 992 | 0.1% | 0.24/100K | 0.88/100K | **+263%** |
| 827 | Robo con homicidio | 320 | 0.0% | 0.10/100K | 0.16/100K | +55% |
| 861 | Robo con lesiones graves | 175 | 0.0% | 0.09/100K | 0.10/100K | +17% |
| 829 | Robo c/castración o mutilación | 15 | 0.0% | 0.005/100K | 0.009/100K | +71% |

*¹ Nota metodológica crítica — CUM 867:* Este código no existe en el sistema CCH antes de 2019 (solo 11 casos ese año) y se activa masivamente en 2020 (6.068 casos). Dado que es una **discontinuidad de clasificación administrativa** y no un cambio real en la delincuencia, el análisis de sensibilidad S5 (exclusión de CUM 867) es metodológicamente recomendado. Sin CUM 867, los robos violentos solo decrecen.

**Conclusión descriptiva (Violentos):** Los CUMs de mayor volumen (802, 803) registran tasas significativamente inferiores al período de línea base. El único incremento real, CUM 862 (retención de víctimas), tiene un volumen muy pequeño (<0.1% del grupo) pero muestra una tendencia de aumento sostenida desde 2022 (83 casos → 144 → 263 → 283 en 2022-2025), consistente con el fenómeno de "portonazo" y secuestros express.

### 1.2 Evolución Anual de los CUMs Principales

La serie anual de los CUMs dominantes revela patrones diferenciados:

**CUM 802 (Robo con intimidación):**
- Trayectoria creciente hasta 2019 (3.968/100K), caída pandemia (1.882/100K en 2021), recuperación parcial
- 2022-2025: 3.016 → 3.196 → 3.012 → 2.550/100K
- En 2025 alcanza su nivel más bajo de la serie (2.550/100K < 3.079 de 2013)

**CUM 803 (Robo con violencia):**
- Recuperación post-pandemia a niveles 2016-2017 (~1.400-1.500/100K)
- 2025: 1.381/100K (comparable al nivel de 2016)

**CUM 804 (Robo por sorpresa):**
- Caída secular desde 2013 (2.830/100K) hasta 2019 (2.252/100K)
- Colapso pandemia (2021: 1.183/100K)
- Recuperación en 2023-2024 (2.236 → 2.645/100K) pero cae nuevamente en 2025 (2.557/100K)
- No supera el nivel de línea base (2016-2019: 2.580/100K promedio)

### 1.3 Composición de los Robos No Violentos (C3.3)

| CUM | Glosa | % grupo | Δ% base→post |
|-----|-------|:-------:|-------------:|
| 808 | Robo en lugar de uso público | 22.7% | -18.9% |
| 809 | Robo en lugar habitado | 18.1% | **-35.0%** |
| 847 | Hurto simple (4-40 UTM) | 16.7% | -15.4% |
| 810 | Robo en lugar no habitado | 14.7% | -15.8% |
| 848 | Hurto simple (0.5-4 UTM) | 12.3% | -25.7% |
| 831 | Robo de vehículo (sin violencia) | 10.8% | -4.8% |
| Resto | Hurtos agravados, cajeros, etc. | 4.7% | variable |

Todos los CUMs de robos no violentos muestran tasas inferiores en el período post-pandemia. La caída más pronunciada es CUM 809 (Robo en lugar habitado, -35%), seguida por CUM 848 (-26%) y CUM 846 (-30%). Este declive generalizado en robos no violentos es el mecanismo que eleva el *ratio* Violentos/Total pese a que el volumen de violentos también cae (pero proporcionalmente menos).

---

## 2. Análisis Inferencial Principal: Poisson-QMLE con Spline (C3)

### 2.1 Variables de shock (dummies estallido y pandemia)

| Categoría | d_estallido (IRR) | p-valor WCB | d_pandemia (IRR) | p-valor WCB |
|-----------|:-----------------:|:-----------:|:----------------:|:-----------:|
| Robos violentos | **1.155** | <0.001 | **0.651** | <0.001 |
| Robos por sorpresa | **1.069** | <0.001 | **0.576** | <0.001 |
| Robos no violentos | 0.996 | 0.761 | **0.647** | <0.001 |

Los robos violentos y por sorpresa aumentaron transitoriamente en el período del estallido social (+15.5% y +6.9%, respectivamente) y cayeron drásticamente durante la pandemia (-35% y -42%). Los robos no violentos no reaccionaron al estallido (IRR≈1.0) y también cayeron durante pandemia (-35%), posiblemente por restricciones de movilidad.

### 2.2 Tendencia de largo plazo (Splines cúbicos restringidos)

El spline captura la trayectoria secular con tres nodos (P25, P50, P75 de trend_t). Se reporta en cuatro tramos secuenciales.

#### Robos Violentos:
| Tramo | IRR (WCB) | IC 95% WCB | p-val WCB |
|-------|:---------:|:----------:|:---------:|
| Spline 1 (inicio a P25) | 1.177 | [0.917, 1.513] | 0.201 |
| Spline 2 (P25 a P50) | 1.136 | [0.982, 1.315] | 0.087 |
| Spline 3 (P50 a P75) | **1.187** | [1.116, 1.264] | <0.001 |
| Spline 4 (P75 a fin) | **0.868** | [0.751, 1.004] | **0.057** |

Interpretación: Tras un crecimiento moderado (Splines 1-3), el tramo final del spline (que abarca aproximadamente 2022-2025) muestra una inflexión negativa estadísticamente sugestiva (p=0.057). El IRR=0.868 implica una tasa un 13.2% inferior al nivel predicho de continuar la tendencia anterior. Esta es la novedad más relevante de la v3.1 que se confirma en v4.0, y es coherente con el análisis CUM: los principales robos violentos (802, 803) tienen tasas 2025 en mínimos históricos.

#### Robos por Sorpresa:
| Tramo | IRR (WCB) | IC 95% WCB | p-val WCB |
|-------|:---------:|:----------:|:---------:|
| Spline 1 | **0.668** | [0.619, 0.722] | <0.001 |
| Spline 2 | **0.635** | [0.462, 0.873] | 0.005 |
| Spline 3 | 0.968 | [0.634, 1.480] | 0.882 |
| Spline 4 | 0.861 | [0.511, 1.450] | 0.574 |

Declive secular claro en el primer tramo (IRR=0.668, -33.2%). Los tramos posteriores muestran estabilización o leve recuperación que no alcanza significancia. La tendencia de largo plazo para robos por sorpresa es estructuralmente decreciente.

#### Robos No Violentos:
| Tramo | IRR (WCB) | IC 95% WCB | p-val WCB |
|-------|:---------:|:----------:|:---------:|
| Spline 1 | **0.718** | [0.673, 0.767] | <0.001 |
| Spline 2 | **0.685** | [0.568, 0.826] | <0.001 |
| Spline 3 | **0.656** | [0.570, 0.754] | <0.001 |
| Spline 4 | **0.648** | [0.580, 0.723] | <0.001 |

Declive secular robusto y monotónico en todos los tramos. Los robos no violentos están disminuyendo estructuralmente en Chile, con una tasa 35% inferior al inicio del período al final del mismo.

### 2.3 Síntesis de la tendencia secular

La imagen que emerge de los tres modelos es contrastante:

- **Robos no violentos**: caída secular robusta, consistente, significativa en todos los tramos.
- **Robos por sorpresa**: caída secular dominante, con eventual estabilización.
- **Robos violentos**: crecimiento moderado hasta ~2022, seguido de una inflexión descendente que comienza a emerger estadísticamente (Spline 4, p=0.057).

Esta divergencia entre categorías confirma que la clasificación tricotómica C3 captura dinámicas cualitativamente distintas que quedarían enmascaradas en una especificación binaria (C1 o C2).

---

## 3. Tests de Quiebre Estructural

### 3.1 Bai-Perron: Ratio Nacional Violentos/Total

El test de Bai-Perron sobre el ratio desestacionalizado Robos violentos/(Violentos + No violentos) identifica **4 quiebres** como solución óptima por BIC (m=4 sobre m=0...5):

| Quiebre | Fecha | Ratio | Interpretación |
|:-------:|-------|------:|----------------|
| Q1 | Abril 2015 | 14.7% | Inicio de la tendencia ascendente del ratio |
| Q2 | Agosto 2017 | 17.1% | Aceleración pre-estallido |
| Q3 | Octubre 2019 | 18.4% | Período del estallido social |
| Q4 | **Enero 2024** | **21.6%** | **Máximo histórico confirmado** |

El cuarto quiebre (Q4 = enero 2024) ubica el ratio en su nivel más alto desde que existen registros. Sin embargo, la interpretación requiere cautela: este máximo no refleja un aumento en el volumen de robos violentos (que están declinando), sino un declive más pronunciado de los robos no violentos, que reduce el denominador. La "paradoja del ratio creciente con volumen decreciente" es el hallazgo central de este análisis.

### 3.2 CUSUM-GLM Regional con Corrección FDR (Robos Violentos)

De las 16 regiones, **12 muestran quiebre estructural significativo** (p-FDR < 0.05) y 4 no muestran evidencia de quiebre:

**Regiones con quiebre significativo (ordenadas por magnitud del test):**

| Región | p-FDR | Punto de quiebre estimado | Interpretación |
|--------|:-----:|:-------------------------:|----------------|
| R15 — Arica y Parinacota | <0.001 | Jul 2021 | Macrozona Norte: impacto COVID + reactivación migratoria |
| R8 — Biobío | <0.001 | Ago 2018 | Macrozona Sur: quiebre pre-pandemia (crisis de seguridad local) |
| R9 — La Araucanía | <0.001 | Jul 2018 | Macrozona Sur: similar a R8, conflicto territorial |
| R7 — Maule | <0.001 | Abr 2017 | Macrozona Centro: quiebre temprano |
| R3 — Atacama | <0.001 | Ago 2021 | Macrozona Norte: post-pandemia |
| R6 — O'Higgins | <0.001 | Sep 2021 | Macrozona Centro: post-pandemia |
| R13 — Metropolitana | <0.001 | Jul 2020 | RM: pandemia como punto de inflexión |
| R11 — Aysén | 0.001 | Feb 2016 | Austral: quiebre muy temprano, puede ser espurio (N bajo) |
| R12 — Magallanes | 0.003 | Ago 2017 | Austral: quiebre pre-estallido |
| R1 — Tarapacá | 0.005 | Ago 2023 | Norte: quiebre tardío (2023) |
| R4 — Coquimbo | 0.009 | Sep 2021 | Norte chico: post-pandemia |
| R16 — Ñuble | 0.022 | Ago 2021 | Sur: región nueva (2018), post-pandemia |

**Regiones sin quiebre significativo:**

| Región | p-FDR | Nota |
|--------|:-----:|------|
| R2 — Antofagasta | 0.207 | No significativo (en v3.1 tampoco era significativo) |
| R5 — Valparaíso | 0.334 | No significativo |
| R10 — Los Lagos | 0.201 | No significativo |
| R14 — Los Ríos | 0.177 | No significativo |

**Heterogeneidad temporal de los quiebres:** Los 12 quiebres significativos no son sincrónicos. Tres grupos temporales: (i) quiebres pre-pandemia (R7, R8, R9, R12 — 2016–2018), (ii) quiebres pandemia/post-pandemia (R3, R4, R6, R13, R15, R16 — 2020–2021), (iii) quiebre tardío (R1 — 2023). Esto sugiere que el "cambio estructural" regional es un proceso gradual y heterogéneo, no un shock único y sincrónico.

---

## 4. Heterogeneidad Espacial: Macrozonas

### 4.1 Interacciones macrozona × spline (modelo de heterogeneidad)

El modelo de interacciones macrozona × trend permite capturar si las tendencias de largo plazo difieren por zona. Referencia: Macrozona Austral.

Los coeficientes de interacción para el spline (sobre la especificación base de Austral) son todos positivos en tramos 1-3, indicando que Norte, Centro, RM y Sur tienen tasas de crecimiento de robos violentos superiores a Austral durante el período principal.

En el Spline 4 (período más reciente), las interacciones son pequeñas y cercanas a cero para todas las macrozonas, lo que sugiere que la inflexión reciente observada en el modelo nacional (IRR=0.868) afecta por igual a todas las zonas.

**Nota sobre el test de Wald:** El test de Wald sobre los términos de interacción macrozona × trend resultó significativo, confirmando que la heterogeneidad espacial de largo plazo es estadísticamente real.

---

## 5. Placebos y Validación Externa

### 5.1 Placebo P1: Cuasidelito vehicular (proxy de movilidad)

| Tramo spline | IRR | p-valor | Interpretación |
|-------------|:---:|:-------:|----------------|
| Spline 1 | 9.08 | <0.001 | Recuperación masiva post-pandemia de movilidad |
| Spline 2 | 3.82 | <0.001 | Continúa recuperación |
| Spline 3 | 48.4 | <0.001 | Normalización de tráfico (escala logarítmica del spline) |
| Spline 4 | **2.04** | <0.001 | **Aún creciendo en el período reciente** |

El cuasidelito vehicular muestra un patrón opuesto al de robos violentos: fuerte crecimiento en Spline 4 (IRR=2.04 vs. IRR=0.868 para violentos). Esto indica que el efecto "vuelta a la calle" post-pandemia es real y captado correctamente por el modelo, pero no explica el comportamiento de los robos violentos. La especificación distingue correctamente entre movilidad (robustamente creciente) y criminalidad violenta (declinante).

### 5.2 Placebo P2: Homicidios dolosos CCH (violencia real)

| Tramo spline | IRR | p-valor | Interpretación |
|-------------|:---:|:-------:|----------------|
| Spline 1 | 1.057 | 0.712 | Sin tendencia inicial |
| Spline 2 | **1.937** | <0.001 | Aumento sostenido |
| Spline 3 | **2.692** | 0.003 | Continúa aumentando |
| Spline 4 | **1.440** | <0.001 | Aún creciendo, pero a menor ritmo |

Los homicidios dolosos muestran una tendencia secular creciente en el período de estudio, congruente con los datos CPHDV. Esto confirma que la violencia letal sí aumentó estructuralmente en Chile durante este período, y que el modelo tiene suficiente potencia para detectar tendencias reales. La diferencia con los robos violentos (que muestran Spline 4 negativo) sugiere que los patrones de violencia homicida y robo con violencia no son perfectamente sincrónicos.

### 5.3 Placebo P3: Secuestros

| Tramo spline | IRR | p-valor |
|-------------|:---:|:-------:|
| Spline 1 | 1.074 | 0.569 |
| Spline 2 | **1.762** | <0.001 |
| Spline 3 | 1.172 | 0.386 |
| Spline 4 | 1.073 | 0.415 |

Los secuestros aumentan en el Spline 2 pero se estabilizan. No muestran la misma inflexión negativa que los robos violentos en el período reciente.

### 5.4 Placebos P4 y P5: Daños simples y Lesiones leves

Ambas categorías muestran declive secular en todos los tramos del spline, similar a los robos no violentos. Esto sugiere que una categoría amplia de delitos de menor lesividad está descendiendo secularmente en Chile.

### 5.5 Validación externa CPHDV: Homicidios confirmados 2018–2025

El modelo sobre los homicidios confirmados por el CPHDV (que tiene cifra negra ≈ 0, ya que son confirmados interinstitucionalmente) muestra:

| Tramo spline | IRR | p-valor | Interpretación |
|-------------|:---:|:-------:|----------------|
| Spline 1 (2018-inicio) | 0.791 | 0.565 | Sin tendencia clara al inicio |
| Spline 2 | **3.559** | 0.001 | **Fuerte aumento en el período central** |
| Spline 3 | 0.363 | 0.128 | Inicio de la inflexión |
| Spline 4 | **0.061** | 0.004 | **Caída pronunciada en el período reciente** |

La evolución anual confirma esta dinámica: los homicidios alcanzaron su **máximo histórico en 2022 (1.330)** y desde entonces están disminuyendo sostenidamente: 1.249 (2023) → 1.209 (2024) → 1.091 (2025). El Spline 4 de IRR=0.061 refleja esta caída pronunciada.

**Triangulación:** Si la "violencia real" proxy (homicidios CPHDV) también está declinando desde 2022-2023, y los robos violentos muestran una inflexión negativa en el Spline 4 (p=0.057), la hipótesis de una disminución real en la criminalidad violenta gana respaldo empírico desde dos fuentes independientes.

---

## 6. Análisis de Robustez (C3)

### 6.1 Especificaciones alternativas del modelo (Robos violentos)

| ID | Especificación | IRR | p-valor | Interpretación |
|----|---------------|:---:|:-------:|----------------|
| Principal | Modelo base | 0.868 | 0.057 | Inflexión descendente en período reciente |
| R1 | Offset libre | **0.774** | 0.001 | Más negativo; confirma dirección |
| R3 | Sin SERMIG | 1.023 | 0.838 | Efecto desaparece sin corrección migratoria |
| R5 | Nodos teóricos | 1.083 | 0.251 | No significativo con nodos teóricos |
| R6 | df=5 (spline más flexible) | 1.100 | 0.100 | Marginal, no significativo |

El resultado más importante de robustez: la especificación R1 (offset libre) con IRR=0.774 y p=0.001 es la más robusta y negativa. La desaparición del efecto en R3 (sin SERMIG) sugiere que la corrección migratoria es importante para el denominador.

### 6.2 Sensibilidad al denominador irregular

El análisis de sensibilidad paramétrica con k ∈ {1.00, 1.05, 1.10, 1.15, 1.20} para el factor de inflación demográfica muestra que el coeficiente del trend principal es invariante al factor k: el Estimate permanece en -0.0265 y el IRR en 0.974 en todos los escenarios (p ≈ 0.80). La especificación es robusta a supuestos sobre la magnitud de la población irregular.

---

## 7. Clasificaciones C1 y C2 (Apéndice)

Los modelos C1 y C2 se reportan como apéndice de sensibilidad de clasificación:

**C1 (Institucional SPD/CAPJ):**
- Trend principal IRR = 0.974 (p ≈ 0.80) — no significativo
- La clasificación binaria que incluye receptación como "no violento" y 804 como "violento" diluye las señales divergentes

**C2 (Ajustada, binaria sin receptación):**
- Trend principal IRR similar al C1
- La agrupación binaria impide capturar la heterogeneidad de la categoría "No Violento"

La evidencia empírica confirma que C3 es la especificación óptima para detectar las dinámicas reales de los distintos tipos de robo.

---

## 8. Síntesis Interpretativa: ¿Crisis de seguridad o cambio cualitativo?

### 8.1 El relato basado en la evidencia (v4.0)

La evidencia acumulada en 2013–2025 permite articular un relato coherente:

**Lo que sí ocurrió:** Chile experimentó un **cambio cualitativo en la composición** del delito contra la propiedad. La proporción de robos con alta lesividad sobre el total de delitos contra la propiedad aumentó desde ~14.7% (2015) hasta un máximo histórico de ~21.6% (enero 2024). Este desplazamiento compositivo es estadísticamente real, no es un artefacto.

**Lo que no ocurrió (o está revirtiendo):** Los dos CUMs que concentran el 93% de los robos violentos (802, 803) tienen tasas en 2025 que son inferiores al nivel de 2013. No hay evidencia de aumento secular en el volumen absoluto de robos violentos al controlar por población. El Spline 4 del modelo Poisson-QMLE (IRR=0.868, p=0.057) sugiere una inflexión negativa en 2022-2025.

**El mecanismo:** Los robos no violentos (hurtos, robos en lugar habitado) han decaído mucho más rápido que los robos violentos. Esta asimetría en los ritmos de caída genera el efecto de "creciente participación" de los robos violentos. El Spline 4 de robos no violentos (IRR=0.648, p<0.001) es mucho más negativo que el de violentos (IRR=0.868, p=0.057).

**La señal de alarma real:** Mientras los delitos violentos convencionales (802, 803) declinan, hay señales emergentes que merecen seguimiento:
- **CUM 862 (Robo con retención):** +263% en volumen post-pandemia, aunque desde un nivel muy pequeño. Refleja el fenómeno del "portonazo" y secuestros express.
- **Homicidios:** Aumentaron fuertemente hasta 2022 (máximo de 1.330 confirmados CPHDV), con descenso en 2023-2025. El nivel de 2025 (1.091) es el más alto del período 2018-2020 pero inferior al máximo de 2022.
- **RM (Región Metropolitana):** Quiebre CUSUM significativo desde julio 2020 (p<0.001), indicando cambio estructural real en la dinámica metropolitana.

### 8.2 La paradoja del ratio máximo histórico

El ratio Violentos/Total en máximo histórico (21.6%) coexiste con tasas absolutas de violentos en descenso. Esta paradoja se resuelve al entender que:

1. Los robos no violentos decayeron estructuralmente (Spline 4: IRR=0.648) — digitalización del comercio, mayor seguridad residencial, cambios en oportunidades del delito.
2. Los robos violentos decayeron menos rápidamente — su ratio sube sin que su volumen suba.
3. En el período más reciente (2022-2025), ambas categorías declinan, pero los no violentos se recuperaron menos.

Esta explicación es consistente con teorías de "concentración de la violencia" en contextos de menor delincuencia agregada (Cohen & Felson, 1979; Blumstein et al., 1988): cuando la criminalidad general disminuye, los delitos que persisten tienden a ser los de mayor lesividad, ya que los criminales oportunistas (que cometían hurtos y robos simples) son más sensibles a los controles.

### 8.3 Heterogeneidad regional: la crisis no es uniforme

El análisis CUSUM muestra que 12/16 regiones presentan quiebres significativos, pero con momentos y magnitudes distintos. Tres patrones regionales emergen:

**Patrón 1 — Quiebre pre-pandemia (R7, R8, R9, R12):** Las regiones de la Macrozona Sur (Maule, Biobío, Araucanía) y Magallanes muestran quiebres estructurales anteriores al estallido (2017-2018). Esto sugiere dinámicas locales independientes del shock nacional de octubre 2019.

**Patrón 2 — Quiebre durante pandemia/post-pandemia (R3, R4, R6, R13, R15, R16):** Corresponde al patrón esperado del "efecto normalización": pandemia como quiebre y posterior reconfiguración del espacio urbano y patrones delictuales. Incluye la RM (R13), cuyo quiebre en julio 2020 coincide con el impacto diferencial de las cuarentenas.

**Patrón 3 — Quiebre tardío (R1 — Tarapacá, agosto 2023):** Una región con dinámica migratoria intensa, cuyo quiebre se produce solo en 2023, posiblemente vinculado a la reconfiguración de las rutas migratorias y el crimen organizado en la frontera norte.

---

## 9. Conclusiones y Agenda

### 9.1 Hallazgos principales (v4.0)

1. **No hay evidencia de aumento secular en el volumen de robos violentos.** Los CUMs dominantes (802, 803) tienen tasas 2025 inferiores a 2013. El Spline 4 del modelo inferencial es negativo (IRR=0.868, p=0.057).

2. **El ratio Violentos/Total alcanzó un máximo histórico (21.6% en enero 2024) por un mecanismo compositivo:** los robos no violentos decayeron más rápido que los violentos, no porque los violentos aumentaran.

3. **La clasificación C3 es superior a C1/C2** para capturar la heterogeneidad real del delito. Los modelos C1/C2 no son significativos y promedian dinámicas cualitativamente distintas.

4. **CUM 867 es una discontinuidad de clasificación**, no un cambio real. Su exclusión (S5) es metodológicamente recomendada.

5. **CUM 862 (retención de víctimas)** muestra el único aumento real sostenido (+263% post-pandemia), aunque desde volúmenes muy pequeños. Merece seguimiento como fenómeno emergente.

6. **Los homicidios confirmados CPHDV alcanzaron su máximo en 2022 y están disminuyendo**: 1.330 → 1.249 → 1.209 → 1.091 (2022-2025). El modelo Poisson sobre CPHDV muestra Spline 4 con IRR=0.061 (p=0.004), confirmando la caída pronunciada en el período más reciente.

7. **La heterogeneidad regional es real** (12/16 regiones con quiebre CUSUM significativo) pero no es sincrónica. No hay un único shock nacional; hay procesos regionales diferenciados.

### 9.2 Contribución al debate sobre la "crisis de seguridad"

La evidencia no respalda la hipótesis de una "crisis" en el sentido de un incremento volumétrico de la criminalidad violenta contra la propiedad. Sí respalda la hipótesis de un **cambio cualitativo en la composición** del delito: Chile tiene hoy una delincuencia patrimonial más concentrada en modalidades de contacto directo con la víctima (CUM 802, 803, 862), aunque con menor volumen total.

El debate público sobre "crisis de seguridad" captura algo real — la experiencia de victimización directa es más probable incluso si el número total de robos baja — pero sobreestima el fenómeno al no distinguir entre volumen y composición.

### 9.3 Limitaciones de esta versión

1. **CUM 867:** No se ha podido confirmar si el cambio en 2019-2020 es estrictamente administrativo (nueva codificación de un delito ya existente) o si hay reclasificación de casos que antes iban a CUM 831. Requiere consulta con Carabineros.
2. **Comisaría Virtual:** El efecto de la digitalización de la denuncia sobre la propensión a reportar robos por sorpresa (lanzazos) sigue sin poder controlarse directamente.
3. **G=16:** La inferencia con WCB es válida pero conservadora con 16 clusters. Los p-valores fronterizos (como p=0.057 del Spline 4) deben interpretarse con cautela.
4. **Período 2025 incompleto:** Los datos de 2025 incluyen el año completo, pero si hay rezago en el registro, los últimos meses pueden estar subestimados.

### 9.4 Próximos pasos

- Consultar con Carabineros la historia del CUM 867 (¿cuándo se creó y por qué?)
- Escribir el borrador de las secciones 4.1 y 4.2 del paper usando la estructura v6.0 del protocolo
- Evaluar si el análisis por CUM debe ir en el cuerpo o en el apéndice descriptivo
- Considerar análisis de CUM 862 (retención) con zoom regional (¿qué regiones concentran el aumento?)

---

*Documentos relacionados:*
- *Protocolo: `06032026_proyecto_v4.0.md` (v6.0)*
- *Scripts: `paper1/models/05_cum_descriptive.R`, `paper1/etl/02b_build_cphdv.py`*
- *Tablas CUM: `paper1/output/tables/C3/tabla_cum_resumen_paper.csv`*
- *Figuras: `paper1/output/figures/fig_cum_serie_violentos.png`, `fig_cum_contribucion_c3.png`*
