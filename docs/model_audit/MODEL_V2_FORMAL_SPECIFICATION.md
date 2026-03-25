# Model V2 Formal Specification

**Status:** Mathematical specification (NOT implementation)  
**Purpose:** Exact model definition before any coding  
**Constraint:** NO illustrative outputs - only structure, parameters, and calibration strategy  
**Date:** 2026-03-25

---

## 1. Event Definitions (Exact)

### 1.1 Event A: First Emergence

**Formal Definition:**  
> The first calendar year in which at least one commercially deployed network of AI agents demonstrates:
> 1. Autonomous task completion in production (not research/demo) for bounded use cases
> 2. Multi-agent coordination without continuous human micromanagement  
> 3. Commercial or operational viability (generates value, not just novelty)
> 4. Deployment under strong local controls, limited blast radius, and human oversight

**What COUNTS as Event A:**
- Enterprise-internal agent networks handling >$10M/year of operational decisions (2030-2033)
- Vertical-specific platforms (coding, trading, customer service) with >1000 paying customers (2031-2034)
- Closed-beta multi-agent systems with real economic transactions (2032-2035)
- Government/institutional deployments in controlled domains (healthcare, logistics) (2033-2036)

**What does NOT count as Event A:**
- Research demos (AutoGPT, babyagi)
- Single-agent systems (not networks)
- Human-in-the-loop systems requiring continuous supervision
- Systems with no economic value creation
- Systems that fail in production within 6 months

**Governance requirement for Event A:**  
> Governance need not be broadly institutionalized or cross-jurisdictional. Bounded-scope deployment must be possible under:
> - Strong local controls within the deploying organization
> - Human oversight at strategic/decision level (not operational)
> - Limited blast radius (failure contained to specific use case)
> - Audit trails exist but need not be standardized

### 1.2 Event B: Broad Viability

**Formal Definition:**  
> The first calendar year when agent networks satisfy ALL of:
> 1. Cross-vendor interoperability (agents from different providers coordinate)
> 2. Routine deployment with manageable risk (not experimental)
> 3. Institutional trust (regulated industries deploy without special waivers)
> 4. Governance frameworks mature and widely adopted
> 5. Meaningful deployment with reduced human oversight (operational, not strategic)

**What COUNTS as Event B:**
- Consumer-facing agent social networks with >10M users (2036-2042)
- Cross-platform agent standards (IEEE, W3C, or de facto) adopted by >3 major vendors (2037-2043)
- Autonomous economic agents operating in regulated markets without special exemptions (2038-2045)
- Government services delivered primarily by agent networks (2039-2047)

**What does NOT count as Event B:**
- Single-vendor walled gardens
- Experimental deployments with extensive human supervision
- Systems requiring regulatory exemptions or sandboxes
- Niche use cases without broad applicability

