# Preparación de Fase 1: ETL parsimonioso

Fecha: 2026-05-13

Este documento deja definidos los insumos disponibles, su estado y las decisiones mínimas para iniciar la Fase 1 del plan de revisión. La lógica de esta fase es auditar y reconstruir lo necesario para que los modelos nuevos descansen en datos consistentes, sin ampliar innecesariamente el artículo.

## Decisión sobre CASEN vs SAE comunal

**Decisión recomendada:** usar ambas fuentes, pero con funciones distintas.

- **CASEN microdatos:** usar solo para contexto regional parsimonioso. Las bases disponibles son representativas a nivel regional y no contienen una variable explícita de comuna de residencia. No deben usarse para generar indicadores comunales directos.
- **Estimaciones SAE comunales:** usar como fuente preferente para heterogeneidad socioeconómica comunal. Son más adecuadas para la robustez comunal porque ya entregan estimaciones por comuna, con código comunal, intervalos y tipo de estimación.

Uso sugerido en el paper:

- Modelo principal: sin CASEN/SAE como covariable central.
- Robustez comunal: CCH comuna-mes con FE comunal; SAE 2017 como baseline socioeconómico pre-pandemia si se desea caracterizar heterogeneidad.
- Contexto regional: CASEN regional solo como insumo descriptivo o de apéndice, no como bloque analítico principal.

Advertencia importante:

- Los SAE 2013 y 2015 usan códigos comunales anteriores a la creación de Ñuble para comunas como Chillán, Bulnes y Yungay. Para unir esos años con el CCH actual, que usa códigos de región 16, se requiere una homologación de códigos. Para evitar ese costo, la opción parsimoniosa es usar SAE 2017 como baseline comunal pre-pandemia y 2022/2024 si se necesita contraste posterior.

## Inventario de insumos

### CCH / Carabineros

Archivo disponible:

- `paper1/output/data/cch_panel_comuna_month.parquet`

Estado:

- Formato largo: comuna × región × año × mes × CUM.
- Cobertura: 2013-2025.
- Regiones: 16.
- Comunas observadas: 345.
- CUM: 32.
- `CUM 804` está clasificado como `Sorpresa`.
- Receptación (`812`, `864`, `869`, `2009`, `12053`) sigue presente en el archivo largo con `C3_categoria = None`.

Problemas a resolver en Fase 1:

- Centralizar clasificación CUM en una sola tabla/fuente de verdad.
- Excluir receptación del panel C3 modelable y documentarla como categoría excluida.
- Cambiar etiquetas internas hacia la nueva nomenclatura: `confrontational`, `snatching`, `non_confrontational`.
- Generar reporte QA con totales por CUM, denuncias/detenciones y consistencia de agregación.
- El panel comunal final debe ser balanceado: 345 comunas × 156 meses = 53.820 filas. El archivo actual solo tiene 51.564 comuna-meses con al menos un CUM objetivo observado, por lo que faltan ceros explícitos.

### Panel regional actual

Archivo disponible:

- `paper1/output/data/panel_region_month.parquet`

Estado:

- Filas: 2.496 = 16 regiones × 156 meses.
- Incluye población regional mensual, SERMIG, dummies de estallido/pandemia, tendencia y macrozona.
- Contiene columna residual `Unknown`, aunque actualmente en cero.

Problemas a resolver en Fase 1:

- Regenerar desde CCH auditado.
- Eliminar `Unknown` como columna modelable.
- Mantener compatibilidad con scripts existentes o crear alias de variables mientras se actualizan modelos.

### Población

Archivos disponibles:

- `data/Poblacion_base_2017/estimaciones-y-proyecciones-2002-2035-comunas.xlsx`
- `data/Poblacion_nacional_base_2024/estimaciones-y-proyecciones-de-población-1992-2070_base-2024_base-de-datos.xlsx`
- `paper1/output/data/poblacion_regional_mensual.csv`
- `paper1/output/data/poblacion_nacional_mensual_base2024.csv`

Estado:

- La base comunal INE 2017 contiene 346 comunas, pero CCH y SAE trabajan con 345. La comuna adicional es Antártica (`12202`), que no aparece en CCH ni SAE.
- La población regional mensual ya existe y cubre 2.496 filas.

Problemas a resolver en Fase 1:

- Crear `poblacion_comunal_mensual.csv` excluyendo o dejando en cero operativo la comuna Antártica según el universo CCH/SAE.
- Interpolar población anual comunal a mensual.
- Mantener SERMIG solo regional; no aplicar corrección migratoria comunal.

### SERMIG

Archivo disponible:

- `paper1/output/data/sermig_correction.csv`

Estado:

- Disponible a región-año.
- Ya se integra al panel regional.

Decisión:

