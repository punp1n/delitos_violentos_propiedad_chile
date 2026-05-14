# Registro de cambios de la revisión de `paper1`

Este archivo documenta los cambios aplicados durante la revisión del manuscrito para el nuevo envío a *Crime, Law and Social Change*. Debe actualizarse después de cada bloque de trabajo sustantivo para mantener trazabilidad entre el plan, el manuscrito, los scripts y los outputs.

## 2026-05-13 — Fase 0: framing, abstract y etiquetas

### Archivos editados

- `paper1/texto/Eng/submission/Manuscript.tex`
- `paper1/comentarios_rev/plan_revision_revisores.md`

### Cambios en el manuscrito

- Se cambió el título a: `Volume or Composition? Reported Robbery and Theft Trends in Chile, 2013--2025`.
- Se eliminaron los campos de autor y afiliación anónimos. El PDF compilado queda sin autor visible.
- Se reescribió el abstract conforme a las guías de *Crime, Law and Social Change*: 191 palabras, sin referencias ni abreviaturas técnicas indefinidas.
- Se actualizaron las keywords a seis términos: `Reported crime`, `Robbery and theft`, `Crime composition`, `Public insecurity`, `Police reports`, `Chile`.
- Se reescribió la introducción para:
  - quitar referencias contingentes a coyuntura electoral;
  - situar la pregunta en la relación entre registros policiales, percepción pública e inseguridad;
  - presentar el problema como una distinción entre volumen y composición de delitos patrimoniales físicos reportados.
- Se cambió el eje terminológico del artículo:
  - `violent robberies` -> `confrontational robberies`;
  - `surprise robberies` -> `snatching`;
  - `non-violent robberies` -> `non-confrontational property offenses`.
- Se separaron tres sentidos de composición:
  - composición entre categorías, que es el objeto empírico principal;
  - cambio cualitativo dentro de la categoría confrontacional, como CUM 862;
  - sustitución modal hacia fraude digital, tratado como señal secundaria y límite.
- Se reescribieron las hipótesis como:
  - H1: volumen;
  - H2: composición;
  - H3: diferenciación de shocks.
- Se revisó la sección de clasificación C3 para explicar por qué las traducciones literales de `robo` y `hurto` son problemáticas en inglés criminológico.

### Cambios en el plan de revisión

- Se corrigió el límite de extensión de CLSC a 10.000 palabras.
- Se eliminó la preparación de carta de respuesta como tarea de envío, porque se trata de un nuevo envío y no de una resubmisión.
- La matriz comentario-acción queda solo como control interno.

### Verificación

- Se compiló `Manuscript.tex` con `pdflatex` dos veces.
- Output generado: `paper1/texto/Eng/submission/Manuscript.pdf`.
- No quedaron errores LaTeX, citas indefinidas ni referencias cruzadas indefinidas.
- Persisten advertencias menores de formato (`underfull`/`overfull`) asociadas a tablas, ecuaciones y referencias largas.
- Conteo aproximado del cuerpo antes de referencias/apéndice: 11.905 palabras. La Fase 5 debe recortar o mover al apéndice cerca de 1.900 palabras.

## 2026-05-13 — Revisión inicial de bases CASEN

### Archivos inspeccionados

- `data/CASEN/casen_2013.sav`
- `data/CASEN/casen_2015.sav`
- `data/CASEN/casen_2017.sav`
- `data/CASEN/casen_en_pandemia_2020.sav`
- `data/CASEN/casen_2022.sav`
- `data/CASEN/casen_2024.sav`

### Objetivo ETL

CASEN se evalúa solo como fuente contextual parsimoniosa para heterogeneidad socioeconómica regional o comunal. No debe convertirse en un bloque analítico del cuerpo principal. Variables prioritarias:

- identificadores de año, región y comuna;
- pesos de expansión;
- pobreza por ingresos;
- ingreso autónomo o monetario del hogar/persona;
- zona urbana/rural si está disponible;
- variables suficientes para calcular pobreza, ingreso regional/comunal y, si es viable, desigualdad.

### Estado

Inspección de metadatos completada con `pyreadstat` sin cargar microdatos completos.

