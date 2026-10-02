# Stability report (experiment 01) — run `make` in this folder.

rapport_instabilite.pdf: rapport_instabilite.tex
	latexmk -pdf -interaction=nonstopmode -halt-on-error $<

clean:
	latexmk -c rapport_instabilite.tex
