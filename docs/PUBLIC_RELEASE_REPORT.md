# Public Release Report

## Executive Summary

This pass turned the repository from an internal working deck project into a more portable public release. The build path is still reproducible with `uv` and `bun`, but machine-specific links, root clutter, and accidental artifacts were removed.

## What Was Reorganized

- moved verification reports into `docs/verification/`
- moved the final QA report into `docs/qa/`
- moved preview renders into `docs/qa/previews/`
- moved the generated deck into `release/`
- added `docs/README.md` and `docs/verification/README.md` as navigation entry points

## Why The New Structure Is Better

- the repo root now highlights source, build config, and the release artifact instead of audit clutter
- verification and QA material are grouped under one `docs/` surface
- the final deck has an intentional home in `release/`
- portable relative links now work on GitHub instead of depending on one workstation path

## What Was Removed

- `Document1.docx`
- `Presentation1.pptx`

Both files were tracked Office artifacts with no references in the repo and no value to the public release.

## What Was Kept And Why

- `release/Moltbook.pptx`
  - kept as the main downloadable artifact for public visitors
- `docs/qa/previews/*`
  - kept because they document slide-by-slide QA without requiring Office
- `requirements.txt`
  - kept as a pip fallback even though `uv` plus `pyproject.toml` and `uv.lock` are the preferred path

## Public-Facing Issues Fixed

- removed absolute local paths from docs and links
- replaced machine-specific `cd /home/...` commands with repo-root commands
- moved public reports out of the root
- made deck output and preview output locations explicit
- added ignore coverage for LibreOffice lock debris

## Remaining Tradeoffs

1. The repo still does not declare an open-source license. That is a publication decision rather than a technical one.
2. Preview renders are useful QA evidence, but they are not a perfect substitute for opening the deck in PowerPoint or LibreOffice.
3. `requirements.txt` duplicates dependency intent already captured in `pyproject.toml` and `uv.lock`, but it remains useful for readers who do not use `uv`.

## Exact Commands Run

```bash
mkdir -p docs/verification docs/qa release
mv VERIFICATION_REPORT.md docs/verification/VERIFICATION_REPORT.md
mv CLAIM_AUDIT.md docs/verification/CLAIM_AUDIT.md
mv ANALYSIS_AUDIT.md docs/verification/ANALYSIS_AUDIT.md
mv SLIDE_SYSTEM_DECISION.md docs/verification/SLIDE_SYSTEM_DECISION.md
mv FINAL_QA_REPORT.md docs/qa/FINAL_QA_REPORT.md
mv Moltbook.pptx release/Moltbook.pptx
rm -f Document1.docx Presentation1.pptx
mkdir -p docs/qa/previews
mv qa/previews/* docs/qa/previews/
rmdir qa/previews qa
MPLCONFIGDIR=/tmp/matplotlib UV_CACHE_DIR=.uv-cache uv run analyses/token_usage.py
MPLCONFIGDIR=/tmp/matplotlib UV_CACHE_DIR=.uv-cache uv run analyses/ai_trends.py
MPLCONFIGDIR=/tmp/matplotlib UV_CACHE_DIR=.uv-cache uv run analyses/forecast_model.py
BUN_TMPDIR=/tmp BUN_INSTALL_CACHE_DIR=.bun-cache bun run build:deck
UV_CACHE_DIR=.uv-cache uv run scripts/export_slide_previews.py
```

## Clean-Worktree Proof

At handoff, the intended proof standard is:

- the moved paths are committed
- the rebuilt deck exists in `release/`
- preview renders exist in `docs/qa/previews/`
- `git status --short` is clean
