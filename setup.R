# ============================================================================
# setup.R — Installation et vérification de l'environnement R
# ============================================================================
#
# Usage :
#   source("setup.R")
#
# Ce script vérifie que les packages nécessaires sont installés et affiche
# les versions utilisées pour garantir la reproductibilité des résultats.
# ============================================================================

cat("=== Vérification de l'environnement R ===\n\n")
cat(sprintf("R version : %s\n", R.version.string))

# --- Packages requis ---
packages_requis <- c(
    "fda",      # Analyse de données fonctionnelles (Ramsay & Silverman)
    "fda.usc",  # Jeux Tecator et utilitaires (et fda pour Canadian/Growth)
    "cluster",  # PAM (Partitioning Around Medoids) + silhouette
    "mclust",   # adjustedRandIndex (ARI)
    "fpc"       # nselectboot (instabilité bootstrap, expérience 01)
)

# --- Installation si absent ---
for (pkg in packages_requis) {
    if (!requireNamespace(pkg, quietly = TRUE)) {
        cat(sprintf("  Installation de %s...\n", pkg))
        install.packages(pkg, repos = "https://cloud.r-project.org")
    }
}

# --- Chargement et affichage des versions ---
cat("\nVersions des packages installés :\n")
for (pkg in packages_requis) {
    v <- packageVersion(pkg)
    cat(sprintf("  %-10s : %s\n", pkg, v))
}

# --- Reproductibilité ---
cat("\n--- sessionInfo() complet ---\n")
si <- sessionInfo()
cat(sprintf("Plateforme : %s\n", si$platform))
cat(sprintf("Locale     : %s\n", Sys.getlocale("LC_TIME")))

# Optionnel : sauvegarder sessionInfo pour traçabilité
tryCatch({
  si_file <- "docs/session_info.txt"
  if (dir.exists("docs")) {
    capture.output(sessionInfo(), file = si_file)
    cat(sprintf("\n  sessionInfo() sauvegardé dans %s\n", si_file))
  }
}, error = function(e) invisible(NULL))

cat("\n[OK] Environnement prêt. Vous pouvez lancer : source('src/main.R')\n")
