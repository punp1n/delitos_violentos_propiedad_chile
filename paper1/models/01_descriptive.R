# 01_descriptive.R — Modelos v4.0: Descriptivos y Series Temporales

library(dplyr)
library(arrow)
library(ggplot2)
library(tidyr)
library(lubridate)
library(stringr)

# -- Creacion de subcarpetas en outputs también
dir.create("paper1/output/tables/C3", showWarnings = FALSE, recursive = TRUE)
dir.create("paper1/output/tables/C1", showWarnings = FALSE, recursive = TRUE)
dir.create("paper1/output/tables/C2", showWarnings = FALSE, recursive = TRUE)

message("Cargando datos...")
panel <- read_parquet("paper1/output/data/panel_region_month.parquet") %>%
  mutate(date = make_date(year, month, 1))
pop_nacional <- read.csv("paper1/output/data/poblacion_nacional_mensual_base2024.csv") %>%
  group_by(year) %>%
  summarise(pop_nacional_base2024 = mean(pop_nacional_base2024), .groups="drop")

message("Generando Tabla 1...")
panel_periods <- panel %>%
  mutate(
    periodo = case_when(
      year <= 2015 ~ "Pre-Línea Base (2013-2015)",
      year >= 2016 & year <= 2019 & (year < 2019 | month <= 9) ~ "Línea Base (2016-Sep 2019)",
      (year == 2019 & month >= 10) | (year == 2020 & month <= 2) ~ "Estallido Social (Oct 2019-Feb 2020)",
      (year == 2020 & month >= 3) | (year == 2021) ~ "Pandemia (Mar 2020-Dic 2021)",
      year >= 2022 ~ "Pandemia Post (2022-2025)",
      TRUE ~ "Otro"
    ),
    tasa_vd = n_robos_violentos / pop_monthly * 100000,
    tasa_c1 = n_violento_c1 / pop_monthly * 100000,
    tasa_c2 = n_violento_c2 / pop_monthly * 100000,
    tasa_sorpresa = n_robos_sorpresa / pop_monthly * 100000,
    tasa_nv = n_robos_no_violentos / pop_monthly * 100000
  )

tabla_1 <- panel_periods %>%
  group_by(periodo) %>%
  summarise(
    meses_n = n_distinct(date),
    vd_media = mean(n_robos_violentos),
    vd_sd = sd(n_robos_violentos),
    vd_tasa_media = mean(tasa_vd),
    sorpresa_media = mean(n_robos_sorpresa),
    sorpresa_sd = sd(n_robos_sorpresa),
    sorpresa_tasa_media = mean(tasa_sorpresa),
    nv_media = mean(n_robos_no_violentos),
    nv_sd = sd(n_robos_no_violentos),
    nv_tasa_media = mean(tasa_nv),
    c1_media = mean(n_violento_c1),
    c1_sd = sd(n_violento_c1),
    c1_tasa_media = mean(tasa_c1),
    c2_media = mean(n_violento_c2),
    c2_sd = sd(n_violento_c2),
    c2_tasa_media = mean(tasa_c2)
  )

write.csv(tabla_1, "paper1/output/tables/C3/tabla_1_descriptivos_periodo.csv", row.names = FALSE)
message("Generando Figura 1...")

nacional_mensual <- panel %>%
  group_by(date, year, month) %>%
  summarise(
    Robos_violentos = sum(n_robos_violentos),
    Robos_por_sorpresa = sum(n_robos_sorpresa),
    Robos_no_violentos = sum(n_robos_no_violentos),
    d_estallido = max(d_estallido),
    d_pandemia = max(d_pandemia),
    .groups = "drop"
  ) %>%
  pivot_longer(
    cols = c(Robos_violentos, Robos_por_sorpresa, Robos_no_violentos),
    names_to = "Categoria",
    values_to = "Denuncias"
  )

# --- Aesthetics configuration ---
academic_colors <- c(
  "Robos_violentos" = "#e34a33", # Rojo/naranja oscuro
  "Robos_por_sorpresa" = "#fdbb84", # Naranja claro
  "Robos_no_violentos" = "#2c7fb8" # Azul profesional
)

# Rectángulos para sombreados en leyenda
rect_data <- data.frame(
  xmin = as.Date(c("2019-10-01", "2020-03-01")),
  xmax = as.Date(c("2020-02-28", "2021-12-31")),
  ymin = -Inf, ymax = Inf,
  Periodo = factor(c("Estallido Social", "Pandemia"), levels = c("Estallido Social", "Pandemia"))
)

