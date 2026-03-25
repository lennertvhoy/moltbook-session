# Ablation Validation Report

**Generated:** 2026-03-25  
**Purpose:** Truth-first validation of ablation results, correcting errors and overstated claims

---

## Corrections to Previous Summary

### Error 1: Incorrect 2-of-3 claim

**What I said:** "2-of-3 jaren ipv 2 strikt → 14.7% crossing"

**What the data actually shows:**
- 1 jaar: **14.7%**
- 2 jaar (strict): **9.0%**
- 2-of-3: **9.2%**

**Correction:** The 2-of-3 rule produces **9.2%**, not 14.7%. It is essentially identical to the strict 2-year rule (difference: 0.2pp). This suggests that most failures to cross are not "just missed by 1 year" but more fundamental misses.

### Error 2: "80% of conservatism" claim was too strong

**What I said:** "Floors are responsible for ~80% of the conservatism"

**What the data actually supports:**
- No floors: 47.1% crossing
- Baseline (floors 60): 9.0% crossing
- Difference: **38.1 percentage points**

**Correction:** Floors reduce crossing probability by **38pp**, which is the largest single effect, but "80% of conservatism" is not a well-defined claim. Better formulation:

> "Within this parameterization, floors are the dominant structural constraint, reducing crossing probability by 38pp compared to an index-only specification."

### Error 3: "Shocks have 0 impact on median" was poorly formulated

**What I said:** "Shocks have 0 impact on median"

**What the data actually shows:**
- Deterministic crossing: **2039**
- Stochastic median (among successes): **2039**

**Correction:** Shocks affect the **distribution shape** and **success rate**, but do not shift the **central tendency of successful crossings**. This is different from "no impact"—it means the median successful run is not systematically delayed or accelerated by noise, but many runs fail entirely due to adverse shock sequences.

---

## Corrected Ablation Results

### 1. Floor Architecture (validated)

| Configuration | P(cross by 2040) | Change from baseline |
|---------------|------------------|---------------------|
| No floors | 47.1% | +38.1pp |
| Floors 50 | 27.1% | +18.1pp |
| Floors 55 | 17.4% | +8.4pp |
| **Floors 60 (baseline)** | **9.0%** | — |
| Floors 65 | 3.6% | -5.4pp |

**Finding:** Floors are the dominant constraint. The effect is monotonic and large.

### 2. Time Horizon (validated)

| Horizon | P(cross by horizon) | P(cross by 2040) | Median year (if crosses) |
|---------|---------------------|------------------|--------------------------|
| 2040 | 9.0% | 9.0% | 2039 |
| 2045 | 37.5% | 9.3% | 2042 |
| 2050 | 62.4% | 8.8% | 2045 |
| 2060 | 88.1% | 8.4% | 2047 |

**Finding:** The "91% never crosses by 2040" is misleading. By 2050, 62% have crossed. The horizon truncation creates an artificial "never" category.

### 3. Consecutive Years Rule (corrected)

| Rule | P(cross by 2040) | Change from baseline |
|------|------------------|---------------------|
| 1 year | 14.7% | +5.7pp |
| **2 years strict (baseline)** | **9.0%** | — |
| 2-of-3 | 9.2% | +0.2pp |
| Rolling 2-year | 9.0% | 0pp |

**Finding:** The 2-year rule reduces crossing by 5.7pp vs 1-year. The 2-of-3 variant provides almost no relaxation (0.2pp), suggesting that failures are not marginal "near misses" but substantial misses.

### 4. Aggregation Method (validated)

| Method | P(cross by 2040) | Change from baseline |
|--------|------------------|---------------------|
| **Geometric (baseline)** | **9.0%** | — |
| Arithmetic | 9.1% | +0.1pp |
| CES (rho=-1) | 8.9% | -0.1pp |
| Softmin | 5.6% | -3.4pp |

**Finding:** Geometric vs arithmetic makes negligible difference (0.1pp). Only softmin (which heavily penalizes low values) has a substantial effect. The "double penalty" hypothesis (geometric mean + floors) is partially incorrect—floors completely dominate.

