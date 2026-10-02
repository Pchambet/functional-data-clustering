# LaTeX documents — run `make -C docs` from the repository root.
# The thesis reads the tables in generated/ (regenerate with `make tables`)
# and the figures in ../figures/ and ../experiments/01_instabilite/figures/.

LATEXMK = latexmk -pdf -interaction=nonstopmode -halt-on-error

.PHONY: all tables clean

all: rapport_stage.pdf soutenance.pdf

%.pdf: %.tex
	$(LATEXMK) $<

# Simulated benchmark table (chapter 5), silhouette/ARI paradox (chapter 4,
# recomputes the grids, needs R), real-data table (chapter 6, needs the
# docs/exports/ CSVs written by `make pipeline`).
tables:
	cd .. && Rscript scripts/generate_rapport_stage_benchmark_tex.R
	cd .. && Rscript scripts/generate_rapport_stage_paradox_tex.R
	cd .. && Rscript scripts/generate_ch6_three_games_table_tex.R

clean:
	latexmk -c rapport_stage.tex soutenance.tex
