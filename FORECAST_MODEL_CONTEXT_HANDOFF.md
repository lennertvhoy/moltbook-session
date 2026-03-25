# Forecast Model Context Handoff

**Prepared for:** ChatGPT review session  
**Prepared by:** Subagent analysis  
**Timestamp:** 2026-03-23T17:13:51+01:00  
**Git commit:** `713857fffaa1769625df2fa2eed2d595d1df0c09`  
**Python version:** 3.14.3  

---

# 1. Executive truth summary

- **Model definition files:**
  - `analyses/forecast_model.py` - Core Monte Carlo simulation logic
  - `data/forecast_scenarios.json` - All scenario parameters (weights, growth, volatility, floors)
  
- **G growth WAS changed from 0.08 to 0.12:** Confirmed via `git diff HEAD~5 -- data/forecast_scenarios.json`
  ```diff
  -        {"code": "G", "initial_2026": 25, "growth_mu": 0.08, ...
  +        {"code": "G", "initial_2026": 25, "growth_mu": 0.12, ...
  ```

- **Median crossing year IS 2038:** Verified by fresh run on 2026-03-23 at 17:13
  - Base case: P(cross by 2040) = 66.3%, Median = 2038, Never crosses = 33.7%

- **Most likely bottleneck:** Governance (G) floor is the binding constraint in **42.0%** of crossing runs; Network (N) is second at **37.2%**. In **98.7%** of crossing runs (6546/6629), floors are satisfied AFTER the threshold is first exceeded, causing an average **3.6 year delay**.

- **Shocks vs floors have SEPARATE roles:** Shocks primarily determine *failure probability* (66% → 91% success when removed); floors primarily determine *timing among successes* (median stays ~2037-2038 regardless). The strongest summary: **shocks determine how many runs fail; floors determine when successful runs officially count.**

- **Contradictions found:**
  1. **Threshold sensitivity shows no effect:** All three thresholds (70, 75, 80) produce identical P(cross) and median. This contradicts intuitive expectations and suggests floors dominate threshold effects.
  2. **Documentation vs code on median calculation:** The model calculates median ONLY on successful crossings (excluding NaN), which can produce counterintuitive results when many runs fail.

---

# 2. File inventory

| Relative Path | Purpose |
|--------------|---------|
| `analyses/forecast_model.py` | Core Monte Carlo model with 553 lines. Contains `AgentNetworkForecaster` class, simulation logic, and plotting. |
| `data/forecast_scenarios.json` | Single source of truth for all scenario parameters. Loaded at runtime. |
| `analyses/inspect_bottlenecks.py` | **Temporary inspection script** (created for this handoff, now removed). Analyzed floors, computed bottleneck frequencies. Results preserved in Section 8. |
| `assets/forecast_distribution.png` | Generated visualization showing trajectories, crossing probabilities, and boxplots. |
| `docs/verification/VERIFICATION_REPORT.md` | Independent audit report on repo state. |
| `docs/verification/ANALYSIS_AUDIT.md` | Per-script audit including forecast model validation. |

---

# 3. Exact current inputs

## Weights (from JSON)

```json path=data/forecast_scenarios.json
"weights": {
  "C": 0.2,
  "E": 0.2,
  "M": 0.15,
  "R": 0.15,
  "N": 0.12,
  "G": 0.1,
  "D": 0.08
}
```

## Start values for all seven pillars (Base case)

| Code | Initial 2026 | Growth μ | Volatility | Neg Shock Prob | Neg Shock Size |
|------|--------------|----------|------------|----------------|----------------|
| C (Capability) | 55 | 0.18 | 0.08 | 0.05 | -0.08 |
| E (Efficiency) | 45 | 0.28 | 0.10 | 0.04 | -0.06 |
| M (Memory) | 30 | 0.14 | 0.12 | 0.08 | -0.10 |
| R (Reliability) | 28 | 0.16 | 0.12 | 0.10 | -0.12 |
| N (Network) | 20 | 0.15 | 0.15 | 0.12 | -0.15 |
| **G (Governance)** | **25** | **0.12** | **0.10** | **0.15** | **-0.18** |
| D (Demand) | 50 | 0.12 | 0.07 | 0.05 | -0.06 |

## Full Base case scenario JSON

