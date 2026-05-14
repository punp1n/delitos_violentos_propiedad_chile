# Análisis Exploratorio Fase 2: Tendencias Temporales y Perfil Sociodemográfico (2014-2024)

## 1. Desagregación de Casos Policiales: Denuncias vs Flagrancia (Temporalidad)
*(Metodología: Se aislaron las 102 comunas históricas urbanas).*

En lugar de tratar las Denuncias y Detenciones como una masa única (Casos Policiales), se separó el flujo criminal para obtener dos ventanas distintas del fenómeno de violencia contra la propiedad:
1. **La Denuncia:** El pulso de victimización relatado por la ciudadanía (donde a menudo el autor es desconocido).
2. **La Flagrancia:** El pulso reaccionario inmediato del Estado, que captura la hostilidad in fraganti.

**Hallazgos de la Temporalidad (Ver `tendencias_temporales_cch.xlsx`):**
* **Ciclo Mensual (`_Mes`):** Permite aislar visualmente picos delictuales estacionarios (por ejemplo, si los robos con intimidación repuntan sistemáticamente en meses de invierno respecto a hurtos).
* **Ciclo Diario (`_Dia`):** Desagrega la violencia según días de la semana (1 a 7), clave para ver si la agresión instrumental tiene correlación con fines de semana o es puramente rutinaria de lunes a viernes.
* **Tramos Horarios (`_Tramo`):** Las 24 horas del día segmentadas proporcionan un indicio fortísimo del *modus operandi*. Los delitos no violentos (hurtos) suelen acompañar el horario comercial diurno, mientras que la nueva ola de robos con intimidación podría mostrar un desplazamiento hacia la pre-noche o madrugada.

## 2. El Perfil Sociodemográfico del Victimario
*(Metodología: Microdatos de la tabla `cch.detenidos` en las 102 comunas de estudio, filtrado por Violento vs No Violento).*

El segundo archivo generado (`perfil_detenidos_cch.xlsx`) aborda directamente la Hipótesis 2 ("Cambio Composicional del victimario"). Al tabular exhaustivamente por año y tipo de violencia, el libro de Excel destraba cuatro dimensiones sociológicas formales de los aprehendidos:

* **Por_Sexo (`id_sexo`):** El análisis de masculinidad hegemónica en el delito patrimonial. ¿La participación de mujeres infractoras en delitos *violentos* ha aumentado o sigue acotada al hurto tradicional?
* **Por_Edad (`id_tramo_etario`):** La curva de maduración criminal. Revela si la crisis post-pandemia de violencia patrimonial es empujada estadísticamente por cohortes juveniles más prematuras o infractores adultos reincidentes.
* **Por_Nacionalidad (`id_nacionalidad`):** Una variable crítica en política pública contemporánea (la llamada "migración delictual"). El cruce demuestra empíricamente, más allá de la percepción, el peso real poblacional de imputados extranjeros en la torta de los delitos violentos frente a la base nacional tradicional.
* **Por_Estado_Civil (`id_estado_civil`):** El factor de arraigo.

**Conclusión Operativa:** Estos dos inputs explorativos nos dotan de todo el mapa empírico necesario de Carabineros para fundamentar las narrativas de los Modelos Econométricos (Tanto el Modelo 1 de Volumen y Choques Temporales, como el Modelo 2 Logit Binomial sociodemográfico). La carpeta queda estandarizada y lista para la fase pre-modelamiento.
