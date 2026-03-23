# Moltbook Session

This repository now treats the Moltbook talk as a verification-first presentation project, not a polish-only slide deck.

## What Changed

The earlier repo state had three major credibility problems:

1. `analyses/ai_trends.py` generated sourced-looking curves from synthetic data.
2. The documented analysis commands did not work from the repo root because the scripts saved to the wrong paths.
3. The deck text overstated confidence on several points, especially the MiniMax vs Opus comparison and the token-cost framing.

The current repo is structured to make those issues visible and auditable.

## Reproducible Workflow

### Python analyses with `uv`

```bash
cd /home/ff/Documents/BoostMeUp/MoltBook_Sessie
UV_CACHE_DIR=.uv-cache uv sync
MPLCONFIGDIR=/tmp/matplotlib UV_CACHE_DIR=.uv-cache uv run analyses/token_usage.py
MPLCONFIGDIR=/tmp/matplotlib UV_CACHE_DIR=.uv-cache uv run analyses/ai_trends.py
MPLCONFIGDIR=/tmp/matplotlib UV_CACHE_DIR=.uv-cache uv run analyses/forecast_model.py
```

### Native PowerPoint build with `bun`

```bash
cd /home/ff/Documents/BoostMeUp/MoltBook_Sessie
BUN_TMPDIR=/tmp BUN_INSTALL_CACHE_DIR=.bun-cache bun install
BUN_TMPDIR=/tmp BUN_INSTALL_CACHE_DIR=.bun-cache bun run build:deck
```

This rebuilds [Moltbook.pptx](/home/ff/Documents/BoostMeUp/MoltBook_Sessie/Moltbook.pptx) as a native `.pptx` via `PptxGenJS`.

## Repo Layout

### Source content

- [slides/slides-main.md](/home/ff/Documents/BoostMeUp/MoltBook_Sessie/slides/slides-main.md): verified slide outline
- [content/01-intro.md](/home/ff/Documents/BoostMeUp/MoltBook_Sessie/content/01-intro.md) to [content/07-slot.md](/home/ff/Documents/BoostMeUp/MoltBook_Sessie/content/07-slot.md): audited talk notes

### Analysis code

- [analyses/token_usage.py](/home/ff/Documents/BoostMeUp/MoltBook_Sessie/analyses/token_usage.py): illustrative token-cost model with explicit assumptions
- [analyses/ai_trends.py](/home/ff/Documents/BoostMeUp/MoltBook_Sessie/analyses/ai_trends.py): sourced trend summary only
- [analyses/forecast_model.py](/home/ff/Documents/BoostMeUp/MoltBook_Sessie/analyses/forecast_model.py): assumption-driven Monte Carlo readiness model

### Data inputs

- [data/token_usage_assumptions.json](/home/ff/Documents/BoostMeUp/MoltBook_Sessie/data/token_usage_assumptions.json)
- [data/ai_trends_metrics.json](/home/ff/Documents/BoostMeUp/MoltBook_Sessie/data/ai_trends_metrics.json)
- [data/forecast_scenarios.json](/home/ff/Documents/BoostMeUp/MoltBook_Sessie/data/forecast_scenarios.json)

### Generated assets

- [assets/token_breakdown.png](/home/ff/Documents/BoostMeUp/MoltBook_Sessie/assets/token_breakdown.png)
- [assets/ai_trends.png](/home/ff/Documents/BoostMeUp/MoltBook_Sessie/assets/ai_trends.png)
- [assets/forecast_distribution.png](/home/ff/Documents/BoostMeUp/MoltBook_Sessie/assets/forecast_distribution.png)

### Verification deliverables

- `VERIFICATION_REPORT.md`
- `CLAIM_AUDIT.md`
- `ANALYSIS_AUDIT.md`
- `SLIDE_SYSTEM_DECISION.md`

## Current Claim Standard

Every non-trivial number in the talk should be read as one of:

- reproduced from code and verified against a source
- reproduced from code but assumption-driven
- source-supported but not directly reproduced locally
- ambiguous or source-misaligned
- unsupported and removed

## Core Thesis

> Moltbook is interesting less as proof that autonomous digital societies already exist, and more as a live stress test of what is still missing: identity, memory, governance, and cost discipline.