### 5. Deterministic Baseline (validated)

Deterministic trajectory (median growth, no shocks):
- All pillars reach 60 by 2039
- Index reaches 75+ by 2039
- **Deterministic crossing: 2039**

**Finding:** The deterministic path crosses at the same year as the stochastic median (2039). Noise affects the probability of success, not the central timing of success.

---

## Honest Interpretation

### What this actually shows

1. **The model is essentially a floor-gated model**
   - Threshold 75 is rarely binding (floors fail first)
   - Floor architecture explains ~38pp of the 9% baseline
   - Aggregation method is almost irrelevant

2. **The 2040 horizon creates artificial truncation**
   - "Never crosses" should be "not by 2040"
   - By 2050, majority (62%) have crossed
   - Horizon choice is presentationally consequential

3. **The 2-year consecutive rule has moderate effect**
   - 5.7pp reduction vs 1-year
   - 2-of-3 provides minimal relaxation (0.2pp)
   - This suggests failures are not "just missed" but substantial

4. **Stochastic elements affect success rate, not median timing**
   - Deterministic: 2039
   - Stochastic median: 2039
   - Shocks create "failures" more than "delays"

### What this does NOT show

1. **"80% of conservatism"** — Not a valid claim
2. **"Aggregation doesn't matter"** — Only true within tested range; softmin matters
3. **"2-of-3 is equivalent to 1-year"** — It is equivalent to 2-year, not 1-year
4. **"Shocks have no effect"** — They have large effect on success rate, not median

---

## Implications for Model Assessment

### The core question is now clearly: floor justification

The ablation shows that:
- Floors dominate all other structural choices
- Floor level (60 vs 55 vs 65) has enormous effect
- Floor uniformity (same for M/R/N/G) is untested

**Therefore:** The substantive debate should focus on:
1. Why 60 specifically?
2. Why uniform across M/R/N/G?
3. Is 60 a capability threshold or a convenience choice?
4. What empirical/theoretical basis supports these levels?

### Reporting must change

Current:
> "91% never crosses by 2040"

Should be:
> "9% cross by 2040; 37% cross by 2045; 62% cross by 2050"

### The "intuition gap" is now clearer

If intuitive expectation is 2033-2035:
- Deterministic path: 2039 (close)
- Stochastic median: 2039 (close)
- Main divergence: floor failures (38pp) + horizon truncation

The gap is not "model is too conservative" but "floors may be too strict relative to intuitive readiness thresholds."

---

## Recommended Next Steps (No Model Changes Yet)

1. **Document floor justification**
   - Current: expert judgment, no empirical basis
   - Need: conceptual framework for why 60, why uniform

2. **Report multi-horizon probabilities**
   - Always show 2040, 2045, 2050
   - Never say "never" without horizon qualifier

3. **Test floor variations as audit, not tuning**
   - Uniform 55, 60, 65
   - Differential (G=55, N=55, M=R=60)
   - Soft floors / penalty functions
   - Report sensitivity, don't change defaults yet

4. **Validate consecutive-years results**
   - ✓ Done: confirmed 2-of-3 ≈ 2-year (not 1-year)

---

## Questions for Floor Justification

To properly justify floors=60, should be able to answer:

1. **What concrete capability does Memory=60 represent?**
   - Persistent context across X sessions?
   - Y% reliability of state reconstruction?

2. **Why is Governance=60 the same as Memory=60?**
   - Are these comparable scales?
   - Should institutional readiness have different threshold?

3. **What happens at 59 vs 60?**
   - Is there a phase transition?
   - Or is this continuous with arbitrary cutoff?

4. **Empirical basis:**
   - Any historical systems that achieved "society-like" function at these levels?
   - Or is this aspirational specification?

Without answers, floors=60 remains an unexamined assumption that happens to dominate model output.

---

**Status:** Validation complete. Ready for floor justification audit.