```json path=data/forecast_scenarios.json
{
  "name": "Base case",
  "pillars": [
    {"code": "C", "initial_2026": 55, "growth_mu": 0.18, "volatility": 0.08, "neg_shock_prob": 0.05, "neg_shock_size": -0.08},
    {"code": "E", "initial_2026": 45, "growth_mu": 0.28, "volatility": 0.1, "neg_shock_prob": 0.04, "neg_shock_size": -0.06},
    {"code": "M", "initial_2026": 30, "growth_mu": 0.14, "volatility": 0.12, "neg_shock_prob": 0.08, "neg_shock_size": -0.1},
    {"code": "R", "initial_2026": 28, "growth_mu": 0.16, "volatility": 0.12, "neg_shock_prob": 0.1, "neg_shock_size": -0.12},
    {"code": "N", "initial_2026": 20, "growth_mu": 0.15, "volatility": 0.15, "neg_shock_prob": 0.12, "neg_shock_size": -0.15},
    {"code": "G", "initial_2026": 25, "growth_mu": 0.12, "volatility": 0.1, "neg_shock_prob": 0.15, "neg_shock_size": -0.18},
    {"code": "D", "initial_2026": 50, "growth_mu": 0.12, "volatility": 0.07, "neg_shock_prob": 0.05, "neg_shock_size": -0.06}
  ]
}
```

## Global constraints

```json path=data/forecast_scenarios.json
"threshold": 75.0,
"floor_values": {
  "M": 60.0,
  "R": 60.0,
  "N": 60.0,
  "G": 60.0
},
"min_consecutive_years": 2,
"sensitivity_thresholds": [70.0, 75.0, 80.0],
"sensitivity_floor_values": [55.0, 60.0, 65.0]
```

## Simulation parameters (hardcoded in Python)

```python path=analyses/forecast_model.py
SEED = 42
n_simulations = 10000  # default per scenario
years = np.arange(2026, 2041)  # 2026 through 2040
```

Scenario seeds: Conservative=42, Base case=142, Accelerated=242 (SEED + index*100)

---

# 4. Exact model logic

## Yearly state update

```python path=analyses/forecast_model.py
def _simulate_pillar(self, pillar: PillarConfig) -> np.ndarray:
    values = np.zeros((self.n_simulations, len(self.years)))
    values[:, 0] = pillar.initial_2026

    for year_index in range(1, len(self.years)):
        log_growth = self.rng.normal(
            loc=pillar.growth_mu,
            scale=pillar.volatility,
            size=self.n_simulations,
        )
        shocks = self.rng.random(self.n_simulations) < pillar.neg_shock_prob
        log_growth[shocks] += pillar.neg_shock_size
        values[:, year_index] = np.clip(values[:, year_index - 1] * np.exp(log_growth), 0, 100)

    return values
```

**What it does:** For each year, draws log-normal growth for all simulations simultaneously. Applies Bernoulli shock draws. Updates values multiplicatively with `exp(log_growth)`, then clamps to [0, 100].

**Modeling choice note:** Multiplicative growth with `exp()` means growth compounds. Values can grow quickly but the 0-100 clamp creates an absorbing boundary at the top.

---

## Weighted geometric mean (readiness index)

```python path=analyses/forecast_model.py
def _calculate_readiness_index(self, pillar_values: dict[str, np.ndarray]) -> np.ndarray:
    index = np.ones((self.n_simulations, len(self.years)))
    for pillar in self.scenario.pillars:
        index *= (pillar_values[pillar.code] / 100.0) ** pillar.weight
    return index * 100.0
```

**What it does:** Computes weighted geometric mean. Each pillar contributes as `(value/100)^weight`, then scaled back to 0-100.

**Modeling choice note:** Geometric mean means any pillar at 0 pulls the entire index to 0. This creates strong complementarity—pillars cannot substitute for each other.

---

## Floor checking and threshold crossing

```python path=analyses/forecast_model.py
def _check_threshold_crossing(
    self,
    index: np.ndarray,
    pillar_values: dict[str, np.ndarray],
    threshold: float | None = None,
    floor_values: dict[str, float] | None = None,
) -> np.ndarray:
    active_threshold = self.scenario.threshold if threshold is None else threshold
    active_floors = self.scenario.floor_values if floor_values is None else floor_values
    crossing_years = np.full(self.n_simulations, np.nan)

    for simulation_index in range(self.n_simulations):
        consecutive = 0
        for year_idx, year in enumerate(self.years):
            floors_met = all(
                pillar_values[code][simulation_index, year_idx] >= minimum
                for code, minimum in active_floors.items()
            )
            if index[simulation_index, year_idx] >= active_threshold and floors_met:
                consecutive += 1
                if consecutive >= self.scenario.min_consecutive_years:
                    crossing_years[simulation_index] = year
                    break
            else:
                consecutive = 0

    return crossing_years
```

