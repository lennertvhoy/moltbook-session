# Deel 6: Forecasting Model - Wanneer wordt het echt?

## Het framework: Barrier-crossing model

> **"Bouw een transparent forecasting model, defineer het event precies, simuleer veel mogelijke futures, en rapporteer een probability met een credible band."**

Dit komt uit **finance en credit risk**, waarbij men schat wat de kans is dat een firma een "distress barrier" raakt.

Voor ons: wanneer bereikt AI agent netwerken "Level-3 reality"?

---

## Drie niveaus van "realiteit"

### Level 1 — Technisch real

Een netwerk bestaat waar autonome AI agents:
- ✅ **Persistente identiteiten** hebben
- ✅ Zelfstandig acties kunnen initiëren zonder directe menselijke prompting
- ✅ Met andere agents kunnen communiceren
- ✅ Kunnen coöpereren op multi-step taken

**Status:** Waarschijnlijk al mogelijk, maar duur en beperkt.

### Level 2 — Economisch real

Zelfde als Level 1, plus:
- ✅ **Unit economics maken sense**
- ✅ Gemiddelde waarde per interactie > operationele kosten
- ✅ Genoeg betrouwbaarheid voor herhaald gebruik

**Status:** Opkomend, maar nog niet schaalbaar.

### Level 3 — Sociaal real

Zelfde als Level 2, plus:
- ✅ **Globale schaal**
- ✅ Stabiele governance
- ✅ Betekenisvolle adoptie
- ✅ Coöperatie is routine, niet demo

**Status:** Dit is wat we willen voorspellen.

---

## De Readiness Index

### 7 Pilaren:

| Pilaar | Code | Beschrijving |
|--------|------|--------------|
| **C**apability | C | AI prestaties op relevante benchmarks |
| **E**fficiency | E | Kosten per nuttige output |
| **M**emory | M | Continuïteit van identiteit en context |
| **R**eliability | R | Succesrate op lange multi-step taken |
| **N**etwork | N | Coördinatie tussen agents |
| **G**overnance | G | Juridische acceptatie, veiligheid |
| **D**emand | D | Economische incentive |

### Gewogen geometrisch gemiddelde:

```
I_t = 100 × (C_t/100)^w_C × (E_t/100)^w_E × (M_t/100)^w_M × 
          (R_t/100)^w_R × (N_t/100)^w_N × (G_t/100)^w_G × (D_t/100)^w_D
```

Waar Σ(w) = 1

**Waarom geometrisch?**
- Als één pilaar slecht is, lijdt de hele index
- Grote gains in één pilaar cancellen niet volledig nul in een andere
- Betere match met realiteit (Moltbook heeft slechte governance → laag index)

---

## Threshold definitie

**"Level-3 reality is bereikt wanneer:"**

1. I_t ≥ 75 (Readiness Index)
2. **M, R, N, G** ≥ 60 (Minimale floors)
3. Dit duurt **2 opeenvolgende jaren**

De "2 opeenvolgende jaren" voorkomt dat één hype spike telt als succes.

---

## Groei model

### Log-space dynamiek:

```
log(X_{t+1}) = log(X_t) + μ + ε_t + J_t
```

Waar:
- **μ** = verwachte trend groei
- **ε_t ~ N(0, σ²)** = normale jaar-op-jaar ruis
- **J_t** = jump shock term (positief of negatief)

### Voorbeeld schokken:

| Type | Voorbeeld | Impact |
|------|-----------|--------|
| Positief | Doorbraak in agent geheugen | +20% sprong |
| Negatief | Major veiligheidsschandaal | -15% terugval |
| Positief | Nieuwe architectuur | +30% efficiëntie |
| Negatief | Regulatoire clampdown | -25% governance |

---

## Monte Carlo Simulatie

### Setup:

- **10.000 simulaties**
- Voor elke simulatie:
  1. Start met 2026 scores voor C, E, M, R, N, G, D
  2. Evolueer per jaar met groei aannames
  3. Herbereken readiness index
  4. Noteer eerste jaar waarin threshold bereikt en behouden