- Mantener solo a nivel regional. No trasladar al panel comunal.

### ENUSC

Archivos disponibles:

- `paper2/output/data/enusc_panel_kish.parquet`
- `paper1/output/tables/enusc_context_series.csv`
- `paper1/output/tables/enusc_context_qa.csv`
- `paper1/output/figures/fig_enusc_perception_context.png`
- `paper1/output/figures/fig_enusc_perception_context.pdf`

Estado:

- Ya fue generada la triangulación contextual desde `paper2`.
- QA previo: 238.262 observaciones Kish con peso válido en 102 comunas históricas.

Decisión:

- No tocar ENUSC en Fase 1 salvo para verificar que los outputs siguen disponibles.
- No usar ENUSC comunal ni denuncia ENUSC.

### CASEN microdatos

Archivos disponibles:

- `data/CASEN/casen_2013.sav`
- `data/CASEN/casen_2015.sav`
- `data/CASEN/casen_2017.sav`
- `data/CASEN/casen_en_pandemia_2020.sav`
- `data/CASEN/casen_2022.sav`
- `data/CASEN/casen_2024.sav`

Estado:

- Útiles para contexto regional: `region`, `area`, `expr`, `pobreza`, `pobreza_2013`, ingresos corregidos y variables distributivas regionales.
- No contienen comuna de residencia explícita.

Decisión:

- No usar para comuna.
- Usar solo si se construye `casen_contexto_regional.csv`.

### Estimaciones comunales SAE

Archivos disponibles:

- `data/Estimaciones_pobreza_comunal/SAE_ingresos_2013.xlsx`
- `data/Estimaciones_pobreza_comunal/SAE_ingresos_multidimensional_2015.xlsx`
- `data/Estimaciones_pobreza_comunal/SAE_ingresos_multidimensional_2017.xlsx`
- `data/Estimaciones_pobreza_comunal/SAE_ingresos_2020.xlsx`
- `data/Estimaciones_pobreza_comunal/SAE_ingresos_2022.xlsx`
- `data/Estimaciones_pobreza_comunal/SAE_ingresos_2024.xlsx`
- `data/Estimaciones_pobreza_comunal/SAE_multidimensional_2022.xlsx`
- `data/Estimaciones_pobreza_comunal/SAE_multidimensional_2024.xlsx`

Estado:

- Todos los archivos tienen 345 comunas con código comunal válido.
- Incluyen porcentaje estimado, límites inferior/superior y metodología/tipo de estimación.
- 2013 y 2015 usan codificación comunal previa a Ñuble; 2017 en adelante usa códigos actuales de Ñuble.

Decisión:

- Usar SAE 2017 como baseline comunal preferente.
- Usar 2022/2024 si se necesita contraste post-pandemia.
- No usar 2013/2015 hasta crear homologación de códigos antiguos a actuales.

### CPHDV homicidios

Archivos disponibles:

- `data/CPHDV/Base_de_Datos_VHC_2018_2025.xlsx`
- `paper1/output/data/cphdv_homicidios.parquet`

Estado:

- Fuente útil como benchmark externo de homicidios.
- El parquet actual contiene región-año-mes y conteo.

Decisión:

- Mantener como benchmark regional; no mover a comuna en Fase 1.

### Placebos y fraude digital

Archivos disponibles:

- `paper1/output/data/placebo_panel.parquet`
- `paper1/output/data/fraude_digital_panel_comuna_month.parquet`

Estado:

- Placebos regionales disponibles.
- Fraude digital comuna-mes disponible, pero debe quedar fuera del cuerpo principal o como apéndice/agenda futura salvo decisión explícita.

Decisión:

- En Fase 1 solo verificar compatibilidad de llaves y cobertura.
- No convertir fraude digital en mecanismo principal.

## Checklist para iniciar Fase 1

1. Crear tabla/fuente única de clasificación CUM.
2. Crear auditoría CCH:
   - totales por CUM;
   - C1/C2/C3;
   - receptación excluida;
   - `CUM 804` separado como snatching;
   - consistencia comuna -> región;
   - completitud región-mes y comuna-mes.
3. Regenerar panel regional auditado sin `Unknown`.
4. Crear población comunal mensual.
5. Crear panel comunal balanceado con ceros explícitos.
6. Crear ETL SAE/CASEN contextual si se confirma usar heterogeneidad socioeconómica.
7. Mantener ENUSC contextual ya generado.

## Decisión pendiente antes de codificar ETL SAE

Confirmar si el bloque socioeconómico comunal usará:

- solo SAE 2017 como baseline pre-pandemia;
- SAE 2017 + 2022/2024 como contraste temporal;
- o también 2013/2015, lo que exige homologar códigos antiguos de comunas de Ñuble.
