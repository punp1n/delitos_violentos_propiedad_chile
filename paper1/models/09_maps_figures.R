# 09_maps_figures.R — Mapas y Figuras restantes

library(dplyr)
library(arrow)
library(tidyr)
library(ggplot2)

dir.create("paper1/output/tables", showWarnings = FALSE, recursive = TRUE)
dir.create("paper1/output/figures", showWarnings = FALSE, recursive = TRUE)

message("Cargando datos para mapas y figuras restantes...")
panel <- read_parquet("paper1/output/data/panel_region_month.parquet")

# Preparamos datos del Mapa 1: Tasa de violencia dura por región 2016 vs 2024
datos_mapa <- panel %>%
  filter(year %in% c(2016, 2024)) %>%
  group_by(region, year) %>%
  summarise(
    vd = sum(n_violencia_dura),
    pop_anual = mean(pop_monthly),
    .groups = "drop"
  ) %>%
  mutate(tasa = vd / pop_anual * 100000)

datos_mapa_wide <- datos_mapa %>%
  select(-vd, -pop_anual) %>%
  pivot_wider(names_from = year, values_from = tasa, names_prefix = "tasa_") %>%
  mutate(delta_pct = (tasa_2024 - tasa_2016) / tasa_2016 * 100)

write.csv(datos_mapa_wide, "paper1/output/tables/datos_mapa_tasas_regionales.csv", row.names = FALSE)

# Simulación de ploteo dummy (ya que no se cuenta con los polígonos sf instalados)
fig_map_proxy <- ggplot(datos_mapa_wide, aes(x = reorder(factor(region), delta_pct), y = delta_pct)) +
  geom_col(fill = "steelblue") +
  coord_flip() +
  labs(title = "Cambio % en Tasa de Violencia Dura (2024 vs 2016)", x = "Región", y = "Cambio (%)") +
  theme_minimal()

ggsave("paper1/output/figures/map_proxy_delta_tasa.png", fig_map_proxy, width = 8, height = 6)

message("Listo 09_maps_figures.R")