### Resultado general

Las bases CASEN descargadas son suficientes para construir un **contexto socioeconómico regional** parsimonioso para el paper. No son suficientes, con la información actualmente visible, para construir un panel **comunal** confiable, porque las bases públicas inspeccionadas no incluyen una variable explícita de comuna de residencia. Existen `segmento` y/o `estrato` con etiquetas del tipo `comuna-área`, pero no debe derivarse comuna desde esas variables sin revisar manuales/codebooks oficiales y confirmar la codificación.

### Cobertura disponible

| Año | Archivo | Filas | Regiones | Comentario |
|---|---:|---:|---:|---|
| 2013 | `casen_2013.sav` | 218.491 | 15 | Ñuble no existe separado. |
| 2015 | `casen_2015.sav` | 266.968 | 15 | Incluye `car`, comunas autorrepresentadas, pero no comuna de residencia general. |
| 2017 | `casen_2017.sav` | 216.439 | 16 y `region_15` | Incluye `region_15`, útil para colapsar Ñuble-Biobío. |
| 2020 | `casen_en_pandemia_2020.sav` | 185.437 | 16 | CASEN en pandemia; usar con cautela por cambio de modo/contexto. |
| 2022 | `casen_2022.sav` | 202.231 | 16 | Incluye `expr_osig`, no necesario para este ETL. |
| 2024 | `casen_2024.sav` | 218.367 | 16 | Incluye pobreza e ingresos comparables básicos. |

### Variables presentes para ETL regional

Variables comunes o suficientes en todos los años:

- Territorio: `region`; `region_15` solo en 2017; `area` urbano/rural.
- Peso: `expr` como factor de expansión regional en todos los años.
- Diseño muestral: `varstrat`; `segmento`/`estrato` en varios años.
- Pobreza por ingresos: `pobreza` y `pobreza_2013` en todos los años.
- Ingresos corregidos:
  - `yautcor`, `ytotcor`;
  - `yautcorh`, `ytotcorh`;
  - `ypchautcor`, `ypchtotcor`, `ypchmonecor`.
- Tamaño del hogar: `numper`.
- Estratificación distributiva regional: `dautr`, `qautr`.

Variables de pobreza multidimensional:

- 2013: `pobreza_multi_4d`.
- 2015 y 2017: `pobreza_multi_2015`, `pobreza_multi_4d`.
- 2022: `pobreza_multi`, `pobreza_multi_2015`, `pobreza_multi_4d`.
- 2024: `pobreza_multi`, `pobreza_multi_2015`, sin `pobreza_multi_4d`.

### Decisión metodológica preliminar

- Para el paper, usar CASEN solo como contexto regional o como insumo exploratorio de heterogeneidad, no como covariable central del modelo principal.
- Indicadores recomendados:
  - pobreza por ingresos usando `pobreza_2013` o `pobreza`;
  - ingreso per cápita corregido del hogar usando `ypchtotcor` o `ypchautcor`;
  - urbanización con `area`;
  - Gini regional calculado con `ypchtotcor` y `expr`, solo si se requiere.
- Para comparaciones longitudinales 2013-2024, decidir si:
  - trabajar en 15 regiones colapsando Ñuble con Biobío, o
  - usar 16 regiones desde 2017/2020 y dejar años previos sin Ñuble separado.
- Dado que el artículo usa CCH 2013-2025 con 16 regiones, la opción más parsimoniosa para CASEN es usar indicadores pre-pandemia de 2017 y, si se requiere longitudinalidad, reportar una versión colapsada Biobío-Ñuble.

### Duda pendiente para decidir

Si se desea usar CASEN a nivel comunal, necesito los manuales/codebooks o documentación oficial que confirme cómo extraer comuna de residencia desde `segmento`/`estrato`, o bien una versión de CASEN con variable explícita de comuna. Sin eso, CASEN debe quedar limitada a nivel regional.

## 2026-05-13 — Preparación de Fase 1 ETL parsimonioso

### Archivos creados o editados

- `paper1/comentarios_rev/preparacion_fase1_etl.md`
- `paper1/comentarios_rev/plan_revision_revisores.md`

### Cambios realizados

