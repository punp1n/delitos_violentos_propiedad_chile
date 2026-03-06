# 03_regional_cusum_fdr.R — CUSUM-GLM regional + FDR + Bai-Perron
# rev.2: Agrega Bai-Perron sin punto pre-especificado

library(dplyr)
library(arrow)
library(strucchange)
library(sandwich)

for (d in c("C3", "C1", "C2")) {
  dir.create(paste0("paper1/output/tables/", d), showWarnings = FALSE, recursive = TRUE)
}

message("Cargando datos...")
panel <- read_parquet("paper1/output/data/panel_region_month.parquet")

# ───────────────────────────────────────────────────
# A) CUSUM-GLM Regional con corrección FDR
# ───────────────────────────────────────────────────
run_regional_cusum <- function(var_name) {
  message(sprintf("Ejecutando CUSUM-GLM regional para %s...", var_name))
  results <- list()
  
  for (reg in sort(unique(panel$region))) {
    data_r <- panel[panel$region == reg, ]
    data_r <- data_r[order(data_r$trend_t), ]
    
    fmla <- as.formula(paste0(var_name, " ~ factor(month_of_year) + d_estallido + d_pandemia + offset(log(pop_monthly))"))
    glm_r <- glm(fmla, family = poisson, data = data_r)
    
    # Proceso empírico de fluctuación CUSUM
    gefp_r <- tryCatch({
      gefp(glm_r, fit = NULL, order.by = data_r$trend_t)
    }, error = function(e) NULL)
    
    if(!is.null(gefp_r)){
      test_r <- sctest(gefp_r, functional = maxBB)
      
      # Estimar posible mes de quiebre absoluto
      process <- as.vector(gefp_r$process)
      max_idx <- which.max(abs(process))
      break_month <- data_r$yyyymm[max_idx]
      
      results[[length(results) + 1]] <- data.frame(
        Region = reg,
        Categoria = var_name,
        Test_Stat = test_r$statistic,
        p_value_raw = test_r$p.value,
        Est_Break_YYYYMM = break_month
      )
    }
  }
  
  res_df <- bind_rows(results)
  # Corrección de Benjamini-Hochberg (FDR)
  res_df$p_value_fdr <- p.adjust(res_df$p_value_raw, method = "BH")
  return(res_df)
}

# ───────────────────────────────────────────────────
# B) Bai-Perron sin punto pre-especificado (nivel nacional)
# ───────────────────────────────────────────────────
run_bai_perron <- function(var_name_violent, var_name_total = NULL) {
  message(sprintf("Ejecutando Bai-Perron para %s...", var_name_violent))
  
  # Agregar a nivel nacional mensual
  panel_nacional <- panel %>%
    group_by(yyyymm, trend_t, month_of_year) %>%
    summarise(
      n_violent = sum(.data[[var_name_violent]], na.rm = TRUE),
      n_total = if (!is.null(var_name_total)) sum(.data[[var_name_total]], na.rm = TRUE) 
                else sum(n_violencia_dura + n_sorpresa + n_no_violento, na.rm = TRUE),
      .groups = "drop"
    ) %>%
    arrange(trend_t)
  
  # Ratio desestacionalizado: primero calcular ratio crudo, luego desestacionalizar
  panel_nacional$ratio <- panel_nacional$n_violent / panel_nacional$n_total
  
  # Desestacionalizar: residuos de regresión sobre dummies mensuales
  mod_season <- lm(ratio ~ factor(month_of_year), data = panel_nacional)
  panel_nacional$ratio_desest <- residuals(mod_season) + mean(panel_nacional$ratio)
  
  # Bai-Perron con errores HAC
  # breakpoints() detecta hasta h*T posibles quiebres
  bp_formula <- ratio_desest ~ 1
  bp <- tryCatch({
    breakpoints(bp_formula, data = panel_nacional, h = 0.15)  # mínimal segmento 15%
  }, error = function(e) {
    message(sprintf("  Error en Bai-Perron: %s", e$message))
    NULL
  })
  
  if (!is.null(bp)) {
    # Resumen con BIC para selección de número de quiebres
    bp_summary <- summary(bp)
    
    # Extraer puntos de quiebre óptimos (por BIC)
    optimal_breaks <- breakpoints(bp)$breakpoints
    
    if (!any(is.na(optimal_breaks))) {
      break_dates <- panel_nacional$yyyymm[optimal_breaks]
      break_ratios <- panel_nacional$ratio_desest[optimal_breaks]
      
      bp_results <- data.frame(
        Categoria = var_name_violent,
        N_Breaks_Optimal = length(optimal_breaks),
        Break_Positions = paste(optimal_breaks, collapse = ","),
        Break_YYYYMM = paste(break_dates, collapse = ","),
        Break_Ratios = paste(round(break_ratios, 4), collapse = ","),
        BIC = bp_summary$RSS["BIC", paste0(length(optimal_breaks), " break")]
      )
    } else {
      bp_results <- data.frame(
        Categoria = var_name_violent,
        N_Breaks_Optimal = 0,
        Break_Positions = "none",
        Break_YYYYMM = "none",
        Break_Ratios = "none",
        BIC = bp_summary$RSS["BIC", "0 break"]
      )
    }
    
    # También reportar F-tests para cada número posible de quiebres
    bp_ftest <- tryCatch({
      # Intervalos de confianza (con HAC)
      ci <- confint(bp, vcov. = vcovHAC)
      data.frame(
        Break_Idx = ci$confint[, "breakpoints"],
        CI_lower = ci$confint[, 1],
        CI_upper = ci$confint[, 3],
        YYYYMM = panel_nacional$yyyymm[ci$confint[, "breakpoints"]]
      )
    }, error = function(e) NULL)
    
    return(list(summary = bp_results, ci = bp_ftest, bp_object = bp))
  }
  return(NULL)
}

