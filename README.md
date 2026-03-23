# Moltbook Session

This repository contains the source, analysis code, audit trail, and native PowerPoint build for a conference-style talk about Moltbook and AI-agent networks. The project treats the deck as a verification-first artifact: charts are reproducible, assumptions are explicit, and claims are narrowed when the evidence does not support stronger wording.

The talk’s core argument is simple: Moltbook is interesting less as proof that autonomous digital societies already exist, and more as a live stress test of what is still missing around identity, memory, governance, and cost discipline.

## What Is Verified vs Assumption-Driven

Verified or source-backed:

- Moltbook product and terms claims
- OpenClaw architecture framing
- source-backed trend metrics
- official pricing snapshots used in the model comparison

Assumption-driven but explicit:

- illustrative token-cost scenarios
- Monte Carlo readiness forecasts
- scenario thresholds, floors, and weighting choices

See the audit set in [docs/verification](docs/verification/README.md) and [docs/qa](docs/qa/FINAL_QA_REPORT.md).

## Quickstart

### Rebuild the analyses with `uv`

```bash
UV_CACHE_DIR=.uv-cache uv sync
MPLCONFIGDIR=/tmp/matplotlib UV_CACHE_DIR=.uv-cache uv run analyses/token_usage.py
MPLCONFIGDIR=/tmp/matplotlib UV_CACHE_DIR=.uv-cache uv run analyses/ai_trends.py
MPLCONFIGDIR=/tmp/matplotlib UV_CACHE_DIR=.uv-cache uv run analyses/forecast_model.py
```

### Rebuild the native `.pptx` with `bun`

```bash
BUN_TMPDIR=/tmp BUN_INSTALL_CACHE_DIR=.bun-cache bun install
BUN_TMPDIR=/tmp BUN_INSTALL_CACHE_DIR=.bun-cache bun run build:deck
```

The production deck is written to [release/Moltbook.pptx](release/Moltbook.pptx).

### Regenerate QA previews

```bash
UV_CACHE_DIR=.uv-cache uv run scripts/export_slide_previews.py
```

Preview renders and metadata are written to [docs/qa/previews](docs/qa/previews).

## Repository Layout

```text
.
├── analyses/              Python analysis scripts
├── assets/                Generated figures, screenshots, and brand assets
├── content/               Audited talk notes
├── data/                  Explicit source snapshots and scenario inputs
├── docs/                  Verification, QA, and release notes
├── release/               Final generated deck output
├── scripts/               Deck build and QA helper scripts
└── slides/                Slide outline and narrative source
```

Key entry points:

- [slides/slides-main.md](slides/slides-main.md): presentation outline
- [scripts/build_deck.ts](scripts/build_deck.ts): native PowerPoint generator
- [scripts/pptx-brand.ts](scripts/pptx-brand.ts): reusable BoostMeUp PptxGenJS housestyle
- [release/Moltbook.pptx](release/Moltbook.pptx): latest committed deck
- [docs/verification/README.md](docs/verification/README.md): verification and audit index
- [docs/qa/FINAL_QA_REPORT.md](docs/qa/FINAL_QA_REPORT.md): final presentation QA report

## Reusable BoostMeUp Theme

The deck generator uses a shared BoostMeUp theme module for PptxGenJS:

- house colors: `#12192c`, `#ffffff`, `#e93325`, `#f2ad18`
- shared slide shells for dark and light slides
- shared panel, body text, quote, and image helpers
- vendored brand assets:
  - [assets/brand/boostmeup-logo.png](assets/brand/boostmeup-logo.png)
  - [assets/brand/boostmeup-mark.png](assets/brand/boostmeup-mark.png)

## Public Outputs

Source inputs:

- [data/token_usage_assumptions.json](data/token_usage_assumptions.json)
- [data/ai_trends_metrics.json](data/ai_trends_metrics.json)
- [data/forecast_scenarios.json](data/forecast_scenarios.json)

Generated figures:

- [assets/token_breakdown.png](assets/token_breakdown.png)
- [assets/ai_trends.png](assets/ai_trends.png)
- [assets/forecast_distribution.png](assets/forecast_distribution.png)

Verification and QA:

- [docs/verification/VERIFICATION_REPORT.md](docs/verification/VERIFICATION_REPORT.md)
- [docs/verification/CLAIM_AUDIT.md](docs/verification/CLAIM_AUDIT.md)
- [docs/verification/ANALYSIS_AUDIT.md](docs/verification/ANALYSIS_AUDIT.md)
- [docs/verification/SLIDE_SYSTEM_DECISION.md](docs/verification/SLIDE_SYSTEM_DECISION.md)
- [docs/qa/FINAL_QA_REPORT.md](docs/qa/FINAL_QA_REPORT.md)
- [docs/PUBLIC_RELEASE_REPORT.md](docs/PUBLIC_RELEASE_REPORT.md)

## Claim Standard

Every non-trivial number in the talk should be read as one of:

- reproduced from code and verified against a source
- reproduced from code but assumption-driven
- source-supported but not directly reproduced locally
- ambiguous or source-misaligned
- unsupported and removed