- Se revisaron las estimaciones SAE comunales en `data/Estimaciones_pobreza_comunal`.
- Se confirmó que los archivos SAE contienen 345 comunas, código comunal, estimación, límites inferior/superior y metodología/tipo de estimación.
- Se identificó una advertencia de homologación: SAE 2013 y 2015 usan códigos comunales previos a la creación de Ñuble para comunas actualmente codificadas como región 16. SAE 2017 en adelante usa códigos actuales.
- Se definió la decisión recomendada:
  - CASEN microdatos: solo contexto regional.
  - SAE comunal: fuente preferente para heterogeneidad socioeconómica comunal.
  - SAE 2017: baseline comunal pre-pandemia preferente.
  - SAE 2022/2024: posible contraste post-pandemia.
  - SAE 2013/2015: no usar sin homologación de códigos antiguos a actuales.
- Se corrigió en el plan de revisión el tamaño esperado del panel comunal balanceado: 345 comunas × 156 meses = 53.820 filas. El archivo CCH actual tiene 51.564 comuna-meses observados con eventos; el ETL debe completar ceros explícitos.

### Hallazgos para Fase 1

- `cch_panel_comuna_month.parquet` existe y cubre 2013-2025, 16 regiones, 345 comunas y 32 CUM.
- El archivo CCH está en formato largo comuna-mes-CUM, no en panel comuna-mes balanceado.
- Receptación (`812`, `864`, `869`, `2009`, `12053`) sigue presente en el CCH largo con `C3_categoria = None`; debe excluirse o documentarse fuera del panel C3 modelable.
- `panel_region_month.parquet` tiene 2.496 filas y está listo como referencia, pero debe regenerarse sin columna residual `Unknown`.
- La población comunal INE contiene 346 comunas; la comuna adicional frente a CCH/SAE es Antártica (`12202`). El panel comunal del paper debe trabajar con el universo de 345 comunas CCH/SAE.

## 2026-05-13 — Fase 1 ejecutada: ETL parsimonioso

### Decisión sobre SAE

Se aplicó la decisión del autor: usar SAE 2017 + 2022/2024 como contraste temporal. Para el indicador comunal se eligió **pobreza por ingresos**, no pobreza multidimensional. Razón: pobreza por ingresos es el indicador más directo para aproximar strain económico y desigualdad material en una robustez comunal; además está disponible de forma comparable en 2017, 2022 y 2024 con códigos comunales actuales.

### Scripts creados o modificados

- `paper1/etl/cum_classification.py`: fuente única de clasificación CUM.
- `paper1/etl/01_extract_cch.py`: actualizado para usar clasificación CUM centralizada.
- `paper1/etl/01b_audit_cch_etl.py`: auditoría CCH y validaciones CUM.
- `paper1/etl/01c_reclassify_cch_existing.py`: re-clasificación determinística del parquet CCH existente cuando la conexión SQL no está disponible.
- `paper1/etl/03b_build_national_population.py`: ruta corregida a path relativo.
- `paper1/etl/03c_build_communal_population.py`: población comunal mensual.
- `paper1/etl/06_assemble_panel.py`: panel regional auditado, sin columna `Unknown` modelable.
- `paper1/etl/06b_assemble_communal_panel.py`: panel comuna-mes balanceado.
- `paper1/etl/08_build_sae_casen_context.py`: ETL SAE comunal por pobreza de ingresos.

### Ejecución

Se intentó ejecutar la extracción desde SQL Server:

- `01_extract_cch.py`
- `02_extract_placebos.py`
- `07_extract_fraude_digital.py`

La ejecución directa desde BD no fue posible en este entorno porque, aunque se instaló `pyodbc`, falta la biblioteca nativa `libodbc.so.2`. Se continuó con los parquets ya extraídos y se re-aplicó la clasificación CUM centralizada sobre `cch_panel_comuna_month.parquet`.

Scripts ejecutados correctamente:

