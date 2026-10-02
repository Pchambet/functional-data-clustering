# Results — nselectboot on simulated data (experiment 01, simulated part)

Same scenarios S1–S4 and generator as experiment 03. The committed files come from the
**fast mode** of `../run_simulated_instabilite_only.R` (6 × 6 grid, B = 60, seed 1;
`make exp01-sim`); `--full` runs the 21 × 21 grid with B = 150 used on the real datasets
(several hours).

| File | Content |
|---|---|
| `nselectboot_simulated_all_runs.csv` | long format: `scenario`, `seed`, `k_vrai` (true k), `alpha`, `omega`, `k_opt`, `instability_min`, `stabk` |
| `nselectboot_simulated_summary_by_run.csv` | one row per (scenario, seed): share of the grid where `k_opt` equals the true k, median and mode of `k_opt` |
| `nselectboot_simulated_S*_seed1.csv` | grid used for the heatmaps `../figures/nselectboot_heatmap_sim_*.png` |
