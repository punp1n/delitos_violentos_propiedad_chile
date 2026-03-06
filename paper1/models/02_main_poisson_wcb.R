# 02_main_poisson_wcb.R — Modelo principal Poisson-QMLE con WCB
# rev.2: Agrega diagnósticos VIF, test de sobredispersión, CRVE convencional

library(dplyr)
library(arrow)
library(splines)
library(sandwich)
library(lmtest)
library(car)       # para vif()
library(AER)       # para dispersiontest()

for (d in c("C3", "C1", "C2")) {
  dir.create(paste0("paper1/output/tables/", d), showWarnings = FALSE, recursive = TRUE)
}

message("Cargando datos...")
panel <- read_parquet("paper1/output/data/panel_region_month.parquet")

# Nodos agnósticos en percentiles
knots_main <- quantile(panel$trend_t, probs = c(0.25, 0.50, 0.75))

run_wcb_model <- function(dv_name, panel_data, out_dir) {
  message(sprintf("Ajustando modelo para %s...", dv_name))
  
  fmla <- as.formula(paste0(
    dv_name, " ~ factor(month_of_year) + d_estallido + d_pandemia + ",
    "ns(trend_t, knots = knots_main) + factor(region) + offset(log(pop_monthly))"
  ))
  
  mod <- glm(fmla, family = poisson, data = panel_data)
  
  # ───────────────────────────────────────────────────
  # Diagnóstico 1: Test de sobredispersión (Cameron-Trivedi)
  # ───────────────────────────────────────────────────
  disp_ratio <- deviance(mod) / df.residual(mod)
  disp_test <- tryCatch(dispersiontest(mod, trafo = 1), error = function(e) NULL)
  
  sink(paste0(out_dir, "/diagnostico_sobredispersion_", dv_name, ".txt"))
  cat(sprintf("=== Diagnóstico de sobredispersión para %s ===\n\n", dv_name))
  cat(sprintf("Deviance / df.residual = %.4f\n", disp_ratio))
  cat(sprintf("  (>1 indica sobredispersión; Poisson QMLE es robusto si E[Y|X] correcta)\n\n"))
  if (!is.null(disp_test)) {
    cat("Test de Cameron-Trivedi (H0: equidispersión):\n")
    print(disp_test)
  }
  sink()
  
  # ───────────────────────────────────────────────────
  # Diagnóstico 2: VIF (multicolinealidad spline × dummies)
  # ───────────────────────────────────────────────────
  vif_res <- tryCatch({
    # vif no acepta offset, re-fit sin offset para VIF
    fmla_nooff <- as.formula(paste0(
      dv_name, " ~ factor(month_of_year) + d_estallido + d_pandemia + ",
      "ns(trend_t, knots = knots_main) + factor(region)"
    ))
    mod_nooff <- glm(fmla_nooff, family = poisson, data = panel_data)
    vif(mod_nooff)
  }, error = function(e) NULL)
  
  if (!is.null(vif_res)) {
    # car::vif() returns GVIF matrix for factor variables 
    if (is.matrix(vif_res)) {
      vif_df <- data.frame(
        Variable = rownames(vif_res),
        GVIF = vif_res[, "GVIF"],
        Df = vif_res[, "Df"],
        GVIF_adj = vif_res[, "GVIF^(1/(2*Df))"]
      )
    } else {
      vif_df <- data.frame(
        Variable = names(vif_res),
        GVIF = as.numeric(vif_res),
        Df = 1,
        GVIF_adj = as.numeric(vif_res)
      )
    }
    write.csv(vif_df, paste0(out_dir, "/diagnostico_vif_", dv_name, ".csv"), row.names = FALSE)
    # Flag high GVIF^(1/2*Df) > 2.5 (equivalent to VIF > ~6 for 1 df)
    high_vif <- vif_df %>% filter(GVIF_adj > 2.5)
    if (nrow(high_vif) > 0) {
      message(sprintf("  ALERTA: %d variables con GVIF^(1/2*Df) > 2.5:", nrow(high_vif)))
      message(paste("   ", high_vif$Variable, "=", round(high_vif$GVIF_adj, 2), collapse = "\n"))
    }
  }
  
  # ───────────────────────────────────────────────────
  # Inferencia: WCB (principal) + CRVE convencional (comparación)
  # ───────────────────────────────────────────────────
  message(sprintf("Calculando Wild Cluster Bootstrap (R=9999) para %s...", dv_name))
  vcov_wcb <- vcovBS(mod, cluster = ~region, R = 9999, type = "fractional")
  res_wcb <- coeftest(mod, vcov = vcov_wcb)
  
  message(sprintf("Calculando CRVE convencional para %s...", dv_name))
  vcov_crve <- vcovCL(mod, cluster = ~region)
  res_crve <- coeftest(mod, vcov = vcov_crve)
  
  terms_to_keep <- c("d_estallido", "d_pandemia", 
                     "ns(trend_t, knots = knots_main)1", 
                     "ns(trend_t, knots = knots_main)2", 
                     "ns(trend_t, knots = knots_main)3", 
                     "ns(trend_t, knots = knots_main)4")
  
  res_df <- data.frame(
    Categoria = dv_name,
    Termino = rownames(res_wcb),
    Estimate = res_wcb[, "Estimate"],
    Std_Error_WCB = res_wcb[, "Std. Error"],
    p_value_WCB = res_wcb[, "Pr(>|z|)"],
    Std_Error_CRVE = res_crve[, "Std. Error"],
    p_value_CRVE = res_crve[, "Pr(>|z|)"]
  ) %>% filter(Termino %in% terms_to_keep)
  
  res_df <- res_df %>%
    mutate(
      IRR = exp(Estimate),
      CI_lower_WCB = exp(Estimate - 1.96 * Std_Error_WCB),
      CI_upper_WCB = exp(Estimate + 1.96 * Std_Error_WCB),
      CI_lower_CRVE = exp(Estimate - 1.96 * Std_Error_CRVE),
      CI_upper_CRVE = exp(Estimate + 1.96 * Std_Error_CRVE)
    )
  
  return(res_df)
}

set.seed(2026)

# --- Clasificación C3 (Especificación Principal) ---
res_vd <- run_wcb_model("n_violencia_dura", panel, "paper1/output/tables/C3")
res_sorpresa <- run_wcb_model("n_sorpresa", panel, "paper1/output/tables/C3")
res_nv <- run_wcb_model("n_no_violento", panel, "paper1/output/tables/C3")
tabla_2_c3 <- bind_rows(res_vd, res_sorpresa, res_nv)
write.csv(tabla_2_c3, "paper1/output/tables/C3/tabla_2_poisson_wcb.csv", row.names = FALSE)
message("Resultados C3 guardados.")

# --- Clasificación C1 (Institucional) ---
res_c1 <- run_wcb_model("n_violento_c1", panel, "paper1/output/tables/C1")
write.csv(res_c1, "paper1/output/tables/C1/tabla_2_poisson_wcb.csv", row.names = FALSE)
message("Resultados C1 guardados.")

# --- Clasificación C2 (Ajustada) ---
res_c2 <- run_wcb_model("n_violento_c2", panel, "paper1/output/tables/C2")
write.csv(res_c2, "paper1/output/tables/C2/tabla_2_poisson_wcb.csv", row.names = FALSE)
message("Resultados C2 guardados.")
