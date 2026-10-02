# Entry points — run from the repository root.
#   make setup      install / check the R packages (fda, fda.usc, cluster, mclust, fpc)
#   make pipeline   smoothing -> FPCA -> distances -> clustering on the 3 labelled datasets
#   make exp01      bootstrap instability (fpc::nselectboot) on the (alpha, omega) grid — hours
#   make exp03      simulated benchmark, 4 scenarios x 50 seeds — hours
#   make tables     regenerate the LaTeX tables in docs/generated/ from the result CSVs
#   make report     compile docs/rapport_stage.pdf and the stability report
#   make figures    rebuild the README figures from the committed result tables (Python, uv)
#   make check      verify README figures and numbers against the result tables

R_LOOP = for (d in c("canadian", "growth", "tecator")) { DATASET <<- d; source("src/main.R") }

.PHONY: all setup pipeline exp01 exp03 tables report figures check clean

all: pipeline exp01 exp03 tables report figures

setup:
	Rscript setup.R

pipeline:
	CNAM_EXPORT_COMPARAISON=1 Rscript -e 'source("setup.R"); $(R_LOOP)'

exp01:
	Rscript -e 'source("experiments/01_instabilite/run_all_complete.R")'

exp03:
	Rscript -e 'source("experiments/03_simulated_hybride/benchmark_all_methods_simulated.R")'

tables:
	$(MAKE) -C docs tables

report:
	$(MAKE) -C docs
	$(MAKE) -C experiments/01_instabilite

figures:
	uv run --locked --script scripts/readme_figures.py

check:
	uv run --locked --script scripts/readme_figures.py --check

clean:
	$(MAKE) -C docs clean
	$(MAKE) -C experiments/01_instabilite clean
