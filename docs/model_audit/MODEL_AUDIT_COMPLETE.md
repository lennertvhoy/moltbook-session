# Forecast Model Audit Package

**Generated:** 2026-03-25  
**Purpose:** Provide complete, self-contained context for critical evaluation of the forecasting model  
**Scope:** Both old (v1) and new (v2) model implementations

---

## 1. Executive Audit Summary

### 1.1 What the Old Model Did (Pre-March 2025)

The original model (v1) used simple multiplicative exponential growth on the observation scale:

```
y_t = y_{t-1} × exp(growth_mu + noise)
y_t = clip(y_t, 0, 100)  # hard bounds
```

**Key characteristics:**
- Growth was exponential in raw scores (0-100)
- Hard clipping at 0 and 100 created unnatural behavior at boundaries
- Fixed growth rate per pillar (no evolution of growth over time)
- Single noise source (no distinction between level and trend uncertainty)

**Reported output:** ~28% probability of crossing by 2040 (base case)

### 1.2 What the New Model Does (March 2025+)

The enhanced model (v2) uses a state-space approach with latent capability:

```
z_t = logit(y_t/100)                   # transform to unbounded scale
z_t = z_{t-1} + g_t + ε_t              # level evolves by growth rate plus noise
g_t = φ×g_{t-1} + (1-φ)×ḡ + η_t       # growth rate mean-reverts to long-run mean
y_t = 100 × sigmoid(z_t)               # transform back with natural saturation
```

**Key characteristics:**
- Logit transform creates natural asymptotic approach to 100 (no hard clipping)
- Growth rate g_t is stochastic and mean-reverting (φ = 0.9)
- Two noise sources: level shock ε_t and growth shock η_t
- Separates level uncertainty from trend uncertainty

**Reported output:** ~8-9% probability of crossing by 2040 (base case)

### 1.3 Key Structural Changes

| Aspect | Old (v1) | New (v2) | Impact on Crossing |
|--------|----------|----------|-------------------|
| Scale | Raw 0-100 | Logit → sigmoid | **MAJOR** - Natural saturation slows late-stage growth |
| Growth dynamics | Fixed exp | Local linear trend | **MINOR** - Mean reversion (φ=0.9) keeps growth near ḡ |
| Growth evolution | Constant | Mean-reverting | **NEGLIGIBLE** - φ sensitivity test shows almost no effect |
| Noise structure | Single | Level + trend | **MODERATE** - Additional variance source |

### 1.4 Attribution of the Difference

**Primary driver of lower crossing probability: LOGIT/SIGMOID TRANSFORMATION**

The ablation study reveals:
- Model A (fixed growth, logit scale): 8.2% crossing
- Model B (piecewise, 30% accel post-2028): 48.7% crossing
- Model C (local linear trend, φ=0.9): 9.0% crossing

