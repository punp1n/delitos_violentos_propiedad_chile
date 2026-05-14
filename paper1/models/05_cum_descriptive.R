###############################################################################
# 05_cum_descriptive.R — Análisis descriptivo por CUM dentro de categorías C3
# Proyecto v5.0: Cambio Estructural en Delitos Violentos contra la Propiedad
#
# Objetivo: Desagregar los conteos y tasas de cada CUM individual que compone
# cada categoría C3 (Robos violentos / Robos por sorpresa / Robos no violentos),
# mostrando su contribución relativa y evolución por período.
#
# Outputs:
#   paper1/output/tables/C3/tabla_cum_robos_violentos.csv
#   paper1/output/tables/C3/tabla_cum_robos_sorpresa.csv
#   paper1/output/tables/C3/tabla_cum_robos_no_violentos.csv
#   paper1/output/tables/C3/tabla_cum_comparacion_periodos.csv
#   paper1/output/figures/fig_cum_contribucion_c3.png
#   paper1/output/figures/fig_cum_serie_violentos.png
###############################################################################

suppressPackageStartupMessages({
  library(arrow)
  library(dplyr)
  library(tidyr)
  library(ggplot2)
  library(scales)
  library(readr)
})

# ── Directorios ──────────────────────────────────────────────────────────────
dir_data   <- "paper1/output/data"
dir_tables <- "paper1/output/tables/C3"
dir_figs   <- "paper1/output/figures"
dir.create(dir_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(dir_figs,   recursive = TRUE, showWarnings = FALSE)

cat("=== 05_cum_descriptive.R ===\n\n")

# ── 1. Cargar datos CUM-nivel (comunas × mes) ─────────────────────────────
cat("Cargando datos CUM-nivel...\n")
cch_cum <- read_parquet(file.path(dir_data, "cch_panel_comuna_month.parquet"))

cat("  Dimensiones raw:", nrow(cch_cum), "x", ncol(cch_cum), "\n")
cat("  Años disponibles:", min(cch_cum$year), "-", max(cch_cum$year), "\n")
cat("  CUMs únicos en C3:", length(unique(cch_cum$cum[!is.na(cch_cum$C3_categoria)])), "\n\n")

# ── 2. Cargar denominadores poblacionales ─────────────────────────────────
cat("Cargando población...\n")
pop <- read_csv(file.path(dir_data, "poblacion_regional_mensual.csv"),
                show_col_types = FALSE) |>
  group_by(year) |>
  summarise(pop_nacional = sum(pop_monthly) / 12, .groups = "drop")

# ── 3. Filtrar C3 y agregar a nivel nacional × año × CUM ─────────────────
cat("Agregando denuncias por CUM × año (solo C3)...\n")

c3_anual <- cch_cum |>
  filter(!is.na(C3_categoria)) |>
  group_by(C3_categoria, cum, glosa_cum, year) |>
  summarise(n_denuncias = sum(n_denuncias, na.rm = TRUE), .groups = "drop") |>
  left_join(pop, by = "year") |>
  mutate(
    tasa_100k = n_denuncias / pop_nacional * 1e5,
    periodo = case_when(
      year %in% 2013:2015 ~ "Pre-base",
      year %in% 2016:2019 ~ "Línea base",
      year %in% 2019:2019 & FALSE ~ NA_character_,   # placeholder
      year == 2020 ~ "COVID-init",
      year %in% 2020:2021 ~ "Pandemia",
      year %in% 2022:2025 ~ "Post-pandemia",
      TRUE ~ as.character(year)
    )
  )

# Definición limpia de períodos
c3_anual <- c3_anual |>
  mutate(
    periodo = case_when(
      year %in% 2013:2015 ~ "Pre-base (2013-2015)",
      year %in% 2016:2019 ~ "Línea base (2016-2019)",
      year %in% 2020:2021 ~ "Pandemia (2020-2021)",
      year %in% 2022:2025 ~ "Post-pandemia (2022-2025)",
      TRUE ~ as.character(year)
    )
  )

# ── 4. Tabla por períodos: CUM × período ──────────────────────────────────
cat("Construyendo tabla comparativa por períodos...\n")

tabla_periodos <- c3_anual |>
  group_by(C3_categoria, cum, glosa_cum, periodo) |>
  summarise(
    n_total    = sum(n_denuncias),
    tasa_media = mean(tasa_100k),
    .groups = "drop"
  ) |>
  pivot_wider(
    names_from  = periodo,
    values_from = c(n_total, tasa_media),
    values_fill = 0
  )

write_csv(tabla_periodos,
          file.path(dir_tables, "tabla_cum_comparacion_periodos.csv"))
cat("  Guardado: tabla_cum_comparacion_periodos.csv\n")

# ── 5. Tabla detalle por categoría C3 ─────────────────────────────────────
periodos_orden <- c("Pre-base (2013-2015)", "Línea base (2016-2019)",
                    "Pandemia (2020-2021)", "Post-pandemia (2022-2025)")

make_cum_table <- function(cat_c3, label) {
  df <- c3_anual |>
    filter(C3_categoria == cat_c3) |>
    group_by(cum, glosa_cum, periodo) |>
    summarise(n_total = sum(n_denuncias), tasa = mean(tasa_100k), .groups = "drop")

  # Calcular totales por CUM (para ordenar)
  totales <- df |> group_by(cum, glosa_cum) |> summarise(n_grand = sum(n_total), .groups = "drop") |>
    arrange(desc(n_grand))

  # Variación línea base → post-pandemia
  var_df <- df |>
    filter(periodo %in% c("Línea base (2016-2019)", "Pandemia (2020-2021)", "Post-pandemia (2022-2025)")) |>
    select(cum, periodo, tasa) |>
    pivot_wider(names_from = periodo, values_from = tasa, values_fill = 0) |>
    rename(tasa_base_normal = `Línea base (2016-2019)`,
           tasa_base_pandemia = `Pandemia (2020-2021)`,
           tasa_post = `Post-pandemia (2022-2025)`) |>
    mutate(
      tasa_base = ifelse(cum == 867, tasa_base_pandemia, tasa_base_normal),
      cambio_pct = ifelse(tasa_base > 0,
                               (tasa_post - tasa_base) / tasa_base * 100, NA_real_)
    )

  # Pivot wide
  df_wide <- df |>
    pivot_wider(names_from = periodo, values_from = c(n_total, tasa), values_fill = 0) |>
    left_join(var_df |> select(cum, cambio_pct), by = "cum") |>
    left_join(totales, by = c("cum", "glosa_cum")) |>
    arrange(desc(n_grand))

  # Calcular participación dentro del grupo
  total_cat <- sum(df$n_total)
  df_wide <- df_wide |>
    mutate(
      pct_grupo = round(n_grand / total_cat * 100, 1),
      cambio_pct = round(cambio_pct, 1)
    )

  cat(sprintf("  [%s] %d CUMs, %s denuncias totales 2013-2025\n",
              label, nrow(df_wide), format(total_cat, big.mark = ".")))

  df_wide
}

tbl_violentos   <- make_cum_table("Violencia Dura", "Robos violentos")
tbl_sorpresa    <- make_cum_table("Sorpresa",       "Robos por sorpresa")
tbl_no_violento <- make_cum_table("No Violento",    "Robos no violentos")

write_csv(tbl_violentos,   file.path(dir_tables, "tabla_cum_robos_violentos.csv"))
write_csv(tbl_sorpresa,    file.path(dir_tables, "tabla_cum_robos_sorpresa.csv"))
write_csv(tbl_no_violento, file.path(dir_tables, "tabla_cum_robos_no_violentos.csv"))
cat("  Guardadas tablas por categoría.\n\n")

# ── 6. Tabla resumen limpia (para paper) ──────────────────────────────────
cat("Construyendo tabla resumen para paper...\n")

resumen_paper <- c3_anual |>
  group_by(C3_categoria, cum, glosa_cum, periodo) |>
  summarise(n = sum(n_denuncias), tasa = mean(tasa_100k), .groups = "drop") |>
  filter(periodo %in% periodos_orden) |>
  group_by(C3_categoria, cum, glosa_cum) |>
  summarise(
    n_total_2013_2025 = sum(n),
    tasa_base = if (cum[1] == 867) sum(tasa[periodo == "Pandemia (2020-2021)"]) else sum(tasa[periodo == "Línea base (2016-2019)"]),
    tasa_post = sum(tasa[periodo == "Post-pandemia (2022-2025)"]),
    cambio_pct = if_else(tasa_base > 0, round((tasa_post - tasa_base) / tasa_base * 100, 1), NA_real_),
    .groups = "drop"
  ) |>
  group_by(C3_categoria) |>
  mutate(pct_grupo = round(n_total_2013_2025 / sum(n_total_2013_2025) * 100, 1)) |>
  ungroup() |>
  arrange(C3_categoria, desc(n_total_2013_2025))

write_csv(resumen_paper, file.path(dir_tables, "tabla_cum_resumen_paper.csv"))
cat("  Guardado: tabla_cum_resumen_paper.csv\n\n")

# ── 7. Figura: contribución por CUM dentro de C3 ─────────────────────────
cat("Generando figuras...\n")

# Serie anual por CUM dentro de Robos violentos
series_violentos <- c3_anual |>
  filter(C3_categoria == "Violencia Dura") |>
  mutate(glosa_corta = case_when(
    cum == 802 ~ "Robo c/intimidación (802)",
    cum == 803 ~ "Robo c/violencia (803)",
    cum == 827 ~ "Robo c/homicidio (827)",
    cum == 828 ~ "Robo c/violación (828)",
    cum == 829 ~ "Robo c/castración (829)",
    cum == 861 ~ "Robo c/lesiones graves (861)",
    cum == 862 ~ "Robo c/retención (862)",
    cum == 867 ~ "Robo vehículo-violencia (867)",
    TRUE ~ paste0(cum, ": ", substr(glosa_cum, 1, 25))
  )) |>
  group_by(cum, glosa_corta) |>
  mutate(n_total_cum = sum(n_denuncias)) |>
  ungroup() |>
  mutate(glosa_corta = reorder(glosa_corta, -n_total_cum))

fig_violentos <- ggplot(series_violentos,
       aes(x = year, y = tasa_100k, color = glosa_corta, group = glosa_corta)) +
  geom_line(linewidth = 0.8) +
  geom_point(size = 1.5) +
  geom_vline(xintercept = c(2019.75, 2022), linetype = "dashed",
             color = c("orange", "steelblue"), alpha = 0.7) +
  annotate("text", x = 2019.6, y = Inf, label = "Estallido",
           hjust = 1, vjust = 1.5, size = 3, color = "orange") +
  annotate("text", x = 2022.1, y = Inf, label = "Post-COVID",
           hjust = 0, vjust = 1.5, size = 3, color = "steelblue") +
  scale_x_continuous(breaks = 2013:2025) +
  scale_color_brewer(palette = "Dark2") +
  labs(
    title    = "Tasas anuales por CUM — Robos violentos (C3.1)",
    subtitle = "Tasa por 100.000 hab. (población corregida SERMIG)",
    x = NULL, y = "Tasa por 100.000 hab.",
    color = "CUM"
  ) +
  theme_minimal(base_size = 11) +
  theme(
    legend.position  = "right",
    legend.text      = element_text(size = 8),
    axis.text.x      = element_text(angle = 45, hjust = 1),
    panel.grid.minor = element_blank()
  )

ggsave(file.path(dir_figs, "fig_cum_serie_violentos.png"),
       fig_violentos, width = 14, height = 6, dpi = 150)
ggsave(file.path(dir_figs, "fig_cum_serie_violentos.pdf"),
       fig_violentos, width = 14, height = 6)

# Figura 2: Contribución % por CUM dentro de cada categoría C3 (barras apiladas)
contrib_data <- c3_anual |>
  filter(periodo %in% c("Línea base (2016-2019)", "Post-pandemia (2022-2025)")) |>
  group_by(C3_categoria, cum, glosa_cum, periodo) |>
  summarise(n = sum(n_denuncias), .groups = "drop") |>
  group_by(C3_categoria, periodo) |>
  mutate(pct = n / sum(n) * 100) |>
  ungroup() |>
  mutate(
    cat_label = case_when(
      C3_categoria == "Violencia Dura" ~ "Robos violentos",
      C3_categoria == "Sorpresa"       ~ "Robos por sorpresa",
      C3_categoria == "No Violento"    ~ "Robos no violentos"
    ),
    glosa_corta = paste0(cum, ": ", substr(glosa_cum, 1, 30))
  )

fig_contrib <- ggplot(contrib_data,
       aes(x = periodo, y = pct, fill = glosa_corta)) +
  geom_col(position = "stack") +
  facet_wrap(~cat_label, scales = "free_y", ncol = 1) +
  scale_fill_viridis_d(option = "turbo") +
  labs(
    title    = "Composición por CUM dentro de cada categoría C3",
    subtitle = "% del total de denuncias en cada período",
    x = NULL, y = "% dentro del grupo",
    fill = "CUM"
  ) +
  theme_minimal(base_size = 10) +
  theme(
    legend.position  = "right",
    legend.text      = element_text(size = 7),
    strip.text       = element_text(face = "bold"),
    axis.text.x      = element_text(angle = 20, hjust = 1)
  )

ggsave(file.path(dir_figs, "fig_cum_contribucion_c3.png"),
       fig_contrib, width = 12, height = 14, dpi = 150)
ggsave(file.path(dir_figs, "fig_cum_contribucion_c3.pdf"),
       fig_contrib, width = 12, height = 14)

# ── 8. Tabla dinámica: CUM × año (nivel nacional) ─────────────────────────
cat("Generando tabla dinámica CUM × año...\n")

cum_anual_wide <- c3_anual |>
  group_by(C3_categoria, cum, glosa_cum, year) |>
  summarise(n = sum(n_denuncias), tasa = mean(tasa_100k), .groups = "drop") |>
  pivot_wider(
    names_from  = year,
    values_from = c(n, tasa),
    values_fill = 0
  ) |>
  arrange(C3_categoria, desc(rowSums(across(starts_with("n_")), na.rm = TRUE)))

write_csv(cum_anual_wide, file.path(dir_tables, "tabla_cum_anual_wide.csv"))
cat("  Guardado: tabla_cum_anual_wide.csv\n\n")

# ── 9. Resumen por consola ─────────────────────────────────────────────────
cat("=== RESUMEN CUM × C3 (Tasa media anual por 100K) ===\n\n")

resumen_print <- resumen_paper |>
  mutate(
    grupo = case_when(
      C3_categoria == "Violencia Dura" ~ "ROBOS VIOLENTOS",
      C3_categoria == "Sorpresa"       ~ "ROBOS POR SORPRESA",
      C3_categoria == "No Violento"    ~ "ROBOS NO VIOLENTOS"
    )
  ) |>
  select(grupo, cum, glosa_cum, n_total_2013_2025, pct_grupo, tasa_base, tasa_post, cambio_pct)

for (g in unique(resumen_print$grupo)) {
  cat(sprintf("\n--- %s ---\n", g))
  df_g <- resumen_print |> filter(grupo == g) |> select(-grupo)
  print(df_g, n = 30)
}

# ── 10. Análisis ratio Detenciones / Denuncias (D/D) ─────────────────────
cat("=== Análisis ratio Detenciones/Denuncias por C3 ===\n")

# Agregar detenciones por C3 × año (nivel nacional)
c3_det_anual <- cch_cum |>
  filter(!is.na(C3_categoria)) |>
  group_by(C3_categoria, year) |>
  summarise(
    n_denuncias   = sum(n_denuncias,   na.rm = TRUE),
    n_detenciones = sum(n_detenciones, na.rm = TRUE),
    .groups = "drop"
  ) |>
  mutate(
    ratio_dd = round(n_denuncias / pmax(n_detenciones, 1), 2),   # denuncias por cada detención
    cat_label = case_when(
      C3_categoria == "Violencia Dura" ~ "Robos violentos",
      C3_categoria == "Sorpresa"       ~ "Robos por sorpresa",
      C3_categoria == "No Violento"    ~ "Robos no violentos"
    )
  )

write_csv(c3_det_anual, file.path(dir_tables, "tabla_ratio_dd_c3_anual.csv"))
cat("  Guardado: tabla_ratio_dd_c3_anual.csv\n")

# Tabla resumen por período
c3_det_periodo <- c3_det_anual |>
  mutate(periodo = case_when(
    year %in% 2013:2015 ~ "Pre-base (2013-2015)",
    year %in% 2016:2019 ~ "Línea base (2016-2019)",
    year %in% 2020:2021 ~ "Pandemia (2020-2021)",
    year %in% 2022:2025 ~ "Post-pandemia (2022-2025)"
  )) |>
  group_by(C3_categoria, cat_label, periodo) |>
  summarise(
    n_den_total = sum(n_denuncias),
    n_det_total = sum(n_detenciones),
    ratio_dd    = round(n_den_total / pmax(n_det_total, 1), 2),
    .groups = "drop"
  )

write_csv(c3_det_periodo, file.path(dir_tables, "tabla_ratio_dd_c3_periodo.csv"))
cat("  Guardado: tabla_ratio_dd_c3_periodo.csv\n")

# Figura: ratio D/D por año y categoría C3
fig_dd <- ggplot(c3_det_anual, aes(x = year, y = ratio_dd, color = cat_label, group = cat_label)) +
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  geom_vline(xintercept = c(2019.75, 2022), linetype = "dashed",
             color = c("orange", "steelblue"), alpha = 0.7) +
  scale_x_continuous(breaks = 2013:2025) +
  scale_color_manual(values = c("Robos violentos"   = "#c0392b",
                                 "Robos por sorpresa" = "#e67e22",
                                 "Robos no violentos" = "#7f8c8d")) +
  labs(
    title    = "Ratio Denuncias / Detención por categoría C3",
    subtitle = "Denuncias registradas por cada detención efectuada (2013–2025)",
    x = NULL, y = "Denuncias por detención",
    color = NULL
  ) +
  theme_minimal(base_size = 11) +
  theme(
    legend.position  = "bottom",
    axis.text.x      = element_text(angle = 45, hjust = 1),
    panel.grid.minor = element_blank()
  )

ggsave(file.path(dir_figs, "fig_ratio_dd_c3.png"), fig_dd, width = 11, height = 5, dpi = 150)
ggsave(file.path(dir_figs, "fig_ratio_dd_c3.pdf"), fig_dd, width = 11, height = 5)
cat("  Guardadas figuras ratio D/D.\n\n")

# Imprimir resumen por período
cat("=== RATIO DENUNCIAS/DETENCIÓN POR PERÍODO Y CATEGORÍA ===\n")
print(c3_det_periodo |> select(cat_label, periodo, n_den_total, n_det_total, ratio_dd), n = 20)

cat("\n=== 05_cum_descriptive.R COMPLETADO ===\n")