# Líneas verticales elegentes para los shocks en lugar de rectángulos pesados
fig_1 <- ggplot(nacional_mensual, aes(x = date, y = Denuncias)) +
  # Bandas sutiles para los shocks mapeadas a fill
  geom_rect(data = rect_data, aes(xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax, fill = Periodo), inherit.aes = FALSE, alpha = 0.5) +
  # Líneas guías
  geom_vline(xintercept = as.Date("2019-10-01"), linetype = "dotted", color = "#969696", linewidth = 0.8) +
  geom_vline(xintercept = as.Date("2020-03-01"), linetype = "dotted", color = "#969696", linewidth = 0.8) +
  # Texto de anotación
  annotate("text", x = as.Date("2019-12-15"), y = max(nacional_mensual$Denuncias) * 0.9, label = "Estallido", angle = 90, size = 3.5, color = "#525252") +
  annotate("text", x = as.Date("2021-01-01"), y = max(nacional_mensual$Denuncias) * 0.9, label = "Pandemia", angle = 0, size = 3.5, color = "#525252") +
  # Series
  geom_line(aes(color = Categoria), linewidth = 1.2, alpha = 0.85) +
  scale_fill_manual(name = "Contexto", values = c("Estallido Social" = "#cccccc", "Pandemia" = "#e6e6e6")) +
  scale_color_manual(name = "Delito", values = academic_colors, labels = c("Robos no violentos", "Robos por sorpresa", "Robos violentos")) +
  theme_minimal(base_family = "sans", base_size = 12) +
  labs(
    title = NULL,
    subtitle = NULL,
    x = NULL,
    y = "Denuncias"
  ) +
  theme(
    legend.position = "bottom",
    legend.box = "vertical",
    legend.text = element_text(size = 11, color = "black"),
    plot.title = element_blank(),
    plot.subtitle = element_blank(),
    panel.grid.minor = element_blank(),
    panel.grid.major.x = element_blank(),
    axis.line.x = element_line(color = "black", linewidth = 0.3),
    axis.ticks.x = element_line(color = "black", linewidth = 0.3)
  )

ggsave("paper1/output/figures/fig1_serie_mensual_nacional.png", fig_1, width = 10, height = 5.5, dpi = 300)
ggsave("paper1/output/figures/fig1_serie_mensual_nacional.pdf", fig_1, width = 10, height = 5.5)

# --- Fig 2: Tasas por 100K hab. anuales ---
message("Generando Figura 2...")

nacional_anual <- panel %>%
  group_by(year) %>%
  summarise(
    vd = sum(n_robos_violentos),
    sorpresa = sum(n_robos_sorpresa),
    nv = sum(n_robos_no_violentos),
    .groups = "drop"
  ) %>%
  left_join(pop_nacional, by = "year") %>%
  rename(pop_nacional = pop_nacional_base2024) %>%
  mutate(
    Tasa_Robos_violentos = vd / pop_nacional * 100000,
    Tasa_Robos_por_sorpresa = sorpresa / pop_nacional * 100000,
    Tasa_Robos_no_violentos = nv / pop_nacional * 100000
  )

# Extraer línea de referencia 2013 o 2016 (Usaremos 2016 para el benchmark del estallido)
ref_2016_vd <- nacional_anual %>%
  filter(year == 2016) %>%
  pull(Tasa_Robos_violentos)
ref_2016_sorpresa <- nacional_anual %>%
  filter(year == 2016) %>%
  pull(Tasa_Robos_por_sorpresa)
ref_2016_nv <- nacional_anual %>%
  filter(year == 2016) %>%
  pull(Tasa_Robos_no_violentos)

nacional_anual_long <- nacional_anual %>%
  select(year, Tasa_Robos_violentos, Tasa_Robos_por_sorpresa, Tasa_Robos_no_violentos) %>%
  pivot_longer(
    cols = starts_with("Tasa_"),
    names_to = "Categoria",
    values_to = "Tasa"
  ) %>%
  mutate(Categoria = str_replace(Categoria, "Tasa_", ""))

