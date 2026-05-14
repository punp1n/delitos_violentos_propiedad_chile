# 03_regional_cusum_fdr.R — CUSUM-GLM regional + FDR + Bai-Perron
# rev.2: Agrega Bai-Perron sin punto pre-especificado

library(dplyr)
library(arrow)
library(strucchange)
library(sandwich)
library(ggplot2)
library(lubridate)

for (d in c("C3", "C1", "C2")) {
  dir.create(paste0("paper1/output/tables/", d), showWarnings = FALSE, recursive = TRUE)
}

message("Cargando datos...")
panel <- read_parquet("paper1/output/data/panel_region_month.parquet") %>%
  mutate(date = make_date(year, month, 1))

# ───────────────────────────────────────────────────
# A) CUSUM-GLM Regional con corrección FDR
# ───────────────────────────────────────────────────
run_regional_cusum <- function(var_name) {
  message(sprintf("Ejecutando CUSUM-GLM regional para %s...", var_name))
  results <- list()
  plot_data_list <- list()

  for (reg in sort(unique(panel$region))) {
    data_r <- panel[panel$region == reg, ]
    data_r <- data_r[order(data_r$trend_t), ]

    fmla <- as.formula(paste0(var_name, " ~ factor(month_of_year) + d_estallido + d_pandemia + offset(log(pop_monthly))"))
    glm_r <- glm(fmla, family = poisson, data = data_r)

    # Proceso empírico de fluctuación CUSUM
    gefp_r <- tryCatch(
      {
        gefp(glm_r, fit = NULL, order.by = data_r$trend_t)
      },
      error = function(e) NULL
    )

    if (!is.null(gefp_r)) {
      test_r <- sctest(gefp_r, functional = maxBB)

      # El proceso de fluctuación es una matriz N+1 x K.
      # Para maxBB, tomamos el máximo absoluto por fila y excluimos t=0.
      process <- apply(abs(gefp_r$process), 1, max)[-1]
      max_idx <- which.max(process)
      break_month <- data_r$yyyymm[max_idx]

      results[[length(results) + 1]] <- data.frame(
        Region = reg,
        Categoria = var_name,
        Test_Stat = test_r$statistic,
        p_value_raw = test_r$p.value,
        Est_Break_YYYYMM = break_month
      )

      plot_data_list[[length(plot_data_list) + 1]] <- data.frame(
        Region = reg,
        Categoria = var_name,
        Date = data_r$date,
        Process = process
      )
    }
  }

  res_df <- bind_rows(results)
  # Corrección de Benjamini-Hochberg (FDR)
  res_df$p_value_fdr <- p.adjust(res_df$p_value_raw, method = "BH")
  return(list(results = res_df, plot_data = bind_rows(plot_data_list)))
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
      n_total = if (!is.null(var_name_total)) {
        sum(.data[[var_name_total]], na.rm = TRUE)
      } else {
        sum(n_robos_violentos + n_robos_sorpresa + n_robos_no_violentos, na.rm = TRUE)
      },
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
  bp <- tryCatch(
    {
      breakpoints(bp_formula, data = panel_nacional, h = 0.15) # mínimal segmento 15%
    },
    error = function(e) {
      message(sprintf("  Error en Bai-Perron: %s", e$message))
      NULL
    }
  )

  if (!is.null(bp)) {
    # Extraer puntos de quiebre óptimos (por BIC)
    optimal_breaks <- tryCatch(breakpoints(bp)$breakpoints, error = function(e) NA)

    if (!any(is.na(optimal_breaks))) {
      break_dates <- panel_nacional$yyyymm[optimal_breaks]
      break_ratios <- panel_nacional$ratio_desest[optimal_breaks]

      # BIC via AIC con k=log(n)
      bic_val <- tryCatch(AIC(bp, k = log(nrow(panel_nacional))), error = function(e) NA)

      bp_results <- data.frame(
        Categoria = var_name_violent,
        N_Breaks_Optimal = length(optimal_breaks),
        Break_Positions = paste(optimal_breaks, collapse = ","),
        Break_YYYYMM = paste(break_dates, collapse = ","),
        Break_Ratios = paste(round(break_ratios, 4), collapse = ","),
        BIC = as.numeric(bic_val[1])
      )
    } else {
      bp_results <- data.frame(
        Categoria = var_name_violent,
        N_Breaks_Optimal = 0,
        Break_Positions = "none",
        Break_YYYYMM = "none",
        Break_Ratios = "none",
        BIC = NA_real_
      )
    }

    # También reportar intervalos de confianza para los quiebres
    bp_ftest <- tryCatch(
      {
        ci <- confint(bp, vcov. = vcovHAC)
        ci_mat <- ci$confint
        data.frame(
          Break_Idx = ci_mat[, "breakpoints"],
          CI_lower = ci_mat[, 1],
          CI_upper = ci_mat[, 3],
          YYYYMM = panel_nacional$yyyymm[ci_mat[, "breakpoints"]]
        )
      },
      error = function(e) NULL
    )

    return(list(summary = bp_results, ci = bp_ftest, bp_object = bp))
  }
  return(NULL)
}

set.seed(2026)

# ─── CUSUM ───
# C3
res_cusum_c3_obj <- run_regional_cusum("n_robos_violentos")
write.csv(res_cusum_c3_obj$results, "paper1/output/tables/C3/tabla_3_cusum_fdr.csv", row.names = FALSE)

