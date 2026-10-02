# 01 — Choix de \(k\) par instabilité bootstrap (Fang & Wang, 2012)

**Source article** : Fang & Wang (2012), *Computational Statistics and Data Analysis*.  
**Implémentation** : `fpc::nselectboot` (package R **fpc**).

## Idée

Pour chaque couple **(\(\alpha\), \(\omega\))** de la grille, on construit la distance mixte **\(D_w(\alpha,\omega)\)** (même pipeline que le projet : lissage, FPCA, distances).  
On estime, par **bootstrap**, une **instabilité** des partitions pour chaque **\(k\)** candidat ; le **\(k\)** qui minimise l’instabilité moyenne est retenu pour ce couple.

Une grille complète en **(\(\alpha\), \(\omega\))** (ici 21×21, pas 0,05) permet de cartographier **\(k_\text{opt}(\alpha,\omega)\)** et de tracer des heatmaps d’instabilité.

## Scripts (pipeline actuel)

| Script | Rôle |
|--------|------|
| **`run_all_nselectboot.R`** | 3 datasets réels (Canadian, Growth, Tecator ; hors AEMET), \(B=150\), grille 21×21 ; **optionnel** ensuite le volet simulé (voir ci-dessous) |
| **`run_nselectboot.R`** | Un dataset (`DATASET` défini avant `source`) |
| **`run_nselectboot_simulated.R`** | **Enrichissement** : mêmes paramètres nselectboot sur données **simulées** (Cas2_deriv, aligné exp. 3). Sorties dans `results_simulated/`. N’altère pas `experiments/03_simulated_hybride/`. |
| **`analyse_nselectboot.R`** | Heatmaps `experiments/01_instabilite/figures/nselectboot_heatmap_*.png` (3 jeux réels) — intégrées au mémoire `docs/rapport_projet_long.tex` |
| **`analyse_nselectboot_simulated.R`** | Heatmaps `experiments/01_instabilite/figures/nselectboot_heatmap_sim_*.png` (scénarios S1–S4, seed de référence) |
| **`generate_confusion_nselectboot.R`** | Matrices `confusion_nselectboot_*.csv` (règle : premier couple avec \(k_\text{opt}=k_\text{vrai}\), sinon le plus proche) — **jeux réels uniquement** |
| **`run_all_complete.R`** | Enchaîne : nselectboot (3 réels **+** volet simulé activé) → heatmaps réels → heatmaps simulés → confusion |
| **`run_simulated_instabilite_only.R`** | **Simulé seulement** : nselectboot + heatmaps. **Par défaut** : mode rapide (grille 6×6, `B=60`, ~15–25 min). **`--full`** : 21×21 et `B=150` comme les jeux réels (très long). |
| **`rapport_instabilite.tex`** | Rapport PDF **d’instabilité** (exp. 1). Compilation : `make` dans ce dossier |

### Volet simulé (complément contrôlé)

- **Objectif** : sous **\(k\)** et labels connus, évaluer le comportement de nselectboot avec le **même** pipeline (lissage, FPCA, distances) que sur les vraies données — **sans remplacer** l’évaluation empirique sur les 3 jeux réels.
- **Activation** : dans `run_all_nselectboot.R`, définir avant `source` : `RUN_NSELECTBOOT_SIMULATED <- TRUE`. Par défaut le volet simulé est **désactivé** pour limiter le coût CPU ; `run_all_complete.R` l’**active** automatiquement.
- **Paramètres** : `SEEDS_SIM` (défaut `1L` ; pour alignement complet avec le benchmark exp. 3 : `1:50`), `P_Z_SIM` (défaut 20), `REFERENCE_SEED` pour les CSV « référence » heatmaps (**défaut = premier élément de `SEEDS_SIM`**, pas le seed 42). Voir `results_simulated/README.md`.
- **Limites** : le générateur Cas2_deriv n’est pas le « monde réel » ; les conclusions sur la méthode restent **conditionnelles** à ce modèle. Toujours présenter les résultats réels en parallèle dans le rapport.

## Ancien protocole « stabilité » (hors pipeline)

Un prototype ad hoc (bootstrap + ARI sur sous-échantillon 80 %) **sans article de référence** a été retiré du pipeline. Les scripts correspondants sont dans **`archive/`** (voir `archive/README.md`).

## Paramètres modifiables

Dans **`run_all_nselectboot.R`** : `B_NSELECT`, `ALPHAS_NB`, `OMEGAS_NB`, `K_RANGE` — **référence commune** pour les trois jeux réels et, si activé, pour le **volet simulé** (mêmes valeurs re-verrouillées avant `run_nselectboot_simulated.R`).

Pour le **volet simulé** seuls varient en principe : `SEEDS_SIM` (défaut `1L` ; benchmark exp. 3 : `1:50`), `P_Z_SIM`, générateur Cas2\_deriv (`NC_SIM`, `DELTA_SIM`, etc., alignés exp. 3).

**Parité stricte nselectboot (recommandée pour comparer au réel)** : \(B=150\), grille \(21\times21\) avec pas \(0{,}05\) sur \(\alpha\) et \(\omega\), `K_RANGE = 2:6`. Le script impose ces valeurs par défaut et **refuse** une autre grille sauf **`NSELECTBOOT_SIM_RELAXED <- TRUE`** (débogage uniquement).

## Références

- Fang, Y., Wang, J. (2012). Selection of the number of clusters via the bootstrap method.
- Liste complète avec DOI : [`docs/biblio/README.md`](../../docs/biblio/README.md).