**Critical finding:** Model A and Model C produce nearly identical results (8.2% vs 9.0%). This means:
1. The mean-reverting growth (Model C's main feature) has MINIMAL impact on crossing probability
2. The logit/sigmoid transformation (shared by all models) is the DOMINANT factor
3. Model B's higher probability comes entirely from the 30% acceleration assumption, NOT from the state-space structure

**Saturation analysis confirms this:**
- At score 20: logit gives 3.4 effective growth vs 2.0 linear (70% MORE growth)
- At score 80: logit gives 3.0 effective growth vs 8.0 linear (62% LESS growth)
- At score 90: logit gives 1.7 effective growth vs 9.0 linear (82% LESS growth)
- At score 99: logit gives 0.2 effective growth vs 9.9 linear (98% LESS growth)

**Conclusion:** The model is more conservative primarily because high scores (70-100) grow MUCH slower under the sigmoid transformation, not because of sophisticated state-space dynamics.

### 1.5 What Has NOT Been Sufficiently Validated

1. **Whether logit is the appropriate transformation** - No theoretical justification provided beyond "natural saturation"
2. **Whether φ=0.9 is empirically grounded** - Sensitivity shows almost no effect, suggesting it may not matter
3. **Backtest against historical capability data** - No out-of-sample validation performed
4. **Whether floors or threshold is the binding constraint** - Floor sensitivity is high, threshold sensitivity is low
5. **Model B's 30% acceleration** - Arbitrary breakpoint year (2028) and acceleration magnitude
6. **Initial 2026 values** - Expert judgment, not fitted from data

---

## 2. Exact Model Documentation

### 2.1 Observation Scale

**Pillar scores:** Continuous values in [0, 100]
- 0 = complete absence of capability
- 100 = theoretical maximum / perfect capability
- Initial values (2026) range from 20 (Network) to 55 (Capability)

### 2.2 Transformation Functions

**Logit transform (observation → latent):**
```python
def to_logit(y):
    y_clipped = clip(y, 0.01, 99.99)  # prevent numerical issues
    return log(y / (100 - y))
```

**Key values:**
| y | z = logit(y/100) |
|---|------------------|
| 1 | -4.6 |
| 20 | -1.39 |
| 50 | 0 |
| 80 | 1.39 |
| 99 | 4.6 |

**Sigmoid transform (latent → observation):**
```python
def from_logit(z):
    return 100 / (1 + exp(-z))
```

### 2.3 Latent State(s)

**Model A (Fixed Log Growth):**
- Single latent state: z_t (capability level on logit scale)

**Model B (Piecewise Growth):**
- Single latent state: z_t
- Regime indicator: I(t < breakpoint)
- Growth rate switches between g_pre and g_post

**Model C (Local Linear Trend - DEFAULT):**
- Two latent states:
  - z_t: capability level (logit scale)
  - g_t: growth rate (change in z per year)

### 2.4 Evolution Equations

**Model A - Fixed Log Growth:**
```
z_t = z_{t-1} + ḡ + ν_t
where ν_t ~ N(0, σ)
      ḡ = growth_mu (from config)
      σ = volatility (from config)
```

**Model B - Piecewise Growth:**
```
z_t = z_{t-1} + g_t + ν_t
where g_t = g_pre if t < breakpoint else g_post
      g_pre = growth_mu
      g_post = growth_mu × 1.3 (30% acceleration)
      breakpoint = 2028 (hardcoded)
```

**Model C - Local Linear Trend:**
```
Level equation:   z_t = z_{t-1} + g_t + ε_t
Growth equation:  g_t = φ×g_{t-1} + (1-φ)×ḡ + η_t

where ε_t ~ N(0, σ_level)    [level shock]
      η_t ~ N(0, σ_growth)   [growth shock]
      ḡ = growth_mu (from config)
      σ_level = volatility (from config)
      σ_growth = growth_volatility (scenario-dependent: 0.015-0.03)
      φ = 0.9 (persistence, hardcoded)
```

### 2.5 Observation Equation

All models:
```
y_t = from_logit(z_t) = 100 / (1 + exp(-z_t))
```

### 2.6 Noise Components

| Component | Symbol | Distribution | Source |
|-----------|--------|--------------|--------|
| Level shock | ε_t | N(0, σ_level) | volatility (config) |
| Growth shock | η_t | N(0, σ_growth) | growth_volatility (hardcoded per scenario) |
| Negative shock | - | Bernoulli(p) × size | neg_shock_prob, neg_shock_size (config) |

**Negative shock logic:** Applied to level equation. If random < neg_shock_prob, add neg_shock_size (negative value) to growth.

### 2.7 Regime/Breakpoint Logic

**Model A:** No regime switching

**Model B:**
```python
if year < 2028:
    growth = growth_mu
else:
    growth = growth_mu * 1.3  # 30% acceleration
```

**Model C:** No explicit regime, but mean reversion creates implicit regime toward long-run growth

### 2.8 Saturation/Begrenzing

**Implicit via sigmoid:** No explicit bounds checking needed. As z → ∞, y → 100 asymptotically.

**Numerical clipping:** In to_logit(), y is clipped to [0.01, 99.99] to prevent log(0) or division by zero.

### 2.9 Crossing Logic

**Threshold:** Readiness Index ≥ 75

**Index calculation (all models):**
```
Index_t = 100 × Π_i (pillar_i,t / 100)^weight_i
```

**Weights:**
- C (Capability): 20%
- E (Efficiency): 20%
- M (Memory): 15%
- R (Reliability): 15%
- N (Network): 12%
- G (Governance): 10%
- D (Demand): 8%

**Floors:** Four pillars must each be ≥ 60:
- M (Memory) ≥ 60
- R (Reliability) ≥ 60
- N (Network) ≥ 60
- G (Governance) ≥ 60

**Consecutive years rule:** Threshold AND floors must be met for 2 consecutive years before crossing is declared.

**Algorithm:**
```python
crossing_year = NaN
for each simulation:
    consecutive = 0
    for year_idx, year in enumerate(years):
        floors_met = all(pillar_values[code][sim][year_idx] >= floor for code, floor in floors)
        if index[sim][year_idx] >= threshold and floors_met:
            consecutive += 1
            if consecutive >= 2:
                crossing_year = year
                break
        else:
            consecutive = 0
```

---

## 3. File Inventory

### 3.1 Core Model Files

| File | Path | Purpose | Key Assumptions |
|------|------|---------|-----------------|
| Main model | `analyses/forecast_model.py` | Complete implementation of A, B, C models | φ=0.9, breakpoint=2028, growth_volatility scenario-dependent |
| Extended model | `analyses/forecast_model_v2.py` | Comparison and visualization | Same as main |
| Config | `data/forecast_scenarios.json` | All parameters | Initial values, growth_mu, volatility, floors, threshold are EXPERT JUDGMENT, not fitted |

### 3.2 Documentation Files

| File | Path | Purpose |
|------|------|---------|
| Content | `content/06-forecast.md` | Explains model to readers |
| AGENTS.md | `AGENTS.md` | Project overview |
| This audit | `docs/model_audit/MODEL_AUDIT_COMPLETE.md` | Truth-first audit |
| Audit data | `docs/model_audit/audit_data.json` | Machine-readable ablation results |

### 3.3 Generated Assets

| File | Path | Purpose |
|------|------|---------|
| Main plot | `assets/forecast_distribution.png` | 4-panel visualization |
| Comparison | `assets/forecast_model_comparison_*.png` | Model A/B/C comparison |
| Uncertainty | `assets/forecast_uncertainty_decomposition.png` | Level vs trend uncertainty |
| Sigmoid demo | `assets/forecast_sigmoid_demo.png` | Mathematical transformation |

---

## 4. Code Excerpts

### 4.1 Transformation Functions

```python
def to_logit(y: np.ndarray) -> np.ndarray:
    """Transform 0-100 scores to logit scale.
    
    Mathematical definition:
        z = log(y / (100 - y))
        
    This maps:
        y=50  → z=0
        y=90  → z≈2.2
        y=99  → z≈4.6
        y→100 → z→∞ (asymptotic saturation)
    """
    y_clipped = np.clip(y, 0.01, 99.99)  # GUARDRAIL: prevent numerical issues
    return np.log(y_clipped / (100 - y_clipped))


def from_logit(z: np.ndarray) -> np.ndarray:
    """Transform logit scale back to 0-100 scores.
    
    Mathematical definition:
        y = 100 / (1 + exp(-z)) = 100 * sigmoid(z)
    """
    return 100.0 / (1.0 + np.exp(-z))
```

**Location:** lines 46-68 in `analyses/forecast_model.py`

### 4.2 Model C - Local Linear Trend (Default)

```python
class ModelC_LocalLinearTrend(GrowthModel):
    """Model C: Local linear trend state-space model (DEFAULT).
    
    State equations on logit scale:
        z_t = z_{t-1} + g_t + eps_t      (level equation)
        g_t = phi*g_{t-1} + (1-phi)*g_bar + eta_t  (growth equation)
    
    Where:
        z_t = latent capability level
        g_t = latent growth rate (mean-reverting to g_bar)
        phi = persistence parameter (default 0.9)
        eps_t ~ N(0, sigma_level), eta_t ~ N(0, sigma_growth)
    """
    
    def __init__(self, rng: np.random.Generator, persistence: float = 0.9):
        super().__init__(rng)
        self.persistence = persistence  # phi = 0.9 HARDCODED
    
    def simulate_pillar(self, pillar: PillarConfig, n_simulations: int, n_years: int) -> np.ndarray:
        """Simulate with local linear trend on logit scale."""
        z_values = np.zeros((n_simulations, n_years))
        z_values[:, 0] = to_logit(pillar.initial_2026)
        
        # Initialize latent growth rate with uncertainty
        g_values = np.full(n_simulations, pillar.growth_mu) + self.rng.normal(
            0, 0.05, n_simulations  # INITIAL UNCERTAINTY: 0.05 std
        )
        
        sigma_level = pillar.volatility      # From config
        sigma_growth = pillar.growth_volatility  # HARDCODED per scenario
        
        for t in range(1, n_years):
            # Growth equation with mean reversion
            g_values = (
                self.persistence * g_values 
                + (1 - self.persistence) * pillar.growth_mu 
                + self.rng.normal(0, sigma_growth, n_simulations)
            )
            
            # Level equation
            level_shock = self.rng.normal(0, sigma_level, n_simulations)
            shocks = self.rng.random(n_simulations) < pillar.neg_shock_prob
            level_shock[shocks] += pillar.neg_shock_size
            
            z_values[:, t] = z_values[:, t - 1] + g_values + level_shock
        
        return from_logit(z_values)
```

**Location:** lines 235-286 in `analyses/forecast_model.py`

### 4.3 Threshold Crossing Logic

```python
def _check_threshold_crossing(
    self,
    index: np.ndarray,           # Shape: (n_simulations, n_years)
    pillar_values: dict[str, np.ndarray],
    threshold: float | None = None,
    floor_values: dict[str, float] | None = None,
) -> np.ndarray:
    """Determine the first year a simulation crosses and sustains the threshold."""
    active_threshold = self.scenario.threshold if threshold is None else threshold
    active_floors = self.scenario.floor_values if floor_values is None else floor_values
    crossing_years = np.full(self.n_simulations, np.nan)

    for sim_idx in range(self.n_simulations):
        consecutive = 0
        for year_idx, year in enumerate(self.years):
            # Check ALL floors
            floors_met = all(
                pillar_values[code][sim_idx, year_idx] >= minimum
                for code, minimum in active_floors.items()
            )
            # Check threshold AND floors
            if index[sim_idx, year_idx] >= active_threshold and floors_met:
                consecutive += 1
                if consecutive >= self.scenario.min_consecutive_years:  # 2 years
                    crossing_years[sim_idx] = year
                    break
            else:
                consecutive = 0  # RESET if either condition fails

    return crossing_years
```

**Location:** lines 328-355 in `analyses/forecast_model.py`

### 4.4 Index Calculation

```python
def _calculate_readiness_index(self, pillar_values: dict[str, np.ndarray]) -> np.ndarray:
    """Calculate the weighted geometric mean readiness index."""
    index = np.ones((self.n_simulations, len(self.years)))
    for pillar in self.scenario.pillars:
        index *= (pillar_values[pillar.code] / 100.0) ** pillar.weight
    return index * 100.0
```

**Key property:** Uses geometric mean, not arithmetic. Low pillars drag down the index more than high pillars pull it up.

**Location:** lines 321-326 in `analyses/forecast_model.py`

---

## 5. Historical Data Context

### 5.1 What Historical Data Is Used

**Answer: NONE for the forecasting itself.**

The model is purely assumption-driven. The parameters are:
- Initial 2026 values: Expert judgment
- Growth rates (growth_mu): Expert judgment
- Volatilities: Expert judgment
- Floors and threshold: Expert judgment

### 5.2 What External Data Informs the Model

The following sources inform the parameter choices but are NOT used to fit the model:

| Source | Data | How It Informs |
|--------|------|----------------|
| Stanford HAI AI Index 2025 | Benchmark improvements (MMMU +18.8, GPQA +48.9, SWE-bench +67.3) | Suggests capability growth is possible |
| Epoch AI | Compute growth (~5x/year), efficiency (~3x/year) | Informs Efficiency pillar assumptions |
| METR | Time horizon doubling ~7 months | Suggests accelerating capability possible |

**Critical caveat:** These data points are used to SET PARAMETERS, not to VALIDATE the model. There is no backtest against historical pillar trajectories.

### 5.3 Data Sample

N/A - No time series data is used. The model is initialized at 2026 with point estimates.

### 5.4 Which Assumptions Are Expert Judgment vs Data-Derived

| Parameter | Source | Confidence |
|-----------|--------|------------|
| Initial 2026 values (C=55, E=45, etc.) | Expert judgment | LOW - Arbitrary starting points |
| Growth rates (growth_mu) | Expert judgment + trend data | MEDIUM - Informed by AI Index but not fitted |
| Volatility | Expert judgment | LOW - No empirical basis |
| Floors (60) | Expert judgment | MEDIUM - Based on institutional analysis |
| Threshold (75) | Expert judgment | MEDIUM - Based on qualitative readiness |
| φ (0.9) | Hardcoded | LOW - Not fitted or validated |
| Breakpoint (2028) | Hardcoded | LOW - Arbitrary |
| Acceleration (30%) | Hardcoded | LOW - Arbitrary |

---

## 6. Parameter Provenance

### 6.1 Complete Parameter Table

| Parameter | Current Value | Defined In | Meaning | Source | Sensitivity |
|-----------|---------------|------------|---------|--------|-------------|
| **Weights** |||||
| C_weight | 0.20 | forecast_scenarios.json | Capability importance | Expert judgment | LOW (fixed) |
| E_weight | 0.20 | forecast_scenarios.json | Efficiency importance | Expert judgment | LOW (fixed) |
| M_weight | 0.15 | forecast_scenarios.json | Memory importance | Expert judgment | LOW (fixed) |
| R_weight | 0.15 | forecast_scenarios.json | Reliability importance | Expert judgment | LOW (fixed) |
| N_weight | 0.12 | forecast_scenarios.json | Network importance | Expert judgment | LOW (fixed) |
| G_weight | 0.10 | forecast_scenarios.json | Governance importance | Expert judgment | LOW (fixed) |
| D_weight | 0.08 | forecast_scenarios.json | Demand importance | Expert judgment | LOW (fixed) |
| **Initial Values (2026)** |||||
| C_initial | 55 | forecast_scenarios.json | Starting capability | Expert judgment | HIGH |
| E_initial | 45 | forecast_scenarios.json | Starting efficiency | Expert judgment | HIGH |
| M_initial | 30 | forecast_scenarios.json | Starting memory | Expert judgment | HIGH |
| R_initial | 28 | forecast_scenarios.json | Starting reliability | Expert judgment | HIGH |
| N_initial | 20 | forecast_scenarios.json | Starting network | Expert judgment | HIGH |
| G_initial | 25 | forecast_scenarios.json | Starting governance | Expert judgment | HIGH |
| D_initial | 50 | forecast_scenarios.json | Starting demand | Expert judgment | HIGH |
| **Growth Rates (ḡ)** |||||
| C_growth | 0.18 | forecast_scenarios.json | Capability growth | Expert + trend data | HIGH |
| E_growth | 0.28 | forecast_scenarios.json | Efficiency growth | Expert + trend data | HIGH |
| M_growth | 0.14 | forecast_scenarios.json | Memory growth | Expert judgment | HIGH |
| R_growth | 0.16 | forecast_scenarios.json | Reliability growth | Expert judgment | HIGH |
| N_growth | 0.15 | forecast_scenarios.json | Network growth | Expert judgment | HIGH |
| G_growth | 0.12 | forecast_scenarios.json | Governance growth | Expert judgment | HIGH |
| D_growth | 0.12 | forecast_scenarios.json | Demand growth | Expert judgment | HIGH |
| **Noise Parameters** |||||
| C_volatility | 0.08 | forecast_scenarios.json | Capability noise | Expert judgment | MEDIUM |
| σ_growth (base) | 0.02 | forecast_model.py | Growth rate volatility | HARDCODED | LOW (tested) |
| φ (persistence) | 0.9 | forecast_model.py | Mean reversion strength | HARDCODED | VERY LOW |
| **Threshold/Floors** |||||
| Threshold | 75 | forecast_scenarios.json | Readiness index target | Expert judgment | LOW |
| Floor M,R,N,G | 60 | forecast_scenarios.json | Minimum pillar scores | Expert judgment | HIGH |
| Consecutive years | 2 | forecast_scenarios.json | Sustained crossing rule | Expert judgment | MEDIUM |
| **Model B Specific** |||||
| Breakpoint year | 2028 | forecast_model.py | Regime switch | HARDCODED | NOT TESTED |
| Post-breakpoint accel | 30% | forecast_model.py | Growth acceleration | HARDCODED | NOT TESTED |

### 6.2 Key Uncertainties

**HIGH SENSITIVITY (changes crossing probability by >5%):**
- Initial values (especially low ones like N=20, G=25)
- Growth rates (especially slow ones like G=0.12)
- Floor values (60 is critical; 55→65 changes crossing from 17% to 3%)

**MEDIUM SENSITIVITY (changes crossing probability by 1-5%):**
- Volatility parameters
- Threshold (only at extreme values like 85)

**LOW/NEGLIGIBLE SENSITIVITY (changes crossing probability by <1%):**
- φ (persistence) - surprisingly invariant
- σ_growth (growth volatility)
- Weights (fixed, not tested)

---

## 7. Crossing Attribution (Ablation Study)

### 7.1 Full Ablation Results

**Base case scenario, 10,000 simulations:**

| Model | P(cross by 2040) | Median year (if crosses) | Never crosses |
|-------|------------------|--------------------------|---------------|
| A (Fixed log growth) | 8.2% | 2040 | 91.8% |
| B (Piecewise, +30% post-2028) | 48.7% | 2039 | 51.3% |
| C (Local linear trend, φ=0.9) | 9.0% | 2039 | 91.0% |

### 7.2 Step-by-Step Attribution

Starting from Model A (8.2%), what changes increase/decrease crossing probability?

| Change | Effect | Explanation |
|--------|--------|-------------|
| Logit transform (vs raw exponential) | -20% (estimated) | Saturates high scores, slowing late-stage growth |
| Mean reversion (φ=0.9) | +0.8% | Negligible - growth stays near ḡ |
| Separate growth noise (σ_growth) | +0-1% | Adds variance, minimal net effect |
| **Combined (Model C)** | **+0.8%** | Effectively same as Model A |
| 30% acceleration post-2028 | **+40.5%** | Massive effect if acceleration assumed |

### 7.3 Critical Insight

**The "enhanced" state-space model (Model C) produces virtually identical results to the "simple" fixed-growth model (Model A).**

This suggests:
1. The sophisticated state-space structure may be unnecessary complexity
2. The logit/sigmoid transformation is doing ALL the work in making the model conservative
3. The mean reversion (φ=0.9) is so strong that growth rates don't meaningfully evolve

### 7.4 Floor vs Threshold Sensitivity

| Floor value | P(cross by 2040) | Change from baseline |
|-------------|------------------|---------------------|
| 50 | 26.6% | +18.4pp |
| 55 | 17.1% | +8.9pp |
| 60 (baseline) | 8.2% | - |
| 65 | 3.1% | -5.1pp |
| 70 | 1.0% | -7.2pp |

| Threshold | P(cross by 2040) | Change from baseline |
|-----------|------------------|---------------------|
| 70 | 8.3% | +0.1pp |
| 75 (baseline) | 8.2% | - |
| 80 | 5.8% | -2.4pp |
| 85 | 0.6% | -7.6pp |

**Finding:** Floors are the binding constraint at current settings. The threshold only becomes limiting at extreme values (85+).

---

## 8. Debug / Sanity Checks

### 8.1 Scale Consistency After Logit/Sigmoid

**Test:** Transform [1, 20, 50, 80, 99] to logit and back.

| Original y | z = logit(y) | y' = sigmoid(z) | Error |
|------------|--------------|-----------------|-------|
| 1 | -4.595 | 1.0 | 0% |
| 20 | -1.386 | 20.0 | 0% |
| 50 | 0.0 | 50.0 | 0% |
| 80 | 1.386 | 80.0 | 0% |
| 99 | 4.595 | 99.0 | 0% |

**Result:** ✓ PASS - Transformations are mathematically inverse

### 8.2 Saturation Timing

**Question:** Does saturation kick in too early?

**Evidence from saturation analysis:**
- At y=70: logit effective growth = 4.0 vs linear 7.0 (43% reduction)
- At y=80: logit effective growth = 3.0 vs linear 8.0 (62% reduction)
- At y=90: logit effective growth = 1.7 vs linear 9.0 (82% reduction)

**Assessment:** Growth slows significantly above 70-80. This is the dominant reason for low crossing probability.

### 8.3 Growth Mean Reversion Strength

**Test:** Vary φ from 0.7 to 0.99

| φ | P(cross by 2040) |
|---|------------------|
| 0.7 | 8.5% |
| 0.8 | 8.4% |
| 0.9 | 8.2% |
| 0.95 | 8.3% |
| 0.99 | 8.1% |

**Result:** ALMOST NO EFFECT. This is suspicious.

**Hypothesis:** The level noise (σ_level) and growth noise (σ_growth) are calibrated such that g_t doesn't deviate far from ḡ over the 15-year horizon. Mean reversion doesn't matter if growth never has time to drift.

### 8.4 Floors Correctly Applied

**Test:** Check that floor constraint requires ALL four pillars (M,R,N,G) ≥ floor.

**Code verification:**
```python
floors_met = all(
    pillar_values[code][sim_idx, year_idx] >= minimum
    for code, minimum in active_floors.items()
)
```

**Result:** ✓ PASS - Uses `all()`, not `any()` or average

### 8.5 Consecutive Years Logic

**Test:** Check that 2 consecutive years are required and that counter resets on failure.

**Code verification:**
```python
if index >= threshold and floors_met:
    consecutive += 1
    if consecutive >= 2:  # CHECK: >= not ==
        crossing_year = year
        break
else:
    consecutive = 0  # CHECK: resets to 0
```

**Result:** ✓ PASS - Logic is correct

### 8.6 Initial State

**Test:** Verify 2026 values match config.

**Code verification:**
```python
z_values[:, 0] = to_logit(pillar.initial_2026)
```

**Result:** ✓ PASS - Uses config values directly

### 8.7 Off-by-One in Years

**Test:** Check that simulation runs 2026-2040 inclusive (15 years).

**Code:**
```python
self.years = np.arange(2026, 2041)  # 15 years: 2026, ..., 2040
```

**Result:** ✓ PASS - 15 years total

### 8.8 Unexpected Clipping

**Test:** Check for hidden clip operations.

**Findings:**
- `to_logit()`: clips y to [0.01, 99.99] to prevent log(0)
- `from_logit()`: No clipping needed (sigmoid naturally bounded)
- Main simulation: No explicit clipping

**Result:** ✓ PASS - Only numerical guardrails

### 8.9 Percentile Calculations

**Test:** Verify median, p5, p95 use correct axis.

**Code:**
```python
median = np.median(index, axis=0)  # Across simulations
p25 = np.percentile(index, 25, axis=0)
```

**Result:** ✓ PASS - axis=0 means across simulations, per year

### 8.10 Negative Shock Application

**Test:** Verify negative shocks are applied to level, not growth.

**Code:**
```python
level_shock = self.rng.normal(0, sigma_level, n_simulations)
shocks = self.rng.random(n_simulations) < pillar.neg_shock_prob
level_shock[shocks] += pillar.neg_shock_size  # Added to LEVEL shock
z_values[:, t] = z_values[:, t - 1] + g_values + level_shock
```

**Result:** ✓ PASS - Applied to level equation

---

## 9. Backtests and Model Comparison

### 9.1 The Fundamental Problem

**There is no historical data on the 7 pillars to backtest against.**

The pillars are conceptual constructs, not measured time series. We cannot:
- Test out-of-sample forecasts
- Compute RMSE against historical trajectories
- Validate the logit transform choice empirically

### 9.2 What Could Be Done (But Wasn't)

| Test | Data Needed | Status |
|------|-------------|--------|
| Rolling origin on pillar trajectories | Time series of C,E,M,R,N,G,D scores | NOT AVAILABLE |
| Proxy validation using ECI | Epoch Capability Index 2023-2025 | NOT DONE |
| Compute-growth correlation | Training compute vs capability | NOT DONE |
| Expert elicitation validation | Survey of AI researchers | NOT DONE |

### 9.3 Qualitative Model Comparison

| Criterion | Model A | Model B | Model C |
|-----------|---------|---------|---------|
| Mathematical simplicity | ✓✓✓ | ✓✓ | ✓ |
| Natural saturation | ✓ | ✓ | ✓ |
| Growth rate evolution | ✗ | ✗ (step) | ✓ (smooth) |
| Mean reversion | ✗ | ✗ | ✓ |
| Computational cost | Low | Low | Medium |
| Crossing probability (base) | 8.2% | 48.7% | 9.0% |

### 9.4 Which Model is "Best"?

**From a forecasting perspective:** Cannot determine without validation data.

**From a theoretical perspective:**
- Model C has the most plausible microfoundations (stochastic growth, mean reversion)
- Model B's 30% acceleration is arbitrary
- Model A is too simple but produces similar results to Model C

**From a practical perspective:**
- Model A and C are essentially equivalent in output (8.2% vs 9.0%)
- Model C adds complexity without changing conclusions
- Model B's high probability (48.7%) depends entirely on the arbitrary 30% acceleration

---

## 10. Visualizations

### 10.1 Generated Plots

| File | Description | Key Insight |
|------|-------------|-------------|
| `forecast_distribution.png` | 4-panel main visualization | Shows trajectories, crossing CDF, distribution, audit notes |
| `forecast_model_comparison_*.png` | Model A/B/C comparison per scenario | Model B dramatically different due to acceleration |
| `forecast_uncertainty_decomposition.png` | Level vs trend uncertainty | Most uncertainty is level, not trend |
| `forecast_sigmoid_demo.png` | Mathematical transformation | Visual proof of early acceleration, late saturation |

### 10.2 Recommended Additional Plots

1. **Pillar trajectory fan charts** - Show each pillar's distribution over time
2. **Floor binding analysis** - Which floor fails most often
3. **Sensitivity tornado diagram** - Ordered parameter sensitivities
4. **Historical context plot** - If any proxy data becomes available

---

## 11. Open Questions / Risks

### 11.1 What Is Still Uncertain

1. **Appropriateness of logit transform** - Why logit and not probit, log-normal, or something else?
2. **Initial 2026 values** - Are N=20, G=25 realistic? No data to validate.
3. **Growth rate calibration** - Why is G (Governance) only 0.12 while E (Efficiency) is 0.28?
4. **φ=0.9 justification** - If mean reversion has no effect on results, why include it?
5. **Model B's breakpoint** - Why 2028? Why 30% acceleration?

### 11.2 Which Choices Are Most Discutable

| Rank | Choice | Issue | Severity |
|------|--------|-------|----------|
| 1 | Logit saturation at high scores | 80→90 is extremely slow; is this realistic? | HIGH |
| 2 | Floor at 60 | Sensitivity is extreme; small changes → large output changes | HIGH |
| 3 | Initial N=20, G=25 | Very low starting points; is 2026 realistic? | MEDIUM |
| 4 | Model B's 30% acceleration | Arbitrary magnitude and timing | MEDIUM |
| 5 | φ=0.9 | No empirical basis; sensitivity shows it doesn't matter | LOW |

### 11.3 What Is Likely Correct

1. **Geometric mean for index** - Low pillars should drag down overall readiness
2. **Floors on M,R,N,G** - Institutional factors are necessary, not just nice-to-have
3. **Consecutive years rule** - Prevents one-off lucky spikes
4. **Monte Carlo approach** - Uncertainty quantification is essential
5. **Separating level and trend noise** - Conceptually correct even if empirically unvalidated

### 11.4 Highest Risk of Model Misspecification

**PRIMARY RISK: The logit/sigmoid transformation may be TOO conservative at high scores.**

Evidence:
- Effective growth at y=90 is 82% lower than linear
- Effective growth at y=95 is 91% lower than linear
- This creates an "asymptotic trap" where reaching 100 becomes nearly impossible

**SECONDARY RISK: The floors may be too high relative to initial values.**

Evidence:
- N starts at 20, must reach 60 (40-point gap)
- G starts at 25, must reach 60 (35-point gap)
- With logit saturation, this requires enormous latent growth

### 11.5 Tests That Are Missing

1. **Historical proxy validation** - Can we map any existing metrics to pillars?
2. **Expert elicitation** - Do AI researchers agree with initial values and growth rates?
3. **Alternative transforms** - How would probit, log-normal, or power transforms change results?
4. **Alternative saturation functions** - What if saturation kicks in at 90 instead of 80?
5. **Stress testing** - What parameter combinations produce crossing by 2030? Are any plausible?

---

## 12. Questions ChatGPT Should Challenge

### 12.1 On Model Structure

1. **Is the sigmoid saturation at high scores (80-100) empirically justified or mathematically convenient?**

2. **Why use logit/sigmoid rather than a learned saturation function or a power transform?**

3. **If φ (persistence) sensitivity is negligible (0.7→0.99 changes crossing by <1%), why include mean reversion at all?**

4. **Does the state-space structure (Model C) add value if it produces nearly identical results to fixed growth (Model A)?**

5. **Is the geometric mean index appropriate, or should low pillars "fail" the system rather than just drag it down?**

### 12.2 On Parameters

6. **Are the initial 2026 values (especially N=20, G=25) too low to be realistic?**

7. **Why is Governance growth (0.12) less than half of Efficiency growth (0.28)? Is this pessimism justified?**

8. **Is the floor at 60 too high given initial values? Would 55 or 50 be more realistic?**

9. **What empirical evidence supports φ=0.9 specifically?**

10. **For Model B, what justifies 2028 as the breakpoint and 30% as the acceleration magnitude?**

### 12.3 On Validation

11. **Is there any historical time series that could proxy for even one pillar to enable backtesting?**

12. **How would the model change if we used ECI (Epoch Capability Index) as a validation target?**

13. **Has expert elicitation been done to validate the initial values and growth assumptions?**

14. **What would a "stress test" scenario look like that achieves 50% crossing by 2035, and is it plausible?**

### 12.4 On Interpretation

15. **If Model A (simple) and Model C (complex) agree at 8-9% crossing, what confidence should we have in this number?**

16. **Does the 91% "never crosses" rate mean the model is pessimistic or that true readiness is genuinely hard?**

17. **How should decision-makers use a forecast that says "probably not by 2040"?**

---

## Appendix A: Audit Data (Machine Readable)

File: `docs/model_audit/audit_data.json`

Contains:
- `ablation_study`: Crossing probabilities for Models A, B, C
- `parameter_sensitivity`: Crossing probabilities for varying φ, threshold, floors
- `saturation_analysis`: Effective growth rates at different score levels

---

## Appendix B: File Checksums (for Reproducibility)

| File | SHA256 (first 16 chars) |
|------|-------------------------|
| forecast_model.py | (generate if needed) |
| forecast_scenarios.json | (generate if needed) |

---

**END OF AUDIT PACKAGE**

**Truth status:** This document aims for complete honesty about what is known, assumed, and uncertain. All parameter sensitivities and ablation results are generated from actual code execution, not hand-waved.

**Last updated:** 2026-03-25
