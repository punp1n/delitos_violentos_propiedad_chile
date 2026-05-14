# Evaluación Metodológica: Cambio Estructural en Delitos Violentos contra la Propiedad (Chile 2014-2024)

En respuesta a la solicitud de revisión del protocolo (v4.0 rev.1) sobre el cambio estructural en delitos violentos en Chile, el presente documento estructura la evaluación crítica del diseño metodológico, la validación cruzada empírica por clasificación, y la coherencia narrativa de las distintas fuentes de datos consultadas.

=============================================================
## PARTE 1 — EVALUACIÓN CRÍTICA DE LA METODOLOGÍA
=============================================================

### 1. Clasificación de Delitos (C1, C2, C3)
**(a) Justificación teórica de separar Sorpresa y Violencia Dura:**
La decisión de desagregar el componente violento en C3 es desde un punto de vista criminológico impecable. Los delitos de Sorpresa (CUM 804, arrebatos o "lanzazos") son fenotípicamente dependientes de aglomeración transeúnte y contacto físico leve; como bien mostraron en el apéndice, colapsaron drásticamente (-55%) en pandemia debido al confinamiento. La "Violencia Dura", en cambio, obedece a confrontación directa de alta lesividad (armas, intimidación) y rutinas delictuales coactivas. Agruparlos bajo C1/C2 ofusca la etiología del delito e induce al error lógico de ver aumentos post-COVID que resultan ser meros rebotes de movilidad, no radicalizaciones delincuenciales.
**(b) Circularidad y cherry-picking:** 
Aislar el CUM 804 post-exploración de datos expone a críticas de adaptación (modificar la hipótesis al ver la varianza). Para mitigar el sesgo, utilizar C1 y C2 como análisis de sensibilidad y anclar C3 de manera ex-ante a convenciones internacionales (ej. ICCS-ONU) es un blindaje robusto.
**(c) Exclusión de la Receptación (C2/C3):**
Es una decisión metodológicamente defensible y necesaria. Al registrar casi 90.000 detenciones frente a poco más de 2.000 denuncias en la década, la receptación se consolida puramente como un "delito de patrullaje y pesquisa", indexando la eficiencia o el foco temporal de Carabineros/PDI en rastrear especies transadas.
**(d) Pérdida de información si se usara sólo C1:**
Restringirse a C1 llevaría a confundir un "cambio cualitativo" hacia mayor letalidad extrema con un simple aumento cuantitativo inercial o recuperativo de los lanzazos urbanos. C1 enmascara la heterogeneidad delictiva fundamental.

### 2. Modelo Econométrico Principal — Poisson-QMLE con WCB
**(a) Idoneidad del conteo Poisson:** El abordaje de Poisson mediante Quasi-Maximum Likelihood Estimation es perfecto para la distribución y modelado de denuncias o registros policiales, los cuales son procesos discretos count-data con varianzas habitualmente infladas.
**(b) Riesgo de sobredispersión:** En un ajuste clásico, usar Negative Binomial controla la sobredispersión temporal y espacial. Sin embargo, al aplicar QMLE con errores estándar Wild Cluster Bootstrap (WCB), los problemas inherentes a Poisson se neutralizan asintóticamente sin forzar la suposición restrictiva paramétrica de la Binomial Negativa frente a excesos de ceros ocasionales.
**(c) Nodos del spline basados en percentiles:** Usar percentiles P25, P50, P75 de la tendencia elimina notablemente la circularidad. Las pruebas de Chow o nodos discrecionales obligan a prefijar quiebres según sesgos mediáticos (e.g. 2019, 2022). Un spline agnóstico deja que la data dicte libremente las aceleraciones de curvatura.
**(d) WCB con G=16:** 16 regiones es un número pequeño de clústeres donde Huber-White sobreestima. El diseño de usar WCB con pesos de distribución discreta de Webb es correcto e imperativo (dado que Rademacher se quiebra en G<20).
**(e) Flexibilidad (df=4):** Un spline cúbico con pocos nodos está balanceado para captar macro-dinámicas temporales protegiendo sobre-ajustes (overfitting) dentro del modelo ya penalizado con dos dummies absorbentes gruesas para pandemia y estallido. 
**(f) Multicolinealidad spline-dummy:** Controlada si el spline describe el patrón secular mientras las dummies absorben la disrupción paramétrica directa (los caídas interceptales puras).