- `01c_reclassify_cch_existing.py`
- `01b_audit_cch_etl.py`
- `02b_build_cphdv.py`
- `03_build_population.py`
- `03b_build_national_population.py`
- `03c_build_communal_population.py`
- `04_build_enusc.py`
- `04_build_sermig.py`
- `04b_build_enusc_context_from_paper2.py`
- `06_assemble_panel.py`
- `06b_assemble_communal_panel.py`
- `08_build_sae_casen_context.py`

### Validaciones CCH solicitadas

Todas pasaron exactamente:

- CUM 804, nacional 2025: observado 35.678; esperado 35.678.
- CUM 804, Valparaíso 2025: observado 2.399; esperado 2.399.
- CUM 808, nacional 2025: observado 55.543; esperado 55.543.
- CUM 808, Región Metropolitana 2025: observado 28.121; esperado 28.121.

Output: `paper1/output/tables/cch_validation_checks.csv`.

### Outputs principales generados

- `paper1/output/data/cch_panel_comuna_month.parquet`: CCH largo comuna-mes-CUM reclasificado con CUM central.
- `paper1/output/tables/cch_etl_audit_report.csv`: auditoría CCH.
- `paper1/output/tables/cch_cum_totals.csv`: totales por CUM.
- `paper1/output/tables/cum_classification_table.csv`: tabla canónica de clasificación CUM.
- `paper1/output/data/poblacion_regional_mensual.csv`: población regional mensual con corrección SERMIG.
- `paper1/output/data/poblacion_nacional_mensual_base2024.csv`: población nacional mensual base 2024.
- `paper1/output/data/poblacion_comunal_mensual.csv`: población comunal mensual, 53.820 filas.
- `paper1/output/data/panel_region_month.parquet`: panel regional final para modelos principales, 2.496 filas.
- `paper1/output/data/panel_comuna_month.parquet`: panel comunal balanceado para robustez, 53.820 filas.
- `paper1/output/data/sae_pobreza_comunal.csv`: SAE pobreza por ingresos 2017, 2022 y 2024.
- `paper1/output/tables/sae_pobreza_comunal_qa.csv`: QA SAE.

### Estado de paneles finales

- Panel regional: 16 regiones x 156 meses = 2.496 filas; sin `Unknown`; población no faltante.
- Panel comunal: 345 comunas x 156 meses = 53.820 filas; población no faltante; ceros explícitos incluidos.
- Comunas densas: 185 comunas con promedio mensual de confrontational robberies >= 1.
- Totales C3 coinciden entre panel regional y comunal:
  - `n_confrontational`: 807.346.
  - `n_non_confrontational`: 3.266.836.
  - `n_snatching`: 382.445.

### Archivo principal para modelos

El archivo principal para los nuevos modelos inferenciales regionales es:

- `paper1/output/data/panel_region_month.parquet`

El archivo para robustez comunal es:

- `paper1/output/data/panel_comuna_month.parquet`

## 2026-05-13 — Actualización Fase 1: extracción ODBC 17 ejecutada

Se reintentó la conexión a SQL Server usando el Python de Windows, que sí tiene acceso a `ODBC Driver 17 for SQL Server` y `pyodbc 5.3.0`. La limitación anterior correspondía al entorno WSL, donde faltan `unixodbc`/`libodbc.so.2` y no hay permisos `sudo` para instalarlos.

### Scripts con extracción desde BD ejecutados

- `paper1/etl/01_extract_cch.py`: ejecutado contra SQL Server y guardado inicialmente en `paper1/output/data/cch_panel_comuna_month_from_db.parquet`.
- `paper1/etl/02_extract_placebos.py`: ejecutado contra SQL Server y actualizado `paper1/output/data/placebo_panel.parquet`.
- `paper1/etl/07_extract_fraude_digital.py`: ejecutado contra SQL Server y actualizado `paper1/output/data/fraude_digital_panel_comuna_month.parquet`.

El parquet CCH extraído desde BD fue comparado con el canónico previo: mismas llaves `comuna-region-year-month-cum`, mismos conteos de denuncias y detenciones, 4.459.418 denuncias y 1.009.582 detenciones. Luego se reemplazó el canónico `paper1/output/data/cch_panel_comuna_month.parquet` con la extracción recién generada desde BD.

### Validación CUM posterior a extracción BD

