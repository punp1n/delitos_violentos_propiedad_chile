# 06_placebos.R — Modelos Placebo y Falsificación
# rev.2: Agrega P4 (Daños simples), P5 (Lesiones leves), P2 regional,
#         P2b (CPHDV homicidios confirmados)

library(dplyr)
library(arrow)
library(splines)
library(sandwich)
library(lmtest)
library(tidyr)

dir.create("paper1/output/tables", showWarnings = FALSE, recursive = TRUE)

message("Cargando datos principales y placebos...")
panel <- read_parquet("paper1/output/data/panel_region_month.parquet")
placebos <- read_parquet("paper1/output/data/placebo_panel.parquet")

# Merge con el panel para heredar pop_monthly, d_estallido, etc.
panel_placebo <- panel %>%
  select(region, year, month, yyyymm, pop_monthly, d_estallido, d_pandemia,
         month_of_year, trend_t, macrozona) %>%
  left_join(placebos, by = c("region", "year", "month"))

knots_main <- quantile(panel$trend_t, probs = c(0.25, 0.50, 0.75))

# ═══════════════════════════════════════════════════════════════
#  Helper para extraer resultados
# ═══════════════════════════════════════════════════════════════
terms_to_keep <- c("d_estallido", "d_pandemia",
                   "ns(trend_t, knots = knots_main)1",
                   "ns(trend_t, knots = knots_main)2",
                   "ns(trend_t, knots = knots_main)3",
                   "ns(trend_t, knots = knots_main)4")

extract_res <- function(res, name) {
  df <- data.frame(
    Categoria = name,
    Termino = rownames(res),
    Estimate = res[, "Estimate"],
    Std_Error = res[, "Std. Error"],
    p_value = res[, "Pr(>|z|)"]
  ) %>% filter(Termino %in% terms_to_keep) %>%
    mutate(
      IRR = exp(Estimate),
      CI_lower = exp(Estimate - 1.96 * Std_Error),
      CI_upper = exp(Estimate + 1.96 * Std_Error)
    )
  return(df)
}

# ═══════════════════════════════════════════════════════════════
#  P1: Cuasidelito vehicular (proxy movilidad) — panel regional
# ═══════════════════════════════════════════════════════════════
message("=== P1 (Cuasidelito vehicular - Proxy Movilidad) ===")
panel_p1 <- panel_placebo %>%
  filter(tipo_placebo == "cuasidelito_vehicular") %>%
  mutate(n_denuncias = replace_na(n_denuncias, 0))

mod_p1 <- glm(
  n_denuncias ~ factor(month_of_year) + d_estallido + d_pandemia +
               ns(trend_t, knots = knots_main) + factor(region) +
               offset(log(pop_monthly)),
  family = poisson, data = panel_p1
)
message("  Calculando WCB (R=9999)...")
vcov_wcb_p1 <- vcovBS(mod_p1, cluster = ~region, R = 9999, type = "fractional")
res_p1 <- coeftest(mod_p1, vcov = vcov_wcb_p1)

# ═══════════════════════════════════════════════════════════════
#  P2: Homicidios dolosos (violencia real) — Nivel NACIONAL
# ═══════════════════════════════════════════════════════════════
message("=== P2 (Homicidios dolosos - Nacional) ===")
panel_p2 <- panel_placebo %>%
  filter(tipo_placebo == "homicidio_doloso") %>%
  group_by(yyyymm, year, month, trend_t, month_of_year, d_estallido, d_pandemia) %>%
  summarise(
    n_homicidios = sum(n_denuncias, na.rm = TRUE),
    pop_monthly_nacional = sum(pop_monthly),
    .groups = "drop"
  )

mod_p2 <- glm(
  n_homicidios ~ factor(month_of_year) + d_estallido + d_pandemia +
                 ns(trend_t, knots = knots_main) +
                 offset(log(pop_monthly_nacional)),
  family = poisson, data = panel_p2
)
vcov_hac_p2 <- vcovHAC(mod_p2)
res_p2 <- coeftest(mod_p2, vcov = vcov_hac_p2)

