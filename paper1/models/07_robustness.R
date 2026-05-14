# 07_robustness.R — Análisis de Robustez en la estimación

library(dplyr)
library(arrow)
library(splines)
library(sandwich)
library(lmtest)

dir.create("paper1/output/tables/C3", showWarnings = FALSE, recursive = TRUE)
dir.create("paper1/output/tables/C1", showWarnings = FALSE, recursive = TRUE)
dir.create("paper1/output/tables/C2", showWarnings = FALSE, recursive = TRUE)

message("Cargando datos principales...")
panel <- read_parquet("paper1/output/data/panel_region_month.parquet")
knots_main <- quantile(panel$trend_t, probs = c(0.25, 0.50, 0.75))

extract_trend <- function(mod, name, is_wcb = TRUE) {
  if (is_wcb) {
    vcov_rob <- vcovBS(mod, cluster = ~region, R = 999, type = "fractional")
  } else {
    vcov_rob <- vcovHC(mod, type = "HC1")
  }

  res <- tryCatch(coeftest(mod, vcov = vcov_rob), error = function(e) NULL)
  if (is.null(res)) {
    return(NULL)
  }

  idx <- grep("trend_t", rownames(res))
  if (length(idx) == 0) {
    return(NULL)
  }

  # Spline 4 = último término del spline (período más reciente, ~2022-2025)
  # Es el coeficiente clave para comparar con el resultado principal (IRR=0.868)
  idx_s4 <- idx[length(idx)]

  df <- data.frame(
    Especificacion = name,
    Spline_term = rownames(res)[idx_s4],
    Estimate = res[idx_s4, "Estimate"],
    Std_Error = res[idx_s4, "Std. Error"],
    p_value = res[idx_s4, "Pr(>|z|)"]
  ) %>% mutate(IRR = exp(Estimate))
  return(df)
}

run_robustness <- function(var_name, det_var_name, out_dir) {
  results_list <- list()

  # R1: offset libre (log(pop) como regresor, no offset fijo)
  fmla_R1 <- as.formula(paste0(var_name, " ~ factor(month_of_year) + d_estallido + d_pandemia + ns(trend_t, knots = knots_main) + factor(region) + log(pop_monthly)"))
  results_list[[1]] <- extract_trend(glm(fmla_R1, family = poisson, data = panel), "R1_Offset_Libre")

  # R3: sin corrección SERMIG (denominador solo INE)
  fmla_R3 <- as.formula(paste0(var_name, " ~ factor(month_of_year) + d_estallido + d_pandemia + ns(trend_t, knots = knots_main) + factor(region) + offset(log(pop_ine))"))
  results_list[[2]] <- extract_trend(glm(fmla_R3, family = poisson, data = panel %>% mutate(pop_ine = ifelse(pop_ine <= 0, 1, pop_ine))), "R3_Sin_SERMIG")

  # R5: nodos histórico-políticos (abr-2014=mes16, abr-2018=mes64, nov-2019=mes83, oct-2021=mes106)
  # Inicio 2° mandato Bachelet | Inicio 2° mandato Piñera | Estallido social | Fin estado excepción pandemia
  fmla_R5 <- as.formula(paste0(var_name, " ~ factor(month_of_year) + d_estallido + d_pandemia + ns(trend_t, knots = c(16, 64, 83, 106)) + factor(region) + offset(log(pop_monthly))"))
  results_list[[3]] <- extract_trend(glm(fmla_R5, family = poisson, data = panel), "R5_Nodos_Historicos")

  # R6: detenciones como VD (en lugar de denuncias)
  # Evalúa disociación entre victimización ciudadana y reacción policial
  if (!is.null(det_var_name) && det_var_name %in% colnames(panel)) {
    fmla_R6 <- as.formula(paste0(det_var_name, " ~ factor(month_of_year) + d_estallido + d_pandemia + ns(trend_t, knots = knots_main) + factor(region) + offset(log(pop_monthly))"))
    results_list[[4]] <- extract_trend(glm(fmla_R6, family = poisson, data = panel), "R6_Detenciones")
  } else {
    message(sprintf("  AVISO: columna '%s' no encontrada, omitiendo R6.", det_var_name))
  }

  # R7: spline más flexible (df=5, 4 nodos)
  fmla_R7 <- as.formula(paste0(var_name, " ~ factor(month_of_year) + d_estallido + d_pandemia + ns(trend_t, df = 5) + factor(region) + offset(log(pop_monthly))"))
  results_list[[5]] <- extract_trend(glm(fmla_R7, family = poisson, data = panel), "R7_df_5")

  tabla_6 <- bind_rows(Filter(Negate(is.null), results_list))
  write.csv(tabla_6, paste0(out_dir, "/tabla_6_robustez.csv"), row.names = FALSE)
  message(sprintf("  Guardado: %s/tabla_6_robustez.csv (%d especificaciones)", out_dir, nrow(tabla_6)))
}

set.seed(2026)
message("=== Robustez C3: Robos violentos ===")
run_robustness("n_robos_violentos", "n_det_violentos", "paper1/output/tables/C3")

message("=== Robustez C1 (Apéndice) ===")
run_robustness("n_violento_c1", "n_det_violentos", "paper1/output/tables/C1")

message("=== Robustez C2 (Apéndice) ===")
run_robustness("n_violento_c2", "n_det_violentos", "paper1/output/tables/C2")

message("Fin script 07")