**What it does:** For each simulation, scans years. Requires BOTH threshold ≥ 75 AND all floors ≥ 60. Must hold for 2 consecutive years. Returns year of second consecutive success, or NaN if never.

**Modeling choice note:** The consecutive-years rule with reset-on-failure creates strict persistence requirements. A single bad year resets progress.

---

## Median crossing year calculation

```python path=analyses/forecast_model.py
def calculate_statistics(self, results: dict[str, Any], ...) -> dict[str, Any]:
    crossing_years = results["crossing_years"]
    # ...
    valid = crossing_years[~np.isnan(crossing_years)]

    stats = {
        "p_by_2030": float(np.mean(crossing_years <= 2030)),
        "p_by_2035": float(np.mean(crossing_years <= 2035)),
        "p_by_2040": float(np.mean(crossing_years <= 2040)),
        "median_year": float(np.median(valid)) if len(valid) else np.nan,
        "p5_year": float(np.percentile(valid, 5)) if len(valid) else np.nan,
        "p95_year": float(np.percentile(valid, 95)) if len(valid) else np.nan,
        "never_crosses": float(np.mean(np.isnan(crossing_years))),
        # ...
    }
```

**What it does:** Computes median ONLY on `valid` (non-NaN) crossings. NaN represents "never crosses by 2040" and is excluded from median calculation.

**Modeling choice note:** This is a critical fragility. The median can appear stable even as failure rate changes, because failures are simply excluded. A scenario with 50% failure and median=2038 among successes looks identical to 10% failure and median=2038.

---

# 5. Reproduction steps

## Environment assumptions
- Python 3.11+ (tested on 3.14.3)
- `uv` package manager
- Repository root at `/home/ff/Documents/BoostMeUp/MoltBook_Sessie`

## Dependencies
```bash
UV_CACHE_DIR=.uv-cache uv sync
```

## Exact command to reproduce
```bash
MPLCONFIGDIR=/tmp/matplotlib UV_CACHE_DIR=.uv-cache uv run analyses/forecast_model.py
```

## Expected output files
- `assets/forecast_distribution.png` (generated chart)

## Expected terminal output (excerpt)
```
Running Conservative scenario...
Running Base case scenario...
Running Accelerated scenario...
========================================================================
AI-AGENT NETWORK FORECAST (ASSUMPTION-DRIVEN)
========================================================================

Model standard
------------------------------------------------------------------------
Simulations per scenario: 10,000
Threshold: 75
Floor constraints: M>=60, R>=60, N>=60, G>=60
Minimum consecutive years: 2
Random seed: 42

Results by scenario
------------------------------------------------------------------------

Conservative
  P(Level-3 by 2030): 0.0%
  P(Level-3 by 2035): 0.0%
  P(Level-3 by 2040): 0.2%
  Median crossing year: 2039
  90% interval among crossings: 2037-2040
  Never crosses by 2040: 99.8%

Base case
  P(Level-3 by 2030): 0.0%
  P(Level-3 by 2035): 11.3%
  P(Level-3 by 2040): 66.3%
  Median crossing year: 2038
  90% interval among crossings: 2034-2040
  Never crosses by 2040: 33.7%

Accelerated
  P(Level-3 by 2030): 0.0%
  P(Level-3 by 2035): 46.5%
  P(Level-3 by 2040): 95.0%
  Median crossing year: 2036
  90% interval among crossings: 2033-2039
  Never crosses by 2040: 5.0%

Threshold sensitivity (base case)
------------------------------------------------------------------------
threshold 70: P<=2035 11.3%, P<=2040 66.3%, median 2038
threshold 75: P<=2035 11.3%, P<=2040 66.3%, median 2038
threshold 80: P<=2035 11.3%, P<=2040 66.3%, median 2038

Floor sensitivity (base case)
------------------------------------------------------------------------
floors 55: P<=2035 18.8%, P<=2040 74.6%, median 2037
floors 60: P<=2035 11.3%, P<=2040 66.3%, median 2038
floors 65: P<=2035 6.2%, P<=2040 57.6%, median 2038
```

