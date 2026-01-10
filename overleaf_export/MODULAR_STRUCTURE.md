# Modular LaTeX Structure

The LaTeX document has been reorganized into separate, manageable section files for better maintainability and collaboration in Overleaf.

## File Organization

```
main.tex                          # Master file (imports all sections)
├── sections/
│   ├── 01_introduction.tex       # Background, filters, segmentation, metrics
│   ├── 02_methodology.tex        # Experimental setup, noise model, implementation
│   ├── 03_results.tex            # Filter and segmentation performance data, figures
│   ├── 04_discussion.tex         # Analysis, recommendations, clinical implications
│   ├── 05_conclusions.tex        # Summary, clinical workflow, limitations
│   ├── 06_references.tex         # Bibliography
│   └── 07_appendix.tex           # Implementation code, reproduction instructions
├── images/
│   ├── step1/                    # 54 filter evaluation results
│   └── step2/                    # 108 segmentation results
```

## Benefits of Modular Structure

1. **Easier Collaboration**: Multiple people can edit different sections simultaneously
2. **Better Organization**: Each section is self-contained and focused
3. **Faster Compilation**: Smaller files compile quicker during editing
4. **Easy Updates**: Modify specific sections without touching the entire document
5. **Cleaner Git History**: Track changes per section more effectively

## How to Use

### Overleaf:
1. Upload the `main.tex` along with the `sections/` folder
2. All imports will automatically resolve
3. Compile normally with the "Compile" button

### Local Compilation:
```bash
pdflatex main.tex      # Compile main file
# or
xelatex main.tex       # Alternative TeX engine
```

## Customization

### To edit a section:
Open the corresponding `.tex` file in `sections/` and make your changes.

### To add a new section:
1. Create a new file (e.g., `08_custom.tex`) in `sections/`
2. Add this line to `main.tex`: `\input{sections/08_custom}`

### To reorder sections:
Simply change the order of `\input{}` commands in `main.tex`.

### To temporarily skip a section:
Comment out its line in `main.tex`:
```tex
% \input{sections/03_results}
```

## File Sizes

- **main.tex**: 75 lines (header, abstract, imports)
- **01_introduction.tex**: 85 lines
- **02_methodology.tex**: 70 lines
- **03_results.tex**: 170 lines
- **04_discussion.tex**: 102 lines
- **05_conclusions.tex**: 63 lines
- **06_references.tex**: 34 lines
- **07_appendix.tex**: 118 lines

**Total**: ~75 + 642 = ~717 content lines (same as original)

## Important Notes

- The `sections/` folder must be in the same directory as `main.tex`
- Image paths are relative to the main document location
- All LaTeX packages and settings are defined in the preamble of `main.tex`
- The document can be compiled successfully with Overleaf's default LaTeX distribution

## Version Control

When using Git:
```bash
git add main.tex sections/        # Track modular structure
git commit -m "Modular LaTeX setup"
```

This makes it easy to see which sections changed in each commit.
