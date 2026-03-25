# Model V2 Design: Two-Stage AI Agent Network Forecast

**Status:** Design document for next-generation forecasting model  
**Objective:** Separate "first emergence" from "broad viability" to resolve intuition-model conflict  
**Date:** 2026-03-25

---

## 1. Core Insight: Two Different Events

The intuition-model conflict arises from conflating two distinct phenomena:

| Aspect | Event A: First Emergence | Event B: Broad Viability |
|--------|-------------------------|--------------------------|
| **What** | First real Level-3-like network appears | Mature, trusted, routine deployment |
| **Scope** | Bounded, limited domains | Broad, cross-vendor, general use |
| **Governance** | Guardrails present, human oversight | Strong governance, lower oversight |
| **Reliability** | "Good enough" for specific use | High reliability, institutional trust |
| **When (intuition)** | 2030-2035 | 2036-2040+ |
| **Current model** | Not explicitly modeled | What current model forecasts |

**Key realization:** The current model forecasts Event B (mature deployability), while intuition often targets Event A (first emergence).

---

## 2. Event Definitions

### Event A: First Emergence (Bounded-Scope Level-3)

**Definition:** The first year when a network of AI agents demonstrates:
- Autonomous task completion in bounded domains
- Meaningful multi-agent coordination
- Commercial or operational viability (not just research demo)
- Some governance (not necessarily mature)
- Limited scope: specific use cases, controlled environment

**Characteristics:**
- Soft feasibility: pillars can be "good enough" rather than "excellent"
- Capabilities-weighted: C, E, D matter most
- Governance-lite: G exists but is immature
- Early interoperability: N works for specific partners/protocols

**Examples:**
- Enterprise internal agent networks (2028-2032)
- Vertical-specific agent ecosystems (finance, coding) (2030-2034)
- Closed beta multi-agent platforms (2031-2035)

### Event B: Broad Viability (Mature Deployability)

**Definition:** The year when agent networks become:
- Cross-vendor interoperable
- Routinely trusted for important decisions
- Governed by established frameworks
- Deployable with manageable risk
- Institutionally accepted

**Characteristics:**
- Harder requirements: all pillars must be mature
- Governance-heavy: G, R are critical
- Network effects: N must be universal, not fragmented
- Institutional trust: requires track record

**Examples:**
- Consumer-facing agent social networks (2036-2042)
- Autonomous economic agents with minimal oversight (2038-2045)
- Cross-platform agent standards widely adopted (2037-2043)

---

## 3. Architectural Changes: V1 → V2

### 3.1 From Hard Floors to Soft Feasibility

**V1 (Current):**
```
if pillar < floor:
    fail
```

**V2 (Proposed):**
```
feasibility = sigmoid((pillar - threshold) / steepness)
```

**Rationale:**
- V1 treats 59 as complete failure, 60 as success
- V2 treats feasibility as continuous, with steep transition around threshold
- Event A uses shallower slope (more forgiving)
- Event B uses steeper slope (stricter)

### 3.2 From Independent Pillars to Coupled System

**V1 (Current):**
- Each pillar evolves independently
- No interaction between C and N, or G and D

**V2 (Proposed):**
- Endogenous coupling between pillars

**Coupling mechanisms:**

| From | To | Mechanism | Rationale |
|------|-----|-----------|-----------|
| C (Capability) | D (Demand) | Better capabilities → more use cases → higher demand | Capability creates demand |
| E (Efficiency) | D (Demand) | Lower costs → broader adoption | Economic accessibility |
| D (Demand) | N (Network) | More users → need better coordination protocols | Scale requires standards |
| N (Network) | R (Reliability) | Better coordination → fewer failures | Infrastructure stability |
| G (Governance) | Deployment Scope | Better governance → broader allowed deployment | Regulatory acceptance |
| D (Demand) | G (Governance) | More deployment → pressure for governance | Regulatory response |

**Mathematical form:**
```
growth_mu_D(t) = base_D + α×C(t) + β×E(t)
growth_mu_N(t) = base_N + γ×D(t-1)
shock_G(t) = f(D(t), regulatory_events)
```