### 3. Tests de Quiebre Estructural — CUSUM-GLM Regional
**(a) CUSUM sobre scores GLM:** Para regiones pequeñas con bajas cotas de eventos (Magallanes, Aysén), el estadístico CUSUM sufre pérdida fatal de potencia (probabilidad alta de Error Tipo II). Afortunadamente, se introdujo el estudio de potencia computacional ex-post y el test de interacciones de Macrozona, que estabilizan las varianzas sumando masa crítica territorial.
**(b) FDR sobre las 16 hipótesis:** Ajuste de Benjamini-Hochberg es estándar de oro para pruebas comparadas moderadas como estas, superior a corrección estricta de Bonferroni. 
**(c) Macrozonas:** La consolidación Macrozonal (Norte / RM / Sur) captura ecosistemas delictivos reales compartidos (corredores fronterizos y logísticos), siendo un parche orgánicamente justificable a la alta varianza del Sur o extremo Austral.
**(d) Test de Chow pre-especificado (ene-2022):** Funciona como benchmark referencial, pero tiene poco valor etiológico real frente a la progresión difusa del re-ingreso a las calles en Chile.

### 4. Corrección Poblacional del Denominador (SERMIG)
**(a) Asumir permanencia 100% de residencia:** Es un postulado contablemente extremo y empíricamente irreal debido a re-emigraciones no formalizadas. Sin embargo, en calidad de "Cota Inferior Demográfica" es estrictamente útil porque minimiza la inflación artificial de tasas (al agrandar el dominador artificialmente). 
**(b) Inicio 2018:** Cronológicamente justificable porque las oleadas post-Censo 2017 irrumpen de forma asimétrica al perfil histórico poblacional chileno contemplado en series base del INE.
**(c) Sensibilidad parametrizada de irreculares:** La variable $k \in \{1.00 - 1.20\}$ es esencial. Sin ella y basándose solo en regularizados, el alza desproporcionada de la tasa (Norte del país) podría deberse matemáticamente a que la región dobló su población "fantasma" sin subir la población formal. 

### 5. Triangulación ENUSC — Índice Relativo
**(a) Índice Relativo:** Al normalizar a 2016 resolvió de forma elegante la asimetría temporal. Transforma el ejercicio en una evaluación del tracking o correlación proporcional: si ambas métricas ascienden sincrónicamente, el índice queda cerca a 1.0, disipando la teoría exclusiva de explosión del pánico mediático a denunciar en comisarías físicas/virtuales. 
**(b) Solapamiento Olas ENUSC:** Genera un efecto perverso de suavizamiento. Un shock hiper-agudo transcurrido en agosto de 2022 aparecerá licuado entre la ENUSC de 2022 y la de 2023 amortiguando artificialmente la medición estadística en series anualizadas.
**(c) Pérdida de representatividad rural (102 comunas):** El efecto urbano descarta realidades de robo de maderas o maquinaria pesada, concentrando el análisis en patrones criminales de ciudad, los cuales deben clarificarse en los contornos del abstract general del artículo.
**(d) Delta Method:** Técnicamente preciso para estimar las bandas de error asintótico utilizando las varianzas previas de diseño complejo (`svytotal`).

### 6. Placebos de Falsificación
**(a) Tipos de shocks evaluados:** P1 y P2 son brillantes porque abordan las principales falacias argumentales críticas al artículo: el P1 (cuasidelito vehicular) controla orgánicamente por el impacto estricto que ocasionó la baja y alta movilidad ciudadana urbana ("vuelta al taco vial"); y el P2 (homicidios) falsifica tendencias latentes de criminalidad altamente lesiva con cifra negra inexistente.
**(b) Análisis Homicidios Nacional:** Es el trade-off empírico obvio. Carece del peso regional del modelo primario pero blinda un anclaje general de validez interna general.
**(c) Confusiones de reporte letal:** Existe ciertamente algo de inflación de muertes ambiguas sin calificar. Aún así, un +134% en el crecimiento pre-post asume fuertemente un aumento general agudo de letalidad en disputas por territorio y rentas.