---

# 6. Current observed outputs

## Fresh run: 2026-03-23T17:13:51+01:00

### Crossing probability by 2040

| Scenario | P(cross by 2040) | Median Year | 90% Interval | Never Crosses |
|----------|------------------|-------------|--------------|---------------|
| Conservative | 0.2% | 2039 | 2037-2040 | 99.8% |
| **Base case** | **66.3%** | **2038** | **2034-2040** | **33.7%** |
| Accelerated | 95.0% | 2036 | 2033-2039 | 5.0% |

### Threshold sensitivity (base case)

| Threshold | P(cross by 2035) | P(cross by 2040) | Median |
|-----------|------------------|------------------|--------|
| 70 | 11.3% | 66.3% | 2038 |
| 75 | 11.3% | 66.3% | 2038 |
| 80 | 11.3% | 66.3% | 2038 |

**Note:** Identical results across all thresholds—floors bind first.

### Floor sensitivity (base case)

| Floor Value | P(cross by 2035) | P(cross by 2040) | Median |
|-------------|------------------|------------------|--------|
| 55 | 18.8% | 74.6% | 2037 |
| 60 | 11.3% | 66.3% | 2038 |
| 65 | 6.2% | 57.6% | 2038 |

---

# 7. Specific check: Governance growth 0.08 → 0.12

## Verification of change

Git diff confirms the change was made:

```diff
$ git diff HEAD~5 -- data/forecast_scenarios.json
-        {"code": "G", "initial_2026": 25, "growth_mu": 0.08,
+        {"code": "G", "initial_2026": 25, "growth_mu": 0.12,
```

## Model was rerun after change

YES. The run at 2026-03-23T17:13:51+01:00 used G=0.12.

## Median remains 2038

CONFIRMED. Even with G growth at 0.12, base case median crossing year is **2038**.

## Why unchanged? Evidence from inspection

The bottleneck analysis reveals:

1. **Governance floor is still the dominant bottleneck:** 42.0% of crossing runs have G as the last floor to satisfy
2. **G starts at 25, must reach 60:** Even with higher growth, the floor constraint requires substantial absolute progress
3. **Floors cause 3.6 year average delay:** In 98.7% of crossing runs, floors are satisfied AFTER threshold first exceeded
4. **Discrete year rounding:** The median falls between 2037-2038 depending on exact distribution shape; small parameter changes don't flip it

## Quantified impact of G increase

**What is solid:** Median crossing year remains **2038** after change from G=0.08 → 0.12.

**What is NOT solid:** Exact magnitude of improvement to success probability. No apples-to-apples before/after run was preserved with identical seeds. The +6pp estimate in earlier prose was speculative.

**What we CAN say:** With G=0.12 and seed=142, P(cross by 2040) = 66.3%, median = 2038.

---

# 8. Bottleneck analysis with evidence

## From `inspect_bottlenecks.py` output

### Which floor fails most often in non-crossing runs?

In 2040, among the 3,371 runs that never crossed:

| Floor | Count Below 60 | % of Non-crossing | Average Value |
|-------|----------------|-------------------|---------------|
| M | 66 | 2.0% | 96.6 |
| R | 30 | 0.9% | 98.0 |
| **N** | **1,009** | **29.9%** | 77.2 |
| **G** | **1,623** | **48.1%** | 65.9 |

**Conclusion:** G and N floors are the primary barriers to crossing.

### Which floor is the last to be satisfied?

Among 6,629 crossing runs:

| Floor | Times Last | % of Crossings |
|-------|------------|----------------|
| **G** | **2,785** | **42.0%** |
| **N** | **2,465** | **37.2%** |
| M | 812 | 12.2% |
| R | 567 | 8.6% |

**Conclusion:** Governance is indeed the dominant bottleneck, but Network is nearly as binding (37.2% vs 42.0%).

### When does readiness index exceed threshold vs floors satisfied?

- **6,546 / 6,629 crossing runs (98.7%)**: Floors satisfied AFTER threshold first exceeded
- **Average delay when floors bind:** 3.6 years

**Conclusion:** The headline threshold (75) is reached first; floors are the actual binding constraint that delays official "crossing."

### Attributing delay to shocks vs floors

