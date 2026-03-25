# Moltbook Session

This repository contains the source, analysis code, and materials for a conference-style talk about Moltbook and AI-agent networks. The project treats the deck as a verification-first artifact: charts are reproducible, assumptions are explicit, and claims are narrowed when the evidence does not support stronger wording.

The talk's core argument is simple: Moltbook is interesting less as proof that autonomous digital societies already exist, and more as a live stress test of what is still missing around identity, memory, governance, and cost discipline.

## Quickstart

### Read the content

The main content is in [`content/`](content/):

1. [`content/01-intro.md`](content/01-intro.md) — Introduction and core thesis
2. [`content/02-ai-agents.md`](content/02-ai-agents.md) — What is an AI agent?
3. [`content/03-agents-md.md`](content/03-agents-md.md) — Context, memory, and token costs
4. [`content/04-kritiek.md`](content/04-kritiek.md) — Why this isn't yet convincing autonomy
5. [`content/05-trends.md`](content/05-trends.md) — Trends in AI capability and economics
6. [`content/06-forecast.md`](content/06-forecast.md) — Forecast model and scenario analysis
7. [`content/07-slot.md`](content/07-slot.md) — Synthesis and conclusions
8. [`content/08-bronnen-qa-spreekspiekbrief.md`](content/08-bronnen-qa-spreekspiekbrief.md) — Sources and speaker notes

### Rebuild the analyses

```bash
UV_CACHE_DIR=.uv-cache uv sync
MPLCONFIGDIR=/tmp/matplotlib UV_CACHE_DIR=.uv-cache uv run analyses/token_usage.py
MPLCONFIGDIR=/tmp/matplotlib UV_CACHE_DIR=.uv-cache uv run analyses/ai_trends.py
MPLCONFIGDIR=/tmp/matplotlib UV_CACHE_DIR=.uv-cache uv run analyses/forecast_model.py
```

### Rebuild the deck

```bash
BUN_TMPDIR=/tmp BUN_INSTALL_CACHE_DIR=.bun-cache bun install
BUN_TMPDIR=/tmp BUN_INSTALL_CACHE_DIR=.bun-cache bun run build:deck
```

Output: [`release/Moltbook.pptx`](release/Moltbook.pptx)

### Build supporting notes PDF (optional)

Merge all `/docs` into a single PDF for reference:

```bash
./scripts/build_docs_pdf.sh
```

Output: `output/moltbook-supporting-notes.pdf` (~80 pages)

Requires: `pandoc` and `google-chrome` (for HTML-to-PDF conversion)

## Repository Layout

```text
.
├── analyses/              Python analysis scripts (reproducible)
├── assets/                Generated figures and screenshots
├── content/               Main content (chapters 01-08)
├── data/                  Explicit assumptions and inputs
├── docs/                  Internal documentation (audit trail)
├── release/               Final generated deck
├── scripts/               Deck build scripts
└── slides/                Slide outline
```

## Verified vs Assumption-Driven

**Verified or source-backed:**
- Moltbook product and terms claims
- OpenClaw architecture framing
- Source-backed trend metrics (Stanford HAI, Epoch)
- Official pricing snapshots

**Assumption-driven but explicit:**
- Illustrative token-cost scenarios
- Monte Carlo readiness forecasts
- Scenario thresholds and parameters

## Core Thesis

> Moltbook is interesting, not because it is already a real social network for AI, but because it reveals what is still missing: identity, memory, governance, and economic efficiency.

This thesis runs through the entire project:
- The content makes it learnable
- The analyses make it reproducible
- The audit trail makes it transparent

## What This Project Does Not Claim

- ❌ That Moltbook proves autonomous digital societies already exist
- ❌ That current agents have stable institutional identity
- ❌ That governance is already solved
- ❌ That the economic cost structure is already sustainable
- ❌ That forecasts predict the future with high confidence

## Internal Documentation

The following are available for transparency but are **not** part of the public-facing narrative:

- [`docs/verification/`](docs/verification/) — Verification and audit reports
- [`docs/qa/`](docs/qa/) — QA reports and process documentation
- [`docs/model_audit/`](docs/model_audit/) — Detailed model audit (internal)

See [`docs/README.md`](docs/README.md) for the internal documentation index.

## Claim Standard

Every non-trivial number in the talk should be read as one of:

- Reproduced from code and verified against a source
- Reproduced from code but assumption-driven
- Source-supported but not directly reproduced locally

When in doubt, check the content chapters for explicit caveats.

## Generated Artifacts

### Figures
- [`assets/token_breakdown.png`](assets/token_breakdown.png) — Token cost analysis
- [`assets/ai_trends.png`](assets/ai_trends.png) — AI trend visualization
- [`assets/forecast_distribution.png`](assets/forecast_distribution.png) — Forecast output

### Data Inputs
- [`data/token_usage_assumptions.json`](data/token_usage_assumptions.json)
- [`data/ai_trends_metrics.json`](data/ai_trends_metrics.json)
- [`data/forecast_scenarios.json`](data/forecast_scenarios.json)

## License and Usage

This repository is provided as a transparent, reproducible research artifact. When citing or referencing:
- Prefer linking to the content chapters
- Distinguish between verified claims and scenario analyses
- Note the date of access (the project evolves)

---

*Last updated: March 2026*
