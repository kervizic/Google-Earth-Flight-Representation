pdflatex global.tex
bibtex global.aux
pdflatex global.tex
latex2rtf global.tex
pdftk tex/pageDeGarde.pdf global.pdf cat output KERVIZIC_Emmanuel_SEI0910_Rapport_final.pdf
evince KERVIZIC_Emmanuel_SEI0910_Rapport_final.pdf
