# References

Papers and books the project builds on. Publisher PDFs are not redistributed here;
follow the DOI links.

## Functional data and hybrid PCA

- Ramsay, J. O., & Silverman, B. W. (2005). *Functional Data Analysis* (2nd ed.).
  Springer. [doi:10.1007/b98888](https://doi.org/10.1007/b98888)
  — smoothing, functional PCA; source of the Canadian Weather and Berkeley Growth data.
- Jang, J. H. (2021). Principal component analysis of hybrid functional and vector data.
  *Statistics in Medicine*, 40(24). [doi:10.1002/sim.9117](https://doi.org/10.1002/sim.9117)
  — joint covariance of curve scores and vector covariates; basis of the HFV step
  (`src/02b_pca_hybride_reconstruction.R`).

## Kernel clustering

- Ferreira, M. R. P., & de Carvalho, F. A. T. (2014). Kernel-based hard clustering
  methods in the feature space with automatic variable weighting. *Pattern Recognition*,
  47(9). [doi:10.1016/j.patcog.2014.03.026](https://doi.org/10.1016/j.patcog.2014.03.026)
  — kernel-space clustering framework behind strategy C (product of Gaussian kernels).

## Choosing k and validating partitions

- Rousseeuw, P. J. (1987). Silhouettes: a graphical aid to the interpretation and
  validation of cluster analysis. *Journal of Computational and Applied Mathematics*, 20.
  [doi:10.1016/0377-0427(87)90125-7](https://doi.org/10.1016/0377-0427(87)90125-7)
- Hubert, L., & Arabie, P. (1985). Comparing partitions. *Journal of Classification*, 2.
  [doi:10.1007/BF01908075](https://doi.org/10.1007/BF01908075) — Adjusted Rand Index.
- Dudoit, S., & Fridlyand, J. (2002). A prediction-based resampling method for estimating
  the number of clusters in a dataset (Clest). *Genome Biology*, 3(7).
  [doi:10.1186/gb-2002-3-7-research0036](https://doi.org/10.1186/gb-2002-3-7-research0036)
- Dudoit, S., & Fridlyand, J. (2003). Bagging to improve the accuracy of a clustering
  procedure. *Bioinformatics*, 19(9).
  [doi:10.1093/bioinformatics/btg038](https://doi.org/10.1093/bioinformatics/btg038)
- Wang, J. (2010). Consistent selection of the number of clusters via crossvalidation.
  *Biometrika*, 97(4). [doi:10.1093/biomet/asq061](https://doi.org/10.1093/biomet/asq061)
- Fang, Y., & Wang, J. (2012). Selection of the number of clusters via the bootstrap
  method. *Computational Statistics & Data Analysis*, 56(3).
  [doi:10.1016/j.csda.2011.09.003](https://doi.org/10.1016/j.csda.2011.09.003)
  — implemented in `fpc::nselectboot`, used in `experiments/01_instabilite/`.

## Datasets

All three labelled datasets ship with CRAN packages; nothing is downloaded by hand.

| Dataset | R source | Curve | Covariates | Label |
|---|---|---|---|---|
| Canadian Weather (35 stations) | `fda::CanadianWeather` | daily mean temperature, 365 days | latitude, longitude, mean precipitation | climate region (4) |
| Berkeley Growth (93 children) | `fda::growth` | height at 31 ages, 1–18 years | final height, total growth (both derived from the curve) | sex (2) |
| Tecator (215 meat samples) | `fda.usc::tecator` | NIR absorbance, 100 wavelengths (850–1050 nm) | water, protein content | fat class: <15 %, 15–30 %, >30 % (3) |