set.seed(2026)

# ─── CUSUM ───
# C3
res_cusum_vd <- run_regional_cusum("n_violencia_dura")
write.csv(res_cusum_vd, "paper1/output/tables/C3/tabla_3_cusum_fdr.csv", row.names = FALSE)

# C1
res_cusum_c1 <- run_regional_cusum("n_violento_c1")
write.csv(res_cusum_c1, "paper1/output/tables/C1/tabla_3_cusum_fdr.csv", row.names = FALSE)

# C2
res_cusum_c2 <- run_regional_cusum("n_violento_c2")
write.csv(res_cusum_c2, "paper1/output/tables/C2/tabla_3_cusum_fdr.csv", row.names = FALSE)

message("CUSUM finalizado para las tres clasificaciones.")

# ─── Bai-Perron ───
message("\n=== Bai-Perron (sin punto pre-especificado) ===")

bp_c3 <- run_bai_perron("n_violencia_dura")
if (!is.null(bp_c3)) {
  write.csv(bp_c3$summary, "paper1/output/tables/C3/bai_perron_results.csv", row.names = FALSE)
  if (!is.null(bp_c3$ci)) {
    write.csv(bp_c3$ci, "paper1/output/tables/C3/bai_perron_ci.csv", row.names = FALSE)
  }
  sink("paper1/output/tables/C3/bai_perron_summary.txt")
  cat("=== Bai-Perron: Violencia Dura (C3) ===\n\n")
  print(summary(bp_c3$bp_object))
  sink()
}

bp_c1 <- run_bai_perron("n_violento_c1")
if (!is.null(bp_c1)) {
  write.csv(bp_c1$summary, "paper1/output/tables/C1/bai_perron_results.csv", row.names = FALSE)
  sink("paper1/output/tables/C1/bai_perron_summary.txt")
  cat("=== Bai-Perron: Violento C1 ===\n\n")
  print(summary(bp_c1$bp_object))
  sink()
}

bp_c2 <- run_bai_perron("n_violento_c2")
if (!is.null(bp_c2)) {
  write.csv(bp_c2$summary, "paper1/output/tables/C2/bai_perron_results.csv", row.names = FALSE)
  sink("paper1/output/tables/C2/bai_perron_summary.txt")
  cat("=== Bai-Perron: Violento C2 ===\n\n")
  print(summary(bp_c2$bp_object))
  sink()
}

message("Bai-Perron finalizado para las tres clasificaciones.")