# C1
res_cusum_c1_obj <- run_regional_cusum("n_violento_c1")
write.csv(res_cusum_c1_obj$results, "paper1/output/tables/C1/tabla_3_cusum_fdr.csv", row.names = FALSE)

# C2
res_cusum_c2_obj <- run_regional_cusum("n_violento_c2")
write.csv(res_cusum_c2_obj$results, "paper1/output/tables/C2/tabla_3_cusum_fdr.csv", row.names = FALSE)

message("CUSUM finalizado para las tres clasificaciones.")

# ─── Bai-Perron ───
message("\n=== Bai-Perron (sin punto pre-especificado) ===")

bp_c3 <- run_bai_perron("n_robos_violentos")
if (!is.null(bp_c3)) {
  write.csv(bp_c3$summary, "paper1/output/tables/C3/bai_perron_results.csv", row.names = FALSE)
  if (!is.null(bp_c3$ci)) {
    write.csv(bp_c3$ci, "paper1/output/tables/C3/bai_perron_ci.csv", row.names = FALSE)
  }
  sink("paper1/output/tables/C3/bai_perron_summary.txt")
  cat("=== Bai-Perron: Robos violentos (C3) ===\n\n")
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

# ───────────────────────────────────────────────────
# C) Generar Figura 4: Panel CUSUM-GLM 4x4
# ───────────────────────────────────────────────────
message("\n=== Generando Figura 4: CUSUM-GLM Facet 4x4 ===")
plot_df <- res_cusum_c3_obj$plot_data
res_df <- res_cusum_c3_obj$results

if (nrow(plot_df) > 0) {
  # Nombres de regiones
  nombres_regiones <- c(
    "1" = "Tarapacá", "2" = "Antofagasta", "3" = "Atacama", "4" = "Coquimbo",
    "5" = "Valparaíso", "6" = "O'Higgins", "7" = "Maule", "8" = "Biobío",
    "9" = "La Araucanía", "10" = "Los Lagos", "11" = "Aysén", "12" = "Magallanes",
    "13" = "RM", "14" = "Los Ríos", "15" = "Arica y Parinacota", "16" = "Ñuble"
  )

  # Añadir etiqueta para el facet con p-valor
  plot_df <- plot_df %>%
    left_join(res_df %>% select(Region, p_value_fdr), by = "Region") %>%
    mutate(
      NombreRegion = nombres_regiones[as.character(Region)],
      Facet_Label = sprintf("%s (p=%.3f)", NombreRegion, p_value_fdr)
    )

  # Límite crítico asintótico (Brownian Bridge maxBB 5%)
  bound_val <- 1.358

  fig_4 <- ggplot(plot_df, aes(x = Date, y = Process)) +
    # Líneas de significancia
    geom_hline(yintercept = c(-bound_val, bound_val), color = "#e34a33", linetype = "dashed", alpha = 0.7) +
    # Línea origen
    geom_hline(yintercept = 0, color = "black", linewidth = 0.3) +
    # Serie de score
    geom_line(color = "#2c7fb8", linewidth = 0.9) +
    facet_wrap(~Facet_Label, ncol = 4) +
    theme_minimal(base_family = "sans", base_size = 11) +
    labs(
      title = NULL,
      subtitle = NULL,
      x = NULL, y = "Proceso Empírico"
    ) +
    theme(
      strip.background = element_rect(fill = "#f2f0f7", color = NA),
      strip.text = element_text(face = "bold", size = 9, color = "#252525"),
      panel.grid.minor = element_blank(),
      panel.border = element_rect(color = "#e5e5e5", fill = NA, linewidth = 0.5),
      plot.title = element_blank(),
      plot.subtitle = element_blank()
    )

  ggsave("paper1/output/figures/fig4_cusum_regional_facet.png", fig_4, width = 12, height = 9, dpi = 300)
  ggsave("paper1/output/figures/fig4_cusum_regional_facet.pdf", fig_4, width = 12, height = 9)
  
  # English version
  fig_4_eng <- ggplot(plot_df, aes(x = Date, y = Process)) +
    geom_hline(yintercept = c(-bound_val, bound_val), color = "#e34a33", linetype = "dashed", alpha = 0.7) +
    geom_hline(yintercept = 0, color = "black", linewidth = 0.3) +
    geom_line(color = "#2c7fb8", linewidth = 0.9) +
    facet_wrap(~Facet_Label, ncol = 4) +
    theme_minimal(base_family = "sans", base_size = 11) +
    labs(
      title = NULL,
      subtitle = NULL,
      x = NULL, y = "Empirical Process"
    ) +
    theme(
      strip.background = element_rect(fill = "#f2f0f7", color = NA),
      strip.text = element_text(face = "bold", size = 9, color = "#252525"),
      panel.grid.minor = element_blank(),
      panel.border = element_rect(color = "#e5e5e5", fill = NA, linewidth = 0.5),
      plot.title = element_blank(),
      plot.subtitle = element_blank()
    )

  ggsave("paper1/output/figures/fig4_cusum_regional_facet_eng.png", fig_4_eng, width = 12, height = 9, dpi = 300)
  ggsave("paper1/output/figures/fig4_cusum_regional_facet_eng.pdf", fig_4_eng, width = 12, height = 9)
  
  message("Figura 4 guardada con éxito.")
}
