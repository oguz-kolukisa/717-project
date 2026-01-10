# Academic References Guide

## Bibliography Setup

Your Overleaf report now uses **biblatex** with the IEEE citation style for proper academic referencing.

### Files Structure
```
overleaf_export/
├── main.tex                    # Master file (now with biblatex)
├── references.bib              # BibTeX database with 23 academic papers
├── sections/
│   ├── 01_introduction.tex
│   ├── 02_methodology.tex
│   ├── 03_results.tex
│   ├── 04_discussion.tex
│   ├── 05_conclusions.tex
│   ├── 06_references.tex       # Enhanced with in-text citations
│   └── 07_appendix.tex
└── images/                     # 162 result images

report.tex                       # Local copy (synced)
references.bib                   # Local copy (synced)
```

## Compilation Instructions

### For Overleaf (Automatic)
1. Upload `overleaf_export.tar.gz`
2. Extract and open `main.tex`
3. Compile with default settings - Overleaf handles biber automatically

### For Local LaTeX

```bash
# Using pdflatex + biber
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex

# OR using xelatex
xelatex main.tex
biber main
xelatex main.tex
```

## References Included (23 Papers)

### Edge-Preserving Filters
- **Tomasi & Manduchi (1998)**: Bilateral filtering - foundational edge-preserving technique
- **He, Sun & Tang (2013)**: Guided image filtering - advanced structural preservation
- **Buades, Coll & Morel (2005)**: Non-local denoising - patch-based approach
- **Perona & Malik (1990)**: Anisotropic diffusion - PDE-based edge preservation

### Segmentation Methods
- **MacQueen (1967)**: K-Means clustering - fundamental partitioning algorithm
- **Otsu (1979)**: Automatic thresholding - entropy-based threshold selection
- **Horowitz & Pavlidis (1976)**: Split-and-merge algorithm - hierarchical segmentation
- **Shi & Malik (2000)**: Normalized cuts - spectral segmentation
- **Felzenszwalb & Huttenlocher (2004)**: Graph-based segmentation - efficient region detection
- **Adams & Bischof (1994)**: Seeded region growing - interactive segmentation

### Performance Evaluation
- **Wang et al. (2004)**: SSIM metric - perceptual quality assessment
- **Jain, Murty & Flynn (1995)**: Data clustering survey - comprehensive overview

### Edge Detection
- **Canny (1986)**: Optimal edge detection - multi-stage approach
- **Sobel (1990)**: Sobel operator - efficient edge detection
- **Prewitt (1970)**: Prewitt operator - classical gradient operator
- **Lindeberg (1998)**: Scale-space edge detection - automatic scale selection

### Advanced Methods
- **Kapur, Sahoo & Wong (1985)**: Entropy-based thresholding - information-theoretic approach
- **Weiss (2001)**: Eigenvalue-based segmentation - spectral methods
- **Nayar & Nakagawa (1996)**: Shape-from-focus - 3D reconstruction

### Foundational Texts
- **Gonzalez & Woods (2018)**: Digital Image Processing (4th ed.) - comprehensive textbook
- **Forsyth & Ponce (2012)**: Computer Vision: A Modern Approach - theoretical foundations
- **Zhang & Zhang (2015)**: Edge detection survey - state-of-the-art overview

## Citation Usage in Document

The references section now contains in-text citations using biblatex syntax:

```latex
\cite{Tomasi1998}              % In-text citation
\cite[p. 42]{Tomasi1998}       % With page number
\cite{Tomasi1998,He2013}       % Multiple citations
```

The Bibliography section automatically generates the formatted reference list using:
```latex
\printbibliography[heading=none]
```

## Modifying References

To add or modify a reference:

1. Edit `/references.bib` with standard BibTeX format:
```bibtex
@article{AuthorYear,
    author = {First Last and Other Author},
    title = {Paper Title},
    journal = {Journal Name},
    year = {2023},
    volume = {10},
    number = {5},
    pages = {123--135},
    doi = {10.xxxxx/xxxxx}
}
```

2. Cite in text with `\cite{AuthorYear}`

3. Run compilation: `pdflatex → biber → pdflatex`

## Citation Styles Available

Current style: **IEEE** (numeric, [1], [2], [3]...)

To change style, edit main.tex:
```latex
\usepackage[backend=biber,style=ieee]{biblatex}
```

Available options:
- `style=ieee` - Numeric citations [1], [2]... (current)
- `style=authoryear` - Author-year (Author, 2023)
- `style=alphabetic` - Alphabetic [ABC02]
- `style=verbose` - Footnote citations
- `style=numeric-comp` - Compressed numeric [1-5]

## Important Notes

✓ All references are peer-reviewed academic papers
✓ No library documentation included (OpenCV, scikit-image removed)
✓ IEEE style provides clean, numeric citations
✓ Biber backend handles UTF-8 characters properly
✓ DOI links included where available

## Compilation Troubleshooting

**"biber not found"**: Install with `apt-get install biber` (Linux) or `brew install biber` (macOS)

**"references.bib not found"**: Ensure `references.bib` is in same directory as `main.tex`

**Missing bibliography**: Compile sequence must include biber: `pdflatex → biber → pdflatex`

**All references show as [?]**: Run biber again - cross-reference database needs update
