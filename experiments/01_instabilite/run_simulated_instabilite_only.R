# ============================================================================
# Expérience 01 — Volet simulé uniquement (sans toucher aux 3 jeux réels)
# ============================================================================
#
# Enchaîne : nselectboot sur données simulées → heatmaps dans figures/
#
# Usage (depuis la racine du dépôt) :
#   Rscript experiments/01_instabilite/run_simulated_instabilite_only.R
#
# Mode COMPLET (long : grille 21×21, B=150, aligné jeux réels) :
#   Rscript experiments/01_instabilite/run_simulated_instabilite_only.R --full
#
# Le mode par défaut est RAPIDE (~15–25 min selon machine) : grille 6×6 (pas 0.2),
# B=60 — pas comparable aux heatmaps réelles en précision ; documenter dans le rapport.
#
# ============================================================================

if (!file.exists("experiments/01_instabilite/run_simulated_instabilite_only.R")) {
  stop("Run from the repository root (see the Makefile).")
}

args <- commandArgs(trailingOnly = TRUE)
use_full <- "--full" %in% args || identical(Sys.getenv("CNAM_SIM_NSELECTBOOT_FULL", ""), "1")

if (use_full) {
  cat(">>> Mode COMPLET : grille 21×21, B=150 (aligné jeux réels) — très long.\n\n")
  cat(">>> Étape 1/2 : nselectboot simulé\n")
} else {
  # Rapide : documenter l’écart dans le rapport / protocole
  NSELECTBOOT_SIM_RELAXED <- TRUE
  B_NSELECT <- 60L
  ALPHAS_NB <- seq(0, 1, by = 0.2)   # 6 points → 6×6 = 36 couples par scénario
  OMEGAS_NB <- seq(0, 1, by = 0.2)
  K_RANGE <- 2:6
  cat(">>> Mode RAPIDE (~15–25 min) : grille 6×6 (pas 0,2), B=60 — pas le même protocole que les 3 jeux réels (21×21, B=150).\n\n")
  cat(">>> Étape 1/2 : nselectboot simulé\n")
}

source("experiments/01_instabilite/run_nselectboot_simulated.R", local = FALSE)
cat("\n")

cat(">>> Étape 2/2 : Heatmaps instabilité (données simulées)\n")
source("experiments/01_instabilite/analyse_nselectboot_simulated.R", local = FALSE)
cat("\n")

cat("══════════════════════════════════════════════════════════════════════\n")
cat("  TERMINÉ. Résultats : results_simulated/ — figures : figures/nselectboot_heatmap_sim_*.png\n")
cat("  Compiler le rapport : make (depuis experiments/01_instabilite/)\n")
cat("══════════════════════════════════════════════════════════════════════\n\n")
