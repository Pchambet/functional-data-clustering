# Simulated benchmark — summary (4 scenarios × 50 seeds)

Detailed report (French): [`../RAPPORT_DETAILLE_EXPERIENCE_03.md`](../RAPPORT_DETAILLE_EXPERIENCE_03.md).
Output files and metric definitions: [`../PROTOCOLE_SORTIES.md`](../PROTOCOLE_SORTIES.md).

## Protocol

- Generator `Cas2_deriv` ([`src/simulate_cas2_deriv.R`](../../../src/simulate_cas2_deriv.R)):
  K = 3 classes of 100, curves on N = 60 points of [0, 1], covariate block of p = 20.
- Scenarios δ = (δ₁ curve level, δ₂ curve derivative, δ₃ covariate means):
  S1 (1, 1, 1), S2 (1, 1, 0.5), S3 (0.5, 0.5, 1), S4 (0.5, 0.5, 0.5).
- Seeds 1–50 per scenario. Hyperparameters (α, ω) chosen by silhouette on a 21 × 21 grid; the
  ARI is used only to evaluate the final partitions.

## Mean ARI (from `metrics_summary_by_scenario_method.csv`)

| Method | S1 | S2 | S3 | S4 | All |
|---|---|---|---|---|---|
| `D0` curves, level | 0.830 | 0.830 | 0.226 | 0.226 | 0.528 |
| `D1` curves, derivative | 0.873 | 0.873 | 0.378 | **0.378** | 0.626 |
| `Df_silopt` curves, Dp(α) | 0.873 | 0.873 | 0.237 | 0.237 | 0.555 |
| `Ds` covariates | 0.567 | 0.333 | 0.511 | 0.247 | 0.414 |
| `A` FPCA + Z, k-means | 0.782 | 0.524 | **0.623** | 0.315 | 0.561 |
| `B_silopt` Dw(α, ω) | 0.873 | 0.873 | 0.239 | 0.238 | 0.556 |
| `C_DK_ancien` kernel product | **0.938** | **0.887** | 0.464 | 0.317 | **0.651** |
| `DK_reconstruit` HFV + DK | 0.897 | 0.802 | 0.433 | 0.301 | 0.608 |

## Reading

- While the curves separate the classes (S1, S2) the kernel product C leads; the
  silhouette-tuned B and Dp(α) collapse to the derivative distance D1 (same ARI, 0.873).
- When the curve signal is halved (S3), B still picks a curves-only corner and drops to 0.239,
  while FPCA + k-means (A) and the covariates alone (Ds) do best.
- The HFV reconstruction (DK_reconstruit) is below C in every scenario on average.
- Silhouette is highest for B / Dp(α) (≈ 0.29) and among the lowest for C / HFV (0.12–0.13), the opposite of
  the ARI ranking: the silhouette/ARI paradox.