### 3.3 From Static Growth to Regime-Switching

**V1 (Current):**
- Fixed growth rates per scenario
- Random shocks but no structural shifts

**V2 (Proposed):**
- Regime-switching for Governance (G) and Network (N)

**Governance regimes:**
1. **Wild West:** Minimal regulation, fast innovation, high risk
2. **Crisis Response:** Major incident triggers regulatory action
3. **Framework Emergence:** Standards and guidelines developed
4. **Mature Governance:** Established oversight, predictable rules

**Network regimes:**
1. **Fragmented:** Proprietary protocols, siloed systems
2. **Consolidation:** Winners emerge, some interoperability
3. **Standardization:** Industry standards adopted
4. **Universal:** Seamless cross-platform coordination

**Transition dynamics:**
- Triggered by threshold crossings (e.g., D > 70 triggers governance response)
- History-dependent (once in regime 3, hard to go back to 1)
- Stochastic transition probabilities

### 3.4 From Binary Crossing to Time-to-Event Distribution

**V1 (Current):**
```
crossing = True if (index > 75 AND floors_met) for 2 years
result: "crosses in 2038" or "never"
```

**V2 (Proposed):**
```
hazard_A(t) = f(C(t), E(t), D(t), soft_feasibility(G,N,R,M))
hazard_B(t) = f(all_pillars, hard_feasibility(G,N,R,M), coupling_effects)

result: "P(Event A in 2032) = 25%, P(Event A by 2035) = 60%"
        "P(Event B in 2038) = 15%, P(Event B by 2042) = 55%"
```

**Reporting:**
- Survival curves: "P(not yet emerged by year t)"
- Hazard rates: "P(emergence in year t | not yet emerged)"
- Cumulative distributions: "P(emerged by year t)"

---

## 4. Mathematical Specification

### 4.1 Soft Feasibility Function

For each pillar i, define feasibility:

```
φ_i(y_i) = 1 / (1 + exp(-k_i × (y_i - θ_i)))

where:
  y_i = pillar score (0-100)
  θ_i = threshold (inflection point)
  k_i = steepness (higher = more threshold-like)
```

**Event A parameters (forgiving):**
- k = 0.1 (gradual transition)
- θ = 50 (lower threshold)

**Event B parameters (strict):**
- k = 0.2 (sharper transition)
- θ = 60 (higher threshold)

### 4.2 Coupled Growth Dynamics

**Base growth with coupling:**

```
Δz_C(t) = g_C + ε_C(t)                           # Capability: exogenous
Δz_E(t) = g_E + ε_E(t)                           # Efficiency: exogenous
Δz_D(t) = g_D + α×z_C(t) + β×z_E(t) + ε_D(t)    # Demand: driven by C, E
Δz_N(t) = g_N + γ×z_D(t-1) + ε_N(t)             # Network: driven by D
Δz_R(t) = g_R + δ×z_N(t) + ε_R(t)              # Reliability: driven by N
Δz_M(t) = g_M + ε_M(t)                           # Memory: exogenous

z_G(t) = regime-dependent:
  Regime 1: g_G = low, high volatility
  Regime 2: g_G = medium, crisis shocks possible
  Regime 3: g_G = medium, lower volatility
  Regime 4: g_G = high, low volatility
```

**Regime transitions:**

```
P(Regime(t+1) = r' | Regime(t) = r, z(t)) = f(z(t), threshold_matrix)

Example:
  If z_D > 70 AND z_G < 40: high P(transition to Regime 2 - crisis response)
  If z_G > 60 for 3 years: high P(transition to Regime 4 - mature)
```

### 4.3 Hazard Functions

**Event A (First Emergence):**

```
h_A(t) = h0_A × exp(β_C×z_C + β_E×z_E + β_D×z_D) 
         × φ_G(z_G) × φ_N(z_N) × φ_R(z_R) × φ_M(z_M)

Interpretation:
- Exponential in core capabilities (C, E, D)
- Modulated by soft feasibility of support pillars (G, N, R, M)
- High hazard when C,E,D strong, even if G,N,R,M mediocre
```