# ═══════════════════════════════════════════════════════════════
#  P2-Regional: Homicidios dolosos — por Macrozona
# ═══════════════════════════════════════════════════════════════
message("=== P2-Regional (Homicidios por Macrozona) ===")
panel_p2_reg <- panel_placebo %>%
  filter(tipo_placebo == "homicidio_doloso") %>%
  group_by(macrozona, yyyymm, year, month, trend_t, month_of_year, d_estallido, d_pandemia) %>%
  summarise(
    n_homicidios = sum(n_denuncias, na.rm = TRUE),
    pop_monthly = sum(pop_monthly),
    .groups = "drop"
  )

# Modelo por macrozona
res_p2_reg_list <- list()
for (mz in unique(panel_p2_reg$macrozona)) {
  data_mz <- panel_p2_reg %>% filter(macrozona == mz)
  mod_mz <- tryCatch({
    glm(n_homicidios ~ factor(month_of_year) + d_estallido + d_pandemia +
          ns(trend_t, knots = knots_main) + offset(log(pop_monthly)),
        family = poisson, data = data_mz)
  }, error = function(e) NULL)

  if (!is.null(mod_mz)) {
    res_mz <- coeftest(mod_mz, vcov = vcovHAC(mod_mz))
    res_p2_reg_list[[mz]] <- extract_res(res_mz, paste0("P2_Homicidios_", mz))
  }
}
tabla_p2_regional <- bind_rows(res_p2_reg_list)

# ═══════════════════════════════════════════════════════════════
#  P2b: CPHDV Homicidios confirmados — Regional
# ═══════════════════════════════════════════════════════════════
message("=== P2b (CPHDV Homicidios confirmados) ===")
cphdv_exists <- file.exists("paper1/output/data/cphdv_homicidios.parquet")
tabla_p2b <- NULL

if (cphdv_exists) {
  cphdv <- read_parquet("paper1/output/data/cphdv_homicidios.parquet")
  
  # Nacional (region == 0)
  cphdv_nacional <- cphdv %>%
    filter(region == 0) %>%
    select(year, month, n_homicidios_cphdv)
  
  # Merge con panel temporal (solo 2018-2024)
  panel_cphdv <- panel %>%
    filter(year >= 2018) %>%
    group_by(yyyymm, year, month, trend_t, month_of_year, d_estallido, d_pandemia) %>%
    summarise(pop_monthly_nacional = sum(pop_monthly), .groups = "drop") %>%
    left_join(cphdv_nacional, by = c("year", "month")) %>%
    mutate(n_homicidios_cphdv = replace_na(n_homicidios_cphdv, 0))
  
  # Recalcular knots para el rango 2018-2024
  knots_cphdv <- quantile(panel_cphdv$trend_t, probs = c(0.25, 0.50, 0.75))
  
  mod_cphdv <- glm(
    n_homicidios_cphdv ~ factor(month_of_year) + d_estallido + d_pandemia +
                         ns(trend_t, knots = knots_cphdv) +
                         offset(log(pop_monthly_nacional)),
    family = poisson, data = panel_cphdv
  )
  vcov_hac_cphdv <- vcovHAC(mod_cphdv)
  res_cphdv <- coeftest(mod_cphdv, vcov = vcov_hac_cphdv)
  
  cphdv_terms <- c("d_estallido", "d_pandemia",
                   grep("trend_t", rownames(res_cphdv), value = TRUE))
  
  tabla_p2b <- data.frame(
    Categoria = "P2b_CPHDV_Confirmados",
    Termino = rownames(res_cphdv),
    Estimate = res_cphdv[, "Estimate"],
    Std_Error = res_cphdv[, "Std. Error"],
    p_value = res_cphdv[, "Pr(>|z|)"]
  ) %>%
    filter(Termino %in% cphdv_terms) %>%
    mutate(
      IRR = exp(Estimate),
      CI_lower = exp(Estimate - 1.96 * Std_Error),
      CI_upper = exp(Estimate + 1.96 * Std_Error)
    )
  
  # Comparación CCH vs CPHDV (tabla anual)
  homicidios_comp <- panel_p2 %>%
    group_by(year) %>%
    summarise(Homicidios_CCH = sum(n_homicidios), .groups = "drop") %>%
    left_join(
      cphdv %>% filter(region == 0) %>%
        group_by(year) %>%
        summarise(Homicidios_CPHDV = sum(n_homicidios_cphdv), .groups = "drop"),
      by = "year"
    ) %>%
    mutate(
      Ratio_CCH_CPHDV = round(Homicidios_CCH / Homicidios_CPHDV, 3)
    )
  write.csv(homicidios_comp, "paper1/output/tables/comparacion_homicidios_cch_cphdv.csv", row.names = FALSE)
  message("  Tabla de comparación CCH vs CPHDV guardada.")
} else {
  message("  CPHDV parquet no encontrado, saltando P2b.")
}