**Governance requirement for Event B:**  
> Governance MUST be:
> - Institutionalized across jurisdictions (not just one organization's policy)
> - Standardized (common frameworks, not ad-hoc)
> - Enforced (violations have consequences)
> - Proven (track record of handling incidents)

---

## 2. Mathematical Specification (Exact)

### 2.1 Time Structure

- Discrete time steps: t ∈ {2026, 2027, ..., 2070}
- Annual resolution (no sub-year steps)
- Horizon: 2026-2070 (45 years, right-censoring at 2070)

### 2.2 State Space

**Observed variables (7 pillars):**
- C(t), E(t), M(t), R(t), N(t), G(t), D(t) ∈ [0, 100]

**Latent variables:**
- z_C(t), ..., z_D(t) ∈ ℝ (logit scale for each pillar)
- Regime_G(t) ∈ {1, 2, 3, 4} (governance regime)
- Regime_N(t) ∈ {1, 2, 3, 4} (network regime)

### 2.3 Observation Model (Logit Transform)

```
y_i(t) = 100 × σ(z_i(t))

where σ(x) = 1 / (1 + exp(-x)) is the sigmoid

Inverse:
z_i(t) = logit(y_i(t)/100) = log(y_i(t) / (100 - y_i(t)))
```

**Properties:**
- Maps [0, 100] to [-∞, +∞]
- Natural saturation: y → 100 as z → +∞
- Linear dynamics on z-scale approximate logistic growth on y-scale

### 2.4 State Evolution (Coupled Local Linear Trend)

**Core pillars (exogenous):**
```
z_C(t) = z_C(t-1) + g_C(t-1) + ε_C(t)
z_E(t) = z_E(t-1) + g_E(t-1) + ε_E(t)
z_M(t) = z_M(t-1) + g_M(t-1) + ε_M(t)

where:
  g_i(t) = persistence_i × g_i(t-1) + (1 - persistence_i) × ḡ_i + η_i(t)
  ε_i(t) ~ N(0, σ_level_i)  [level shock]
  η_i(t) ~ N(0, σ_growth_i)  [growth rate shock]
```

**Coupled pillars (endogenous):**
```
z_D(t) = z_D(t-1) + g_D(t-1) + α_C×z_C(t-1) + α_E×z_E(t-1) + ε_D(t)
z_N(t) = z_N(t-1) + g_N(t-1) + β_D×D(t-1) + regime_effect_N(t) + ε_N(t)
z_R(t) = z_R(t-1) + g_R(t-1) + γ_N×N(t-1) + ε_R(t)

where:
  D(t-1) = 100 × σ(z_D(t-1))  [back to observation scale]
  regime_effect_N(t) = f(Regime_N(t))
```

**Governance (regime-switching):**
```
z_G(t) = z_G(t-1) + g_G(t-1) + regime_effect_G(t) + ε_G(t)

Regime_G(t) | Regime_G(t-1), D(t-1), shocks
  Transition matrix depends on demand level and incident history
```

### 2.5 Regime Definitions (Governance)

| Regime | Name | Characteristics | Transition triggers |
|--------|------|-----------------|-------------------|
| 1 | Wild West | Minimal regulation, fast innovation, high risk | High D + low G triggers → 2 |
| 2 | Crisis Response | Major incident occurred, reactive regulation | After major incident |
| 3 | Framework Emergence | Standards developing, proactive governance | G sustained > 40 for 3 years → 4 |
| 4 | Mature Governance | Established oversight, predictable rules | (absorbing or can degrade) |

**Regime effects on growth:**
```
regime_effect_G(t) = 
  +0.05 if Regime_G(t) = 4 (mature governance enables faster deployment)
   0.00 if Regime_G(t) = 3
  -0.10 if Regime_G(t) = 2 (crisis slows things down)
  +0.10 if Regime_G(t) = 1 (wild west allows fast but risky growth)
```

### 2.6 Soft Feasibility Function

For each pillar i, define feasibility φ_i:

```
φ_i(y_i; θ_i, k_i) = 1 / (1 + exp(-k_i × (y_i - θ_i) / 10))

where:
  y_i = pillar score on [0, 100]
  θ_i = inflection point (where feasibility = 0.5)
  k_i = steepness parameter (higher = sharper threshold)
  Division by 10 scales to roughly [-10, +10] range for typical y differences
```

**Event A parameters:**
| Pillar | θ_i | k_i | Rationale |
|--------|-----|-----|-----------|
| C | 45 | 0.15 | Capability matters most, lower threshold |
| E | 45 | 0.15 | Efficiency enables deployment |
| D | 40 | 0.12 | Demand can be emerging |
| M | 50 | 0.10 | Memory should be decent |
| R | 50 | 0.10 | Reliability important but bounded-scope forgiving |
| N | 45 | 0.10 | Early interoperability okay |
| G | 40 | 0.08 | Governance can be immature (local controls suffice) |

**Event B parameters:**
| Pillar | θ_i | k_i | Rationale |
|--------|-----|-----|-----------|
| C | 60 | 0.20 | High capability required |
| E | 60 | 0.20 | Efficiency at scale |
| D | 55 | 0.18 | Established demand |
| M | 60 | 0.18 | Robust memory |
| R | 65 | 0.22 | High reliability critical |
| N | 65 | 0.22 | Universal interoperability |
| G | 65 | 0.25 | Mature governance essential (steepest) |

### 2.7 Hazard Functions (Time-to-Event)

**Event A Hazard:**
```
h_A(t) = h0_A × exp(λ_C×z_C(t) + λ_E×z_E(t) + λ_D×z_D(t)) 
         × φ_G(y_G(t)) × φ_N(y_N(t)) × φ_R(y_R(t)) × φ_M(y_M(t))

where:
  h0_A = baseline hazard (to be calibrated)
  λ_C, λ_E, λ_D = loadings on core capabilities
  φ_G, φ_N, φ_R, φ_M = soft feasibility of support pillars
```

**Properties:**
- Exponential in core capabilities (C, E, D)
- Modulated by feasibility of support pillars
- Even with weak G/N/R/M, high C/E/D can drive hazard

**Event B Hazard:**
```
h_B(t) = h0_B × exp(Σ_i λ_i×z_i(t))
         × [min(φ_G(y_G(t)), φ_N(y_N(t)), φ_R(y_R(t)), φ_M(y_M(t)))]^γ

where:
  h0_B = baseline hazard (lower than h0_A)
  γ = 2.0 (bottleneck sensitivity)
  min() = bottleneck function
```

**Properties:**
- Based on all pillars
- Strongly penalized by weakest critical pillar
- γ > 1 creates severe bottleneck effect
- Governance and network are hardest to satisfy

### 2.8 Survival and Cumulative Distribution

```
S_A(t) = P(T_A > t) = exp(-Σ_{s=2026}^t h_A(s))
F_A(t) = P(T_A ≤ t) = 1 - S_A(t)

S_B(t) = P(T_B > t) = exp(-Σ_{s=2026}^t h_B(s))
F_B(t) = P(T_B ≤ t) = 1 - S_B(t)
```

**Reporting quantities:**
- Median: t where F(t) = 0.5
- 90% CI: [t_0.05, t_0.95] where F(t_p) = p
- P(by year): F(2030), F(2035), F(2040), etc.

---

## 3. Parameter Strategy

### 3.1 Parameter Classification

| Parameter | Type | Source | Confidence |
|-----------|------|--------|------------|
| **Initial z_i(2026)** | Point estimate | Expert judgment + proxy data | LOW |
| **ḡ_i (long-run growth)** | Point estimate | Stanford HAI, Epoch trends | MEDIUM |
| **persistence_i** | Point estimate | Literature on technology diffusion | LOW |
| **σ_level_i, σ_growth_i** | Distribution | Expert elicitation | LOW |
| **α_C, α_E (coupling to D)** | Range [0.1, 0.5] | Historical analogies | MEDIUM |
| **β_D (coupling to N)** | Range [0.1, 0.3] | Network effects literature | MEDIUM |
| **γ_N (coupling to R)** | Range [0.1, 0.3] | Infrastructure reliability | LOW |
| **θ_i (thresholds)** | Range | Maturity framework mapping | MEDIUM |
| **k_i (steepness)** | Distribution | Expert elicitation on "fuzziness" | LOW |
| **h0_A, h0_B** | Calibrated | Match historical analogies | MEDIUM |
| **λ_i (hazard loadings)** | Normalized | Equal weighting as starting point | LOW |
| **γ (bottleneck exponent)** | Range [1.5, 3.0] | Sensitivity analysis | LOW |

### 3.2 Sensitivity Strategy

**Must vary:**
- All θ_i ± 10 points
- All k_i ± 50%
- Coupling parameters across their ranges
- Baseline hazards h0_A, h0_B over 2 orders of magnitude
- Regime transition probabilities

**Output:** Uncertainty intervals, not point estimates.

---

## 4. Calibration Plan

### 4.1 Direct Calibration (where possible)

| Target | Data Source | How to Use |
|--------|-------------|------------|
| C growth | Epoch ECI, MMLU, HumanEval | Fit trend 2020-2025, project |
| E growth | Stanford HAI cost trends | Extrapolate cost decline |
| D growth | AI investment, enterprise adoption | Elasticity to C, E |
| M, R, G, N | No direct data | Expert elicitation only |

### 4.2 Proxy Calibration

| Pillar | Proxy | Source |
|--------|-------|--------|
| G (Governance) | Oxford Gov AI Readiness, OECD AI Policy | Annual indices |
| | AI incident rates | AIAAIC database |
| | Regulatory enactment | Stanford HAI, national trackers |
| N (Network) | Multi-agent repos (GitHub) | Dependency graphs |
| | Protocol standardization | IETF, W3C activity |
| | Cross-platform tools | npm, PyPI metrics |

### 4.3 Historical Analogies for Baseline Hazard

**Event A analogies:**
- First cloud deployments (AWS 2006): time from concept to production viability
- First mobile apps (App Store 2008): time from SDK to commercial viability
- First SaaS (Salesforce 1999): time from idea to enterprise adoption

**Event B analogies:**
- Cloud maturity (AWS → multi-cloud standardization): 2010-2020
- Mobile maturity (iOS → cross-platform): 2008-2015
- Internet maturity (ARPANET → commercial internet): 1983-1995

**Use:** Calibrate h0 to match analogous historical durations.

### 4.4 Expert Elicitation Protocol

**For parameters without data:**
1. Define observable implications of each parameter value
2. Ask experts for P(parameter < x) distributions
3. Aggregate using Cooke's Classical Model (weighted by calibration)
4. Propagate uncertainty through Monte Carlo

**Parameters needing elicitation:**
- θ_G, θ_N (what's "good enough" governance/network?)
- k_G, k_N (how sharp is the feasibility transition?)
- σ_G, σ_N (volatility of institutional factors)
- Regime transition probabilities

---

## 5. Validation Plan

### 5.1 Sanity Checks

| Check | Expected | If Fails |
|-------|----------|----------|
| C, E fastest growing | Yes | Check growth rate priors |
| G slowest growing | Yes | Consistent with institutional friction |
| Event A before Event B | Yes | By construction (higher hazard) |
| Both events after 2025 | Yes | No backcasting failure |
| S(t) decreasing | Yes | Mathematical check |

### 5.2 Ablations (Required)

1. **No coupling:** Set α, β, γ = 0
2. **No regimes:** Fix Regime_G = 3, Regime_N = 2
3. **Hard floors:** Replace sigmoid with step function
4. **Single event:** Only Event A or only Event B
5. **Exogenous only:** No D→N→R coupling
6. **Softer/steeper feasibility:** Vary all k_i ± 50%

### 5.3 Pseudo-Backtests

**Test:** Can model "predict" historical technology diffusion?

**Approach:**
- Treat cloud, mobile, internet as "Event A" analogies
- Fit model to 2000-2020 data
- See if it predicts 2020-2025 correctly
- Use to validate coupling strengths

**Limitation:** No true "Level-3 agent" historical data exists.

### 5.4 Alternative Event Definitions

**Test robustness:**
- Event A with θ_G = 35 vs 45 vs 55
- Event B with γ = 1.5 vs 2.0 vs 3.0
- Different bottleneck definitions (min vs geometric mean)

---

## 6. Risks and Open Questions

### 6.1 Fundamental Uncertainties

1. **No historical precedent for Level-3 agents**
   - All analogies (cloud, mobile) are imperfect
   - May be category error to assume continuity

2. **Discontinuity risk**
   - Model assumes smooth dynamics
   - Breakthrough (GPT-4 moment for agents) not captured

3. **Regime transitions are speculative**
   - We have no validated theory of AI governance evolution
   - Crisis timing inherently unpredictable

4. **Coupling parameters unobserved**
   - Cannot directly measure "C → D elasticity"
   - Historical analogies may not apply

### 6.2 Model Limitations

1. **Annual resolution misses sub-year dynamics**
   - If emergence happens mid-year, model rounds

2. **No spatial/geographic differentiation**
   - Governance regimes vary by jurisdiction
   - Model treats world as homogeneous

3. **Binary event definition**
   - Real world has degrees of emergence/viability
   - Model forces discrete threshold

4. **No feedback from forecast to reality**
   - Model is passive observer
   - Real forecasts can accelerate/slow development

### 6.3 Ethical/Strategic Considerations

1. **Self-fulfilling prophecy risk**
   - If forecast says "2038", does this slow investment?
   - Or accelerate if perceived as race?

2. **Strategic misrepresentation**
   - Incentives to forecast early (hype) or late (caution)
   - Model must resist manipulation

3. **Distributional impacts**
   - Who benefits from early emergence? Late?
   - Model is agnostic but stakes are high

---

## 7. Deliverables and Next Steps

### 7.1 Before Implementation

- [ ] Validate event definitions with stakeholders
- [ ] Confirm mathematical framework choice (discrete-time logit hazard)
- [ ] Finalize parameter ranges (not point values)
- [ ] Design expert elicitation protocol
- [ ] Identify historical analogy datasets

### 7.2 Implementation Phases

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| 1: Core structure | 1 week | Basic hazard functions, no coupling |
| 2: Coupling | 1 week | C,E→D→N→R dynamics |
| 3: Regimes | 1 week | G and N regime switching |
| 4: Calibration | 2 weeks | Fit to proxies, expert elicitation |
| 5: Validation | 1 week | Ablations, sensitivity, documentation |

**Total: 6 weeks**

### 7.3 Success Criteria

Model V2 is successful if:
1. It produces interpretable survival curves (not binary "cross/don't cross")
2. Event A and Event B have meaningfully different distributions
3. Uncertainty is explicit in output (ranges, not points)
4. Sensitivity to floor/governance parameters is clearly documented
5. It can be updated quarterly as new data arrives

---

## 8. Explicit Absence

**NOT in this specification:**
- ❌ Any claimed median year (2033, 2038, etc.)
- ❌ Any claimed probability ("60% by 2035")
- ❌ Any "illustrative" outputs
- ❌ Implementation code
- ❌ Parameter point values (only ranges/priors)

**What IS in this specification:**
- ✅ Exact mathematical forms
- ✅ Exact event definitions with examples
- ✅ Parameter classification and sources
- ✅ Calibration strategy
- ✅ Validation plan
- ✅ Honest uncertainty documentation

---

**Status:** Specification complete. Awaiting validation before implementation.