**Event B (Broad Viability):**

```
h_B(t) = h0_B × exp(β_all × weighted_avg(z))
         × min(φ_G(z_G), φ_N(z_N), φ_R(z_R), φ_M(z_M))^γ

Interpretation:
- Based on all pillars
- Strongly penalized by weakest critical pillar (min function)
- γ > 1 makes this a "bottleneck-sensitive" hazard
```

### 4.4 Survival and Cumulative Distribution

```
S(t) = P(T > t) = exp(-∫_0^t h(s) ds)           # Survival: not yet happened
F(t) = 1 - S(t) = P(T ≤ t)                      # CDF: happened by t
f(t) = h(t) × S(t)                              # PDF: happens at t
```

**Reporting:**
- Median time: t where F(t) = 0.5
- 90% CI: [t where F(t) = 0.05, t where F(t) = 0.95]
- P(by year): F(2030), F(2035), F(2040), etc.

---

## 5. Parameterization Strategy

### 5.1 Exogenous Parameters (from data/expert)

| Parameter | Source | Confidence |
|-----------|--------|------------|
| C, E growth rates | Stanford HAI, Epoch trends | Medium |
| M growth rate | Expert judgment | Low |
| Initial values (2026) | Expert judgment | Low |
| Volatilities | Expert judgment | Low |

### 5.2 Coupling Parameters (to be estimated/calibrated)

| Parameter | How to Set | Prior |
|-----------|-----------|-------|
| α (C→D) | Historical analogies: did better AI increase demand? | 0.3 |
| β (E→D) | Elasticity: demand response to cost decreases | 0.4 |
| γ (D→N) | Network effects literature | 0.2 |
| δ (N→R) | Infrastructure reliability studies | 0.25 |

**Validation:** Sensitivity analysis on coupling strength.

### 5.3 Regime Parameters (expert elicitation needed)

| Parameter | Question for Experts |
|-----------|---------------------|
| Transition thresholds | At what demand level does governance pressure spike? |
| Crisis probabilities | How likely is a major AI incident triggering regulation? |
| Recovery rates | How fast can governance mature after crisis? |

### 5.4 Event Definition Parameters (normative choice)

| Parameter | Event A | Event B |
|-----------|---------|---------|
| Soft threshold θ | 50 | 60 |
| Steepness k | 0.1 (gradual) | 0.2 (sharp) |
| Weakest-link exponent γ | 1.0 (moderate) | 2.0 (strong) |

---

## 6. Data Sources for Calibration

### 6.1 Direct Proxies

| Pillar | Data Source | Notes |
|--------|-------------|-------|
| C (Capability) | Epoch Capabilities Index (ECI) | Quarterly updates |
| | MMLU, HumanEval, SWE-bench | Specific benchmarks |
| E (Efficiency) | AI training cost trends | Stanford HAI |
| | Inference cost per token | OpenAI, Anthropic pricing |
| D (Demand) | AI investment flows | Crunchbase, PwC |
| | Enterprise adoption surveys | McKinsey, Deloitte |

### 6.2 Governance Proxies

| Proxy | Source | Mapping to G |
|-------|--------|--------------|
| National AI strategies | OECD.AI | G framework presence |
| AI regulations enacted | Stanford HAI | G maturity |
| AI incidents database | AIAAIC | G failure rate |
| Governance frameworks | NIST, ISO 42001 | G adoption |

### 6.3 Network Proxies

| Proxy | Source | Mapping to N |
|-------|--------|--------------|
| Multi-agent platform adoption | GitHub, npm | N usage |
| Protocol standardization | IETF, W3C | N standards |
| Vendor interoperability | Industry reports | N maturity |

### 6.4 Calibration Approach

1. **Backcast:** Fit 2020-2025 dynamics to observed trends
2. **Validate:** Out-of-sample test 2023-2025 if data allows
3. **Project:** Forward simulation with uncertainty
4. **Update:** Quarterly refresh as new data arrives

---

## 7. V1 vs V2 Comparison