- CUM 804, nacional 2025: observado 35.678; esperado 35.678.
- CUM 804, Valparaíso 2025: observado 2.399; esperado 2.399.
- CUM 808, nacional 2025: observado 55.543; esperado 55.543.
- CUM 808, Región Metropolitana 2025: observado 28.121; esperado 28.121.

### Derivados reconstruidos después de la extracción BD

- `paper1/output/data/cphdv_homicidios.parquet`
- `paper1/output/data/sermig_correction.csv`
- `paper1/output/data/poblacion_regional_mensual.csv`
- `paper1/output/data/poblacion_nacional_mensual_base2024.csv`
- `paper1/output/data/poblacion_comunal_mensual.csv`
- `paper1/output/data/enusc_microdata_filtered.parquet`
- `paper1/output/tables/enusc_context_series.csv`
- `paper1/output/data/sae_pobreza_comunal.csv`
- `paper1/output/data/panel_region_month.parquet`
- `paper1/output/data/panel_comuna_month.parquet`

### Outputs finales verificados

- `paper1/output/data/cch_panel_comuna_month.parquet`: 425.551 filas.
- `paper1/output/data/panel_region_month.parquet`: 2.496 filas; 16 regiones; sin columna `Unknown`.
- `paper1/output/data/panel_comuna_month.parquet`: 53.820 filas; 345 comunas.
- `paper1/output/data/placebo_panel.parquet`: 10.117 filas.
- `paper1/output/data/fraude_digital_panel_comuna_month.parquet`: 72.691 filas.
- `paper1/output/data/sae_pobreza_comunal.csv`: 1.035 filas.

Los totales C3 coinciden entre panel regional y comunal:

- `confrontational`: 807.346 denuncias.
- `non_confrontational`: 3.266.836 denuncias.
- `snatching`: 382.445 denuncias.

## 2026-05-14 — Fase 2 ejecutada: evidencia inferencial nueva

### Scripts creados

- `paper1/models/model_helpers.py`
- `paper1/models/10_composition_models.py`
- `paper1/models/11_its_diagnostics.py`
- `paper1/models/04b_macrozona_shock_interaction.py`
- `paper1/models/12_communal_robustness.py`

Los scripts se ejecutaron con el Python de Windows mediante `py.exe -3`, porque el alias `py` no está disponible dentro de la shell WSL.

### Outputs generados

- `paper1/output/tables/C3/tabla_9_composition_logit.csv`
- `paper1/output/tables/C3/tabla_9b_logratio_model.csv`
- `paper1/output/tables/C3/tabla_9c_marginal_shares.csv`
- `paper1/output/tables/C3/tabla_9d_composition_sensitivity.csv`
- `paper1/output/tables/C3/tabla_9e_counts_rates_period_change.csv`
- `paper1/output/tables/C3/tabla_9f_multinomial_sensitivity.csv`
- `paper1/output/tables/C3/tabla_10_its_diagnostics.csv`
- `paper1/output/tables/C3/tabla_10b_autoregressive_sensitivity.csv`
- `paper1/output/tables/C3/tabla_10c_spline_knot_sensitivity.csv`
- `paper1/output/tables/C3/tabla_4b_macrozona_shock_interactions.csv`
- `paper1/output/tables/C3/tabla_11_communal_robustness.csv`
- `paper1/output/tables/C3/tabla_11b_communal_composition.csv`
- `paper1/output/tables/C3/tabla_11c_communal_dense_sensitivity.csv`
- `paper1/output/tables/C3/tabla_11d_communal_share_distribution.csv`
- `paper1/output/figures/fig6_predicted_composition.png/pdf`
- `paper1/output/figures/fig7_pacf_residuals.png/pdf`
- `paper1/output/figures/fig7b_spline_trend_fit.png/pdf`
- `paper1/output/figures/fig8_communal_distribution.png/pdf`
- `paper1/output/figures/fig9_macrozona_shock_effects.png/pdf`
- `paper1/output/figures/fig9b_macrozona_composition_trends.png/pdf`

### Resultados principales

