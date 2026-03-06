# 08_sensitivity_pop.R — Sensibilidad al denominador irregular

library(dplyr)
library(arrow)
library(splines)
library(sandwich)
library(lmtest)

dir.create("paper1/output/tables/C3", showWarnings = FALSE, recursive = TRUE)
dir.create("paper1/output/tables/C1", showWarnings = FALSE, recursive = TRUE)
dir.create("paper1/output/tables/C2", showWarnings = FALSE, recursive = TRUE)

message("Cargando datos...")
panel <- read_parquet("paper1/output/data/panel_region_month.parquet")
knots_main <- quantile(panel$trend_t, probs = c(0.25, 0.50, 0.75))

run_sensitivity <- function(var_name, out_dir) {
  results_sens <- list()
  k_values <- c(1.00, 1.05, 1.10, 1.15, 1.20)
  high_mig_regions <- c(15, 1, 2, 13)
  
  for (k in k_values) {
    panel_k <- panel %>% mutate(pop_sens = if_else(region %in% high_mig_regions, pop_monthly * k, pop_monthly))
    fmla <- as.formula(paste0(var_name, " ~ factor(month_of_year) + d_estallido + d_pandemia + ns(trend_t, knots = knots_main) + factor(region) + offset(log(pop_sens))"))
    mod_k <- glm(fmla, family = poisson, data = panel_k)
    
    vcov_rob <- vcovBS(mod_k, cluster = ~region, R = 999, type = "fractional")
    res <- tryCatch(coeftest(mod_k, vcov = vcov_rob), error=function(e) NULL)
    
    if(!is.null(res)) {
      idx <- grep("trend_t", rownames(res))
      if (length(idx) > 0) {
        results_sens[[length(results_sens) + 1]] <- data.frame(
          Factor_k = k,
          Estimate = res[idx[1], "Estimate"], 
          Std_Error = res[idx[1], "Std. Error"],
          p_value = res[idx[1], "Pr(>|z|)"]
        ) %>% mutate(IRR = exp(Estimate))
      }
    }
  }
  
  tabla_7 <- bind_rows(Filter(Negate(is.null), results_sens))
  write.csv(tabla_7, paste0(out_dir, "/tabla_7_sensibilidad_poblacional.csv"), row.names = FALSE)
}

set.seed(2026)
run_sensitivity("n_violencia_dura", "paper1/output/tables/C3")
run_sensitivity("n_violento_c1", "paper1/output/tables/C1")
run_sensitivity("n_violento_c2", "paper1/output/tables/C2")
message("Fin script 08")
