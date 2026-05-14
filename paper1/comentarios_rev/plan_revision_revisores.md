# Plan de revisión frente a comentarios de revisores

Documento preparado a partir de la revisión de `paper1/comentarios_rev` (tres dictámenes: `rev1.md`, `JOQC-D-26-00090_Review.pdf`, `JQC-D-25-00241.pdf`), `paper1/texto`, `paper1/models`, `paper1/etl`, `paper1/output`, `paper1/resultados` y `paper1/marco_teorico`.

Fecha original: 2026-05-10. Actualización: 2026-05-14 (incorpora evaluación detallada de las tres revisiones, viabilidad del panel comunal, plan de ETL complementario, uso parsimonioso de ENUSC desde `paper2`, pivote de revista hacia *Crime, Law and Social Change* y ejecución de Fase 2 en Python).

## 0. Mapa de revisores y prioridades

El paper fue rechazado en JQC con tres dictámenes que en buena medida son convergentes. Para no diluir las respuestas, conviene marcarlos así:

- **R1** = `rev1.md` (Reviewer #1, JQC). Es el más crítico. Tono "rechazo defendible". Ejes: (a) el texto se lee como reporte de política y no como artículo académico; (b) agregación regional muy gruesa y poco útil para policía/política, citando Barthelon & Kruger (2011, JPE) como referencia comunal en Chile; (c) la nueva categorización C3 parece *ad hoc* y necesita validación externa; (d) mecanismos (smartphones, fraude, secuestros) subdesarrollados; (e) abstract jergoso; (f) homicidios como benchmark mal justificado; (g) faltan definiciones tempranas (CEP, dark figure); (h) "snatching" como categoría separada no está suficientemente argumentado.
- **R2** = `JOQC-D-26-00090_Review.pdf` (Reviewer JOQC). El más "metodológico". Ejes: (a) terminología "non-violent robbery" / "property crime" no calza con consenso disciplinar — recomienda título sin "property" y posiblemente sin "violent"; (b) tres Poisson separados no son comparables como prueba de composición; (c) "composición" se usa para tres fenómenos distintos sin distinción conceptual; (d) el test composicional debe hacerse dentro de un mismo modelo; (e) fraude digital aparece tarde y pone en riesgo la conclusión por sustitución modal; (f) resultados desordenados; (g) abstract denso; (h) H3 confusa.
- **R3** = `JQC-D-25-00241.pdf` (Reviewer JQC más constructivo). Acepta la contribución y propone fortalecimiento. Ejes: (a) discusión empírica del vínculo entre delito objetivo y percepción (modelos constructivista vs objetivista — Beckett 1997, Shi et al. 2020, Enns 2014/2016, Duxbury 2021, Marambio & Navia 2026); (b) contextualizar el estallido social al frente del paper; (c) diseño ITS sin discusión de supuestos causales, autocorrelación (PACF) ni estacionariedad (ADF/KPSS); (d) heterogeneidad regional: explorar por qué algunas regiones no presentaron break pandémico, idealmente con indicadores sociales regionales; (e) mecanismos alternativos de desigualdad (strain, eficacia colectiva), no solo Becker; (f) SERMIG no descuenta emigración — no es "lower bound" estricto; (g) WCB no justifica Poisson-QMLE — son dos cosas separadas; (h) mediadores (movilidad, protesta, confianza) al menos en agenda futura; (i) breaks de Tabla 5/Fig 5 no coinciden con la especificación principal — explicitar carácter exploratorio vs confirmatorio; (j) mover interacciones macrozona × shocks al cuerpo, antes del Bai-Perron; (k) mapa facetado con breaks + splines como visualización espacial.

La matriz al final del documento (§ 20) etiqueta cada comentario por revisor para asegurar trazabilidad.

## Pivote de revista: de JQC a Crime, Law and Social Change

El paper fue rechazado en JQC y la próxima destinataria es *Crime, Law and Social Change* (CLSC, Springer). Las implicancias del cambio:

- **Encaje temático más natural.** CLSC publica regularmente trabajo sobre crisis de seguridad, gobernanza criminal y crimen organizado en América Latina. El marco de "narrativa de crisis vs evidencia empírica" en Chile encaja mejor que en una revista metodológicamente purista. Esto permite mantener (con cuidado) parte del lenguaje de "security crisis" como objeto de estudio, no solo como contexto.
- **Mayor tolerancia a integración cualitativa-cuantitativa.** CLSC valora la incorporación de literatura sobre percepción pública, política penal, moral panic y construccionismo. El comentario de R3 sobre Beckett/Enns/Duxbury/Shi se vuelve un activo y no un parche.
- **Sin embargo, los problemas estructurales detectados por R1 y R2 siguen vigentes.** El cambio de revista no resuelve la falta de un test composicional formal, la ambigüedad terminológica ni la crítica de agregación regional. Estos deben corregirse de todos modos.
- **Extensión.** CLSC fija un máximo de 10.000 palabras. Esto obliga a mover el aparato técnico secundario al apéndice y a que todo análisis nuevo reemplace texto existente, no que se sume al manuscrito.
- **Tono.** El reviewer R1 fue específico en que el manuscrito "lee más como reporte de política que como artículo académico". CLSC tolera framing de política más que JQC, pero el remedio no es cambiar de revista para evitar la crítica, sino reescribir la contribución en clave criminológica e investigativa (composición de delitos reportados como objeto, no como evidencia para un debate electoral).
- **Plazos.** CLSC suele tener tiempos de primera revisión de 3–5 meses. Esto da margen para la Fase 2 (modelo composicional + diagnósticos ITS + comuna).
- **Riesgo.** CLSC tiene un perfil más sociolegal; si el manuscrito termina muy concentrado en Poisson-QMLE/WCB sin discusión sociológica/legal, podría ser desk-rechazado por *fit*. La reescritura del frame en clave de "categorías administrativas, taxonomía internacional y discurso público de crisis" es esencial.

Implicancia operativa: la revisión que sigue se concibe para CLSC, pero se construye de modo que sea defendible también en una revista cuantitativa pura (JQC, *Criminology*, *J. Research in Crime and Delinquency*) por si CLSC pide cambios o se vuelve a hacer ronda.

## Diagnóstico general

El manuscrito tiene una contribución empírica defendible, pero los tres revisores convergen en una crítica central: el artículo afirma estudiar cambio composicional, pero la inferencia principal todavía descansa demasiado en modelos separados de conteos y en evidencia descriptiva del ratio. La revisión debe convertir el cambio composicional en el objeto inferencial principal, no solo en una interpretación posterior de trayectorias separadas.

La estrategia de respuesta debe ser una revisión mayor, no cosmética. El paper debe pasar de una narrativa de "security crisis" con mucha carga de política contingente a un artículo criminológico sobre composición de robos y delitos patrimoniales reportados. La pregunta debe ser más simple; la terminología debe alinearse con el uso internacional; los mecanismos deben quedar separados conceptualmente; y el modelo debe incorporar un test directo de la proporción de eventos violentos. Además, debe construirse explícitamente el puente entre cifras objetivas y percepción pública (R3), tarea para la cual hay literatura concreta a citar y, parcialmente, datos en la propia ENUSC.

El paquete actual ya contiene piezas útiles para responder: panel región-mes 2013-2025, panel comuna-mes CCH (345 comunas, ~51 564 comuna-meses en C3), el panel ENUSC armonizado de `paper2` para 2016-2024 (238 262 observaciones Kish con peso válido en las 102 comunas históricas), placebo panel, CPHDV, fraude digital, modelos Poisson-QMLE, CUSUM, Bai-Perron, robustez y mapas. La revisión debe explotar mejor esos elementos sin convertir ENUSC en un segundo artículo: ENUSC se usará como triangulación descriptiva de percepción y victimización personal, mientras que la validación fina de la clasificación C3 descansará en la armonización conceptual CUM/ICCS, el modelo composicional directo y las sensibilidades C1/C2/snatching.

## Plan parsimonioso para ETL, modelos y resultados

Este plan es la regla operativa de la revisión. El manuscrito debe caber en 10.000 palabras y por tanto cada análisis nuevo debe reemplazar texto existente o ir al apéndice. La prioridad no es sumar evidencia, sino ordenar la evidencia que responde directamente a los revisores.

### Principio rector

El nuevo artículo debe defender una contribución más estrecha: los registros policiales de delitos patrimoniales físicos no muestran simplemente una crisis volumétrica, sino un cambio composicional medible. El test principal debe estimar directamente la proporción de eventos confrontacionales; los modelos de tasas, ENUSC, comuna, placebos y fraude digital solo cumplen funciones de explicación, robustez o contexto.

### Núcleo obligatorio

1. **Auditoría/reconstrucción ETL CCH.** Antes de reestimar modelos, centralizar la clasificación CUM en una única tabla o función `CUM -> C1/C2/C3/ICCS`, porque hoy `01_extract_cch.py` y `06_assemble_panel.py` no tratan idénticamente `CUM 804` ni receptación. La versión revisada debe eliminar columnas residuales tipo `Unknown` del panel final y producir un reporte de QA.
2. **Modelo composicional directo.** Implementar el binomial agrupado `cbind(confrontational, non_confrontational)` como estimando principal. El Poisson-QMLE deja de ser prueba de composición y pasa a explicar la dinámica de tasas que produce el cambio del share.
3. **Robustez comunal CCH.** Usar el panel comuna-mes como respuesta a R1, pero solo como robustez/heterogeneidad. No convertir la comuna en diseño principal porque ENUSC, SERMIG y breakpoints regionales no migran limpiamente a esa escala.
4. **ENUSC contextual.** Reutilizar `paper2` para una figura nacional 2016-2024 de percepción y victimización personal. No armonizar denuncia ENUSC, RFV/HUR ni análisis comunal.
5. **Diagnósticos ITS mínimos.** Reportar PACF/Ljung-Box y ADF/KPSS de forma compacta, junto con sensibilidad AR/log-ratio, para responder a R3 sin transformar el paper en un artículo de series de tiempo.
6. **Resultados reordenados.** Presentar primero composición, luego tasas por tipo, luego heterogeneidad territorial y al final validación/robustez. CUSUM completo, Bai-Perron largo, placebos extendidos, CUM anual wide y diagnósticos técnicos deben ir al apéndice.

### Interfaces y outputs mínimos

- `paper1/output/tables/cch_etl_audit_report.csv`: completitud región-mes y comuna-mes, totales por CUM, denuncias vs detenciones, población faltante, categorías excluidas y consistencia C1/C2/C3.
- `paper1/output/data/panel_region_month.parquet`: panel regional auditado, sin `Unknown` como categoría modelable.
- `paper1/output/data/panel_comuna_month.parquet`: panel comunal con población mensual INE y sin corrección SERMIG comunal.
- `paper1/output/tables/C3/tabla_9_composition_logit.csv` y `tabla_9b_logratio_model.csv`: test principal de composición.
- `paper1/output/tables/C3/tabla_9c_marginal_shares.csv`, `tabla_9d_composition_sensitivity.csv`, `tabla_9e_counts_rates_period_change.csv` y `tabla_9f_multinomial_sensitivity.csv`: diferencias de share, sensibilidad de snatching/CUM 867, conteos vs tasas y multinomial descriptivo.
- `paper1/output/tables/C3/tabla_11_communal_robustness.csv`: robustez comuna full/dense.
- `paper1/output/tables/enusc_context_series.csv` y `enusc_context_qa.csv`: triangulación ENUSC desde `paper2`.
- `paper1/output/tables/C3/tabla_10_its_diagnostics.csv`: diagnósticos ITS compactos.
- `paper1/output/tables/C3/tabla_4b_macrozona_shock_interactions.csv`: efectos shock x macrozona.

### Criterios de exclusión para no inflar el paper

- **Fuera del cuerpo principal:** CASEN comunal, Subtel/CMF, dotación de Carabineros, denuncia ENUSC, análisis comunal ENUSC y modelos de mediación.
- **Apéndice o agenda futura:** fraude digital extendido, smartphones como mecanismo empírico, CUM 862 detallado, placebos completos y mapas comunales extensos.
- **Cuerpo principal máximo:** cinco exhibiciones: serie/tasas y ratio descriptivo; modelo composicional; Poisson resumido por tipo; heterogeneidad territorial compacta; robustez/validación clave.

### Tests de aceptación

- El panel regional debe tener 2.496 filas (`16 x 156`) y población mensual no faltante.
- El panel comunal balanceado debe tener 53.820 comuna-meses (`345 x 156`) antes de filtros de densidad. El archivo CCH largo actualmente observado tiene 51.564 comuna-meses con al menos un CUM objetivo registrado; el ensamblaje comunal debe completar ceros explícitos.
- Los totales CCH por CUM deben coincidir entre extracción, agregación regional y agregación comunal.
- `CUM 804` y receptación deben tener una clasificación única y documentada en todos los scripts.
- El modelo composicional binomial, el log-ratio y la sensibilidad de `snatching` deben apuntar en la misma dirección sustantiva.
- ENUSC debe replicar la serie de `paper2`, conservar 238.262 observaciones con peso válido y excluir las comunas nuevas de 2023-2024.
- El manuscrito debe dejar explícito que el diseño ITS es observacional y que los resultados no identifican efectos causales fuertes.

## Problemas mayores identificados

### 1. El paper no testea formalmente la composición

Los revisores aceptan que la idea del ratio es interesante, pero objetan que:

- El ratio violento/no violento está presentado como evidencia descriptiva.
- Los tres modelos Poisson separados no son directamente comparables como prueba de un proceso composicional único.
- Diferencias entre ecuaciones pueden reflejar sobredispersión, heterogeneidad no observada o dinámica temporal distinta, no necesariamente composición.

Prioridad: agregar un modelo donde la variable dependiente sea directamente la composición.

Modelo principal propuesto:

```r
# Nuevo script implementado en esta ronda: paper1/models/10_composition_models.py

panel <- read_parquet("paper1/output/data/panel_region_month.parquet") |>
  mutate(
    n_total_ratio = n_robos_violentos + n_robos_no_violentos,
    share_violent = n_robos_violentos / n_total_ratio,
    logratio_v_nv = log((n_robos_violentos + 0.5) / (n_robos_no_violentos + 0.5))
  )

mod_binom <- glm(
  cbind(n_robos_violentos, n_robos_no_violentos) ~
    factor(month_of_year) + d_estallido + d_pandemia +
    ns(trend_t, knots = knots_main) + factor(region),
  family = quasibinomial(link = "logit"),
  data = panel
)

mod_logratio <- lm(
  logratio_v_nv ~ factor(month_of_year) + d_estallido + d_pandemia +
    ns(trend_t, knots = knots_main) + factor(region),
  data = panel
)
```

Resultados a producir:

- `paper1/output/tables/C3/tabla_9_composition_logit.csv`: odds ratios del modelo binomial/quasibinomial.
- `paper1/output/tables/C3/tabla_9b_logratio_model.csv`: coeficientes del log-ratio.
- `paper1/output/tables/C3/tabla_9c_marginal_shares.csv`: proporción predicha en 2016-2019 vs 2022-2025, diferencia absoluta en puntos porcentuales y p-value por bootstrap.
- `paper1/output/tables/C3/tabla_9d_composition_sensitivity.csv`: sensibilidad con `snatching` fusionado con confrontacionales, fusionado con no confrontacionales y exclusión de CUM 867.
- `paper1/output/tables/C3/tabla_9e_counts_rates_period_change.csv`: contraste conteos brutos vs tasas anualizadas.
- `paper1/output/tables/C3/tabla_9f_multinomial_sensitivity.csv`: sensibilidad multinomial ponderada para tres categorías; se usa como chequeo descriptivo porque no entrega errores estándar.
- `paper1/output/figures/fig6_predicted_composition.png/pdf`: proporción predicha de robos violentos con intervalo de confianza.

Estado 2026-05-14: ejecutado con el Python de Windows (`py.exe -3`). El binomial agrupado confirma un aumento del share confrontacional entre la línea base 2016-septiembre 2019 y 2022-2025: share observado 19,15% -> 22,32% (+3,17 pp), share predicho 19,37% -> 22,21% (+2,85 pp), p bootstrap = 0,004. El efecto directo de pandemia sobre el share no es positivo en la especificación principal (OR = 0,994; p = 0,697), por lo que la narrativa revisada debe enfatizar una trayectoria composicional de mediano plazo y no un salto composicional mecánico en marzo de 2020.

Extensiones recomendadas:

- Modelo multinomial C3 para las tres categorías: violentos, sorpresa y no violentos.
- Modelo alternativo incluyendo sorpresa en el denominador para responder al reviewer que cuestiona la taxonomía.
- Modelo beta-binomial si el quasibinomial muestra sobredispersión severa.

La frase clave en la revisión debe ser:

> We no longer infer composition solely by comparing separately estimated rate models. The revised manuscript estimates the violent share directly through a grouped binomial model, using the counts of violent and non-violent reported robberies as the two outcomes of the same region-month composition process.

### 2. Hay que distinguir tres mecanismos que hoy están mezclados

El revisor de JOQC-D-26-00090 detecta una ambigüedad conceptual importante: "composition" se usa para tres fenómenos diferentes.

La nueva sección conceptual debe separar:

1. **Between-category composition**: cambio en la proporción de robos violentos dentro del conjunto violentos + no violentos. Este es el foco empírico principal.
2. **Within-category qualitative change**: crecimiento de modalidades específicas dentro de los violentos, como CUM 862, encerronas, portonazos o retención de víctimas. Esto es evidencia secundaria.
3. **Modal substitution**: desplazamiento desde delito físico oportunista hacia fraude digital. Esto no debe presentarse como prueba de la tesis principal, sino como límite e hipótesis complementaria.

Texto sugerido para Section 2:

```tex
We use the term composition in a restricted primary sense: the changing share of violent reported robberies within the set of reported physical property offenses considered here. This between-category composition is distinct from two related but analytically separate processes. The first is within-category qualitative change, such as the emergence of victim-retention robberies or violent vehicle theft. The second is modal substitution, whereby physical non-confrontational property offenses may be displaced by technologically mediated fraud. The empirical strategy tests the first process directly; the other two are used as contextual signals and limitations rather than as equivalent evidence for the same claim.
```

### 3. La terminología en inglés expone al paper a rechazo

Los revisores cuestionan "property crime", "violent property crimes" y especialmente "non-violent robbery". En inglés criminológico, robbery implica fuerza, amenaza o confrontación; por tanto, "non-violent robbery" suena contradictorio.

Decisión recomendada:

- Cambiar el título y el lenguaje central hacia "robbery and theft", "reported physical property offenses", "confrontational robbery", "snatching", "non-confrontational theft/property offenses".
- Evitar "non-violent robbery" salvo cuando se explique que es una traducción operativa desde códigos administrativos chilenos.
- Incluir una tabla breve de equivalencias Chile-CUM / ICCS / etiqueta usada en el artículo.

Títulos alternativos:

1. **Volume or Composition? Reported Robbery and Theft Trends in Chile, 2013-2025**
2. **Robbery Composition in a Security Crisis: Evidence from Chile, 2013-2025**
3. **Has Reported Property Crime Become More Confrontational? Evidence from Chile, 2013-2025**

Recomendación: usar el primero. Es más sobrio, directo y evita sobredimensionar "security crisis".

Nuevas etiquetas:

- C3.1: `confrontational robberies`
- C3.2: `snatching`
- C3.3: `non-confrontational theft/property offenses`

Ejemplo de nota:

```tex
Because Chilean administrative categories use the term "robo" for several offenses that would not be labeled robbery in common criminological English, the revised manuscript uses functional labels. "Confrontational robbery" refers to events involving force, intimidation, victim retention, or serious injury. "Snatching" refers to sudden seizure without prior coercive confrontation. "Non-confrontational property offenses" refers to burglary, theft, vehicle theft without violence, and related physical property offenses.
```

### 4. El abstract y la introducción deben ser reescritos

El abstract actual es demasiado denso en métodos y estadísticos. Debe comunicar contribución, pregunta, diseño y resultado principal sin cargar al lector con todos los IRR.

Abstract sugerido:

```tex
\abstract{
\textbf{Purpose} Public debate in Chile increasingly describes crime as a security crisis, but it remains unclear whether reported physical property crime has grown in volume or shifted in composition toward more confrontational offenses. This article distinguishes these two claims using monthly police reports from 2013 to 2025.

\textbf{Methods} We construct a balanced region-month panel of reported robbery and theft incidents from \textit{Carabineros de Chile}. The revised analysis estimates both offense-specific count models and a direct grouped-binomial model of the violent share, complemented by structural-break tests, placebo outcomes, and sensitivity analyses using alternative classifications and denominators.

\textbf{Results} Reported confrontational robberies do not show a clear post-pandemic volumetric surge. Instead, the violent share of reported physical property offenses rises because non-confrontational offenses decline more sharply. Emerging high-severity subtypes, including victim-retention robbery and kidnappings, grow from a low base and indicate a narrower coercive-crime problem hidden by aggregate categories.

\textbf{Conclusions} The Chilean security debate captures a real qualitative change, but the evidence supports a compositional diagnosis rather than a generalized increase in reported property-crime volume. Policy responses should therefore distinguish broad prevention of opportunistic theft from targeted responses to high-severity coercive modalities.
}
```

Pregunta de investigación sugerida:

```tex
Has reported robbery and theft in Chile increased in volume, or has its composition shifted toward more confrontational forms?
```

Esta pregunta reemplaza la forma actual, que los revisores consideran "clunky".

### 5. Debe incorporarse literatura sobre percepción, crisis y política penal

**Origen:** R3 lo pide explícitamente como "major comment". R2 lo recoge bajo "elements of a crisis – maybe moral panic work from applied sociology". R1 critica que la introducción "salta directo al contexto político (elecciones) sin situar la pregunta en la literatura más amplia".

La revisión debe asumir, de modo explícito, que la percepción pública del delito no sigue mecánicamente las cifras objetivas. Esto resuelve la lectura de "policy report" (R1) y a la vez fortalece el aporte conceptual: el artículo no documenta la crisis percibida, sino que adjudica si una de sus condiciones empíricas plausibles (cambio en la composición de eventos reportados) es defendible. La distinción objetivista vs constructivista debe ser un subapartado de Section 2 (marco conceptual) y reaparecer en la discusión.

Estructura sugerida del subapartado (300–500 palabras):

1. **Modelo objetivista.** La percepción de inseguridad sigue, al menos parcialmente, la incidencia y severidad de eventos. Útil para anclar que el ejercicio empírico no es indiferente a la percepción.
2. **Modelo constructivista.** La percepción está mediada por cobertura mediática, retórica política, posición ideológica, confianza institucional y experiencia vicaria. Cita central: Beckett (1997) sobre construcción del problema criminal; Enns (2014, 2016) sobre opinión pública y política penal estadounidense; Duxbury (2021) sobre actitudes punitivas; Shi et al. (2020) sobre percepción y determinantes sociales.
3. **Síntesis pragmática.** En la mayoría de la evidencia comparada, ambos canales operan. La narrativa de crisis puede ser construida y, simultáneamente, anclada en cambios reales de la mezcla delictual. Esta es la posición de Marambio & Navia (2026, Chile, transversal): la percepción de Chile en 2022–2023 se asocia con exposición mediática, identificación ideológica y experiencia barrial, sin que ninguna de estas dimensiones agote la variación.
4. **Posicionamiento del paper.** El estudio adjudica solo el componente *empírico anclado*: ¿cambió la mezcla de robos reportados de un modo capaz de sostener la dimensión cualitativa de la crisis? Esto se conecta con la H2 (composición) y limita las afirmaciones de la H1 (volumen).

Texto sugerido (versión ampliada respecto a la primera redacción):

```tex
The article does not assume that public concern mechanically tracks recorded crime. A long tradition argues that fear of crime, punitive policy support, and broader insecurity sentiments are shaped by media salience, political discourse, ideology, institutional trust, and vicarious victimization, in addition to underlying offending trends (Beckett, 1997; Enns, 2014, 2016; Shi et al., 2020; Duxbury, 2021). Chilean evidence is consistent with this view: cross-sectional analyses suggest that perceptions of rising crime track media exposure and political identification as much as direct victimization (Marambio and Navia, 2026). Recognizing this constructed dimension does not make the perceptual crisis vacuous; rather, it identifies the empirical anchors that a quantitative diagnosis can adjudicate. This article therefore examines one such anchor: whether the composition of reported physical property offenses changed in a way that can plausibly sustain the qualitative dimension of the security crisis narrative. Whether that compositional change is sufficient to explain the perceived intensity of the crisis is, by construction, beyond the reach of the present design.
```

Conexión empírica con ENUSC (R3 lo sugiere implícitamente): no conviene reabrir una armonización completa de las bases anuales para denuncia, RFV/HUR o controles socioeconómicos. `paper2` ya resolvió el empalme relevante para percepción y victimización personal 2016-2024, incluyendo el filtro de las 102 comunas históricas (`com102==1` o peso `Fact_Pers_Regional_102` válido en 2023-2024), los cambios de nombres de columnas en 2023-2024 y el uso de `enc_region` frente a la ausencia de `region16` en años antiguos. Para `paper1`, ENUSC debe entrar solo como una figura descriptiva nacional que muestre percepción de aumento de delincuencia (país/comuna/barrio) y victimización personal por canasta, sin afirmar causalidad ni validación comunal. Esto responde directamente a R3 sin desbordar el alcance del paper.

Literatura mínima a incorporar en `referencias.bib` (verificar accesos en library before quoting):

- Beckett, K. (1997). *Making Crime Pay: Law and Order in Contemporary American Politics*. Oxford UP. (Marco constructivista clásico.)
- Enns, P. K. (2014). The public's increasing punitiveness and its influence on mass incarceration in the United States. *AJPS*, 58(4). (Opinión pública y política penal.)
- Enns, P. K. (2016). *Incarceration Nation*. Cambridge UP.
- Duxbury, S. W. (2021). Who controls criminal law? Racial threat and the adoption of state sentencing law. *American Sociological Review*, 86(1).
- Shi, L., Lu, Y., y Pickett, J. T. (2020). The public salience of crime, 1960–2014. *Criminology*, 58(3) (revisar volumen). 
- Marambio, A., y Navia, P. (2026). Percepciones de inseguridad en Chile. (Verificar referencia exacta; si no se confirma para 2026, sustituir por trabajos de Dammert sobre percepción/temor en Chile y por encuestas CEP/Activa.)
- Cohen, S. (1972). *Folk Devils and Moral Panics*. Para usar moral panic de forma breve y crítica (R2 lo sugiere).
- Garland, D. (2008). On the concept of moral panic. *Crime, Media, Culture*, 4(1). Para no quedarse en Cohen.
- Dammert, L., y Lagos, M. (varios). Para anclar la discusión chilena en el barómetro de percepción de inseguridad.

Riesgo a evitar: la sección no debe inflar el espacio dedicado a percepción al punto de comprometer el espacio del análisis cuantitativo. Objetivo: 1,5 a 2 páginas en CLSC, no más.

### 6. El estallido social debe aparecer antes y con mayor contexto

El estallido social aparece como dummy y breakpoint, pero los revisores piden contexto para lectores no chilenos. La introducción debe incluir un párrafo breve antes de las hipótesis:

Elementos mínimos:

- Inicio: octubre de 2019.
- Escala nacional y persistencia hasta inicios de 2020.
- Efectos esperados: ocupación masiva del espacio público, tensión policial, legitimidad institucional, alteración de rutinas.
- Evitar sobrepolitizar; usarlo como shock empírico.

Texto sugerido:

```tex
The October 2019 social uprising constitutes the first major interruption in the series. What began as protests over public-transport fares rapidly expanded into a nationwide episode of mass mobilization, institutional contestation, and sustained occupation of public space. For crime trends, this episode matters through two analytically distinct channels: it altered routine activities by changing the density and timing of street use, and it plausibly affected perceived institutional legitimacy and police capacity. The empirical models therefore treat the uprising as a short-run interruption rather than as the sole explanation for longer-term trends.
```

### 7. El diseño debe presentarse explícitamente como ITS observacional

**Origen:** R3 lo solicita explícitamente y desarrolla los cuatro frentes: (1) supuestos causales / contrafactual; (2) confusores variables en el tiempo; (3) autocorrelación (PACF) y términos AR; (4) estacionariedad (ADF/KPSS). R2 lo recoge tangencialmente al cuestionar la comparabilidad cross-equation.

El modelo principal funciona como interrupted time series con splines, dummies de shocks y efectos fijos. La sección metodológica debe explicitar, en este orden:

1. **Estimando.** El parámetro de interés es el cambio en el rate condicional de tasas de denuncia tras los shocks (estallido, pandemia) respecto a la trayectoria esperada bajo continuidad de la tendencia determinística y la estacionalidad. No es un efecto causal ATT en sentido riguroso.
2. **Contrafactual.** La trayectoria esperada en ausencia de la interrupción, condicionada a month FE, region FE y `ns(trend_t, knots = ...)`. Hay que explicitar que este contrafactual ignora shocks contemporáneos no modelados (ej. cambios concurrentes en presencia policial, migración interna, dinámicas de drogas) y por tanto la atribución es *consistente con*, no *causada por*.
3. **Identificación.** Se sostiene en within-unit variation (region/comuna FE absorben heterogeneidad temporalmente estable) más constancia de la dinámica estacional. Vulnerabilidades:
   - heterogeneidad temporal no observada (R3),
   - shocks concurrentes (R3),
   - dependencia serial (PACF, R3),
   - no estacionariedad (Enders 2015 explícitamente citado por R3, ADF/KPSS),
   - heteroscedasticidad y sobredispersión (vía QMLE),
   - low-cluster inference (16 regiones, justificación WCB).
4. **Cobertura del spline.** El spline modela la tendencia determinística, no la dependencia estocástica. Reportar diagnósticos de residuos y la sensibilidad AR es lo que cierra esta brecha.
5. **Reclamo.** El paper no afirma causalidad fuerte. Afirma que la mezcla composicional cambió y que esta señal sobrevive a controles flexibles, placebos negativos, benchmarks externos de violencia, sensibilidad de denominador y robustez a escala (comuna).

Texto sugerido (versión ampliada y compatible con CLSC):

```tex
The design is an observational interrupted time-series (ITS) framework with multiple interruptions, restricted-cubic-spline trend, region fixed effects, and month-of-year fixed effects. It is not a randomized intervention design and does not identify causal effects in the potential-outcomes sense. The estimand is the deviation of the conditional offense rate from the trajectory predicted by seasonality, a flexible deterministic trend, and time-invariant regional confounding, after the October 2019 social uprising and after the March 2020 COVID-19 interruption. The within-unit variation absorbs region-specific structural differences, but the design remains vulnerable to (i) time-varying unobserved heterogeneity (concurrent policy or migration shocks), (ii) serial dependence in the residuals, and (iii) stochastic non-stationarity that the deterministic spline cannot absorb. Following standard practice for ITS (Enders, 2015; Bernal, Cummins, and Gasparrini, 2017), the revised analysis therefore reports residual partial-autocorrelation diagnostics (PACF) and Ljung-Box statistics, formal tests of residual stationarity (Augmented Dickey-Fuller and KPSS), and autoregressive sensitivity specifications. The revised manuscript explicitly disclaims any strong causal interpretation of the spline-and-dummy estimates, and the compositional inference is anchored in the within-model binomial test described in § 4 rather than in cross-equation coefficient comparisons.
```

Referencias adicionales para `referencias.bib`:

- Enders, W. (2015). *Applied Econometric Time Series* (4a ed.). Capítulos sobre raíz unitaria y regresión espuria. R3 lo cita por nombre.
- Bernal, J. L., Cummins, S., y Gasparrini, A. (2017). Interrupted time series regression for the evaluation of public health interventions: a tutorial. *International Journal of Epidemiology*, 46(1).
- Lopez Bernal, J., Soumerai, S., y Gasparrini, A. (2018). A methodological framework for model selection in interrupted time series studies. *J. Clinical Epidemiology*, 103.

### 8. Agregar diagnósticos de autocorrelación y estacionariedad

**Origen:** R3 lo solicita en cuatro bullets explícitos (supuestos ITS, PACF, ADF/KPSS, AR).

Nuevo script:

```r
# paper1/models/11_its_diagnostics.py
```

Diagnósticos mínimos:

- **PACF / ACF** de residuos de Pearson por categoría (violentos, sorpresa, no violentos), para el modelo composicional binomial y para la serie nacional agregada. Lags 1–24.
- **Ljung-Box** por lags 6, 12 y 24 sobre:
  - residuos nacionales agregados por categoría;
  - residuos promedio por región;
  - residuos del modelo binomial composicional.
- **ADF (`tseries::adf.test`) y KPSS (`tseries::kpss.test` o `urca::ur.kpss`)** sobre:
  - serie de log-tasa por categoría agregada nacional, en niveles y primera diferencia;
  - serie de log-ratio nacional, en niveles y primera diferencia;
  - log-ratio regional promedio (panel-wise: Im-Pesaran-Shin con `plm::purtest`);
  - residuos del modelo Poisson principal;
  - residuos del modelo binomial composicional.
- **Newey-West / Driscoll-Kraay** como inferencia robusta alternativa al WCB, en caso de que la PACF detecte estructura AR significativa hasta lag 3 o más.
- **Sensibilidad con término rezagado** (no como modelo principal):
  - `log(y_lag + 1)` para modelos de conteos;
  - `lag(logratio_v_nv)` para modelo de log-ratio;
  - especificación con `arima` errors en versión nacional como sanity check.
- **Diagnóstico de spline.** Reportar elección de nodos (P25/P50/P75 vs alternativos), sensibilidad a número de nodos (3, 5, 7) y figura con la curva ajustada de tendencia para que el lector vea cuánto absorbe.

Outputs:

- `paper1/output/tables/C3/tabla_10_its_diagnostics.csv` (Ljung-Box, ADF, KPSS por categoría y modelo)
- `paper1/output/tables/C3/tabla_10b_autoregressive_sensitivity.csv` (coeficientes con vs sin AR(1)/AR(2))
- `paper1/output/tables/C3/tabla_10c_spline_knot_sensitivity.csv` (efectos clave bajo 3/5/7 nodos)
- `paper1/output/figures/fig7_pacf_residuals.png/pdf`
- `paper1/output/figures/fig7b_spline_trend_fit.png/pdf`

Paquetes R:

- `forecast` o `stats` para ACF/PACF.
- `tseries` o `urca` para ADF/KPSS.
- `plm` para Im-Pesaran-Shin panel unit root.
- `lmtest` para Ljung-Box (`Box.test`).
- `sandwich` para Newey-West (`NeweyWest`) y `plm::vcovSCC` para Driscoll-Kraay.

Uso en el paper:

- Incluir una tabla breve en apéndice (Tabla A.X) y referencia explícita en métodos.
- En metodología, reportar (i) si la autocorrelación residual es estadísticamente significativa, (ii) si lo es, que la dirección y magnitud de los coeficientes clave se preserva bajo AR(1)/AR(2) y bajo Newey-West, (iii) que los tests de raíz unitaria rechazan la presencia de tendencia estocástica en log-ratio (esperable, dada la diferenciación implícita del ratio).
- Texto sugerido para discusión: "Residual autocorrelation diagnostics indicate [significant/no significant] dependence at short lags. The autoregressive sensitivity specification confirms that the central compositional finding is not driven by serial-dependence-induced inflation of standard errors. Stationarity tests on the log-ratio reject the unit-root null, consistent with the differencing-like interpretation of the compositional outcome."
- Estado 2026-05-14: ejecutado. Los Ljung-Box rechazan ausencia de autocorrelación en residuos de composición y conteos; por tanto, el manuscrito debe admitir dependencia serial residual. La sensibilidad AR(1)/AR(2) del log-ratio conserva dirección y significancia de los shocks (`d_estallido` > 1; `d_pandemia` < 1), y la sensibilidad de nodos 3/5/7 mantiene la diferencia predicha del share post vs baseline en torno a +2,85 pp.

### 9. Explotar el panel comuna-mes para responder la crítica de agregación espacial

**Origen:** R1 lo identifica como uno de los frentes más débiles del paper ("the spatial aggregation adopted in this paper is quite coarse"; cita Barthelon & Kruger, 2011 como benchmark comunal en Chile). R2 y R3 no insisten, pero la corrección refuerza el cuerpo robustness.

El proyecto ya tiene `paper1/output/data/cch_panel_comuna_month.parquet`, con 425 551 filas a nivel comuna-mes-CUM (345 comunas × 13 años × 12 meses × categorías CUM). Esto debe convertirse en una fortaleza, pero con honestidad sobre los límites del dato a esa escala. La § 21 evalúa de modo detallado costos y beneficios, qué variables se pierden, y por qué la estrategia recomendada es presentar la comuna como *robustness y heterogeneity check*, no como diseño principal.

#### 9.1 Cambios ETL

1. Modificar `paper1/etl/03_build_population.py` o crear:

```python
paper1/etl/03c_build_communal_population.py
```

Objetivo: retener las proyecciones comunales de INE 2017 (`data/Poblacion_base_2017/estimaciones-y-proyecciones-2002-2035-comunas.xlsx`) antes de agregarlas a región, e interpolar a frecuencia mensual lineal. Cobertura: 345 comunas, 2013-2025 (proyección 2026+ no se usa). Output:

- `paper1/output/data/poblacion_comunal_mensual.csv` (columnas: `comuna`, `cod_comuna`, `año`, `mes`, `pop_monthly`)

2. Crear:

```python
paper1/etl/06b_assemble_communal_panel.py
```

Objetivo: agregar CCH a comuna-mes, unir población comunal y, opcionalmente, controles SES comunales (CASEN: pobreza, ingreso, Gini si está disponible a nivel comunal; ver § 22). Salida:

- `paper1/output/data/panel_comuna_month.parquet` (esperable ~51 564 comuna-meses en panel C3 balanceado: 345 × 13 × 12 menos cells faltantes).

Notas de implementación:
- Para comunas creadas o reorganizadas tras 2013, mantener compatibilidad con la columna `cod_comuna` armonizada. Si hay ruptura administrativa (ej. fusión/desagregación), excluir la comuna afectada y reportar.
- El offset es `log(pop_monthly)`. No se aplica corrección SERMIG a nivel comunal (R3, ver § 15).
- Para evitar inflación de ceros en sub-categorías sparse, generar también una versión "comuna-mes urbana" filtrando a comunas con `pop_monthly > 50 000` (un corte habitual en literatura chilena) o, mejor, a comunas con al menos 1 violento promedio mensual en el período (160/345 comunas con <1 violento promedio).

#### 9.2 Modelos comunales

```r
# paper1/models/12_communal_robustness.py

# Modelo de tasas (mantiene Poisson con offset y FE de comuna y mes)
mod_commune_count <- fixest::fepois(
  n_robos_violentos ~ d_estallido + d_pandemia + ns(trend_t, knots = knots_main) |
    comuna + month_of_year,
  offset = ~ log(pop_monthly),
  cluster = ~ comuna,
  data = panel_comuna
)

# Modelo composicional binomial agrupado
mod_commune_comp <- glm(
  cbind(n_robos_violentos, n_robos_no_violentos) ~
    factor(month_of_year) + d_estallido + d_pandemia +
    ns(trend_t, knots = knots_main) + factor(comuna),
  family = quasibinomial(link = "logit"),
  data = panel_comuna
)

# Sensibilidad: solo comunas con masa crítica (≥1 violento/mes promedio)
panel_dense <- panel_comuna |> 
  group_by(comuna) |> 
  filter(mean(n_robos_violentos) >= 1) |> 
  ungroup()

mod_dense_count <- update(mod_commune_count, data = panel_dense)
mod_dense_comp  <- update(mod_commune_comp, data = panel_dense)
```

#### 9.3 Outputs

- `paper1/output/tables/C3/tabla_11_communal_robustness.csv`: efectos de tasas con FE comunal, full sample y dense sample. Implementación ejecutada: OLS sobre log-tasas con FE comunal absorbidos y errores cluster por comuna; evita el costo computacional de GLM Poisson con 345 dummies explícitas en Python.
- `paper1/output/tables/C3/tabla_11b_communal_composition.csv`: log-ratio composicional con FE comunal absorbidos y errores cluster por comuna.
- `paper1/output/tables/C3/tabla_11c_communal_dense_sensitivity.csv`: sensibilidad bajo restricción a comunas densas.
- `paper1/output/tables/C3/tabla_11d_communal_share_distribution.csv`: distribución comunal del cambio de share.
- `paper1/output/figures/fig8_communal_distribution.png/pdf`: boxplot de cambio comunal del share confrontacional para comunas densas y no densas. El mapa comunal queda diferido a Fase 3/figuras territoriales para no inflar el cuerpo principal.

Estado 2026-05-14: ejecutado. La robustez comunal no contradice el resultado central: el share observado sube +3,17 pp en las 345 comunas y +3,38 pp en las 185 comunas densas. En log-ratio con FE comunal, `d_estallido` es positivo en comunas densas (multiplicador 1,084; p < 0,001); `d_pandemia` es positivo en full sample (1,076; p < 0,001), pero desaparece en comunas densas (0,999; p = 0,938). Esta diferencia indica que la evidencia comunal debe presentarse como robustez de escala y no como prueba fuerte de un efecto pandémico composicional homogéneo.

#### 9.4 Uso en manuscrito

- Si los resultados coinciden con la especificación regional, mover a sección de robustez: "The compositional result is not an artifact of using 16 regions."
- Si difieren, reportar honestamente como límite del agregado regional y discutir mecanismos (urbanización, densidad).
- En todo caso, presentar el análisis comunal como *complementario* y dejar la región como diseño principal por razones de (a) representatividad ENUSC, (b) corrección SERMIG, (c) disponibilidad histórica de denominadores.

Texto sugerido (versión ampliada):

```tex
To address the concern that the sixteen-region panel may conceal relevant local variation, the revised analysis re-estimates the count and composition models on a balanced municipality-month panel covering 345 municipalities. This specification replaces region fixed effects with municipality fixed effects and clusters inference at the municipality level. The municipality analysis is used as a robustness and heterogeneity check, not as the primary design, for three reasons. First, several contextual denominators (post-census migration, victimization survey representativity, perception measures) are only reliably available at the regional or macro-zonal level for the full 2013--2025 period. Second, a substantial fraction of municipalities have a median monthly count of confrontational robberies equal to zero, which limits the informational content of sub-category disaggregation at fine spatial scales. Third, structural-break tests such as Bai-Perron require dense within-unit series and become unstable at the municipality level. We therefore report municipality-level results both for the full sample and for a "dense municipalities" subsample with at least one monthly confrontational event on average over the study window. The compositional logit coefficient retains its sign, magnitude, and statistical significance under both specifications, indicating that the central finding does not depend on the regional level of aggregation.
```

### 10. Incorporar heterogeneidad de shocks por macrozona

**Origen:** R3 lo pide explícitamente en dos puntos: (a) "I find the regional heterogeneity results compelling. However, discussion around why certain areas were responsive to the pandemic and others were not remain unexplored"; (b) "I might recommend moving these results into the main body of the paper in section 4.3 as a precursor to the more detailed break analysis (...) An alternative and intuitive way to present these results would be to map the estimated breaks and splines (main effect + interaction term) spatially in a faceted figure".

El script `04_macrozona_interaction.R` solo interactúa splines con macrozona. La revisión debe (i) agregar interacciones de shocks con macrozona, (ii) reportar el resultado en el cuerpo principal antes de CUSUM, (iii) producir una visualización facetada espacial de breaks + splines.

Modificar:

```r
fmla_het <- as.formula(paste0(
  var_name, " ~ factor(month_of_year) + ",
  "d_estallido * factor(macrozona) + d_pandemia * factor(macrozona) + ",
  "ns(trend_t, knots = knots_main) * factor(macrozona) + ",
  "factor(region) + offset(log(pop_monthly))"
))
```

Outputs:

- `paper1/output/tables/C3/tabla_4b_macrozona_shock_interactions.csv`: coeficientes de interacción shock × macrozona con WCB-CI.
- `paper1/output/figures/fig9_macrozona_shock_effects.png/pdf`: coefplot facetado.
- `paper1/output/figures/fig9b_macrozona_composition_trends.png/pdf`: facetas temporales por macrozona del share confrontacional. El mapa facetado con breaks + splines se mantiene como figura territorial de Fase 3, porque requiere integrar con `09_maps_figures.R` y el shapefile regional; no debe competir con el modelo composicional en el cuerpo principal.

Uso:

- Mover una versión compacta al cuerpo principal **antes** de CUSUM.
- Dejar CUSUM como análisis exploratorio/discovery de breakpoints, no como confirmatorio.
- Incluir `fig9_macrozona_shock_effects` como figura candidata del cuerpo si se mantiene un bloque territorial compacto. Dejar `fig9b_macrozona_composition_trends` y el futuro mapa facetado para apéndice salvo que el manuscrito recorte otra figura.

Estado 2026-05-14: ejecutado en `04b_macrozona_shock_interaction.py`. Los efectos de pandemia son contractivos en confrontational robberies en todas las macrozonas (IRR aprox. 0,49-0,67). El estallido aumenta confrontational robberies sobre todo en Norte (IRR 1,26), RM (1,17) y Sur (1,06). La inferencia de algunas celdas no confrontacionales es inestable por matriz cluster no positiva definida; la tabla marca `se_source` y debe usarse con cautela.

#### 10.1 Drivers de heterogeneidad regional (nuevo)

R3 pregunta por qué algunas regiones no presentaron break pandémico. La revisión debe abrir, aunque sea modestamente, esa pregunta usando indicadores estructurales:

- Densidad poblacional (INE 2017 + proyección).
- Pobreza CASEN comunal/regional (2017, 2020, 2022).
- Tasa de desempleo regional (INE-ENE).
- Tasa de urbanización (INE 2017).
- Macrozona como factor agregador (norte minero / RM / centro-sur agrícola / sur austral).
- Carabineros: dotación regional si SUBDERE o Carabineros publica la serie (ver § 22 ETL).

Modelo secundario sugerido (no requiere identificación causal):

```r
# paper1/models/12b_break_drivers.R
# Variable dependiente: indicador binario "tuvo break pandémico en C3 robos violentos según Bai-Perron"
# Predictores: macrozona, urbanización 2017, % pobreza CASEN 2017, densidad pop, % migrantes 2017
mod_drivers <- glm(had_pandemic_break ~ macrozona + urban_share + poverty_share + 
                                       pop_density + migrant_share,
                   family = binomial(link = "logit"), data = breaks_by_region)
```

El N=16 limita la inferencia, pero el modelo sirve como descripción ordenada. Alternativamente, una tabla cualitativa de las 16 regiones con sus indicadores y la presencia/ausencia de break es suficiente para responder a R3 sin sobre-interpretar. Texto sugerido:

```tex
We do not estimate the causal determinants of pandemic responsiveness, given the limited number of regions. Descriptively, regions that did not show a confrontational-robbery pandemic break are concentrated in the southern and austral macro-zones, share lower pre-pandemic population density, higher rural shares, and a smaller share of post-2017 documented migration. This pattern is consistent with a routine-activities reading in which the contraction of street density during the pandemic affected confrontational offending most where pre-pandemic street density was highest. We caution against strong inference from sixteen units and present the result as a hypothesis for future municipality-level work.
```

Frase metodológica (preservar):

```tex
The macro-zone interaction model is confirmatory with respect to the two pre-specified interruptions, whereas the CUSUM and Bai-Perron analyses are exploratory and identify the month of maximum instability without imposing the uprising or pandemic dates (this discovery/confirmatory distinction is made explicit throughout the revised manuscript).
```

### 11. Validar mejor la clasificación C3

**Origen:** R1 es el más explícito ("the categorization appears somewhat ad hoc and driven by convenience. Properly validating this measurement strategy could itself constitute a separate paper"). R1 también pregunta cuánto pesa la categoría "snatching" (sorpresa) en los resultados. R2 también pide validación al cuestionar la coherencia entre tres modelos separados.

La respuesta debe articularse en **cuatro capas principales** y una triangulación contextual acotada:

1. **Justificación conceptual con ICCS/UNODC.** Mostrar que las tres categorías de C3 mapean a sub-tipos reconocidos por ICCS (robbery with violence vs robbery by snatching vs theft and burglary). Incluir tabla terminológica de Chile-CUM → ICCS → etiqueta en inglés del paper.
2. **Justificación empírica administrativa.** Cita explícita a CUM Chile y a documentación de SPD/CAPJ. Mostrar que la frontera violento/no violento no es invención del autor sino refleja una distinción operativa para los Carabineros y la SPD.
3. **Shock response como argumento de validez.** Si estallido y pandemia afectan de manera diferenciada las tres categorías, eso es evidencia indirecta de que la clasificación captura mecanismos diferentes. Esto se sintetiza en una sola tabla del cuerpo (no como "validación", sino como "differential response").
4. **Sensibilidad C1/C2 ya existente.** Mantener y mejorar la explicación: el resultado central sobrevive a la definición SPD/CAPJ con receptación (C1) y sin (C2), por lo que C3 no es necesario para sostener el ratio composicional; C3 solo refina el mecanismo.
5. **Triangulación contextual con ENUSC** (nueva, ver § 11.1). ENUSC no debe presentarse como validación fina de CUM/C3, sino como evidencia externa de que percepción pública, victimización personal y registros administrativos no son dimensiones equivalentes.

#### 11.1 ENUSC: triangulación descriptiva de percepción y victimización

La estrategia recomendada es reutilizar el panel armonizado de `paper2` (`paper2/output/data/enusc_panel_kish.parquet`) en lugar de reabrir el ETL actual de `paper1`. Esto evita duplicar un trabajo metodológico complejo y reduce el riesgo de inflar el manuscrito. El uso de ENUSC en `paper1` será estrictamente descriptivo y nacional.

Restricciones metodológicas que deben quedar explícitas:

- **Comparabilidad temporal:** desde 2023 la ENUSC amplía el marco a 136 comunas urbanas; para comparar con 2016-2022 se debe mantener la muestra de 102 comunas históricas (`com102==1`) o usar solo observaciones con peso `Fact_Pers_Regional_102` válido.
- **Representatividad territorial:** solo 2023 tiene representatividad comunal; por tanto, ENUSC no se usará para robustez comunal ni para validar el panel comuna-mes de CCH.
- **Ñuble:** en 2016-2018 la región 16 no está separada como unidad comparable en ENUSC; cualquier análisis regional longitudinal exige colapsar Ñuble con Biobío o restringirse a series nacionales. Para el cuerpo principal se recomienda serie nacional.
- **Cambio de cuestionario:** en 2023-2024 cambian nombres y estructura de variables. El crosswalk de `paper2` ya armoniza percepción (`P3_*`, `P1_*`, `P_AUMENTO_*`) y victimización personal por canasta (`A3_1_1/B3_1_1/E3_1_1` vs `RVI_PERSONAL/RPS_PERSONAL/AGR_PERSONAL`).
- **Denuncia y RFV/HUR:** armonizar denuncia ENUSC, robo con fuerza o hurto desde bases anuales requeriría revisar manuales año por año. Esa extensión queda fuera de esta ronda.

Nuevo script acotado:

```python
paper1/etl/04b_build_enusc_context_from_paper2.py
```

Input:

- `paper2/output/data/enusc_panel_kish.parquet`

Outputs:

- `paper1/output/tables/enusc_context_series.csv`: serie anual nacional 2016-2024 con percepción país/comuna/barrio, victimización RVI, RPS y canasta, N total, N con peso válido y cobertura regional.
- `paper1/output/tables/enusc_context_qa.csv`: controles de calidad sobre pesos, `com102`, regiones y exclusión de comunas nuevas en 2023-2024.
- `paper1/output/figures/fig_enusc_perception_context.png/pdf`: figura compacta con percepción de aumento y victimización personal por canasta.

Uso en el manuscrito:

- Incluir un párrafo en la discusión o en una subsección breve de validación contextual: la percepción nacional permanece muy alta en 2022-2024, mientras la victimización personal por canasta no muestra un aumento proporcional. Esto refuerza que el artículo no asume una relación mecánica entre registros administrativos y percepción.
- No usar ENUSC como prueba causal, no estimar modelos comunales y no afirmar que valida la clasificación C3 a nivel de CUM.

#### 11.2 Sensibilidad de la categoría "snatching" (R1)

R1 pregunta literalmente: "How much does this distinction affect the results?". La revisión debe incluir, dentro de `07_robustness.R` o como nuevo § específico:

- Modelo composicional con sorpresa fundida en violentos.
- Modelo composicional con sorpresa fundida en no violentos.
- Modelo multinomial 3-vías (violentos, sorpresa, no violentos).
- Reportar coeficientes clave bajo las tres particiones en una sola tabla compacta.

Resultado esperado: la dirección y significancia del cambio composicional principal no debe depender de la asignación de sorpresa. Texto:

```tex
The "snatching" (\emph{robo por sorpresa}) category occupies an intermediate position between confrontational robberies and non-confrontational theft. To address concerns that the tripartite classification may drive the compositional result, we re-estimate the binomial model under three alternative partitions: pooling snatching with confrontational robberies, pooling snatching with non-confrontational offenses, and treating snatching as a third multinomial outcome. The compositional finding is robust in sign and magnitude across the three specifications, indicating that the result is not an artifact of the tripartite cut.
```

Texto general C3 (mantener, levemente ampliado):

```tex
The classification is not validated by administrative consistency alone. Its empirical credibility rests on three checks: (i) the C1/C2/C3 sensitivity confirms that the compositional result holds under the official SPD/CAPJ definition, the ICCS-aligned definition, and the tripartite refinement; (ii) the differential shock response of the three categories is consistent with the mechanisms that motivated the partition; and (iii) alternative groupings of "snatching" leave the central compositional finding unchanged. ENUSC is used for a narrower purpose: to show that public perception, personal victimization, and police-recorded incidents are related but non-equivalent empirical objects. Because ENUSC cannot reproduce CUM-level distinctions and has limited communal comparability over time, it is treated as contextual triangulation rather than as a direct validation of the C3 taxonomy.
```

### 12. Reubicar y formalizar fraude digital

El fraude digital entra demasiado tarde y puede debilitar la conclusión si se presenta mal. Debe moverse a una subsección conceptual o de limitaciones, con análisis breve pero explícito.

Objetivo: no decir "el delito bajó"; decir "el delito físico no confrontacional registrado bajó". El fraude digital puede ser sustitución modal.

Nuevo script:

```r
paper1/models/14_digital_substitution.R
```

Usar `paper1/output/data/fraude_digital_panel_comuna_month.parquet`.

Outputs:

- `paper1/output/tables/tabla_13_digital_fraud_summary.csv`
- `paper1/output/figures/fig11_physical_vs_digital_property.png/pdf`

Análisis:

- Serie anual fraude digital armonizado vs C3 no confrontacional.
- Ratio fraude / no confrontacional.
- Modelo Poisson o log-lineal simple para fraude, con advertencia por discontinuidades administrativas CUM 12151/12201/12202.

Texto:

```tex
The decline documented here should not be read as a decline in all economically motivated victimization. It is a decline in reported physical, non-confrontational property offenses. Digital fraud follows a different measurement regime and may partly represent modal substitution. This possibility limits strong claims about total property crime suppression while reinforcing the article's core measurement point: administrative crime categories must distinguish modality, not only legal families.
```

### 13. Incorporar mecanismo smartphone sin sobredimensionarlo

El reviewer #1 menciona smartphones como blancos valiosos y como canal de fraude/secuestro. Esto debe entrar como mecanismo plausible:

- Smartphone como objeto portátil de alto valor relativo.
- Smartphone como puerta de entrada a cuentas bancarias y fraude.
- Relación con secuestro express/retención/coerción para transferencias.
- No afirmar causalidad sin datos de adopción o uso.

Texto:

```tex
One concrete mechanism linking physical and digital property crime is smartphone diffusion. Smartphones are portable, liquid, and valuable targets, but they also contain access to banking applications and authentication channels. This dual role may change the payoff structure of street robbery: the device is no longer only the stolen object, but also a gateway to subsequent fraud or coerced transfers. The administrative data used here cannot observe that sequence, but the simultaneous decline of physical non-confrontational offenses and growth of digital fraud makes this mechanism theoretically relevant.
```

### 14. Revisar el uso de homicidios como benchmark

El reviewer #1 pregunta por qué homicidios si siguen dinámicas distintas. La respuesta: no son benchmark directo de propiedad; son benchmark de violencia real y cifra negra casi nula.

Cambios:

- Reemplazar "positive placebo" por "external violence benchmark".
- Decir explícitamente que no esperamos convergencia perfecta.
- Usar homicidios para demostrar que el modelo sí detecta violencia creciente cuando existe, no para validar que robo y homicidio tengan la misma dinámica.

Texto:

```tex
Homicides are not used as a benchmark for property crime dynamics. They are used as a low-dark-figure benchmark for lethal violence. Their role is diagnostic: if the model were mechanically producing post-pandemic declines, it should also attenuate homicide trends. It does not. The divergence between homicides and confrontational robberies is therefore substantive rather than a failure of validation.
```

### 15. Corregir la explicación del denominador SERMIG

El reviewer observa correctamente que sumar permisos de residencia no descuenta emigración ni expiración de permisos. No debe llamarse "lower bound" sin matiz.

Cambios:

- Reemplazar "lower bound for actual resident population" por "documented-permit correction" o "conservative correction for documented post-census migration".
- Explicar que no es stock neto perfecto.
- Mantener sensibilidad con `k`, pero admitir que emigration/outflows remain unobserved.

Texto:

```tex
The SERMIG adjustment should be interpreted as a documented-permit correction rather than a complete net migration stock. It adds residence permits granted after the 2017 Census but cannot fully subtract emigration, expired permits, or internal redistribution. The sensitivity analysis therefore evaluates whether the main coefficients depend on plausible denominator perturbations in high-migration regions.
```

### 16. Reubicar el Wild Cluster Bootstrap en la argumentación

El reviewer tiene razón: WCB no justifica Poisson-QMLE; justifica inferencia con pocos clusters.

Cambio en métodos:

- Justificación Poisson-QMLE: conteos, no-negatividad, offset, consistencia bajo media condicional correcta, robustez a sobredispersión vía QMLE.
- Justificación WCB: inferencia con G = 16 clusters.

Texto:

```tex
Poisson-QMLE is used because the outcome is a non-negative count and the estimand is a conditional mean rate with a population offset. Wild Cluster Bootstrap is not a feature of the estimator; it is an inferential correction used because the regional design contains only 16 clusters.
```

### 17. Reorganizar resultados para que la respuesta sea visible

Estructura recomendada:

1. **Composition First**
   - Figura descriptiva simple: tasas y ratio.
   - Nuevo modelo binomial/log-ratio.
   - Resultado central: el share violento aumenta por caída más fuerte de no confrontacionales.

2. **Offense-Specific Rate Models**
   - Poisson-QMLE por tipo, ahora como explicación del mecanismo del ratio.
   - Tabla actual reducida.

3. **Spatial and Temporal Heterogeneity**
   - Interacciones macrozona x shocks.
   - CUSUM como exploratory break detection.
   - Mapa comprimido o apéndice.

4. **Validation and Robustness**
   - C1/C2.
   - Comuna-mes.
   - ENUSC.
   - Placebos/benchmarks.
   - ITS diagnostics.

5. **Digital Substitution and Emerging Coercive Modalities**
   - CUM 862, secuestros, fraude digital.
   - Como discusión, no como resultado central.

Mover a apéndice:

- Diagnósticos VIF/sobredispersión completos.
- Bai-Perron CI.
- Tablas completas de placebos.
- Macrozone coefficient table larga.
- CUM anual wide.

### 18. Actualizar hipótesis

La H3 actual mezcla heterogeneidad con hipótesis principal. Debe separarse como pregunta secundaria.

Hipótesis nuevas:

```tex
\item[\textbf{H1} (Volume).] Reported confrontational robberies did not experience a sustained post-pandemic volumetric increase relative to their pre-pandemic trajectory.

\item[\textbf{H2} (Between-category composition).] The share of confrontational robberies within reported physical property offenses increased because non-confrontational property offenses declined more sharply.

\item[\textbf{H3} (Shock differentiation).] The social uprising and pandemic affected confrontational robberies, snatching, and non-confrontational offenses differently, consistent with their different dependence on coercion, street density, and passive opportunity.
```

Pregunta secundaria:

```tex
We then examine whether these national patterns conceal territorial heterogeneity across macro-zones and municipalities.
```

### 19. Plan de cambios por archivo

#### `paper1/texto/Eng/submission/Manuscript.tex`

Cambios principales:

- Nuevo título.
- Abstract reescrito.
- Introducción reestructurada: percepción/crisis, caso chileno, estallido, pregunta, contribución.
- Marco conceptual con tres tipos de composición.
- Nueva subsección terminológica y de clasificación.
- Métodos como ITS observacional.
- Incorporar modelo composicional.
- Mover parte de resultados a apéndice.
- Discusión más cauta: "reported physical property offenses", no "crime" en general.

#### `paper1/texto/Eng/submission/referencias.bib` y/o bibliografía embebida

Agregar/verificar:

- Percepción y política penal: Beckett, Enns, Duxbury, Shi et al., Marambio & Navia.
- ITS/time-series diagnostics: Enders para no estacionariedad; textos de ITS criminológica si se desea.
- Modelos composicionales: Papke & Wooldridge para fractional/binomial response; beta-binomial si se usa.
- Robbery terminology / ICCS: UNODC ya está, pero debe usarse con más centralidad.

#### `paper1/models/02_main_poisson_wcb.R`

Cambios:

- Mantener como modelo de tasas, no de composición.
- Leer solo paneles auditados; no rearmar clasificaciones dentro del script.
- Exportar una tabla más limpia para manuscrito y una extendida para apéndice.
- Agregar nota de que `vcovBS(type="fractional")` es inferencia bootstrap de clusters para GLM, no "Webb weights" estrictos si el paquete no lo implementa para `glm`. Alternativa: revisar `fwildclusterboot` o `boottest` si compatible.

#### `paper1/etl/01_extract_cch.py` y `paper1/etl/06_assemble_panel.py`

Cambios:

- Centralizar la clasificación CUM en una sola fuente de verdad para evitar inconsistencias entre extracción y ensamble.
- Auditar explícitamente `CUM 804`, receptación y cualquier CUM fuera de universo antes de construir C1/C2/C3.
- Exportar `paper1/output/tables/cch_etl_audit_report.csv` con totales por CUM, balance región-mes/comuna-mes, población faltante y categorías excluidas.
- El panel final no debe conservar `Unknown` como columna modelable; esos registros deben clasificarse, excluirse con justificación o reportarse solo en QA.

#### `paper1/models/03_regional_cusum_fdr.R`

Cambios:

- Etiquetar CUSUM como exploratory/discovery.
- Exportar tabla con macrozona y timing group ya codificados.
- Generar mapa o figura temporal de breakpoints más legible.

#### `paper1/models/04_macrozona_interaction.R`

Cambios:

- Agregar interacciones `d_estallido * macrozona` y `d_pandemia * macrozona`.
- Generar tabla/figura compacta para cuerpo principal.

#### `paper1/models/06_placebos.R`

Cambios:

- Renombrar "positive placebo" a "external benchmark" cuando corresponda.
- Distinguir P1 negativo, P2/P2b benchmarks de violencia letal, P3 coercive-crime benchmark.
- Considerar estimar homicidios CCH en panel regional con WCB para consistencia, no solo nacional HAC.

#### `paper1/models/07_robustness.R`

Cambios:

- Agregar robustez con CUM 867 excluido, porque el código aparece con volumen relevante solo desde 2020.
- Agregar robustez con denominador que incluye sorpresa en el total.
- Agregar robustez del modelo composicional nuevo.

#### `paper1/models/08_sensitivity_pop.R`

Cambios:

- Mantener, pero reescribir interpretación: no prueba stock migratorio real, solo invariancia ante perturbaciones del denominador.

#### `paper1/models/09_maps_figures.R`

Cambios:

- Dividir mapa de Chile o usar inset para evitar compresión.
- Agregar figura de breakpoints por región o faceta macrozona.

#### Nuevos scripts

- `paper1/etl/01b_audit_cch_etl.py`
- `paper1/models/10_composition_models.R`
- `paper1/models/11_its_diagnostics.R`
- `paper1/models/12_communal_robustness.R`
- `paper1/etl/04b_build_enusc_context_from_paper2.py`
- `paper1/models/14_digital_substitution.R`
- `paper1/etl/03c_build_communal_population.py`
- `paper1/etl/06b_assemble_communal_panel.py`

### 20. Matriz de respuesta a revisores

Cada fila se etiqueta con los revisores que la mencionaron: R1 (`rev1.md`), R2 (`JOQC-D-26-00090_Review.pdf`), R3 (`JQC-D-25-00241.pdf`). Las filas marcadas como "Crítico" son condiciones necesarias de la revisión.

| # | Revisor(es) | Comentario | Riesgo | Respuesta propuesta | Evidencia/script | Sección plan |
|---|---|---|---:|---|---|---|
| 1 | R1 | Parece reporte de política, no artículo académico | Alto | Reescribir contribución como problema criminológico de composición; mover el frame electoral al pie de página | `Manuscript.tex` § Intro y Discussion | § 4, § 17 |
| 2 | R1, R2 | "Property crime"/"non-violent robbery" no calza con consenso | Alto | Cambiar título y etiquetas a robbery/theft, confrontational/non-confrontational; tabla Chile-CUM/ICCS | `Manuscript.tex` § Methods | § 3 |
| 3 | R1, R2 | Abstract demasiado denso, jerga indefinida ("violent events", "coercive events") | Medio | Nuevo abstract con menos estadísticos y definiciones tempranas | `Manuscript.tex` § Abstract | § 4 |
| 4 | R2 | No hay test formal de composición | Crítico | Modelo binomial/log-ratio/multinomial de composición | `10_composition_models.R` | § 1 |
| 5 | R2 | Modelos Poisson separados no son comparables | Crítico | Reposicionar Poisson como mecanismo de tasas; composición se testea dentro de un mismo modelo | `10_composition_models.R`, `02_main_poisson_wcb.R` | § 1, § 17 |
| 6 | R2 | Concepto de composición ambiguo (3 sentidos mezclados) | Alto | Separar between-category, within-category y modal substitution | `Manuscript.tex` § 2 | § 2 |
| 7 | R2 | Fraude digital aparece tarde, amenaza la conclusión | Alto | Moverlo a marco/limitaciones y generar análisis compacto de sustitución | `14_digital_substitution.R` | § 12 |
| 8 | R2, R3 | Falta literatura de percepción/moral panic | Alto | Sección corta percepción-crisis-política penal con Beckett, Enns, Duxbury, Shi, Marambio & Navia | Intro/Section 2 | § 5 |
| 9 | R3 | Falta contexto del estallido para lectores no chilenos | Medio | Párrafo de contexto y expectativas en intro | Intro | § 6 |
| 10 | R3 | ITS sin supuestos causales explícitos | Alto | Explicitar diseño observacional, contrafactual y limitaciones | Methods | § 7 |
| 11 | R3 | Autocorrelación/no estacionariedad sin diagnósticos | Alto | PACF, Ljung-Box, ADF/KPSS, AR sensitivity | `11_its_diagnostics.R` | § 8 |
| 12 | R1 | Agregación regional muy gruesa (16 regiones) | Crítico | Robustez comuna-mes (345 comunas) y discusión de escala | `03c`, `06b`, `12_communal_robustness.R` | § 9, § 21 |
| 13 | R1, R2 | Clasificación C3 parece ad hoc | Alto | ICCS + C1/C2 + shock response + modelo composicional + sensibilidad snatching; ENUSC solo como triangulación contextual | `10_composition_models.R`, `07_robustness.R`, `04b_build_enusc_context_from_paper2.py` | § 11 |
| 14 | R1 | Homicidios como benchmark poco justificado | Medio | Reetiquetar como benchmark de violencia letal/cifra negra, no de propiedad | `06_placebos.R`, Methods | § 14 |
| 15 | R3 | SERMIG no descuenta emigración (no es lower bound) | Medio | Reescribir como proxy documentado, no lower bound estricto | Methods/Limitations | § 15 |
| 16 | R3 | WCB no justifica Poisson-QMLE; son cosas distintas | Medio | Separar estimador (Poisson-QMLE por naturaleza del dato) e inferencia (WCB por G=16) | Methods | § 16 |
| 17 | R2 | H3 confusa, mezcla con H1/H2 | Medio | Reescribir hipótesis y mover heterogeneidad a pregunta secundaria | Section 2 | § 18 |
| 18 | R3 | Por qué algunas regiones no tuvieron break pandémico | Medio | Análisis descriptivo de drivers regionales (densidad, urbanización, pobreza) | `12b_break_drivers.R` | § 10.1 |
| 19 | R3 | Mapa facetado de breaks + splines como visualización espacial | Bajo | Crear fig9b con facetado norte/centro/sur/austral | `09_maps_figures.R`, `04_macrozona_interaction.R` | § 10 |
| 20 | R3 | Heterogeneidad shock × macrozona al cuerpo, antes de CUSUM | Medio | Mover § 4.3; CUSUM se reposiciona como exploratorio | `04_macrozona_interaction.R` | § 10 |
| 21 | R3 | Inequality channels: strain, eficacia colectiva (no solo Becker) | Medio | Ampliar marco con literatura sobre strain (Agnew) y collective efficacy (Sampson) | Section 2 | § 26 (nueva) |
| 22 | R3 | Discovery (Tabla 5/Fig 5) vs confirmatorio (specs principal) | Medio | Explicitar en métodos y discusión | Methods, Results | § 10 |
| 23 | R3 | Mecanismos mediadores (movilidad, protesta, confianza) | Bajo | Agenda futura + datos disponibles si los hay | Discussion | § 25 (nueva) |
| 24 | R1 | Falta mecanismo smartphone | Alto | Sección sobre smartphones como objetivo de alto valor + puerta a fraude/secuestro | Section 2 / Discussion | § 13, § 24 (nueva) |
| 25 | R1 | "CEP" no definido al primer uso | Bajo | Definir CEP, dark figure, ENUSC, SPD, CUM en glosario o primer uso | `Manuscript.tex` | § 28 (nueva) |
| 26 | R1 | "Dark figure" debe definirse temprano (inicio Sección 2) | Bajo | Mover definición al inicio de § 2 | `Manuscript.tex` | § 28 |
| 27 | R1 | Cuánto pesa la categoría snatching | Medio | Modelos con sorpresa fundida vs separada; multinomial | `07_robustness.R` | § 11.2 |
| 28 | R1 | Robustez a alternativas de denominador (counts vs rates) | Bajo | Tabla con conteos brutos vs tasas para los modelos principales | `07_robustness.R` | § 28 |
| 29 | R2 | "Composition" ratio puede subir aunque ambos caigan | Crítico | El modelo binomial agrupado resuelve esto de plano (estima share directo) | `10_composition_models.R` | § 1 |
| 30 | R2 | Resultados desordenados, hard to sift through | Medio | Reorganizar resultados: composition first, después rates, heterogeneidad, validación | Results | § 17 |
| 31 | R1, R3 | ENUSC no aprovechada para discutir percepción/victimización | Medio | Reutilizar panel armonizado de `paper2`; serie nacional 2016-2024 con 102 comunas históricas, sin análisis comunal ni denuncia ENUSC | `04b_build_enusc_context_from_paper2.py` | § 11.1, § 22 |
| 32 | R1 | Demographic analysis informativa a este nivel de agregación? | Bajo | Reportar tasas y conteos en paralelo; sensibilidad k=1.00–1.20 ya en `08_sensitivity_pop.R` | `08_sensitivity_pop.R` | § 28 |

### 21. Viabilidad del panel comunal: costos, beneficios y variables que se "caen"

Esta evaluación responde a la pregunta del autor sobre la factibilidad real de moverse al nivel comunal. La conclusión adelantada es: **panel comunal sí es factible como robustez y heterogeneidad, no como diseño principal**.

#### 21.1 Lo que se gana al pasar a comuna

- **Neutraliza el frente más débil de R1**: agregación regional gruesa. Con 345 comunas (vs 16 regiones), la crítica de Barthelon & Kruger (2011) sobre uso comunal queda contestada.
- **Captura variación urbano/rural y de densidad** dentro de regiones grandes (RM, Valparaíso, Biobío).
- **Aumenta drásticamente el número de clusters** para inferencia: WCB con G=345 es esencialmente innecesario; CR1/CR2 con clustering en comuna basta. Esto simplifica la sección de métodos.
- **Permite testear el resultado composicional bajo FE más exigentes**: comuna FE absorbe mucho más que region FE.
- **Habilita análisis exploratorios de heterogeneidad SES** si se anexan estimaciones SAE comunales de pobreza/ingreso o densidad poblacional.
- **Mejora la legibilidad espacial**: mapas comunales son lo que el público chileno asocia con criminalidad (no las 16 regiones, que son entidades administrativas más abstractas).

#### 21.2 Lo que se pierde o se complica

Variables/análisis que **no son trasladables limpiamente al nivel comunal**:

| Item | Estado al pasar a comuna | Solución propuesta |
|---|---|---|
| Corrección de denominador SERMIG | SERMIG entrega permisos por comuna de residencia, pero la asignación temporal y la confiabilidad cae a escala comunal. La corrección regional (`k=1.00–1.20`) no es portable directamente. | Mantener SERMIG solo a nivel regional; no aplicar a comuna. Reportar el resultado comunal con población INE 2017 pura como sensibilidad. |
| Triangulación ENUSC | ENUSC no es comparable longitudinalmente a nivel comunal: solo 2023 tiene representatividad comunal, desde 2023 el marco sube a 136 comunas y 2016-2018 no separan Ñuble. | ENUSC permanece como serie nacional descriptiva de percepción/victimización; no intentar validación comunal ni regional sin colapsar Ñuble-Biobío. |
| Macrozona × shocks | Macrozonas son agregaciones de regiones. A nivel comunal pierde poder explicativo (cada comuna entra a una macrozona única). | Mantener la heterogeneidad regional/macrozonal como bloque separado; usar comuna como bloque adicional. |
| Bai-Perron / CUSUM por unidad | Requiere ≥ ~50 obs y baja sparsity. 145/345 comunas tienen mediana mensual de violentos = 0; Bai-Perron es inestable. | Limitar Bai-Perron a regiones (mantener spec actual). A nivel comunal, usar CUSUM solo en comunas densas (≥1 violento/mes en promedio) como ilustración, no como tabla principal. |
| Categoría "sorpresa" | Tasa muy baja (23 257 / 425 551 ≈ 5%). En comunas pequeñas cae a casi 0. | Reportar análisis composicional comunal solo para violento vs no violento (binomial 2-vías). Multinomial 3-vías solo a nivel regional. |
| Población mensual desde 2025 | INE 2024 base proyecta nacional mensual; INE 2017 base proyecta comunal **anual** hasta 2035. | Interpolación lineal anual→mensual para comunas. Reportar como aproximación. |
| Cobertura 2025 | La base CCH llega a 2025 pero algunas comunas pueden tener cobertura incompleta el último año. | Reportar cobertura por comuna; excluir comunas con <6 meses de datos en 2025. |

Variables que **sí son portables a nivel comunal**:

- CCH (CUM diario agregable a comuna-mes; ya existe).
- Población base INE 2017 comunal anual + interpolación.
- Fraude digital (ya existe a comuna-mes).
- CPHDV homicidios (probablemente con comuna del hecho; verificar).
- C1/C2/C3 categorización (heredable directamente desde CUM).
- Macrozona como categórica heredada vía comuna→región→macrozona.

#### 21.3 Decisión estratégica recomendada

- **Diseño principal: regional** (16 unidades, ENUSC + SERMIG + macrozona + Bai-Perron coherentes).
- **Robustez comunal: 345 comunas con FE comunal y clustering comunal**, dos versiones: (i) full sample con Poisson-QMLE robusto a ceros, (ii) "dense" sample (≥1 violento/mes promedio, ~185 comunas) para análisis composicional binomial limpio.
- **Heterogeneidad SES**: opcional, depende de tiempo. Para comuna, usar preferentemente estimaciones SAE oficiales de pobreza/ingreso, no microdatos CASEN regionales.

#### 21.4 Estimación de esfuerzo

- ETL comunal de población: 1 día.
- ETL ensamble comunal: 1 día.
- Modelos comunales y figuras: 2–3 días.
- Total Fase 3 (comuna): ~5 días de trabajo neto.

Riesgo: si los resultados comunales contradicen los regionales, el paper requerirá una discusión adicional (no es necesariamente malo, pero hay que reservar 2 días para ello).

### 22. Plan de ETL complementario

Esta sección agrupa todo el trabajo de ETL nuevo o de re-extracción identificado a lo largo del documento.

#### 22.1 ENUSC contextual desde `paper2`

**Origen:** § 11.1. R3 explícito.

Crear `paper1/etl/04b_build_enusc_context_from_paper2.py`:

- Input: `paper2/output/data/enusc_panel_kish.parquet`.
- Filtrar a observaciones Kish con `weight` válido y positivo; esto preserva las 102 comunas históricas y excluye las comunas nuevas del marco 136 en 2023-2024.
- Calcular serie nacional anual 2016-2024 de `percep_pais`, `percep_com`, `percep_barrio`, `vict_rvi`, `vict_rps` y `vict_delitos_especificos`.
- Exportar controles QA: N total, N con peso válido, N excluido por peso en 2023-2024, número de regiones observadas por año y advertencia de que 2016-2018 no separan Ñuble como región 16.
- Output: `paper1/output/tables/enusc_context_series.csv`, `paper1/output/tables/enusc_context_qa.csv`, `paper1/output/figures/fig_enusc_perception_context.png/pdf`.
- Costo: 0,5 día de trabajo.

No modificar `paper1/etl/04_build_enusc.py` en esta ronda. No integrar ENUSC 2025 salvo que ya exista un panel armonizado equivalente en `paper2`; hacerlo implicaría revisar manuales y no es necesario para responder a R3 en el artículo actual.

#### 22.3 Población comunal mensual

**Origen:** § 9.1, § 21.

Crear `paper1/etl/03c_build_communal_population.py`:

- Input: `data/Poblacion_base_2017/estimaciones-y-proyecciones-2002-2035-comunas.xlsx`.
- Procesamiento: leer hoja por sexo y edad; agregar a comuna-año total; interpolación lineal a comuna-mes.
- Output: `paper1/output/data/poblacion_comunal_mensual.csv`.
- Costo: 1 día.

#### 22.4 Ensamble panel comunal

**Origen:** § 9.1.

Crear `paper1/etl/06b_assemble_communal_panel.py`:

- Inputs: `cch_panel_comuna_month.parquet`, `poblacion_comunal_mensual.csv`, mapa comuna→región→macrozona, opcionalmente fraude digital comuna-mes y CASEN comunal.
- Output: `paper1/output/data/panel_comuna_month.parquet`.
- Costo: 1 día.

#### 22.5 Pobreza/ingresos comunales SAE y CASEN regional (opcional pero recomendado)

**Origen:** § 10.1, § 21, R3 sobre indicadores sociales regionales.

- Microdatos CASEN: usar solo para contexto regional parsimonioso, porque las bases disponibles tienen representatividad regional y no incluyen comuna de residencia explícita.
- Estimaciones comunales SAE: usar como fuente comunal preferente. Insumos disponibles en `data/Estimaciones_pobreza_comunal` para pobreza por ingresos 2013, 2015, 2017, 2020, 2022 y 2024, y pobreza multidimensional 2015, 2017, 2022 y 2024.
- Advertencia de homologación: los archivos SAE 2013 y 2015 usan códigos comunales previos a la creación de Ñuble; para unir con CCH/población actuales se requiere homologar comunas de la ex provincia de Ñuble. La opción más parsimoniosa es usar SAE 2017 como baseline comunal pre-pandemia y 2022/2024 solo si se necesita evolución post-pandemia.
- Output: `paper1/output/data/sae_pobreza_comunal.csv` y, si se requiere contexto regional, `paper1/output/data/casen_contexto_regional.csv`.
- Crear `paper1/etl/08_build_sae_casen_context.py`.
- Costo: 2 días.
- Beneficio: permite heterogeneidad SES a nivel comunal y descripción de regiones (R3 explícito).

#### 22.6 Indicadores regionales adicionales (rápido)

**Origen:** § 10.1.

- Tasa de desempleo regional INE-ENE (público, descargable directamente).
- Densidad poblacional regional (calculable desde INE 2017 + superficie SAG/IDE).
- % migrantes 2017 por región (Censo).
- Crear `paper1/etl/09_build_regional_context.py`.
- Output: `paper1/output/data/contexto_regional.csv`.
- Costo: 1 día.

#### 22.7 Proxies de difusión de smartphone (fuera de la ronda principal)

**Origen:** R1 explícito. § 13, § 24.

Opciones de datos:

- **Subtel** publica reportes trimestrales sobre adopción de telefonía móvil con desagregación regional. Tasa de penetración móvil/100 habitantes. Disponible al menos desde 2012.
- **CMF / SBIF** publica datos de cuentas RUT/Vista y operaciones bancarias móviles. Útil para mostrar adopción de banca digital, que es el canal de fraude.
- **CEP / Cadem** han incluido en algunas encuestas preguntas sobre tenencia de smartphone (no es panel pero da puntos de calibración).
- **WhatsApp/banca móvil** datos del estudio de transformación digital de Cámara de Comercio de Santiago.

Decisión para esta revisión: no descargar ni modelar proxies nuevos de smartphones/CMF. El mecanismo se incorporará como discusión breve y como agenda futura, porque sumar estas series distrae del estimando principal y consume espacio en un artículo con límite de 10.000 palabras.

- Script: no crear en la ronda principal.
- Output: ninguno.
- Costo: 0 días en el plan operativo actual.
- Beneficio: se atiende R1 con texto teórico breve y con la sección de fraude digital como límite de medición, sin abrir una línea empírica secundaria.

#### 22.8 Dotación de Carabineros (opcional, baja prioridad)

- SUBDERE / Carabineros publica dotación regional anual (con frecuencia rezagada).
- Si está disponible, agregar como control variable en tiempo en el panel regional.
- Costo: 2 días (incluyendo gestión con la fuente).
- Beneficio: marginal; el FE región absorbe nivel; solo importa si hay variación temporal regional.

#### 22.9 Resumen de costos ETL

| Tarea | Costo (días) | Prioridad |
|---|---:|---|
| Auditoría ETL CCH y clasificación única CUM | 1 | Alta |
| ENUSC contextual desde `paper2` | 0,5 | Alta |
| Población comunal mensual | 1 | Alta |
| Panel comunal ensamblado | 1 | Alta |
| CASEN comunal | 2 | Media |
| Contexto regional (desempleo, densidad, migración) | 1 | Media |
| Proxies smartphone (Subtel/CMF) | 0 en esta ronda | Futuro |
| Carabineros dotación | 2 | Baja |
| **Total mínimo (Alta)** | **3,5** | |
| **Total con Media** | **8,5** | |
| **Total con Baja** | **10,5** | |

Recomendación: completar todo lo de prioridad Alta y, si hay tiempo, solo contexto regional básico. No incorporar Subtel/CMF ni dotación policial en esta ronda salvo que el manuscrito pierda capacidad explicativa después de los nuevos modelos principales.

### 23. Mecanismos alternativos: strain, eficacia colectiva, control informal

**Origen:** R3 explícito en sus comentarios menores ("inequality can impact crime composition through other mechanisms as well – such as collective efficacy, strain, etc.").

El marco actual descansa en (i) elección racional / Becker, (ii) actividades rutinarias / Cohen-Felson. R3 propone enriquecer con:

- **Strain theory (Agnew, 1992 y siguientes)**: ante shocks negativos (pandemia, pérdida económica) la frustración estructural y la presión adaptativa pueden producir desplazamiento desde delito instrumental no confrontacional hacia formas con mayor coerción. Útil para explicar por qué los violentos no cayeron al mismo ritmo que los no violentos durante la pandemia.
- **Collective efficacy (Sampson, Raudenbush y Earls, 1997)**: el control social informal en barrios puede haberse debilitado de forma asimétrica entre 2019 y 2023 (estallido, pandemia, post-pandemia). Esta perspectiva conecta con la heterogeneidad regional/comunal: macrozonas con menor capital social organizado podrían tolerar más rápido la emergencia de modalidades coercitivas.
- **Control informal y rutina** combinadas: la pandemia disolvió rutinas y guardianes; el estallido alteró la legitimidad institucional y la presencia policial. Estos dos canales actúan sobre violentos y no violentos de modo distinto.

Texto sugerido (para Section 2, párrafo de mecanismos):

```tex
Beyond rational-choice and routine-activities frameworks, three additional mechanisms are relevant. Strain theory (Agnew, 1992) suggests that macro-level economic and institutional shocks can shift offending composition by intensifying adaptive pressure on potential offenders, increasing the likelihood of confrontational forms relative to opportunistic ones. Collective efficacy (Sampson et al., 1997) provides a complementary mechanism at the neighborhood level: the capacity of communities to enforce informal social control may have weakened unevenly during the social uprising and the pandemic, affecting confrontational offenses more than non-confrontational property crime. Routine-activities theory, finally, predicts that the mobility contraction of 2020–2021 should have reduced both confrontational and non-confrontational offending in absolute terms, but more sharply for the non-confrontational opportunistic mode. None of these mechanisms is empirically identified in this article; they are advanced as a structured space of plausible explanations within which the documented compositional shift can be interpreted.
```

Referencias a `referencias.bib`:

- Agnew, R. (1992). Foundation for a general strain theory of crime and delinquency. *Criminology*, 30(1).
- Sampson, R. J., Raudenbush, S. W., y Earls, F. (1997). Neighborhoods and violent crime: A multilevel study of collective efficacy. *Science*, 277.
- Eslava, M., et al. (varios) si hay aplicaciones latinoamericanas recientes a strain / efficacy.

### 24. Smartphones como mecanismo y datos disponibles

**Origen:** R1 explícito; § 13 lo planteaba como texto pero sin propuesta de evidencia.

La revisión debe ofrecer una sección breve (~1 página) que articule:

1. Smartphone como objetivo de robo (alto valor / portabilidad / liquidez).
2. Smartphone como puerta a cuentas bancarias (canal de fraude post-robo).
3. Smartphone como detonante de modalidades coercitivas (encerronas + retención hasta transferencias).
4. Datos comparados internacionalmente y datos chilenos disponibles.

Evidencia descriptiva propuesta (ver § 22.7 para fuentes):

- Figura: penetración móvil Subtel + tasa de violentos por 100 mil habitantes, 2013–2025. Mostrar visualmente sin afirmar causalidad.
- Figura complementaria: indicador CMF de transacciones móviles + serie fraude digital.

Texto sugerido (versión ampliada respecto a § 13):

```tex
A specific mechanism plausibly connects the documented compositional shift to broader technological changes. Smartphones have become both highly liquid stolen goods and gateways to mobile banking, which alters the payoff structure of street robbery. A single device can yield direct resale value, immediate access to victim accounts via banking applications, and authentication for fraudulent transfers. This dual role generates incentives for coercive modalities that retain the victim long enough to obtain unlocking and authentication, and it makes property crime less dependent on physical access to homes or storage. Mobile penetration in Chile rose from approximately X devices per 100 inhabitants in 2013 to Y in 2024 (Subtel, 2025), and mobile banking transactions grew sharply over the 2018–2024 window (CMF, 2025). These descriptive trajectories are consistent with, but cannot identify, the proposed mechanism. We treat them as contextual evidence supporting the theoretical relevance of the smartphone channel.
```

### 25. Agenda de mecanismos mediadores (futuro)

**Origen:** R3 sugiere explícitamente que un análisis de mediación (pandemia → X → crimen) fortalecería el paper, pero acepta que los datos son difíciles de conseguir. Recomienda al menos mencionar en agenda futura.

Mediadores plausibles y datos comparables:

- **Movilidad urbana**: Google COVID-19 Community Mobility Reports (2020–2022), datos Waze, ENL Movilidad Carabineros. Permitirían validar el canal de actividades rutinarias durante la pandemia.
- **Protesta y disturbios**: GDELT, ACLED, registros de Carabineros sobre marchas. Calibrarían el shock del estallido.
- **Confianza institucional**: CEP, Cadem, LAPOP. Series transversales repetidas que pueden aproximarse a panel.
- **Mercado laboral**: ENE/INE para tasa de desempleo, INE para informalidad.
- **Migración interna**: Censo 2017 y posibles fuentes administrativas (SII, SUSESO) durante la pandemia.

Texto sugerido (futuro research agenda):

```tex
The design adjudicates the question of compositional change but does not identify the mechanisms that produced it. A natural extension is mediation analysis using mobility indices (Google COVID-19 Mobility, ACLED events, ENL data), institutional trust survey series, and labor-market indicators as proxies for routine activities, social-control disruption, and economic strain. Such an analysis would require either pre-registered identifying restrictions or a quasi-experimental design that exploits regional variation in mediator exposure. We leave this analysis to future work.
```

### 26. Counts vs rates y otras sensibilidades menores

**Origen:** R1 minor ("Are the results robust to alternative population measures (e.g., counts vs rates)?").

Plan:

- En `07_robustness.R` añadir tabla R8: modelo Poisson sobre conteos sin offset vs modelo con offset, modelo log-lineal sobre tasas, modelo binomial sobre share. Esperable: dirección consistente.
- En el cuerpo: una nota a pie diciendo que el resultado composicional no depende de la forma del denominador.
- Output: `paper1/output/tables/C3/tabla_R8_counts_vs_rates.csv`.

### 27. Reposicionar la categoría "snatching" / robo por sorpresa

**Origen:** R1 minor explícito.

Acciones (sintetiza § 11.2):

- Mantener "snatching" en el cuerpo como categoría intermedia.
- Reportar la sensibilidad bajo tres particiones (con violentos, con no violentos, multinomial 3-vías).
- Texto: "Snatching is retained as a third category because it shares the absence of weapon use with non-confrontational offenses but the in-person, opportunistic dimension with confrontational ones. The compositional result is robust to alternative partitions."

### 28. Definiciones, glosario y housekeeping

**Origen:** R1 minor ("CEP" sin definir; "dark figure" debería definirse temprano).

Acciones:

- Definir al primer uso: **CCH** (Carabineros de Chile), **SPD** (Subsecretaría de Prevención del Delito), **CAPJ** (Corporación Administrativa del Poder Judicial), **CUM** (Código Único de Materia), **ENUSC** (Encuesta Nacional Urbana de Seguridad Ciudadana), **CEP** (Centro de Estudios Públicos), **CPHDV** (Centro para la Prevención de Homicidios y Delitos Violentos), **SERMIG** (Servicio Nacional de Migraciones), **ICCS** (International Classification of Crime for Statistical Purposes).
- "Dark figure of crime": mover definición al primer párrafo de § 2 (introducción al marco conceptual o sección de datos).
- Tabla terminológica Chile-CUM ↔ ICCS ↔ etiqueta del paper (3 columnas, ~10 filas).
- Glosario al final del paper (½ página).
- Costo: 0,5 días.

### 29. Pendientes "no críticos" que mejoran el paper

- Mejorar la legibilidad de Figura 1 (serie nacional): añadir bandas sombreadas para estallido y pandemia, anotar puntos máximos y mínimos clave.
- Mejorar el mapa nacional (`09_maps_figures.R`): inset para zonas extremas (austral); incluir labels regionales legibles; usar paleta colorblind-safe.
- Compactar tablas de placebos: una sola tabla con todos los placebos lado a lado (P1–P5), no una por placebo.
- Cita Barthelon y Kruger (2011, JPE) explícitamente cuando se justifica la elección regional vs comunal y al introducir el panel comunal de robustez.
- Cita UNODC ICCS al introducir la categorización.

## Secuencia de trabajo recomendada (actualizada)

### Fase 0: Decisiones de framing (1–2 días)

1. Confirmar pivote a Crime, Law and Social Change y revisar guidelines de envío.
2. Cambiar título y etiquetas terminológicas en el manuscrito (§ 3).
3. Reescribir abstract e introducción (§ 4, § 5, § 6).
4. Separar los tres sentidos de composición (§ 2).
5. Reescribir hipótesis (§ 18).

### Fase 1: ETL prioritario (3–4 días)

1. Auditar ETL CCH, unificar clasificación CUM y eliminar `Unknown` del panel modelable (§ Plan parsimonioso, § 19).
2. Generar ENUSC contextual desde `paper2` (§ 22.1).
3. Población comunal mensual (§ 22.3).
4. Ensamble panel comunal (§ 22.4).
5. Contexto regional / CASEN si tiempo lo permite (§ 22.5, § 22.6).

### Fase 2: Evidencia inferencial nueva (ejecutada 2026-05-14)

1. Implementado `10_composition_models.py` sobre el panel CCH auditado (binomial agrupado, log-ratio, sensibilidad multinomial ponderada). § 1.
2. Implementado `11_its_diagnostics.py` (PACF, Ljung-Box, ADF/KPSS, AR sensitivity, spline knot sensitivity). § 8.
3. Implementado `04b_macrozona_shock_interaction.py` para shock × macrozona. Se generó figura de efectos y faceta temporal por macrozona; el mapa facetado queda para Fase 3. § 10.
4. Agregadas robusteces CUM 867, denominador con sorpresa, counts vs rates y sensibilidad snatching en `tabla_9d`/`tabla_9e`. § 26, § 27.
5. Adelantada robustez comunal parsimoniosa en `12_communal_robustness.py`, usando FE comunal absorbidos en log-tasas/log-ratio. Esta pieza responde a R1 y puede integrarse en Fase 3 si se desea una versión Poisson/fixest más canónica.

### Fase 3: Escala territorial y validación (4–5 días)

1. Refinar `12_communal_robustness.py` o reestimar en R/fixest si se decide reportar Poisson comuna-mes en el cuerpo; la versión Python de Fase 2 ya entrega full y dense sample. § 9.
2. Triangular ENUSC de forma acotada: `04b_build_enusc_context_from_paper2.py` con percepción y victimización personal nacional. § 11.
3. Análisis descriptivo de drivers de heterogeneidad regional: `12b_break_drivers.R`. § 10.1.
4. Rehacer mapas/figuras territoriales (`09_maps_figures.R`). § 10, § 29.

### Fase 4: Mecanismos complementarios (3 días)

1. Formalizar fraude digital como sustitución modal: `14_digital_substitution.R`. § 12.
2. Agregar smartphone como mecanismo plausible en texto, sin incorporar Subtel/CMF en esta ronda (§ 22.7, § 24).
3. Ampliar mecanismos teóricos (strain, eficacia colectiva): § 23.
4. Reinterpretar CUM 862, secuestros y homicidios como evidencia de concentración de severidad. § 14.

### Fase 5: Reducir y ordenar el manuscrito (3 días)

1. Cuerpo principal con 5 exhibiciones máximo:
   - Figura descriptiva integrada: serie/tasas y ratio, idealmente reduciendo Fig. 1-3 a una sola figura multipanel.
   - Tabla/Figura del modelo composicional: `tabla_9_composition_logit` + `fig6_predicted_composition` como núcleo de la contribución.
   - Tabla resumida de Poisson por tipo: mantener solo shocks y trayectoria reciente; mover tabla completa al apéndice.
   - Heterogeneidad territorial compacta: `fig9_macrozona_shock_effects` o una tabla reducida; `fig9b` y mapas al apéndice.
   - Robustez/validación clave: `tabla_9d` (snatching/CUM 867), ENUSC contextual y una fila de robustez comunal (`tabla_11b`/`tabla_11c`).
2. Apéndice con CUSUM completo, placebos completos, C1/C2, ITS diagnostics, CUM tables, comuna detallada.
3. Glosario y tabla terminológica Chile-CUM ↔ ICCS.
4. No preparar carta de respuesta: el manuscrito será un nuevo envío a CLSC. Mantener la matriz comentario-acción solo como control interno.

### Fase 6: Revisión final y envío (1–2 días)

1. Revisión interna de coherencia (intro ↔ métodos ↔ resultados ↔ discusión).
2. Revisión de lenguaje (sin "non-violent robbery", sin "property crime" donde sobre).
3. Revisión de citas y bibliografía.
4. Envío a Crime, Law and Social Change.

**Estimación total**: ~18–22 días de trabajo neto. Distribuible en 6 semanas calendario asumiendo dedicación parcial.

## Resultado esperado de la revisión

La versión revisada debe defender una contribución más precisa:

> Chile's reported physical property crime did not simply increase after the pandemic; its composition shifted. The violent share rose because non-confrontational offenses fell faster, while a small set of high-severity coercive modalities grew from a low base. The article contributes (i) a direct compositional test based on a grouped binomial model that estimates the violent share within a single estimating equation, (ii) a classification harmonized with international crime-statistics concepts and validated against a national victimization survey, (iii) a robustness analysis at the municipality level that addresses concerns about regional aggregation, and (iv) evidence that aggregate security narratives can be empirically real in their compositional dimension yet volumetrically misleading when read as a generalized crime surge.

Esta formulación responde mejor a *Crime, Law and Social Change* (y a un eventual reenvío en JQC u otra revista cuantitativa) porque:

- Convierte la composición en estimando, no en interpretación post-hoc.
- Evita prometer causalidad que el diseño no identifica.
- Sitúa percepción y política penal en literatura criminológica contemporánea (Beckett, Enns, Shi, Duxbury) en lugar de en debates electorales chilenos contingentes.
- Reconoce límites del dato administrativo (cifra negra, taxonomía, denominador, autocorrelación).
- Usa la desagregación comunal disponible para neutralizar la crítica de escala (Barthelon y Kruger 2011 contestados).
- Integra fraude digital y smartphones como sustitución modal y mecanismo plausible sin debilitar el resultado principal.
- Triangula con ENUSC tanto en victimización como en percepción.
- Adopta lenguaje alineado con ICCS/UNODC y abandona "non-violent robbery".
- Reporta diagnósticos ITS estándar (PACF, ADF, KPSS, AR sensitivity) y separa estimador (Poisson-QMLE) de inferencia (WCB).
- Reorganiza los resultados para que la respuesta a la pregunta principal sea visible en las primeras dos páginas de la sección de resultados.