# ═══════════════════════════════════════════════════════════════
#  P3: Secuestros (nivel nacional)
# ═══════════════════════════════════════════════════════════════
message("=== P3 (Secuestros - Nacional) ===")
panel_p3 <- panel_placebo %>%
  filter(tipo_placebo == "secuestro") %>%
  group_by(yyyymm, year, month, trend_t, month_of_year, d_estallido, d_pandemia) %>%
  summarise(
    n_secuestros = sum(n_denuncias, na.rm = TRUE),
    pop_monthly_nacional = sum(pop_monthly),
    .groups = "drop"
  )

mod_p3 <- glm(
  n_secuestros ~ factor(month_of_year) + d_estallido + d_pandemia +
                 ns(trend_t, knots = knots_main) +
                 offset(log(pop_monthly_nacional)),
  family = poisson, data = panel_p3
)
vcov_hac_p3 <- vcovHAC(mod_p3)
res_p3 <- coeftest(mod_p3, vcov = vcov_hac_p3)

# ═══════════════════════════════════════════════════════════════
#  P4: Daños simples (CUM 840) — panel regional
# ═══════════════════════════════════════════════════════════════
message("=== P4 (Daños simples - Propensión a denunciar estable) ===")
panel_p4 <- panel_placebo %>%
  filter(tipo_placebo == "danos_simples") %>%
  mutate(n_denuncias = replace_na(n_denuncias, 0))

mod_p4 <- glm(
  n_denuncias ~ factor(month_of_year) + d_estallido + d_pandemia +
               ns(trend_t, knots = knots_main) + factor(region) +
               offset(log(pop_monthly)),
  family = poisson, data = panel_p4
)
message("  Calculando WCB (R=9999)...")
vcov_wcb_p4 <- vcovBS(mod_p4, cluster = ~region, R = 9999, type = "fractional")
res_p4 <- coeftest(mod_p4, vcov = vcov_wcb_p4)

# ═══════════════════════════════════════════════════════════════
#  P5: Lesiones leves (CUM 13001) — panel regional
# ═══════════════════════════════════════════════════════════════
message("=== P5 (Lesiones leves - Control no-propiedad) ===")
panel_p5 <- panel_placebo %>%
  filter(tipo_placebo == "lesiones_leves") %>%
  mutate(n_denuncias = replace_na(n_denuncias, 0))

mod_p5 <- glm(
  n_denuncias ~ factor(month_of_year) + d_estallido + d_pandemia +
               ns(trend_t, knots = knots_main) + factor(region) +
               offset(log(pop_monthly)),
  family = poisson, data = panel_p5
)
message("  Calculando WCB (R=9999)...")
vcov_wcb_p5 <- vcovBS(mod_p5, cluster = ~region, R = 9999, type = "fractional")
res_p5 <- coeftest(mod_p5, vcov = vcov_wcb_p5)

# ═══════════════════════════════════════════════════════════════
#  Ensamblar Tabla 8 expandida
# ═══════════════════════════════════════════════════════════════
message("Generando tabla 8 expandida de placebos...")
tabla_8 <- bind_rows(
  extract_res(res_p1, "P1_Cuasidelito_Vehicular"),
  extract_res(res_p2, "P2_Homicidios_Nacional"),
  extract_res(res_p3, "P3_Secuestros"),
  extract_res(res_p4, "P4_Danos_Simples"),
  extract_res(res_p5, "P5_Lesiones_Leves")
)

# Tablas separadas
write.csv(tabla_8, "paper1/output/tables/tabla_8_placebos.csv", row.names = FALSE)
write.csv(tabla_p2_regional, "paper1/output/tables/tabla_8b_homicidios_regional.csv", row.names = FALSE)

if (!is.null(tabla_p2b)) {
  write.csv(tabla_p2b, "paper1/output/tables/tabla_8c_cphdv.csv", row.names = FALSE)
  message("  Tabla P2b (CPHDV) guardada.")
}

message("Resultados guardados en tabla_8_placebos.csv, tabla_8b, tabla_8c")
