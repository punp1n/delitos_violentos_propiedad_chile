# 05_enusc_triangulation.R — Triangulación con ENUSC

library(dplyr)
library(arrow)
library(survey)
library(tidyr)

dir.create("paper1/output/tables", showWarnings = FALSE, recursive = TRUE)

message("Cargando microdatos ENUSC...")
enusc_micro <- read_parquet("paper1/output/data/enusc_microdata_filtered.parquet")
# Corregir problema de encoding en el nombre de la columna año (índice 1 que es "ao")
names(enusc_micro)[1] <- "ano"

message("Configurando diseño muestral complejo...")
options(survey.lonely.psu = "adjust")
options(survey.adjust.domain.lonely = TRUE)
des <- svydesign(
  ids = ~conglomerado,
  strata = ~varstrat,
  weights = ~weight,
  data = enusc_micro,
  nest = TRUE
)

message("Calculando prevalencia anual por región...")
prev_violent <- svyby(~victim_violent, ~region16 + ano, des, svymean, na.rm = TRUE)
prev_hard <- svyby(~victim_hard, ~region16 + ano, des, svymean, na.rm = TRUE)

# Renombrar columnas para merge y usar svytotal para el denominador del ratio
victimas_exp <- svyby(~victim_violent, ~region16 + ano, des, svytotal, na.rm = TRUE)
victimas_exp <- victimas_exp %>%
  rename(region = region16, year = ano, victim_violent = victim_violent, se_victim_violent = se)

message("Calculando índice relativo de propensión a denunciar...")
panel_comuna <- read_parquet("paper1/output/data/cch_panel_comuna_month.parquet")

# Leer comunas 102
comunas_102_df <- read.csv("data/ENUSC/comunas_102_historicas.csv")
if("codigo" %in% names(comunas_102_df)) {
  comunas_102 <- comunas_102_df$codigo
} else {
  comunas_102 <- comunas_102_df[[1]]
}

# Filtrar denuncias a las 102 comunas y solo delitos violentos equivalentes a ENUSC 
denuncias_102 <- panel_comuna %>%
  filter(comuna %in% comunas_102, C3_categoria %in% c("Violencia Dura", "Sorpresa")) %>%
  group_by(region, year) %>%
  summarise(n_denuncias_102 = sum(n_denuncias), .groups = "drop")

# Merge
indice <- merge(denuncias_102, victimas_exp, by = c("region", "year"))
indice$ratio <- indice$n_denuncias_102 / indice$victim_violent

indice <- indice %>%
  group_by(region) %>%
  mutate(
    base_ratio = if(any(year == 2016)) ratio[year == 2016][1] else ratio[which.min(year)],
    indice_rel = ratio / base_ratio
  ) %>%
  ungroup()

# CIs by Delta Method
indice$se_ratio <- indice$ratio * (indice$se_victim_violent / indice$victim_violent)
indice$ci_lower <- indice$ratio - 1.96 * indice$se_ratio
indice$ci_upper <- indice$ratio + 1.96 * indice$se_ratio

# Componente cualitativo (Tabla 5 proxy)
message("Generando tabla de tendencias cualitativas...")
tendencias <- indice %>%
  mutate(periodo = case_when(
    year >= 2016 & year <= 2019 ~ "Pre",
    year >= 2022 & year <= 2024 ~ "Post",
    TRUE ~ NA_character_
  )) %>%
  filter(!is.na(periodo)) %>%
  group_by(region, periodo) %>%
  summarise(
    mean_denuncias = mean(n_denuncias_102),
    mean_victimas = mean(victim_violent),
    .groups = "drop"
  ) %>%
  pivot_wider(names_from = periodo, values_from = c(mean_denuncias, mean_victimas)) %>%
  mutate(
    delta_denuncias = (mean_denuncias_Post - mean_denuncias_Pre) / mean_denuncias_Pre,
    delta_victimas = (mean_victimas_Post - mean_victimas_Pre) / mean_victimas_Pre,
    dir_denuncias = case_when(delta_denuncias > 0.1 ~ "↑", delta_denuncias < -0.1 ~ "↓", TRUE ~ "→"),
    dir_victimas = case_when(delta_victimas > 0.1 ~ "↑", delta_victimas < -0.1 ~ "↓", TRUE ~ "→")
  )

write.csv(prev_violent, "paper1/output/tables/tabla_4_enusc_prevalencia.csv", row.names = FALSE)
write.csv(indice, "paper1/output/tables/tabla_5a_indice_relativo.csv", row.names = FALSE)
write.csv(tendencias, "paper1/output/tables/tabla_5b_convergencia.csv", row.names = FALSE)

message("Resultados guardados en tabla_4 y tabla_5")
