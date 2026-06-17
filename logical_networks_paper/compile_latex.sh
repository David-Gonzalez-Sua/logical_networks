#!/bin/bash
# 
# Compile the LaTeX files for the paper.
# Run this script from the 'paper' directory of the project.

pdflatex tex_files/main
# bibtex tex_files/main
biber main
pdflatex tex_files/main
pdflatex tex_files/main

rm *.aux
rm *.bbl
rm *.bcf
rm *.blg
rm *.run.xml
rm *.fff
rm *.toc
rm *.log