fig_2 <- ggplot(nacional_anual_long, aes(x = year, y = Tasa, color = Categoria)) +
  geom_line(linewidth = 1.2, alpha = 0.8) +
  geom_point(size = 2.5) +
  # Lineas de referencia 2016 con dataframe dummy para evitar warning de aesthetics
  geom_segment(data = data.frame(year = 2013), aes(x = 2013, xend = 2025, y = ref_2016_vd, yend = ref_2016_vd), color = "#e34a33", linetype = "22", alpha = 0.4, inherit.aes = FALSE) +
  geom_segment(data = data.frame(year = 2013), aes(x = 2013, xend = 2025, y = ref_2016_sorpresa, yend = ref_2016_sorpresa), color = "#fdbb84", linetype = "22", alpha = 0.4, inherit.aes = FALSE) +
  geom_segment(data = data.frame(year = 2013), aes(x = 2013, xend = 2025, y = ref_2016_nv, yend = ref_2016_nv), color = "#2c7fb8", linetype = "22", alpha = 0.4, inherit.aes = FALSE) +
  scale_color_manual(name = "Categoría", values = academic_colors, labels = c("Robos no violentos", "Robos por sorpresa", "Robos violentos")) +
  scale_x_continuous(breaks = 2013:2025) +
  theme_minimal(base_family = "sans", base_size = 12) +
  labs(
    title = NULL,
    subtitle = NULL,
    x = NULL,
    y = "Tasa (x 100.000 hab.)",
  ) +
  theme(
    legend.position = "bottom",
    plot.title = element_blank(),
    plot.subtitle = element_blank(),
    panel.grid.minor = element_blank(),
    panel.grid.major.x = element_blank(),
    axis.line.x = element_line(color = "black", linewidth = 0.3)
  )

ggsave("paper1/output/figures/fig2_tasa_anual_nacional.png", fig_2, width = 10, height = 5.5, dpi = 300)
ggsave("paper1/output/figures/fig2_tasa_anual_nacional.pdf", fig_2, width = 10, height = 5.5)

# --- Fig 3: Ratio mensual Violentos / Total ---
message("Generando Figura 3: Ratio mensual de Violencia Dura...")
nacional_ratio <- nacional_mensual %>%
  pivot_wider(names_from = Categoria, values_from = Denuncias) %>%
  mutate(
    Total = Robos_violentos + Robos_por_sorpresa + Robos_no_violentos,
    Ratio_VD = Robos_violentos / Total
  )

nacional_ratio_long <- nacional_ratio %>%
  select(date, Ratio_VD)

# Extraemos el trend suavizado con LOESS
fig_3 <- ggplot() +
  geom_rect(data = rect_data, aes(xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax, fill = Periodo), inherit.aes = FALSE, alpha = 0.5) +
  geom_vline(xintercept = as.Date("2015-04-01"), linetype = "dashed", color = "#252525", linewidth = 0.7) +
  geom_vline(xintercept = as.Date("2017-08-01"), linetype = "dashed", color = "#252525", linewidth = 0.7) +
  geom_vline(xintercept = as.Date("2019-10-01"), linetype = "dashed", color = "#252525", linewidth = 0.7) +
  geom_vline(xintercept = as.Date("2024-01-01"), linetype = "dashed", color = "#252525", linewidth = 0.7) +
  annotate("text", x = as.Date("2015-04-01"), y = 0.12, label = "Q1 (Abr 15)", angle = 90, vjust = -0.5, size = 3.5, color = "#252525") +
  annotate("text", x = as.Date("2017-08-01"), y = 0.12, label = "Q2 (Ago 17)", angle = 90, vjust = -0.5, size = 3.5, color = "#252525") +
  annotate("text", x = as.Date("2019-10-01"), y = 0.12, label = "Q3 (Oct 19)", angle = 90, vjust = -0.5, size = 3.5, color = "#252525") +
  annotate("text", x = as.Date("2024-01-01"), y = 0.12, label = "Q4 (Ene 24)", angle = 90, vjust = -0.5, size = 3.5, color = "#252525") +
  geom_line(data = nacional_ratio_long, aes(x = date, y = Ratio_VD, color = "Serie Original"), linewidth = 0.7) +
  geom_smooth(data = nacional_ratio_long, aes(x = date, y = Ratio_VD, color = "Tendencia (LOESS)"), method = "loess", span = 0.2, fill = "#fee0d2", linewidth = 1.2, alpha = 0.5) +
  scale_fill_manual(name = "Contexto", values = c("Estallido Social" = "#cccccc", "Pandemia" = "#e6e6e6")) +
  scale_color_manual(name = "Estimación", values = c("Serie Original" = "#bdbdbd", "Tendencia (LOESS)" = "#de2d26")) +
  scale_y_continuous(
    labels = scales::percent_format(accuracy = 1),
    limits = c(0, NA),
    expand = expansion(mult = c(0, 0.05))
  ) +
  theme_minimal(base_size = 12) +
  labs(
    title = NULL,
    subtitle = NULL,
    x = NULL,
    y = "Participación Relativa (%)"
  ) +
  theme(
    legend.position = "bottom",
    legend.box = "vertical",
    plot.title = element_blank(),
    plot.subtitle = element_blank(),
    panel.grid.minor = element_blank(),
    panel.grid.major.x = element_blank(),
    axis.line.x = element_line(color = "black", linewidth = 0.3)
  )

