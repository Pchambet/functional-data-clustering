# Experiments

Protocols and results that go beyond the single-dataset pipeline in
[`src/main.R`](../src/main.R). Detailed protocol notes inside each folder are in French.

| Folder | Question | Entry point |
|---|---|---|
| [`01_instabilite/`](01_instabilite/) | Can bootstrap instability (Fang & Wang, `fpc::nselectboot`) choose k on the (α, ω) grid? Real datasets (21 × 21 grid, B = 150) and simulated scenarios (6 × 6 grid, B = 60, seed 1). | `make exp01`, `make exp01-sim` |
| [`03_simulated_hybride/`](03_simulated_hybride/) | Which fusion strategy recovers the classes when the signal is moved between curves and covariates? 4 scenarios × 50 seeds. | `make exp03` |

Summary of the results: [`../README.md`](../README.md). Full write-up: the project report
[`../docs/rapport_projet_long.pdf`](../docs/rapport_projet_long.pdf) and the stability report
[`01_instabilite/rapport_instabilite.pdf`](01_instabilite/rapport_instabilite.pdf)
(revised to match the result files). The project report (March 2026) predates the
re-analysis in the README; where they differ, the README numbers are the checked ones.