=============================================================
## PARTE 2 — EVALUACIÓN DE RESULTADOS POR CLASIFICACIÓN
=============================================================

### A) El espejismo de la clasificación C1 (Dummy Institucional)
Al analizar la serie C1 de forma indiferenciada, y a la luz de los datos extraídos (Apéndice pre-analítico), uno podría interpretar precipitadamente que "la suma de la violencia patrimonial en Chile creció a un techo en el año 2024 producto de una recesión en la seguridad". Sin embargo, si examinamos las tendencias disgregadas, la C1 agrupa dos categorías con trayectorias colisionantes:
En primer lugar, incluye los robos por Sorpresa, mismos que cayeron en -55% para 2021 frente a encierros, y que para 2024 acusan un desmedido impacto recuperativo o rebote (+3.3% sobre 2016). En adición interclasificatoria, Sorpresa se contamina con un delito que sí cayó mucho menos y reaccionó de forma distinta en pandemias (Violencia Dura con -36.5% de caída). Agremiarlos conduce irremediablemente a interpretar gran parte del estallido denunciante post-2022 como una ola masiva inédita de "robos armados", cuando matemáticamente obedece al retorno parcial del lanzazo en aglomeraciones. Concluir una "crisis estructural postpandemia" basados únicamente en C1 conlleva riesgo de grave imprecisión conceptual e invalidación entre pares.

### B) Aporte acotado de la exclusión C2 (Dummy Ajustada)
La exclusión de la receptación elimina la correlación espuria dictada por operativos de interceptación y aduanas orientados a confiscar y rastrear el patrimonio robado; en otras palabras, extrae al fin el filtro de "oferta policial" que distorsionaba con 89 mil detenciones el catálogo de robos No Violentos.
Sin embargo, esta restructuración del denominador o baseline sigue precarizada por el mismo sesgo flagrante que C1: mantiene empotrados los robos de oportunidad (lanzazos) junto con delitos agresivos brutales en la dimensión "Numerador de la Violencia" . De este modo, aunque el volumen basal sea más prístino, C2 es inefectiva corrigiendo la falla primaria de agrupamiento narrativo.

### C) Revelaciones empíricas de C3 (Tricotómica) y viabilidad de H1
C3 aísla dinámicas asíncronas y revela la fragilidad temporal detrás de la hipótesis de "cambio estructural o explosión de salto repentino" después de las pandemias (2022). 
Al aislar **Violencia Dura**, se devela una tendencia ininterrumpida pre-existente desde 2016 al 2019 (+16.4%). Al sufrir un embate parcial pandémico, su proceso de reemancipación hasta 2024 se estanca (+7.6% frente a 2016). Es decir, **los chilenos hoy denuncian volumétricamente menos violencia dura de lo que denunciaban en el peak histórico previo a los shocks de 2019 (-7.5% de diferencial inferior).** 
La narrativa de la "crisis de seguridad" queda de esta forma disociada empíricamente del volumen numérico absoluto de las denuncias de atraco. En su lugar, el concepto real de "crisis profunda de seguridad" queda atado únicamente al aumento del homicidio (+134%) como un termómetro extremo transversal de nuevas coacciones corporativas asociadas a mercados criminales, y no a un aumento desproporcionado inédito de asaltos a transeúntes generalizados país tras país. Esto debilita profundamente una tesis nacional y generalizada (H1) en términos de puro recuento volumétrico de denuncias de asaltos.

=============================================================
## PARTE 3 — COMENTARIO DE RESULTADOS POR FUENTE Y ESCALA
=============================================================

