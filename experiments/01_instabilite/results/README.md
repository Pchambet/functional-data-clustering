# Results — experiment 01 (bootstrap instability, `fpc::nselectboot`)

- `nselectboot_<dataset>.csv` — one row per (α, ω) on the 21 × 21 grid (step 0.05),
  B = 150 bootstrap replicates, k ∈ {2, …, 6}. Columns: `k_opt` (k with the lowest
  instability) and `stabk` (instability for k = 1…6, `;`-separated).
- `confusion_nselectboot_<dataset>.csv` — confusion matrix of the partition at the first
  grid point whose `k_opt` equals the true number of classes (otherwise the closest one),
  see `../generate_confusion_nselectboot.R`.
- `clest_prototype_canadian.csv` — standalone Clest prototype, not part of
  `run_all_complete.R`.

Heatmaps: `../figures/nselectboot_heatmap_<dataset>.png`, regenerated with
`Rscript -e 'source("experiments/01_instabilite/analyse_nselectboot.R")'` from the
repository root.
