#!/bin/bash
# Script to prepare files for Overleaf upload
# This script organizes all necessary files into a structured directory ready for Overleaf

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
EXPORT_DIR="$PROJECT_DIR/overleaf_export"

echo "═════════════════════════════════════════════════════════"
echo "Preparing project for Overleaf upload..."
echo "═════════════════════════════════════════════════════════"

# Create export directory structure
mkdir -p "$EXPORT_DIR"
mkdir -p "$EXPORT_DIR/images/step1"
mkdir -p "$EXPORT_DIR/images/step2"

echo ""
echo "📁 Creating directory structure..."

# Copy main LaTeX file
cp "$PROJECT_DIR/report.tex" "$EXPORT_DIR/main.tex"
echo "✓ Copied report.tex → main.tex"

# Copy images
echo ""
echo "🖼️  Copying images..."
cp "$PROJECT_DIR/results/step1"/*.png "$EXPORT_DIR/images/step1/" 2>/dev/null && \
    echo "✓ Copied $(ls $PROJECT_DIR/results/step1/*.png 2>/dev/null | wc -l) Step 1 images"

cp "$PROJECT_DIR/results/step2"/*.png "$EXPORT_DIR/images/step2/" 2>/dev/null && \
    echo "✓ Copied $(ls $PROJECT_DIR/results/step2/*.png 2>/dev/null | wc -l) Step 2 images"

# Create README for Overleaf
cat > "$EXPORT_DIR/README.txt" << 'EOF'
CMP717 - Edge Preserving Filters and Segmentation Project Report

CONTENTS:
- main.tex: Main LaTeX report file
- images/step1/: 54 filter evaluation result images
- images/step2/: 108 segmentation result images

HOW TO USE WITH OVERLEAF:

1. Upload to Overleaf:
   - Go to https://www.overleaf.com
   - Click "New Project" → "Upload Project"
   - Upload all files as a single upload or zip

2. Compile:
   - Click the "Compile" button (or press Ctrl+Enter)
   - Wait for PDF to generate
   - View in preview panel on the right

3. Edit:
   - All images are referenced in main.tex
   - To add more images:
     a) Click Files → Upload
     b) Add reference in LaTeX: \includegraphics{images/filename.png}
     c) Recompile

REPORT FEATURES:
✓ Professional formatting
✓ Complete results with performance metrics
✓ Mathematical equations and explanations
✓ Code samples and implementation details
✓ Figure captions and references
✓ Comprehensive bibliography
✓ ~25-30 pages when compiled

CONTACT:
For issues with Overleaf, visit: https://www.overleaf.com/learn
EOF

echo "✓ Created README.txt"

# Create instructions file
cat > "$EXPORT_DIR/OVERLEAF_INSTRUCTIONS.txt" << 'EOF'
STEP-BY-STEP GUIDE FOR UPLOADING TO OVERLEAF

OPTION 1: Upload All Files Together (Recommended)
────────────────────────────────────────────────

1. Go to https://www.overleaf.com and sign in

2. Click "New Project" → "Upload Project"

3. Create ZIP file:
   - Select all files in this directory
   - Right-click → "Compress" or "Send to" → "Compressed folder"
   - Or use: zip -r project.zip *

4. Upload the ZIP file to Overleaf

5. Click "Compile" button to generate PDF

OPTION 2: Manual Upload
──────────────────────

1. Create blank Overleaf project

2. Delete default main.tex

3. Upload main.tex (this report file):
   - Click "Files" → "Upload File"
   - Select main.tex

4. Create folder structure:
   - Click "New Folder" → name it "images"
   - Inside images folder, create "step1" and "step2" folders

5. Upload images:
   - Upload all PNG files to respective folders
   - Overleaf will organize them automatically

6. Click "Compile" to generate PDF

HELPFUL TIPS
────────────

• Overleaf automatically detects LaTeX files
• You don't need a .bib file for this report (references are in-text)
• Use the "Logs" tab to debug any compilation errors
• Share your project using the "Share" button
• Use "History" to track changes and revert if needed

IMAGE REFERENCE
───────────────

All images are referenced in main.tex using:
\includegraphics[width=0.85\textwidth]{images/step1/filename.png}

If images don't show:
1. Ensure folder names match exactly (case-sensitive on Linux)
2. Check that file extensions are correct (.png, .jpg)
3. Look at error messages in "Logs" tab

CUSTOMIZATION
──────────────

To modify the report in Overleaf:
• Edit main.tex directly
• Overleaf shows preview in real-time
• Changes compile automatically (auto-compile enabled)

To change author name:
Find the line: \author{Student\\...
Replace "Student" with your name

To change date:
Find the line: \date{January 6, 2026}
Modify the date as needed

TROUBLESHOOTING
────────────────

Compilation error "File not found"?
→ Check image paths and folder names

Images display with "?":
→ Verify image file formats and names

Pages look strange:
→ Check for special characters or encoding issues
→ Try recompiling (Ctrl+Enter)

Need more help?
→ Visit: https://www.overleaf.com/learn
→ Check LaTeX documentation: https://www.latex-project.org/

FINAL STEPS
───────────

Before submitting:
1. Review the generated PDF carefully
2. Check all images are displaying correctly
3. Verify page numbers and table of contents
4. Download the PDF: Project Menu → Download PDF
5. Keep the Overleaf link for potential updates

Questions? Refer to the OVERLEAF_README.md file.
EOF

echo "✓ Created OVERLEAF_INSTRUCTIONS.txt"

# Create ZIP file
echo ""
echo "📦 Creating ZIP file for upload..."
cd "$PROJECT_DIR"
zip -r "overleaf_export.zip" "$EXPORT_DIR" -q

ZIP_SIZE=$(du -h "overleaf_export.zip" | cut -f1)
echo "✓ Created overleaf_export.zip ($ZIP_SIZE)"

echo ""
echo "═════════════════════════════════════════════════════════"
echo "✅ READY FOR OVERLEAF!"
echo "═════════════════════════════════════════════════════════"
echo ""
echo "📂 Export directory: $EXPORT_DIR"
echo "📦 ZIP file: $PROJECT_DIR/overleaf_export.zip"
echo ""
echo "NEXT STEPS:"
echo "1. Go to https://www.overleaf.com"
echo "2. Click 'New Project' → 'Upload Project'"
echo "3. Upload overleaf_export.zip"
echo "4. Wait for Overleaf to process"
echo "5. Click 'Compile' to generate PDF"
echo ""
echo "Or:"
echo "1. Manually copy files from: $EXPORT_DIR"
echo "2. Follow OVERLEAF_INSTRUCTIONS.txt"
echo ""
