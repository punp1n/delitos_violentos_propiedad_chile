# 04_macrozona_interaction.R — Heterogeneidad espacial por macrozona

library(dplyr)
library(arrow)
library(splines)
library(sandwich)
library(aod)

dir.create("paper1/output/tables/C3", showWarnings = FALSE, recursive = TRUE)
dir.create("paper1/output/tables/C1", showWarnings = FALSE, recursive = TRUE)
dir.create("paper1/output/tables/C2", showWarnings = FALSE, recursive = TRUE)

message("Cargando datos...")
panel <- read_parquet("paper1/output/data/panel_region_month.parquet")

knots_main <- quantile(panel$trend_t, probs = c(0.25, 0.50, 0.75))

run_macrozona <- function(var_name, out_dir) {
  message(sprintf("Ajustando modelo de interacción por Macrozona para %s...", var_name))
  fmla_het <- as.formula(paste0(var_name, " ~ factor(month_of_year) + d_estallido + d_pandemia + ns(trend_t, knots = knots_main) + ns(trend_t, knots = knots_main):factor(macrozona) + factor(region) + offset(log(pop_monthly))"))
  mod_heterog <- glm(fmla_het, family = poisson, data = panel)
  
  message("Calculando WCB (R=9999)...")
  vcov_wcb <- vcovBS(mod_heterog, cluster = ~region, R = 9999, type = "fractional")
  
  terms_macrozona <- grep("macrozona", names(coef(mod_heterog)), value = TRUE)
  idx_terms <- which(names(coef(mod_heterog)) %in% terms_macrozona)
  
  if (length(idx_terms) > 0) {
    wald_res <- wald.test(b = coef(mod_heterog), Sigma = vcov_wcb, Terms = idx_terms)
    sink(paste0(out_dir, "/tabla_heterogeneidad_wald.txt"))
    print(wald_res)
    sink()
  }
  write.csv(data.frame(Term = names(coef(mod_heterog)), Estimate = coef(mod_heterog)), paste0(out_dir, "/tabla_4_macrozona_coefs.csv"), row.names = FALSE)
}

set.seed(2026)
run_macrozona("n_violencia_dura", "paper1/output/tables/C3")
run_macrozona("n_violento_c1", "paper1/output/tables/C1")
run_macrozona("n_violento_c2", "paper1/output/tables/C2")
message("Fin script 04")