### 3.1 Denuncias (CCH — Nivel Nacional y Regional)
**Tendencia secular a nivel nacional:** Históricamente una trayectoria estable sustitutiva (bajan lo No-violentos, sube a cuentagotas la letalidad armada hasta el pico de 2019).
**Estallido Social (Oct 2019 - Mar 2020):** La contracción de "Sorpresa" y "No Violentos" versus el aislamiento de la "Violencia Dura" nos comunica que para acometer robos de fuerza no era obligante la coacción masiva ciudadana, al contrario de la oportunidad de robo hormiga inhibido por el toque de queda. La digitalización urbana decreció las ocasiones prestando barrera topográfica para la delincuencia basal, pero el secuestro o amedrentamiento se desancló.
**Periodo 2022-2024 vs Baseline:** La post-pandemia a nivel nacional representa el mero retorno rebotador inconcluso a escenarios comparativos de 2018-2019. No es un nuevo clímax de violaciones de propiedad.
**La excepción Macrozona Norte como salvavidas de la métrica y validante de la dimensión espacial:**
La Macrozona norte (Arica +94.3% entre 2016-2024) sí padece de forma incontestable un quiebre estructural orgánico. Tarapacá descendió en un 15%, no como disonancia fenotípica respecto del clúster norte, sino muy posiblemente como clímax extremo en un subreporte o saturación en el colapso del enforcement migratorio/denunciero (ej., víctimas no regularizadas ni legalizadas rehúsan el contacto a Carabineros por temor a fiscalizaciones propias). Estos patrones regionales concentran todo el soporte gravitacional de cara a la Hipótesis 1 (cambio heterogéneo condensado geográficamente). 
La Región Metropolitana (RM) absorbe el mayor abultamiento general (con tasas masivas sobre los >500/100K) pero sin derivas relativas fuertes, demostrando un problema sistémico de stock en desmedro de un problema nuevo de aceleración y flujos migratorios expansivos. 

### 3.2 Detenciones en Flagrancia (Robustez R7)
Apostar parte de los hallazgos en proxis reaccionarias policiales requiere un gran grado de escepticismo institucional debido a las lógicas endógenas del país.
**Implicaciones interpretativas por divergencia:** En un escenario donde el Panel de Detenciones creciese asimétricamente mayor post-2022 respecto al de Denuncias, indicaría que tras el despliegue de políticas como "Calles Sin Violencia", una sobrerreacción ministerial está abultando artificialmente el aprehensión operativa por focalizaciones contingentes, desvinculada por completo de un incremento orgánico de la victimización comunitaria subyacente. 
Asimismo, existe un sesgo inter-generacional irreconciliable para calibrar la eficacia institucional entre 2019 y 2021: Carabineros incurrió en un recogimiento policial por estallido o una paralización y traslape a controles sanitarios. La desvinculación o disociación metodológica para mantener `detenciones` como vector netamente robusto sin contaminar a la `VD` asegura un análisis final sin fallas. 

### 3.3 Victimización y Encuesta (ENUSC 1b)
Al cotejar la violencia dura CCH y su par conceptual autodeclarado (delitos rvi), anticiparíamos una dirección vertical positiva, aunque mitigada por el ruido del solapamiento metodológico propio de muestreos bi-anuales por ciclos. 
**Interpretación de los Índices de Convergencia:** Si el Índice Relativo expide estabilidad a lo largo del encierro pandémico e inicio progresivo de Comisaría Virtual, concluimos que la tendencia dictaminada por el modelo QMLE (Aumento de robos en el Norte y Estancamiento central) emana de procesos subyacentes criminalmente ciertos y no del cambio o facilidad tecnológica del comportamiento de reporte.
**Ausencia de zonas rurales y ruido local:** Restringiendo los componentes a las históricas 102 comunas pre-calibradas, abandonamos inevitablemente a una fracción nada despreciable del contexto criminal chileno como lo referente a La Araucanía interior, asumiendo su costo pero propiciando en intercambio márgenes de error muchísimo más blindados e interpretables de un fenómeno eminentemente urbano-comercial. El salto masivo del Placebo Homicida reitera paralelamente que la degradación cualitativa perniciosa del actuar armado en Chile es fáctica sin sesgos encuestales.

***
**Conclusión al Autoreporte Criminológico**
El esquema actual del artículo está metodológicamente preparado para resistir críticas rigurosas tanto desde validéz conceptual (exclusión y categorizaciones exactas), así como resiliencia de control por regresión y errores geográficos y de oportunidad poblacional. La mayor contribución analítica del paper no está en dictaminar si reventó la violencia a nivel volumen nominal contra el estamento a partir de 2022 (concluyendo de plano que no sucedió), sino en localizar donde reside geográficamente y por cuan letal espectro (Norte del país y Placebos de Extorsivos y Homicidios) de una nueva fase en dinámicas patrimoniales chilenas.
