# 09_maps_figures.R — Mapas y Figuras restantes
# rev.3: Incorpora mapas espaciales reales (sf) para Map 1, 2 y 3.
# Modificado a tasa 2013 vs 2025.

library(dplyr)
library(arrow)
library(tidyr)
library(ggplot2)
library(sf)

dir.create("paper1/output/tables", showWarnings = FALSE, recursive = TRUE)
dir.create("paper1/output/figures", showWarnings = FALSE, recursive = TRUE)

message("Cargando datos para mapas y figuras restantes...")
panel <- read_parquet("paper1/output/data/panel_region_month.parquet")

# Leer Shapefile de Regiones
shp <- st_read("data/Regiones_espacial/Regional.shp", quiet = TRUE)
# Normalizar nombres para join: en el shp es codregion
shp <- shp %>% dplyr::rename(region = codregion)

# ---------------------------------------------------------
# Mapa principal: Log-ratio de tasas (línea base 2016-2019 vs período reciente 2022-2025)
# El log-ratio captura el cambio proporcional por región, evitando el colapso de
# colores que ocurre con tasas absolutas cuando las diferencias inter-período son
# menores a 100 por 100.000 hab.
# ---------------------------------------------------------
datos_lr <- panel %>%
  filter(
    (year >= 2016 & year <= 2019) | (year >= 2022 & year <= 2025)
  ) %>%
  mutate(
    period_lr = if_else(year <= 2019, "base_2016_2019", "reciente_2022_2025")
  ) %>%
  group_by(region, period_lr, year) %>%
  summarise(
    vd_anual  = sum(n_robos_violentos),
    pop_anual = mean(pop_monthly),
    .groups   = "drop"
  ) %>%
  group_by(region, period_lr) %>%
  summarise(
    tasa = mean(vd_anual / pop_anual * 100000),
    .groups = "drop"
  ) %>%
  pivot_wider(names_from = period_lr, values_from = tasa) %>%
  mutate(
    log_ratio  = log(reciente_2022_2025 / base_2016_2019),
    delta_pct  = (reciente_2022_2025 - base_2016_2019) / base_2016_2019 * 100
  )

write.csv(datos_lr, "paper1/output/tables/datos_mapa_logratio_regional.csv", row.names = FALSE)

bbox_chile <- coord_sf(xlim = c(-8500000, -7300000), ylim = c(-7600000, -1900000))

# Unir con shapefile
map_lr_sf <- shp %>% left_join(datos_lr, by = "region")

# --- Mapa principal: Log-ratio (figura en §3.1 del artículo) ---
lim_abs <- max(abs(map_lr_sf$log_ratio), na.rm = TRUE) * 1.05

map_logratio <- ggplot(map_lr_sf) +
  geom_sf(aes(fill = log_ratio), color = "black", linewidth = 0.3) +
  bbox_chile +
  scale_fill_gradient2(
    low      = "#2166ac",
    mid      = "#f7f7f7",
    high     = "#d6604d",
    midpoint = 0,
    limits   = c(-lim_abs, lim_abs),
    name     = "Cambio relativo\n(log-ratio 2022\u20132025\nvs. 2016\u20132019)",
    labels   = function(x) sprintf("%+.2f", x)
  ) +
  theme_void(base_family = "sans", base_size = 12) +
  theme(
    legend.position      = "right",
    legend.title         = element_text(size = 9, face = "bold", lineheight = 1.2),
    legend.text          = element_text(size = 8),
    legend.key.height    = unit(2.0, "cm"),
    legend.key.width     = unit(0.5, "cm"),
    plot.margin          = margin(5, 5, 5, 5)
  ) +
  guides(fill = guide_colorbar(title.position = "top", title.hjust = 0.5,
                               barheight = unit(6, "cm")))

ggsave("paper1/output/figures/map_logratio_regional.png", map_logratio,
       width = 7, height = 9, dpi = 300)
ggsave("paper1/output/figures/map_logratio_regional.pdf", map_logratio,
       width = 7, height = 9)

# English version for log-ratio map
map_logratio_eng <- ggplot(map_lr_sf) +
  geom_sf(aes(fill = log_ratio), color = "black", linewidth = 0.3) +
  bbox_chile +
  scale_fill_gradient2(
    low      = "#2166ac",
    mid      = "#f7f7f7",
    high     = "#d6604d",
    midpoint = 0,
    limits   = c(-lim_abs, lim_abs),
    name     = "Relative change\n(log-ratio 2022\u20132025\nvs. 2016\u20132019)",
    labels   = function(x) sprintf("%+.2f", x)
  ) +
  theme_void(base_family = "sans", base_size = 12) +
  theme(
    legend.position      = "right",
    legend.title         = element_text(size = 9, face = "bold", lineheight = 1.2),
    legend.text          = element_text(size = 8),
    legend.key.height    = unit(2.0, "cm"),
    legend.key.width     = unit(0.5, "cm"),
    plot.margin          = margin(5, 5, 5, 5)
  ) +
  guides(fill = guide_colorbar(title.position = "top", title.hjust = 0.5,
                               barheight = unit(6, "cm")))

ggsave("paper1/output/figures/map_logratio_regional_eng.png", map_logratio_eng,
       width = 7, height = 9, dpi = 300)
ggsave("paper1/output/figures/map_logratio_regional_eng.pdf", map_logratio_eng,
       width = 7, height = 9)

# --- Mapa de referencia: Cambio porcentual (auxiliar, no en texto principal) ---
map_data_sp <- panel %>%
  mutate(
    period_map = case_when(
      year >= 2013 & year <= 2016 ~ "Spline1_2013_2016",
      year >= 2022 & year <= 2025 ~ "Spline4_2022_2025",
      TRUE ~ NA_character_
    )
  ) %>%
  filter(!is.na(period_map)) %>%
  group_by(region, period_map, year) %>%
  summarise(vd_anual = sum(n_robos_violentos), pop_anual = mean(pop_monthly), .groups = "drop") %>%
  group_by(region, period_map) %>%
  summarise(tasa_promedio = mean(vd_anual / pop_anual * 100000), .groups = "drop") %>%
  pivot_wider(names_from = period_map, values_from = tasa_promedio, names_prefix = "tasa_") %>%
  mutate(delta_pct = (tasa_Spline4_2022_2025 - tasa_Spline1_2013_2016) / tasa_Spline1_2013_2016 * 100)

write.csv(map_data_sp, "paper1/output/tables/datos_mapa_tasas_regionales.csv", row.names = FALSE)

map_data_sp_sf <- shp %>% left_join(map_data_sp, by = "region")

map_2 <- ggplot(map_data_sp_sf) +
  geom_sf(aes(fill = delta_pct), color = "black", linewidth = 0.3) +
  bbox_chile +
  scale_fill_gradient2(low = "#2c7fb8", mid = "#ffffbf", high = "#e34a33",
                       midpoint = 0, name = "Cambio (%) Spline 1 vs Spline 4") +
  theme_void(base_family = "sans", base_size = 12) +
  theme(legend.position = "bottom", legend.key.width = unit(1.5, "cm"))

ggsave("paper1/output/figures/map2_cambio_porcentual.png", map_2, width = 6, height = 8, dpi = 300)
ggsave("paper1/output/figures/map2_cambio_porcentual.pdf", map_2, width = 6, height = 8)

message("Mapa log-ratio exportado: map_logratio_regional.pdf/png")

message("Listo 09_maps_figures.R")
