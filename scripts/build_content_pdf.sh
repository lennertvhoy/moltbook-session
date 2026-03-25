#!/bin/bash
# Build PDF from /content markdown files (main presentation content)
# Usage: ./scripts/build_content_pdf.sh
#
# Dependencies:
#   - pandoc (for markdown-to-html conversion)
#   - google-chrome (for html-to-pdf conversion)
#
# Output: output/moltbook-content.pdf

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CONTENT_DIR="$REPO_ROOT/content"
OUTPUT_DIR="$REPO_ROOT/output"
PDF_PATH="$OUTPUT_DIR/moltbook-content.pdf"
HTML_PATH="$OUTPUT_DIR/moltbook-content.html"
TEMP_MD="$OUTPUT_DIR/.merged_content_temp.md"
CSS_PATH="$OUTPUT_DIR/.content-pdf-styles.css"

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

echo "Building Moltbook Content PDF..."
echo ""

# Create CSS for PDF styling
cat > "$CSS_PATH" << 'CSS'
@page {
    size: A4;
    /* Clean margins - no Chrome headers/footers thanks to --no-pdf-header-footer flag */
    margin: 2.5cm;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #333;
}

h1 {
    font-size: 20pt;
    margin-top: 2em;
    page-break-before: always;
    border-bottom: 2px solid #333;
    padding-bottom: 0.3em;
}

h1:first-of-type {
    page-break-before: avoid;
}

h2 {
    font-size: 16pt;
    margin-top: 1.5em;
    color: #444;
}

h3 {
    font-size: 13pt;
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

img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 1em 0;
}

#toc-title {
    font-size: 22pt;
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
title: "Moltbook Session — Full Content"
subtitle: "AI Agent Networks: Analysis, Trends & Forecast"
date: "2026-03-25"
---

FRONTMATTER

echo "Merging content markdown files..."

# Title page info
echo "" >> "$TEMP_MD"
echo "> **Full written content for the Moltbook Session presentation**" >> "$TEMP_MD"
echo "> " >> "$TEMP_MD"
echo "> This document contains the complete text of all presentation chapters," >> "$TEMP_MD"
echo "> including analysis, evidence, and speaker notes. The slide deck provides" >> "$TEMP_MD"
echo "> the visual summary; this document provides the full argumentation." >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

# Chapter 1: Intro
echo "  - Chapter 1: Introduction"
cat "$CONTENT_DIR/01-intro.md" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

# Chapter 2: AI Agents
echo "  - Chapter 2: What is an AI Agent?"
cat "$CONTENT_DIR/02-ai-agents.md" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

# Chapter 3: Context, Memory, Token Costs
echo "  - Chapter 3: Context, Memory & Token Costs"
cat "$CONTENT_DIR/03-agents-md.md" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

# Chapter 4: Critique
echo "  - Chapter 4: Critique & Limits"
cat "$CONTENT_DIR/04-kritiek.md" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

# Chapter 5: Trends
echo "  - Chapter 5: Trends"
cat "$CONTENT_DIR/05-trends.md" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

# Chapter 6: Forecast
echo "  - Chapter 6: Forecast Model"
cat "$CONTENT_DIR/06-forecast.md" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

# Chapter 7: Conclusion
echo "  - Chapter 7: Conclusion"
cat "$CONTENT_DIR/07-slot.md" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

# Chapter 8: Sources & Speaker Notes
echo "  - Chapter 8: Sources & Speaker Notes"
cat "$CONTENT_DIR/08-bronnen-qa-spreekspiekbrief.md" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

echo ""
echo "Merged content chapters"
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
    --no-pdf-header-footer \
    --run-all-compositor-stages-before-draw \
    "$HTML_PATH" \
    2>/dev/null || {
        echo "Error: Failed to generate PDF. Ensure google-chrome is installed."
        exit 1
    }

# Clean up temp files
rm -f "$TEMP_MD" "$CSS_PATH"

echo ""
echo "✓ Content PDF built successfully"
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
