# Manifeste — benchmark données simulées (expérience 03)

**Objectif.** Figer les paramètres qui identifient les sorties CSV du dossier `results/` — à jour après chaque `source("experiments/03_simulated_hybride/benchmark_all_methods_simulated.R")`.

## Générateur

- **Fonction** : `Cas2_deriv` dans `src/simulate_cas2_deriv.R`
- **Entrée pipeline** : `src/00_preprocess_simulated.R`
- **Effectifs** : `NC_SIM = c(100, 100, 100)` → \(n=300\), \(K=3\)
- **Grille temporelle** : `LEN_T_SIM = 60` → \(N=60\) points sur \([0,1]\)
- **Bloc vectoriel** : `P_Z_SIM = 20` (par défaut)
- **Bruit** : `SIGMA2_SIM = 0.2`, `TAU2_SIM = 0.2`
- **Scénarios** \(\delta=(\delta_1,\delta_2,\delta_3)\) :
  - S1 `(1, 1, 1)`
  - S2 `(1, 1, 0.5)` — affaiblit la séparation des moyennes de \(Z\) (\(\delta_3\))
  - S3 `(0.5, 0.5, 1)` — affaiblit niveau et dérivée fonctionnels
  - S4 `(0.5, 0.5, 0.5)` — affaiblissement global

## Benchmark méthodes

- **Script** : `experiments/03_simulated_hybride/benchmark_all_methods_simulated.R`
- **Graines** : `SEEDS = 1:50` par scénario
- **Grille hyperparamètres** (alignée sur `src/03_distances.R`) : $\alpha \in \{0, 0{,}05, \ldots, 1\}$ (21 valeurs) ; pour la stratégie B, $(\alpha,\omega)$ sur une grille **$21 \times 21$** (pas $0{,}05$) ; même pas pour $D_f(\alpha)$ dans le benchmark.
- **Méthodes** : voir en-tête du script (baselines `D0`, `D1`, `Df_silopt`, `Ds`, stratégies A, B, C, `DK_reconstruit`)
- **Règle** : hyperparamètres par silhouette où requis ; **ARI uniquement en évaluation**

## Fichiers de sortie canoniques

- `metrics_all_runs.csv`
- `metrics_summary_by_scenario_method.csv`
- `metrics_global_average_by_method.csv`
- `ranking_by_scenario.csv`
- `confusion_<scenario>_<methode>.csv` (graine de référence 42)

## Mémoire LaTeX

- Fragment tableau ARI : `docs/generated/benchmark_ari_by_scenario.tex`
- **Régénération** : `Rscript scripts/generate_rapport_stage_benchmark_tex.R` (depuis la racine du dépôt)
- **Journal d’un run complet** (optionnel, `tee`) : `experiments/03_simulated_hybride/benchmark_full_run.log`

## Note (versions antérieures)

Les CSV produits avant correction du script pouvaient nommer `delta2` dans `metrics_all_runs.csv` alors qu’il s’agissait de \(\delta_3\) (bug de colonne). Les agrégats **ARI** n’en étaient pas affectés. Les nouveaux runs écrivent `delta1`, `delta2`, `delta3` correctement.