ggsave("paper1/output/figures/fig3_ratio_violentos_mensual.png", fig_3, width = 10, height = 5.5, dpi = 300)
ggsave("paper1/output/figures/fig3_ratio_violentos_mensual.pdf", fig_3, width = 10, height = 5.5)

# --- Generar Figuras en Inglés ---

# Fig 1 English
fig_1_eng <- ggplot(nacional_mensual, aes(x = date, y = Denuncias)) +
  geom_rect(data = rect_data, aes(xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax, fill = Periodo), inherit.aes = FALSE, alpha = 0.5) +
  geom_vline(xintercept = as.Date("2019-10-01"), linetype = "dotted", color = "#969696", linewidth = 0.8) +
  geom_vline(xintercept = as.Date("2020-03-01"), linetype = "dotted", color = "#969696", linewidth = 0.8) +
  annotate("text", x = as.Date("2019-12-15"), y = max(nacional_mensual$Denuncias) * 0.9, label = "Uprising", angle = 90, size = 3.5, color = "#525252") +
  annotate("text", x = as.Date("2021-01-01"), y = max(nacional_mensual$Denuncias) * 0.9, label = "Pandemic", angle = 0, size = 3.5, color = "#525252") +
  geom_line(aes(color = Categoria), linewidth = 1.2, alpha = 0.85) +
  scale_fill_manual(name = "Context", values = c("Estallido Social" = "#cccccc", "Pandemia" = "#e6e6e6"), labels = c("Social Uprising", "Pandemic")) +
  scale_color_manual(name = "Crime type", values = academic_colors, labels = c("Non-violent robberies", "Surprise robberies", "Violent robberies")) +
  theme_minimal(base_family = "sans", base_size = 12) +
  labs(
    title = NULL,
    subtitle = NULL,
    x = NULL,
    y = "Reports"
  ) +
  theme(
    legend.position = "bottom",
    legend.box = "vertical",
    legend.text = element_text(size = 11, color = "black"),
    plot.title = element_blank(),
    plot.subtitle = element_blank(),
    panel.grid.minor = element_blank(),
    panel.grid.major.x = element_blank(),
    axis.line.x = element_line(color = "black", linewidth = 0.3),
    axis.ticks.x = element_line(color = "black", linewidth = 0.3)
  )

ggsave("paper1/output/figures/fig1_serie_mensual_nacional_eng.png", fig_1_eng, width = 10, height = 5.5, dpi = 300)
ggsave("paper1/output/figures/fig1_serie_mensual_nacional_eng.pdf", fig_1_eng, width = 10, height = 5.5)

# Fig 2 English
fig_2_eng <- ggplot(nacional_anual_long, aes(x = year, y = Tasa, color = Categoria)) +
  geom_line(linewidth = 1.2, alpha = 0.8) +
  geom_point(size = 2.5) +
  geom_segment(data = data.frame(year = 2013), aes(x = 2013, xend = 2025, y = ref_2016_vd, yend = ref_2016_vd), color = "#e34a33", linetype = "22", alpha = 0.4, inherit.aes = FALSE) +
  geom_segment(data = data.frame(year = 2013), aes(x = 2013, xend = 2025, y = ref_2016_sorpresa, yend = ref_2016_sorpresa), color = "#fdbb84", linetype = "22", alpha = 0.4, inherit.aes = FALSE) +
  geom_segment(data = data.frame(year = 2013), aes(x = 2013, xend = 2025, y = ref_2016_nv, yend = ref_2016_nv), color = "#2c7fb8", linetype = "22", alpha = 0.4, inherit.aes = FALSE) +
  scale_color_manual(name = "Crime type", values = academic_colors, labels = c("Non-violent robberies", "Surprise robberies", "Violent robberies")) +
  scale_x_continuous(breaks = 2013:2025) +
  theme_minimal(base_family = "sans", base_size = 12) +
  labs(
    title = NULL,
    subtitle = NULL,
    x = NULL,
    y = "Rate (per 100,000 inh.)",
  ) +
  theme(
    legend.position = "bottom",
    plot.title = element_blank(),
    plot.subtitle = element_blank(),
    panel.grid.minor = element_blank(),
    panel.grid.major.x = element_blank(),
    axis.line.x = element_line(color = "black", linewidth = 0.3)
  )