| Aspect | Model V1 (Current) | Model V2 (Proposed) |
|--------|-------------------|---------------------|
| **Events** | Single "crossing" | Two: First Emergence + Broad Viability |
| **Floors** | Hard (59=fail, 60=pass) | Soft (sigmoid feasibility) |
| **Pillars** | Independent | Coupled (C,E→D→N→R) |
| **Governance** | Static growth | Regime-switching |
| **Output** | Binary: year or "never" | Distribution: survival curves |
| **Intuition fit** | Poor (2038 vs 2033 gut) | Good (separate events) |
| **Complexity** | Medium | High |
| **Validation** | Limited | More tractable (time-to-event) |
| **Uncertainty** | Hidden in "never" | Explicit in distributions |

---

## 8. Implementation Roadmap

### Phase 1: Soft Feasibility (2-3 days)
- Replace hard floors with sigmoid functions
- Keep rest of model unchanged
- Test sensitivity to k and θ

### Phase 2: Two Events (3-4 days)
- Implement Event A (emergence) with forgiving parameters
- Implement Event B (viability) with strict parameters
- Report both survival curves

### Phase 3: Basic Coupling (4-5 days)
- Add C→D and E→D coupling
- Add D→N coupling
- Calibrate coupling strengths

### Phase 4: Regime Switching (5-7 days)
- Implement G regimes
- Implement N regimes
- Define transition rules

### Phase 5: Validation & Documentation (3-4 days)
- Backcast to 2020-2025
- Sensitivity analysis
- Full documentation

**Total:** 3-4 weeks for full V2

---

## 9. What Remains Uncalibrated / Expert Judgment

### Inherently Uncertain (no data can resolve)

1. **What is "good enough" governance?**
   - Even with frameworks, actual performance varies
   - Cultural differences in governance acceptance

2. **When does fragmentation become interoperability?**
   - Network effects are path-dependent
   - History of tech standards shows unpredictability

3. **Crisis timing and severity**
   - Major AI incidents are rare (thankfully)
   - Cannot statistically predict next crisis

### Addressable with Better Data

1. **Coupling strengths**
   - Historical analogies: internet, mobile, cloud adoption
   - Can narrow ranges with more research

2. **Regime transition probabilities**
   - Comparative analysis of other regulated technologies
   - Nuclear, aviation, financial systems as analogies

3. **Initial conditions**
   - Better measurement of current governance maturity
   - More systematic capability assessment

---

## 10. Honest Assessment: What V2 Achieves and Doesn't

### What V2 Achieves

✅ Separates intuition (first emergence) from model (broad viability)  
✅ Makes uncertainty explicit in distributions, not binary "never"  
✅ Captures key intuitions: coupling, regime shifts, soft thresholds  
✅ More realistic microfoundations for governance and network dynamics  
✅ Better validation potential via time-to-event methods  

### What V2 Doesn't Solve

❌ Still requires expert judgment for many parameters  
❌ Still no direct historical data on "agent societies"  
❌ Still sensitive to normative choices (what counts as "emergence")  
❌ Cannot predict black swan events or breakthroughs  
❌ Does not reduce fundamental uncertainty, only structures it better  

### The Core Trade-off

| Approach | Simplicity | Realism | Validation | Communication |
|----------|-----------|---------|------------|---------------|
| V1 (Current) | ✓✓✓ | ✓ | ✓ | ✗ |
| V2 (Proposed) | ✓ | ✓✓✓ | ✓✓ | ✓✓ |

V2 is more complex but more honest about what we know and don't know.

---

## 11. Immediate Next Steps (No Code Yet)

Before implementing V2:

1. **Validate the conceptual framework**
   - Does "first emergence vs broad viability" resonate?
   - Are the coupling mechanisms plausible?

2. **Gather calibration data**
   - Collect historical proxy time series
   - Identify expert elicitation candidates

3. **Decide on soft floor parameters**
   - What θ and k for Event A vs B?
   - Sensitivity to these choices?

4. **Define regimes precisely**
   - What are the measurable criteria for each G regime?
   - What triggers transitions?

---

**Status:** Design complete. Ready for conceptual validation before implementation.
