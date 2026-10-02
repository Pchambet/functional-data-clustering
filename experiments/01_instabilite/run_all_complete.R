# ============================================================================
# Exécution complète — Expérience 01 (instabilité / nselectboot uniquement)
# ============================================================================
# nselectboot → heatmaps instabilité → matrices de confusion
#
# Usage : Rscript experiments/01_instabilite/run_all_complete.R
# Ou : source("experiments/01_instabilite/run_all_complete.R")
# ============================================================================

if (!file.exists("experiments/01_instabilite/run_all_complete.R")) {
  stop("Run from the repository root (see the Makefile).")
}

# Exécution complète : inclure le volet simulé après les 3 jeux réels (voir protocole.md)
if (!exists("RUN_NSELECTBOOT_SIMULATED")) RUN_NSELECTBOOT_SIMULATED <- TRUE

cat("\n")
cat("══════════════════════════════════════════════════════════════════════\n")
cat("  EXÉCUTION COMPLÈTE — Expérience 01 (instabilité / nselectboot)\n")
cat("══════════════════════════════════════════════════════════════════════\n\n")

cat(">>> Étape 1/4 : nselectboot (3 datasets, B=150, grille 21×21",
    if (RUN_NSELECTBOOT_SIMULATED) " + volet simulé" else "", ")\n", sep = "")
source("experiments/01_instabilite/run_all_nselectboot.R", local = FALSE)
cat("\n")

cat(">>> Étape 2/4 : Heatmaps instabilité (nselectboot, 3 jeux réels)\n")
source("experiments/01_instabilite/analyse_nselectboot.R", local = FALSE)
cat("\n")

cat(">>> Étape 3/4 : Heatmaps instabilité (nselectboot, données simulées)\n")
source("experiments/01_instabilite/analyse_nselectboot_simulated.R", local = FALSE)
cat("\n")

cat(">>> Étape 4/4 : Matrices de confusion (nselectboot, jeux réels)\n")
source("experiments/01_instabilite/generate_confusion_nselectboot.R", local = FALSE)
cat("\n")

cat("══════════════════════════════════════════════════════════════════════\n")
cat("  TERMINÉ. Compiler le rapport : make (depuis experiments/01_instabilite/)\n")
cat("══════════════════════════════════════════════════════════════════════\n\n")