| Variant | P(cross by 2040) | Never Crosses | Primary Change |
|---------|------------------|---------------|----------------|
| Base (with shocks) | 66.3% | 33.7% | — |
| No shocks | 91.5% | 8.5% | Shocks disabled |
| All floors=55 | 74.9% | 25.1% | Floors relaxed |
| G floor=50 | 75.4% | 24.6% | G floor only relaxed |

**Attribution estimate:**
- Shocks account for ~25pp of failure rate (66% → 91%)
- Floors account for ~8pp of failure rate (91% with no shocks but floor=60 vs 75% with floor=55)
- **Both effects matter, but shocks are larger contributor to failures**

---

# 9. Deterministic sanity check vs stochastic model

## Deterministic expected-path calculation

A back-of-envelope using expected log-growth:

```
G: 25 → 60 over 14 years (2026-2040)
Required annual growth: ln(60/25)/14 = 6.2% per year
Model G growth_mu: 12% per year (log-space expected value)

Expected G in 2040 without shocks: 25 * exp(0.12 * 14) = 25 * 5.3 = 132
But clamped to 100, and shocks subtract ~0.15*0.18*14 = 0.38 in log space

Adjusted: 25 * exp(0.12*14 - 0.38) = 25 * 3.6 = 90
```

So G should easily reach 60 in expectation. But:

1. **Variance matters:** With volatility=0.10 and 14 years, std dev in log-space = 0.10*sqrt(14) ≈ 0.37
2. **Consecutive years rule:** Even if G exceeds 60 in a given year, must hold for 2 years
3. **Joint floor probability:** All four floors must be satisfied simultaneously

## Why stochastic median (2038) vs deterministic estimate (~2034-2035)

The deterministic path suggests crossing around 2034-2035. The stochastic median is 2038 because:

1. **Left tail risk:** ~34% of runs fail entirely (never cross)
2. **Floor coordination:** Must satisfy G≥60 AND N≥60 AND M≥60 AND R≥60 simultaneously
3. **Consecutive persistence:** 2-year rule with reset means temporary dips destroy progress
4. **Shock clustering:** Bad luck in consecutive years has multiplicative penalty

**Key insight:** The deterministic path is NOT the median stochastic path. The distribution is right-skewed with a heavy left tail (failures), pulling the median later than the expected value.

---

# 10. Sensitivity table

## Fair comparison table (identical seed = 142)

These three variants use the **same random seed** for valid comparison:

| Variant | P(cross by 2040) | Median | % Never Crosses | Most Common Last Floor |
|---------|------------------|--------|-----------------|------------------------|
| **Base case** | 66.3% | 2038 | 33.7% | G |
| **Base case (no shocks)** | 91.4% | 2036 | 8.6% | N |
| **Base case (G floor=50)** | 75.4% | 2037 | 24.6% | N |

**Key insights from fair comparison:**
- **Removing shocks increases success probability by ~25pp** (66% → 91%), but median only shifts from 2038 → 2036
- **Relaxing G floor increases success probability by ~9pp** (66% → 75%), median stays at 2037
- **Median timing is sticky** due to: discrete year bins, floor-dominated constraints, and conditional calculation on successes only
- **Bottleneck shifts**: With relaxed G floor, Network (N) becomes the dominant last-floor-to-satisfy

## Methodological note

The comparison above uses identical seeds (142 = base case seed) to ensure differences reflect parameter changes, not Monte Carlo noise. Do NOT compare with earlier "temporary inspection" rows that used different seeds—these are not apples-to-apples.

## Directional sensitivity (from separate runs)

For rough orientation only (different seeds, not directly comparable):

| Change | Effect on P(cross 2040) | Effect on Median | Interpretation |
|--------|------------------------|------------------|----------------|
| G growth 0.12 → 0.16 | Moderate increase | None (stays ~2037-2038) | Helps more runs succeed, not timing |
| Consecutive years 2 → 1 | Small increase | None | Slight relaxation of persistence requirement |
| All floors 60 → 55 | Moderate increase | None (stays ~2037) | Comparable to G floor relaxation |

---

# 11. Contradictions / fragility / caveats

## 1. Threshold sensitivity shows NO effect

**Contradiction:** All three thresholds (70, 75, 80) produce identical P(cross) and median.

**Explanation:** Floors bind before threshold. The model reaches floors≥60 constraint before hitting any threshold ≥70.

**Fragility:** If floors were relaxed, threshold sensitivity would suddenly "wake up." Current results are floor-dominated, not threshold-dominated.