- El modelo binomial agrupado confirma el cambio composicional directo:
  - `d_estallido`: OR = 1,142; p < 0,001.
  - `d_pandemia`: OR = 0,994; p = 0,697.
  - Share observado confrontacional: 19,15% en 2016-septiembre 2019 y 22,32% en 2022-2025.
  - Diferencia observada: +3,17 puntos porcentuales; p bootstrap = 0,004.
  - Diferencia predicha por el modelo: +2,85 puntos porcentuales.
- El log-ratio entrega una lectura coherente pero más sensible al shock pandémico:
  - `d_estallido`: multiplicador = 1,123; p < 0,001.
  - `d_pandemia`: multiplicador = 0,925; p = 0,010.
- La sensibilidad de `snatching` no revierte el resultado:
  - `snatching` fusionado con confrontacionales: diferencia observada +3,58 pp.
  - `snatching` fusionado con no confrontacionales: diferencia observada +2,71 pp.
- La exclusión de CUM 867 reduce fuertemente la diferencia post-baseline a +0,57 pp observados y +0,33 pp predichos. Esto implica que `portonazos/encerronas` explican una parte importante del aumento reciente del share confrontacional y deben discutirse como componente sustantivo, no solo como advertencia de comparabilidad.
- Conteos vs tasas:
  - Confrontational: conteos +18,5%, pero tasa anualizada -4,2%.
  - Non-confrontational: conteos -2,3%, tasa -21,0%.
  - Esto preserva la tesis de composición y aclara que el aumento en conteos confrontacionales no equivale a una expansión de tasa comparable a la narrativa de crisis generalizada.

### Diagnósticos ITS

- Ljung-Box rechaza ausencia de autocorrelación en residuos del binomial composicional y de los Poisson por categoría hasta lag 24.
- La sensibilidad AR(1)/AR(2) del log-ratio conserva el patrón:
  - AR1: `d_estallido` multiplicador = 1,096; p < 0,001; `d_pandemia` = 0,945; p = 0,041.
  - AR2: `d_estallido` = 1,098; p < 0,001; `d_pandemia` = 0,950; p = 0,041.
- La sensibilidad de nodos 3/5/7 mantiene la diferencia predicha post-baseline en torno a +2,85 pp.

### Heterogeneidad territorial y comuna

- `04b_macrozona_shock_interaction.py` muestra que la pandemia contrae confrontational robberies en todas las macrozonas (IRR aprox. 0,49-0,67), mientras el estallido aumenta más en Norte (1,26), RM (1,17) y Sur (1,06).
- Algunas celdas no confrontacionales tienen inferencia inestable por matriz cluster no positiva definida; la tabla marca `se_source` y esas celdas deben usarse con cautela.
- La robustez comunal se ejecutó como OLS sobre log-tasas/log-ratio con FE comunal absorbidos y cluster por comuna, porque el GLM Poisson con 345 dummies explícitas en Python no terminó en un tiempo razonable.
- El resultado comunal no contradice el hallazgo central:
  - Share observado sube +3,17 pp en 345 comunas y +3,38 pp en las 185 comunas densas.
  - En log-ratio con FE comunal, `d_estallido` es positivo en comunas densas (multiplicador 1,084; p < 0,001).
  - `d_pandemia` es positivo en full sample (1,076; p < 0,001), pero nulo en comunas densas (0,999; p = 0,938), por lo que no debe afirmarse un efecto pandémico composicional homogéneo a escala comunal.

### Comparación sustantiva con la versión enviada

Los hallazgos no cambian en su dirección central respecto de `paper1/texto/Eng/submission/Manuscript.tex`: sigue siendo más defendible hablar de cambio composicional que de aumento volumétrico generalizado. Sí cambian tres matices importantes:

1. La evidencia composicional ya no descansa en comparar tres Poisson separados; ahora existe un test directo del share confrontacional.
2. La pandemia no debe presentarse como el motor directo del aumento del share en el binomial principal. El aumento post-2022 es una diferencia de trayectoria de mediano plazo.
3. CUM 867 es más importante de lo que sugería la discusión anterior: al excluirlo, el aumento reciente del share se reduce mucho. La revisión debe tratar `portonazos/encerronas` como parte sustantiva del cambio confrontacional, no solo como limitación administrativa.
