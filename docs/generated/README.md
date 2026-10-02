# Generated LaTeX tables

Do not edit by hand; regenerate with `make tables` from the repository root.

- `benchmark_ari_by_scenario.tex` — ARI and mean silhouette per method and simulated scenario
  (report chapter 5), from the CSVs of `experiments/03_simulated_hybride/results/`
  (`scripts/generate_rapport_stage_benchmark_tex.R`).
- `paradox_silhouette_ari.tex` — silhouette/ARI paradox for strategy B on the three real
  datasets (chapter 4); recomputes the grids (`scripts/generate_rapport_stage_paradox_tex.R`).
- `ch6_real_three_games_table.tex` — six methods on Canadian Weather, Growth and Tecator
  (chapter 6), from `docs/exports/comparaison_*.csv` written by `make pipeline`
  (`scripts/generate_ch6_three_games_table_tex.R`).
