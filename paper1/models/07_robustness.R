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
  if (is_wcb) vcov_rob <- vcovBS(mod, cluster = ~region, R = 999, type = "fractional")
  else vcov_rob <- vcovHC(mod, type = "HC1")
  
  res <- tryCatch(coeftest(mod, vcov = vcov_rob), error=function(e) NULL)
  if(is.null(res)) return(NULL)
  
  idx <- grep("trend_t", rownames(res))
  if (length(idx) == 0) return(NULL)
  
  df <- data.frame(
    Especificacion = name,
    Estimate = res[idx[1], "Estimate"], 
    Std_Error = res[idx[1], "Std. Error"],
    p_value = res[idx[1], "Pr(>|z|)"]
  ) %>% mutate(IRR = exp(Estimate))
  return(df)
}

run_robustness <- function(var_name, out_dir) {
  results_list <- list()
  
  fmla_R1 <- as.formula(paste0(var_name, " ~ factor(month_of_year) + d_estallido + d_pandemia + ns(trend_t, knots = knots_main) + factor(region) + log(pop_monthly)"))
  results_list[[1]] <- extract_trend(glm(fmla_R1, family=poisson, data=panel), "R1_Offset_Libre")
  
  fmla_R3 <- as.formula(paste0(var_name, " ~ factor(month_of_year) + d_estallido + d_pandemia + ns(trend_t, knots = knots_main) + factor(region) + offset(log(pop_ine))"))
  results_list[[2]] <- extract_trend(glm(fmla_R3, family=poisson, data=panel %>% mutate(pop_ine = ifelse(pop_ine <= 0, 1, pop_ine))), "R3_Sin_SERMIG")
  
  fmla_R5 <- as.formula(paste0(var_name, " ~ factor(month_of_year) + d_estallido + d_pandemia + ns(trend_t, knots = c(25, 49, 97)) + factor(region) + offset(log(pop_monthly))"))
  results_list[[3]] <- extract_trend(glm(fmla_R5, family=poisson, data=panel), "R5_Nodos_Teoricos")
  
  fmla_R6 <- as.formula(paste0(var_name, " ~ factor(month_of_year) + d_estallido + d_pandemia + ns(trend_t, df = 5) + factor(region) + offset(log(pop_monthly))"))
  results_list[[4]] <- extract_trend(glm(fmla_R6, family=poisson, data=panel), "R6_df_5")
  
  tabla_6 <- bind_rows(Filter(Negate(is.null), results_list))
  write.csv(tabla_6, paste0(out_dir, "/tabla_6_robustez.csv"), row.names = FALSE)
}

set.seed(2026)
run_robustness("n_violencia_dura", "paper1/output/tables/C3")
run_robustness("n_violento_c1", "paper1/output/tables/C1")
run_robustness("n_violento_c2", "paper1/output/tables/C2")
message("Fin script 07")
