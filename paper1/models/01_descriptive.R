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

message("Generando Tabla 1...")
panel_periods <- panel %>%
  mutate(
    periodo = case_when(
      year <= 2015 ~ "Pre-Línea Base (2014-2015)",
      year >= 2016 & year <= 2019 & (year < 2019 | month <= 9) ~ "Línea Base (2016-Sep 2019)",
      (year == 2019 & month >= 10) | (year == 2020 & month <= 2) ~ "Estallido Social (Oct 2019-Feb 2020)",
      (year == 2020 & month >= 3) | (year == 2021) ~ "Pandemia (Mar 2020-Dic 2021)",
      year >= 2022 ~ "Pandemia Post (2022-2024)",
      TRUE ~ "Otro"
    ),
    tasa_vd = n_violencia_dura / pop_monthly * 100000,
    tasa_c1 = n_violento_c1 / pop_monthly * 100000,
    tasa_c2 = n_violento_c2 / pop_monthly * 100000
  )

tabla_1 <- panel_periods %>%
  group_by(periodo) %>%
  summarise(
    meses_n = n_distinct(date),
    vd_media = mean(n_violencia_dura),
    vd_sd = sd(n_violencia_dura),
    vd_tasa_media = mean(tasa_vd),
    
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
    Violencia_Dura = sum(n_violencia_dura),
    Sorpresa = sum(n_sorpresa),
    No_Violentos = sum(n_no_violento),
    d_estallido = max(d_estallido),
    d_pandemia = max(d_pandemia),
    .groups = "drop"
  ) %>%
  pivot_longer(
    cols = c(Violencia_Dura, Sorpresa, No_Violentos),
    names_to = "Categoria",
    values_to = "Denuncias"
  )

# Rectángulos para sombreados
estallido_rect <- data.frame(
  xmin = as.Date("2019-10-01"),
  xmax = as.Date("2020-02-28"),
  ymin = -Inf,
  ymax = Inf
)

pandemia_rect <- data.frame(
  xmin = as.Date("2020-03-01"),
  xmax = as.Date("2021-12-31"),
  ymin = -Inf,
  ymax = Inf
)

fig_1 <- ggplot(nacional_mensual, aes(x = date, y = Denuncias, color = Categoria)) +
  geom_rect(data = estallido_rect, inherit.aes = FALSE,
            aes(xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax),
            fill = "gray80", alpha = 0.5) +
  geom_rect(data = pandemia_rect, inherit.aes = FALSE,
            aes(xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax),
            fill = "gray90", alpha = 0.5) +
  geom_line(linewidth = 1) +
  scale_color_manual(values = c(
    "Violencia_Dura" = "red",
    "Sorpresa" = "orange",
    "No_Violentos" = "darkgray"
  )) +
  theme_minimal() +
  labs(
    title = "Figura 1: Serie Mensual Nacional de Denuncias (2014-2024)",
    x = "Fecha",
    y = "Cantidad de Denuncias",
    color = "Categoría",
    caption = "Área gris oscuro: Estallido Social. Área gris claro: Pandemia."
  ) +
  theme(legend.position = "bottom")

ggsave("paper1/output/figures/fig1_serie_mensual_nacional.png", fig_1, width = 10, height = 6)
ggsave("paper1/output/figures/fig1_serie_mensual_nacional.pdf", fig_1, width = 10, height = 6)

# --- Fig 2: Tasas por 100K hab. anuales ---
message("Generando Figura 2...")

nacional_anual <- panel %>%
  group_by(year) %>%
  summarise(
    vd = sum(n_violencia_dura),
    sorpresa = sum(n_sorpresa),
    nv = sum(n_no_violento),
    # Usar poblacion de mitad de año o promedio de la mensual para nacional
    pop_nacional = sum(pop_monthly) / 12,
    .groups = "drop"
  ) %>%
  mutate(
    Tasa_Violencia_Dura = vd / pop_nacional * 100000,
    Tasa_Sorpresa = sorpresa / pop_nacional * 100000,
    Tasa_No_Violentos = nv / pop_nacional * 100000
  )

# Extraer línea de referencia 2016
ref_2016_vd <- nacional_anual %>% filter(year == 2016) %>% pull(Tasa_Violencia_Dura)
ref_2016_sorpresa <- nacional_anual %>% filter(year == 2016) %>% pull(Tasa_Sorpresa)
ref_2016_nv <- nacional_anual %>% filter(year == 2016) %>% pull(Tasa_No_Violentos)

nacional_anual_long <- nacional_anual %>%
  select(year, Tasa_Violencia_Dura, Tasa_Sorpresa, Tasa_No_Violentos) %>%
  pivot_longer(
    cols = starts_with("Tasa_"),
    names_to = "Categoria",
    values_to = "Tasa"
  ) %>%
  mutate(Categoria = str_replace(Categoria, "Tasa_", ""))

fig_2 <- ggplot(nacional_anual_long, aes(x = year, y = Tasa, color = Categoria)) +
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  # Lineas de referencia 2016
  geom_hline(yintercept = ref_2016_vd, color = "red", linetype = "dashed", alpha = 0.5) +
  geom_hline(yintercept = ref_2016_sorpresa, color = "orange", linetype = "dashed", alpha = 0.5) +
  geom_hline(yintercept = ref_2016_nv, color = "darkgray", linetype = "dashed", alpha = 0.5) +
  scale_color_manual(values = c(
    "Violencia_Dura" = "red",
    "Sorpresa" = "orange",
    "No_Violentos" = "darkgray"
  )) +
  scale_x_continuous(breaks = 2014:2024) +
  theme_minimal() +
  labs(
    title = "Figura 2: Tasas Anuales Nacionales (por 100.000 hab.)",
    x = "Año",
    y = "Tasa por 100.000 habitantes",
    color = "Categoría",
    caption = "Líneas punteadas indican el nivel de tasa en 2016."
  ) +
  theme(legend.position = "bottom")

ggsave("paper1/output/figures/fig2_tasa_anual_nacional.png", fig_2, width = 10, height = 6)
ggsave("paper1/output/figures/fig2_tasa_anual_nacional.pdf", fig_2, width = 10, height = 6)

message("Listo 01_descriptive.R")
