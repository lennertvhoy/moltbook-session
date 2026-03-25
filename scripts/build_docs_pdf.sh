#!/bin/bash
# Build PDF from /docs markdown files
# Usage: ./scripts/build_docs_pdf.sh
#
# Dependencies:
#   - pandoc (for markdown-to-html conversion)
#   - google-chrome (for html-to-pdf conversion)
#
# Output: output/moltbook-supporting-notes.pdf

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DOCS_DIR="$REPO_ROOT/docs"
OUTPUT_DIR="$REPO_ROOT/output"
PDF_PATH="$OUTPUT_DIR/moltbook-supporting-notes.pdf"
HTML_PATH="$OUTPUT_DIR/moltbook-supporting-notes.html"
TEMP_MD="$OUTPUT_DIR/.merged_docs_temp.md"
CSS_PATH="$OUTPUT_DIR/.pdf-styles.css"

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

echo "Building Moltbook Supporting Notes PDF..."
echo ""

# Create CSS for PDF styling
cat > "$CSS_PATH" << 'CSS'
@page {
    size: A4;
    margin: 2.5cm;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #333;
}

h1 {
    font-size: 18pt;
    margin-top: 2em;
    page-break-before: always;
    border-bottom: 2px solid #333;
    padding-bottom: 0.3em;
}

h1:first-of-type {
    page-break-before: avoid;
}

h2 {
    font-size: 14pt;
    margin-top: 1.5em;
    color: #444;
}

h3 {
    font-size: 12pt;
    margin-top: 1.2em;
}

code {
    font-family: "SF Mono", Monaco, "Cascadia Code", monospace;
    font-size: 0.9em;
    background: #f5f5f5;
    padding: 0.1em 0.3em;
    border-radius: 3px;
}

pre {
    background: #f5f5f5;
    padding: 1em;
    overflow-x: auto;
    border-radius: 5px;
    font-size: 0.85em;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
    font-size: 0.95em;
}

th, td {
    border: 1px solid #ddd;
    padding: 0.5em;
    text-align: left;
}

th {
    background: #f5f5f5;
}

blockquote {
    margin: 1em 0;
    padding-left: 1em;
    border-left: 4px solid #ddd;
    color: #666;
}

a {
    color: #0066cc;
    text-decoration: none;
}

#toc-title {
    font-size: 20pt;
    margin-bottom: 1em;
}

toc > ul {
    font-size: 11pt;
}

toc li {
    margin: 0.3em 0;
}
CSS

# Create merged markdown with proper order
cat > "$TEMP_MD" << 'FRONTMATTER'
---
title: "Moltbook Session — Supporting Notes"
subtitle: "Internal Documentation, Verification & Model Audit"
date: "2026-03-25"
---

FRONTMATTER

echo "Merging markdown files..."

# Part 1: Documentation Index
echo "  - Documentation Index"
cat "$DOCS_DIR/README.md" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

# Part 2: Release Report
echo "  - Release Report"
echo "# Part 2: Release Report" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"
cat "$DOCS_DIR/PUBLIC_RELEASE_REPORT.md" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

# Part 3: Verification Reports
echo "  - Verification Reports"
echo "# Part 3: Verification Reports" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

cat "$DOCS_DIR/verification/VERIFICATION_REPORT.md" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

cat "$DOCS_DIR/verification/CLAIM_AUDIT.md" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

cat "$DOCS_DIR/verification/ANALYSIS_AUDIT.md" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

cat "$DOCS_DIR/verification/SLIDE_SYSTEM_DECISION.md" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

# Part 4: QA Reports
echo "  - QA Reports"
echo "# Part 4: QA Reports" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

cat "$DOCS_DIR/qa/FINAL_QA_REPORT.md" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

cat "$DOCS_DIR/qa/PRESENTATION_REDESIGN_REPORT.md" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

cat "$DOCS_DIR/qa/FINAL_PRESENTATION_POLISH_REPORT.md" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

# Part 5: Model Audit (Internal)
echo "  - Model Audit (Internal)"
echo "# Part 5: Model Audit (Internal)" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"
echo "> **Note:** These documents are for internal methodology review and transparency. They discuss alternative designs, sensitivity analyses, and historical model versions that are not part of the public-facing narrative." >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

cat "$DOCS_DIR/model_audit/README.md" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

cat "$DOCS_DIR/model_audit/MODEL_AUDIT_COMPLETE.md" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

cat "$DOCS_DIR/model_audit/FLOOR_JUSTIFICATION_FRAMEWORK.md" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

cat "$DOCS_DIR/model_audit/ablation_validation_report.md" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

cat "$DOCS_DIR/model_audit/MODEL_V2_DESIGN.md" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

cat "$DOCS_DIR/model_audit/MODEL_V2_FORMAL_SPECIFICATION.md" >> "$TEMP_MD"

echo ""
echo "Merged $(find "$DOCS_DIR" -name '*.md' | wc -l) markdown files"
echo ""

# Convert to HTML with pandoc
echo "Converting to HTML..."
pandoc "$TEMP_MD" \
    --output="$HTML_PATH" \
    --from=markdown \
    --toc \
    --toc-depth=2 \
    --standalone \
    --css="$CSS_PATH" \
    2>/dev/null || {
        echo "Warning: pandoc completed with warnings (likely image references)"
    }

# Convert HTML to PDF with Chrome
echo "Converting to PDF..."
/usr/bin/google-chrome \
    --headless \
    --disable-gpu \
    --print-to-pdf="$PDF_PATH" \
    --print-to-pdf-no-header \
    --run-all-compositor-stages-before-draw \
    "$HTML_PATH" \
    2>/dev/null || {
        echo "Error: Failed to generate PDF. Ensure google-chrome is installed."
        exit 1
    }

# Clean up temp files
rm -f "$TEMP_MD" "$CSS_PATH"

echo ""
echo "✓ PDF built successfully"
echo ""
echo "  Output: $PDF_PATH"
echo "  HTML:   $HTML_PATH"
echo ""

# Show file info
ls -lh "$PDF_PATH"
echo ""

# Show page count if pdfinfo is available
if command -v pdfinfo &> /dev/null; then
    pdfinfo "$PDF_PATH" | grep -E "Pages|Page size"
fi