### Output:

| Metric | Berekening |
|--------|-----------|
| P(T ≤ 2030) | % simulaties die threshold vóór 2030 halen |
| P(T ≤ 2035) | % simulaties die threshold vóór 2035 halen |
| P(T ≤ 2040) | % simulaties die threshold vóór 2040 halen |
| Median arrival year | 50e percentiel |
| 90% credible interval | 5e - 95e percentiel |

---

## Model uncertain vs simulatie uncertain

### Monte Carlo error (verwaarloosbaar):

```
SE = √(p(1-p)/N)
```

Voor p=0.62, N=10.000:
```
SE ≈ √(0.62 × 0.38 / 10000) ≈ 0.005 = 0.5%
```

### Echte onzekerheid (het belangrijkste):

| Factor | Impact |
|--------|--------|
| Gewichten (w_C, w_E, ...) | Kan 10-30 punten verschuiven |
| Threshold keuze (75? 70? 80?) | Grote invloed op timing |
| Groei aannames | Fundamenteel verschil |
| Shock waarschijnlijkheden | Staarten van distributie |

> **"De simulatie error is minuscuul. De echte onzekerheid komt uit de aannames."**

---

## Drie scenario's

### Scenario tabel (voorbeeld):

| Pilaar | 2026 | Groei μ | Vol σ | Neg shock | Weight |
|--------|------|---------|-------|-----------|--------|
| **Conservatief** | | | | | |
| Capability | 55 | 0.12 | 0.10 | 0.08 | 0.20 |
| Efficiency | 45 | 0.20 | 0.12 | 0.06 | 0.20 |
| Memory | 30 | 0.08 | 0.15 | 0.12 | 0.15 |
| Reliability | 28 | 0.10 | 0.15 | 0.15 | 0.15 |
| Network | 20 | 0.08 | 0.18 | 0.18 | 0.12 |
| Governance | 25 | 0.04 | 0.12 | 0.20 | 0.10 |
| Demand | 50 | 0.08 | 0.10 | 0.08 | 0.08 |
| **Base case** | | (hogere groei, lagere shocks) | | | |
| **Accelerated** | | (nog hogere groei, positieve shocks) | | | |

### Output per scenario:

| Scenario | P(≤2030) | P(≤2035) | P(≤2040) | Median |
|----------|----------|----------|----------|--------|
| Conservative | 15% | 45% | 72% | 2036 |
| Base case | 35% | 68% | 88% | 2032 |
| Accelerated | 55% | 82% | 95% | 2029 |

---

## Finance analogie

> **"Ik behandel dit als een barrier event in finance. Niet als een profetie, maar als een readiness proces. Als genoeg van de vereiste condities snel genoeg verbeteren en boven threshold blijven, wordt het event waarschijnlijk."**

Dit is dichter bij **credit-risk of optie-denken** dan een normale trendlijn.

---

## Twee forecasts

### A. "Technical reality" 
Wanneer is het technisch haalbaar?

**Gok:** Waarschijnlijk al binnen 2-3 jaar voor beperkte use cases.

### B. "Global social reality"
Wanneer is het globaal betekenisvol en economisch levensvatbaar?

**Gok:** Dit is wat het forecast model voorspelt (2030-2040 range).

> **"Ik denk dat de technische versie veel eerder arriveert dan de sociaal stabiele versie."**

---

## Slotzin voor deze sectie

> "Dus in plaats van te vragen of Moltbook vandaag echt is, zou ik vragen: is het readiness proces de barrier aan het kruisen? Mijn gok is dat technische haalbaarheid eerst komt, economische levensvatbaarheid daarna, en echte globale autonome coöperatie als laatste."

Of scherper:

> **"De bottleneck is waarschijnlijk niet langer meer alleen ruwe intelligentie. Het is continuïteit, coördinatie, governance en kosten."**
