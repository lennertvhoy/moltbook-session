# Analysis Audit

## `analyses/token_usage.py`

### Input source

- [data/token_usage_assumptions.json](/home/ff/Documents/BoostMeUp/MoltBook_Sessie/data/token_usage_assumptions.json)
- OpenClaw docs anchor for context overhead
- Anthropic pricing
- Artificial Analysis pricing for MiniMax-M2.5

### Method summary

- load documented context anchor and explicit scenario assumptions
- compute one illustrative read-reply-post cycle
- compute per-model token costs
- generate scale examples

### Assumptions

- scenario is illustrative, not measured from Moltbook logs
- AGENTS/project instructions, persona, and prior history token counts are explicit assumptions

### Validation result

- arithmetic reproduced successfully
- script now runs from repo root
- figure now writes to `assets/token_breakdown.png`

### Issues found

- prior script saved to the wrong relative path
- prior narrative did not clearly distinguish measurement from scenario arithmetic

### Fixes made

- moved assumptions into JSON
- fixed save paths
- rewrote titles and labels to say "illustrative" and "assumption-driven"

### Does the chart support the slide claim?

Yes, after the claim was narrowed to: an illustrative social cycle under stated assumptions costs about `$0.377` on Claude Opus 4.6.

## `analyses/ai_trends.py`

### Input source

- [data/ai_trends_metrics.json](/home/ff/Documents/BoostMeUp/MoltBook_Sessie/data/ai_trends_metrics.json)
- Stanford HAI summary metrics
- Epoch AI methodology and homepage trend snapshot

### Method summary

- plot only explicit sourced metrics
- derive a normalized cost-decline line from sourced endpoints
- include an audit note panel instead of synthetic saturation curves

### Assumptions

- the cost-decline line is a normalization from sourced endpoints, not a digitized original dataset
- the model comparison panel is retained only as an audit note, not as a presentation claim

### Validation result

- script runs successfully from repo root
- figure now saves to `assets/ai_trends.png`

### Issues found

- prior script fabricated ECI scores and saturation curves
- prior script embedded a too-confident model comparison

### Fixes made

- removed synthetic time series
- replaced exact ECI benchmark count with an internal-source inconsistency note
- rewrote comparison framing around what can actually be defended

### Does the chart support the slide claim?

Yes, for the narrowed claim that the strongest defendable trends are in cost, compute, efficiency, and broad capability context.

## `analyses/forecast_model.py`

### Input source

- [data/forecast_scenarios.json](/home/ff/Documents/BoostMeUp/MoltBook_Sessie/data/forecast_scenarios.json)

### Method summary

- simulate seven readiness pillars under three scenarios
- compute a weighted geometric readiness index
- apply threshold and floor rules
- report crossing-year probabilities
- run threshold and floor sensitivity checks

### Assumptions

- all growth, volatility, and shock parameters are assumptions
- weights, floors, and threshold are scenario design choices

### Validation result

- script runs successfully from repo root
- outputs reproduced with explicit seed `42`
- chart saves to `assets/forecast_distribution.png`

### Issues found

- prior script saved to the wrong path
- prior presentation framing made the output look too point-estimate-like
- threshold sensitivity alone did not move results because floor constraints bound first

### Fixes made

- moved all scenario inputs into JSON
- fixed save paths
- added floor sensitivity
- rewrote printed interpretation to emphasize assumption error over simulation error

### Does the chart support the slide claim?

Yes, for the narrowed claim that the model is useful as a scenario discipline and that the current base case crosses with about `28.1%` probability by 2040 under the stated assumptions.
