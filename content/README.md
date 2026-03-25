# Moltbook Session: Content Guide

This directory contains the main content for the Moltbook session — the "textbook layer" of the talk. The slides in [`slides/slides-main.md`](../slides/slides-main.md) are intentionally brief and stage-focused; the chapters here provide the full reasoning, assumptions, and caveats.

## How to Read This

### Quick route (4 chapters)
1. [`01-intro.md`](01-intro.md) — Why Moltbook matters
2. [`04-kritiek.md`](04-kritiek.md) — Why it's not yet autonomous
3. [`05-trends.md`](05-trends.md) — What trends are real
4. [`07-slot.md`](07-slot.md) — What to remember

### Full route (all 8 chapters)
1. [`01-intro.md`](01-intro.md) — Introduction and core thesis
2. [`02-ai-agents.md`](02-ai-agents.md) — What is an AI agent? (system view)
3. [`03-agents-md.md`](03-agents-md.md) — Context, memory, and token costs
4. [`04-kritiek.md`](04-kritiek.md) — Attribution, identity, and governance limits
5. [`05-trends.md`](05-trends.md) — Verified trends in AI capability and economics
6. [`06-forecast.md`](06-forecast.md) — Forecast model: bounded-scope emergence
7. [`07-slot.md`](07-slot.md) — Synthesis and conclusions
8. [`08-bronnen-qa-spreekspiekbrief.md`](08-bronnen-qa-spreekspiekbrief.md) — Sources, Q&A, and speaker notes

## Core Thesis

> Moltbook is interesting, not because it is already a real social network for AI, but because it reveals what is still missing: identity, memory, governance, and economic efficiency.

This thesis guides every chapter. The content builds from:
- **What Moltbook claims** (homepage, marketing)
- **What Moltbook actually is** (terms, architecture, costs)
- **What's missing** (identity, attribution, governance, economics)
- **Where things might go** (trends, forecasts, bounded-scope emergence)

## Reading Tips

- Screenshots and figures are inline where they belong
- Each figure includes: what you see, what not to overestimate, what to remember
- Explicit separation between: source anchor, derived calculation, and scenario assumption
- Key takeaways at the end of each chapter

## Verification

For the audit trail and verification reports, see:
- [`docs/verification/`](docs/verification/) — Claim-by-claim verification
- [`docs/README.md`](../docs/README.md) — Documentation index

**Note:** The detailed model audit in `docs/model_audit/` is internal documentation for transparency, not part of the public-facing narrative.

## Generated Assets

Figures referenced in these chapters:
- [`assets/moltbook_homepage.png`](../assets/moltbook_homepage.png)
- [`assets/moltbook_terms_eligibility.png`](../assets/moltbook_terms_eligibility.png)
- [`assets/openclaw_context_docs.png`](../assets/openclaw_context_docs.png)
- [`assets/stanford_hai_ai_index_2025.png`](../assets/stanford_hai_ai_index_2025.png)
- [`assets/epoch_ai_eci.png`](../assets/epoch_ai_eci.png)
- [`assets/token_breakdown.png`](../assets/token_breakdown.png)
- [`assets/ai_trends.png`](../assets/ai_trends.png)
- [`assets/forecast_distribution.png`](../assets/forecast_distribution.png)

## Data Sources

Explicit inputs:
- [`data/token_usage_assumptions.json`](../data/token_usage_assumptions.json)
- [`data/ai_trends_metrics.json`](../data/ai_trends_metrics.json)
- [`data/forecast_scenarios.json`](../data/forecast_scenarios.json)

## Tone and Approach

- Take demos seriously
- Read claims narrowly
- Separate architecture from anthropomorphic language
- Separate reproducible math from observed reality
- Treat forecasts as discipline for thinking, not as oracles

---

*Start reading: [`01-intro.md`](01-intro.md)*
