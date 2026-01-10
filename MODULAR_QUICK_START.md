# Overleaf Import Guide - Modular Structure

## Quick Start

Your LaTeX project is now **modular** - each section is in its own file for easy editing and collaboration!

### What Changed?
- **Before**: Single 718-line `main.tex` file
- **After**: `main.tex` (75 lines) + 7 section files (648 lines total)

### ✅ How to Use in Overleaf

1. **Upload the ZIP file**:
   - Download `overleaf_export.zip`
   - Go to https://www.overleaf.com
   - Click "New Project" → "Upload Project"
   - Select the ZIP file and upload

2. **Compile immediately**:
   - Overleaf auto-detects `main.tex`
   - Click "Compile" button
   - PDF generates with all sections

3. **Edit sections independently**:
   - Left sidebar shows file structure
   - Click `sections/01_introduction.tex` to edit introduction
   - Click `sections/03_results.tex` to add/modify results
   - Changes auto-save and auto-compile

## File Organization

```
main.tex (master file - imports all sections)
│
├─ sections/
│  ├─ 01_introduction.tex ......... Background, theory, metrics
│  ├─ 02_methodology.tex .......... Experimental setup, noise model
│  ├─ 03_results.tex ............ Filter & segmentation results
│  ├─ 04_discussion.tex ........ Analysis & recommendations
│  ├─ 05_conclusions.tex ....... Clinical implications
│  ├─ 06_references.tex ........ Bibliography
│  └─ 07_appendix.tex ......... Code & instructions
│
├─ images/
│  ├─ step1/ (54 PNG files) ... Filter evaluations
│  └─ step2/ (108 PNG files) .. Segmentation results
│
└─ README.txt, OVERLEAF_INSTRUCTIONS.txt, MODULAR_STRUCTURE.md
```

## Working with Sections

### ✏️ Edit a Section
1. Open the section file from the sidebar
2. Make your changes
3. Overleaf auto-saves and recompiles
4. PDF updates automatically

### ➕ Add a New Section
1. Create new file: Click "+" → "From file name" in Overleaf
2. Name it: `08_newsection.tex`
3. Add content
4. In `main.tex`, add: `\input{sections/08_newsection}`
5. Add `\newpage` before it if you want a page break

### 🔄 Reorder Sections
Edit `main.tex` and change the order of `\input{}` commands:
```latex
% Current order:
\input{sections/03_results}    % Results first
\input{sections/04_discussion} % Discussion second

% Change to:
\input{sections/04_discussion} % Discussion first
\input{sections/03_results}    % Results second
```

### 💬 Hide a Section (Temporary)
Comment out its line in `main.tex`:
```latex
% \input{sections/03_results}  % This section won't appear
```

## Collaboration Benefits

### For Multiple Editors:
- **Person A** edits `sections/03_results.tex` (results)
- **Person B** edits `sections/04_discussion.tex` (discussion)
- **No conflicts** - different files!
- Everyone clicks "Compile" and sees updates

### For Version Control (Git):
```bash
git add main.tex sections/
git status  # See which section changed
git diff sections/03_results.tex  # See specific changes
```

## Common Tasks

### Add a Figure to Results Section
1. Open `sections/03_results.tex`
2. Add at the right location:
   ```latex
   \begin{figure}[H]
   \centering
   \includegraphics[width=0.8\textwidth]{images/step1/your_image.png}
   \caption{Your caption here}
   \end{figure}
   ```

### Add a Reference
1. Open `sections/06_references.tex`
2. Add to the list:
   ```latex
   \item Author, Y. (Year). Title. Journal, Vol(Issue), pages.
   ```

### Update Author/Date/Title
1. Edit the preamble in `main.tex`:
   ```latex
   \title{Your New Title}
   \author{Your Name}
   \date{\today}  % or specific date
   ```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `! LaTeX Error: File 'sections/01_...' not found` | Make sure `sections/` folder is uploaded |
| Images don't display | Check image paths: should be `images/step1/filename.png` |
| Won't compile | Click "Recompile from scratch" button (circular arrow) |
| See old PDF | Clear cache: Menu → Settings → Logs and output files → Clear |

## Compilation Notes

- **All packages** are in `main.tex` preamble (graphicx, listings, etc.)
- **Images** are resolved relative to `main.tex` location
- **PDF** compiles in <30 seconds with modular structure
- **No loss** of features or quality vs. single-file version

## Tips for Success

✅ **Do this:**
- Edit section files independently
- Use descriptive names for new sections
- Add comments in `main.tex` for clarity
- Test compilation after major changes

❌ **Avoid this:**
- Don't move the `sections/` folder
- Don't rename section files without updating `main.tex`
- Don't copy preamble definitions into section files
- Don't use absolute paths for images

## File Statistics

| File | Lines | Size |
|------|-------|------|
| main.tex | 75 | 2.2 KB |
| 01_introduction | 74 | 3.2 KB |
| 02_methodology | 75 | 2.6 KB |
| 03_results | 178 | 6.3 KB |
| 04_discussion | 120 | 3.8 KB |
| 05_conclusions | 44 | 2.4 KB |
| 06_references | 19 | 1.3 KB |
| 07_appendix | 138 | 4.3 KB |
| **Total** | **723** | **25.9 KB** |

## Questions?

- **Overleaf Docs**: https://www.overleaf.com/learn
- **LaTeX Documentation**: https://www.latex-project.org/
- **Image Issues**: Check path format (use forward slashes `/`)
- **Compilation Errors**: Click error link to jump to problem location

---

**Your project is ready!** Upload `overleaf_export.zip` and start editing. 🚀