ggsave("paper1/output/figures/fig2_tasa_anual_nacional_eng.png", fig_2_eng, width = 10, height = 5.5, dpi = 300)
ggsave("paper1/output/figures/fig2_tasa_anual_nacional_eng.pdf", fig_2_eng, width = 10, height = 5.5)

# Fig 3 English
fig_3_eng <- ggplot() +
  geom_rect(data = rect_data, aes(xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax, fill = Periodo), inherit.aes = FALSE, alpha = 0.5) +
  geom_vline(xintercept = as.Date("2015-04-01"), linetype = "dashed", color = "#252525", linewidth = 0.7) +
  geom_vline(xintercept = as.Date("2017-08-01"), linetype = "dashed", color = "#252525", linewidth = 0.7) +
  geom_vline(xintercept = as.Date("2019-10-01"), linetype = "dashed", color = "#252525", linewidth = 0.7) +
  geom_vline(xintercept = as.Date("2024-01-01"), linetype = "dashed", color = "#252525", linewidth = 0.7) +
  annotate("text", x = as.Date("2015-04-01"), y = 0.12, label = "Q1 (Apr 15)", angle = 90, vjust = -0.5, size = 3.5, color = "#252525") +
  annotate("text", x = as.Date("2017-08-01"), y = 0.12, label = "Q2 (Aug 17)", angle = 90, vjust = -0.5, size = 3.5, color = "#252525") +
  annotate("text", x = as.Date("2019-10-01"), y = 0.12, label = "Q3 (Oct 19)", angle = 90, vjust = -0.5, size = 3.5, color = "#252525") +
  annotate("text", x = as.Date("2024-01-01"), y = 0.12, label = "Q4 (Jan 24)", angle = 90, vjust = -0.5, size = 3.5, color = "#252525") +
  geom_line(data = nacional_ratio_long, aes(x = date, y = Ratio_VD, color = "Serie Original"), linewidth = 0.7) +
  geom_smooth(data = nacional_ratio_long, aes(x = date, y = Ratio_VD, color = "Tendencia (LOESS)"), method = "loess", span = 0.2, fill = "#fee0d2", linewidth = 1.2, alpha = 0.5) +
  scale_fill_manual(name = "Context", values = c("Estallido Social" = "#cccccc", "Pandemia" = "#e6e6e6"), labels = c("Social Uprising", "Pandemic")) +
  scale_color_manual(name = "Estimate", values = c("Serie Original" = "#bdbdbd", "Tendencia (LOESS)" = "#de2d26"), labels = c("Original Series", "Trend (LOESS)")) +
  scale_y_continuous(
    labels = scales::percent_format(accuracy = 1),
    limits = c(0, NA),
    expand = expansion(mult = c(0, 0.05))
  ) +
  theme_minimal(base_size = 12) +
  labs(
    title = NULL,
    subtitle = NULL,
    x = NULL,
    y = "Relative Share (%)"
  ) +
  theme(
    legend.position = "bottom",
    legend.box = "vertical",
    plot.title = element_blank(),
    plot.subtitle = element_blank(),
    panel.grid.minor = element_blank(),
    panel.grid.major.x = element_blank(),
    axis.line.x = element_line(color = "black", linewidth = 0.3)
  )

ggsave("paper1/output/figures/fig3_ratio_violentos_mensual_eng.png", fig_3_eng, width = 10, height = 5.5, dpi = 300)
ggsave("paper1/output/figures/fig3_ratio_violentos_mensual_eng.pdf", fig_3_eng, width = 10, height = 5.5)

message("Listo 01_descriptive.R")