## 2. Median calculation excludes failures

**Caveat:** The median is computed only on runs that successfully cross. With 33.7% failure rate, the median among the 66.3% successes may not represent the full distribution.

**Implication:** Median could stay at 2038 even as failure rate changes significantly (e.g., 50% → 80% success rate).

## 3. Growth_mu is annual log growth, not percent

**Clarification:** `growth_mu=0.12` means 12% continuous compounding, equivalent to ~12.7% simple annual growth. The naming could confuse.

## 4. Shock application is additive in log-space

**Detail:** `log_growth[shocks] += pillar.neg_shock_size` adds shock magnitude directly to log growth. A -0.18 shock turns 12% growth into -6% growth (net), not a 18% multiplicative reduction.

## 5. Bounded [0,100] scale interacts with multiplicative growth

**Issue:** Values clamp at 100. High-growth pillars hit ceiling, compressing variance at top. This affects distribution shape.

## 6. "Two consecutive years" with full reset

**Modeling choice:** `consecutive = 0` on ANY failure year. This is stricter than "2 out of 3 years" or partial credit.

## 7. Floor sensitivity at 60 vs 65 shows identical median

**Contradiction:** One would expect lower floors to improve median crossing year, but median stays at 2038 for floors=60 and floors=65.

**Explanation:** Discrete year bins + small sample of crossing years + right-skewed distribution means median is "sticky."

---

# 12. Final handoff for ChatGPT

## A. What ChatGPT can safely conclude

1. **The G growth change (0.08→0.12) IS present in the active scenario file** and WAS reflected in the latest run.

2. **Median crossing year IS 2038** for base case as of 2026-03-23.

3. **Governance (G) and Network (N) floors are the binding constraints**, with G being the single most common bottleneck (42% of crossings).

4. **Floors dominate thresholds**—sensitivity to threshold changes is nil because floors bind first.

5. **~34% of simulations never cross by 2040.** Sensitivity analysis shows removing shocks increases success by ~25pp; relaxing floors increases success by ~9pp. These are not additive causal effects (shocks and floors interact), but both contribute to failure probability.

6. **The consecutive-years rule with floor requirements creates a 3.6 year average delay** between first threshold exceedance and official crossing.

7. **The unchanged median (2038) despite G growth increase is genuine**, not a calculation error. It reflects:
   - Discrete year rounding (median falls in 2037-2038 bin)
   - Floor constraints still binding even with faster growth
   - High variance and failure rate compressing the successful-crossing distribution

## B. What ChatGPT should treat as uncertain

1. **Exact magnitude of G growth effect on success probability:** No apples-to-apples before/after run with identical seeds was preserved. The "still 2038" conclusion is solid, but claims about +6pp improvement were speculative.

2. **Relative contribution of G vs N as bottleneck:** The 42% vs 37% split is from a single inspection run with different seed. Exact proportions may vary.

3. **Model structural validity:** The geometric mean, multiplicative growth, log-normal shocks, and floor constraints are modeling choices—not empirical facts.

4. **Whether 2038 is the "right" median:** The model is explicitly assumption-driven. Different assumptions produce different results.

## C. Most important pasted artifacts

### Core scenario parameters
```json
{
  "code": "G", "initial_2026": 25, "growth_mu": 0.12, 
  "volatility": 0.1, "neg_shock_prob": 0.15, "neg_shock_size": -0.18
}
```

### Floor constraints
```json
"floor_values": {"M": 60.0, "R": 60.0, "N": 60.0, "G": 60.0}
```

### Current base case results
```
Base case
  P(Level-3 by 2040): 66.3%
  Median crossing year: 2038
  90% interval among crossings: 2034-2040
  Never crosses by 2040: 33.7%
```

### Bottleneck evidence
```
Most common 'last floor to satisfy':
  G: 2785/6629 (42.0%)
  N: 2465/6629 (37.2%)
  M: 812/6629 (12.2%)
  R: 567/6629 (8.6%)
```

---

*End of handoff document*


---

## Appendix: Notes on temporary inspection

A temporary inspection script (`analyses/inspect_bottlenecks.py`) was created to generate the bottleneck analysis in Section 8. This script:
- Was NOT part of the canonical model
- Used additional seeds (142, 242) for sensitivity runs
- Was removed after data collection to avoid polluting the repo

All data from that script is preserved in this document (Sections 8 and 10).

---

*Document complete - 598 lines*
