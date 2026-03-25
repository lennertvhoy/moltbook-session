# Floor Justification Framework

**Status:** Research-backed recommendations for making floors=60 defensible  
**Based on:** Maturity frameworks (TRL, CMMI), composite indicator methodology, structured expert elicitation

---

## De Kernvraag

> "Waarom 60?"

De ablatie toont dat dit de dominante vraag is. Deze document biedt een framework om die vraag te beantwoorden zonder het model te forceren.

---

## Twee Coherente Interpretaties van Floors

### Optie 1: Floors als Definitional "Stage Gate"

**Visie:** Floors zijn geen empirische parameters - ze definieren wat we bedoelen met "crossing".

**Analogie:** NASA Technology Readiness Levels (TRL)
- TRL 1-3: Basic principles observed
- TRL 4-5: Validation in laboratory/relevant environment  
- TRL 6-7: System/subsystem demonstration
- TRL 8-9: System complete, mission proven

**Toepassing op onze pillars:**

| Pillar | TRL-equivalent bij 60 | Wat het betekent |
|--------|----------------------|------------------|
| **G (Governance)** | TRL 5-6 | Governance framework geïmplementeerd, getest in relevante omgeving |
| **N (Network)** | TRL 5-6 | Coördinatieprotocol stabiel in pilot deployments |
| **M (Memory)** | TRL 5-6 | State persistence betrouwbaar in productie-achtige settings |
| **R (Reliability)** | TRL 5-6 | Betrouwbaarheid gedemonstreerd over langere periodes |

**Voordelen:**
- Maakt "60" interpreteerbaar en debatteerbaar
- Sluit aan bij bestaande engineering practices
- Niet geclaimd als "waarheid" maar als "specificatie"

**Nadeel:** 
- Vereist nog steeds argumentatie waarom TRL 5-6 het juiste niveau is

### Optie 2: Floors als Empirische Parameters (met Uncertainty)

**Visie:** Floors schatten het minimale niveau voor stabiele multi-agent deployment, maar we weten dit onzeker.

**Methode:** Structured Expert Elicitation
- Geen puntinschattingen
- Distributies per pillar (bijv. 50e, 25e, 75e percentiel)
- Monte Carlo samplet uit deze distributies
- Resultaat: confidence intervals ipv puntinschattingen

**Praktisch protocol:**
1. Definieer "floor meaning" per pillar als observable claims
   - G: "auditable risk management, lifecycle controls, accountability institutionalized"
   - N: "protocol stability under realistic load, fault tolerance demonstrated"
   - M: "state reconstruction reliability >X% over Y-day periods"
   - R: "error rates <Z% in production-like conditions"

2. Eliciteer distributies van 5-10 experts
   - "Wat is het minimale governance-niveau voor stabiele agentsamenleving?"
   - Geef median + 90% CI, niet punt

3. Run model met gesamplede floors
   - Resultaat: range van crossing probabilities
   - Bijv. "9% by 2040 (als floors=60), maar 17% (als floors=55)"

**Voordelen:**
- Houdt onzekerheid expliciet
- Kan bijgesteld worden naarmate meer data beschikbaar komt
- Eerlijk over epistemische limieten

---

## Maturity Frameworks voor Anchoring

### NASA Technology Readiness Levels (TRL)

| TRL | Beschrijving | Onze schaal (geschat) |
|-----|-------------|----------------------|
| 1 | Basic principles observed | 0-20 |
| 2-3 | Technology concept formulated/analyzed | 20-40 |
| 4 | Validation in laboratory | 40-50 |
| **5** | **Validation in relevant environment** | **50-65** |
| **6** | **System/subsystem demonstration** | **60-75** |
| 7 | System prototype in operational environment | 75-85 |
| 8-9 | System complete, mission proven | 85-100 |

**Claim:** Floor=60 komt overeen met "TRL 5-6 grens":
- Voorbij lab proof-of-concept
- In relevante omgeving gedemonstreerd
- Maar nog niet volledig operationeel bewezen

### CMMI Staged Levels (voor G - Governance)

| CMMI Level | Beschrijving | Governance Floor |
|------------|-------------|------------------|
| 1 | Initial (chaotic) | < 40 |
| 2 | Managed (project-level) | 40-50 |
| **3** | **Defined (organization-level)** | **50-65** |
| 4 | Quantitatively managed | 65-80 |
| 5 | Optimizing | 80-100 |

**Claim:** Governance=60 komt overeen met "Defined":
- Processen gestandaardiseerd op organisatie-niveau
- Proactief management, niet alleen reactief
- Maar nog niet volledig data-gedreven optimalisatie

### ISO/IEC 42001 & NIST AI RMF (voor G)

**ISO/IEC 42001:** AI Management System (AIMS) requirements
- Governance als cross-cutting function
- Risk management geïntegreerd in lifecycle
- Continuous improvement

**NIST AI RMF:**
- GOVERN: governance als hoofdfunctie
- MAP/MEASURE/MANAGE: ondersteunende functies

**Operationalisatie naar score 60:**
- G=60: "AIMS requirements gedeeltelijk geïmplementeerd, governance framework actief maar nog niet volledig mature"

---

## Horizon Effecten als Right-Censoring

### Het Probleem

"91% never crosses by 2040" is misleidend. Het is **right-censored**: we weten alleen dat het event NA 2040 plaatsvindt, niet dat het nooit plaatsvindt.

### Oplossing: Survival Analysis Reporting

**Huidig (misleading):**
```
P(cross by 2040) = 9%
"91% never crosses"
```

**Gewenst (honest):**
```
Jaar    P(cross by year)    P(nog niet gecrossed)
2030    0.1%                99.9%
2035    2.3%                97.7%
2040    9.0%                91.0%  ← censored
2045    37.5%               62.5%
2050    62.4%               37.6%
2060    88.1%               11.9%

"Median crossing time: 2047 (unconditional)"
"Of: 2039 (conditional on crossing by 2060)"
```

**Visualisatie:** Survival curve (Kaplan-Meier stijl) ipv enkele percentages

---

## Concrete Actiepunten

### Onmiddellijk (zonder model aanpassing)

1. **Vervang "never crosses" taal**
   - In content, slides, rapportage
   - Altijd horizon vermelden: "not by 2040", niet "never"

2. **Presenteer multi-horizon cumulatieve distributie**
   - 2040, 2045, 2050, 2060
   - Maakt right-censoring expliciet

3. **Documenteer floors als specifieke keuze**
   - Niet "het model zegt"
   - Maar: "gegeven floors=60 als definitie van readiness..."

### Korte termijn (met content updates)

4. **Voeg TRL/CMMI mapping toe aan documentatie**
   - Leg uit: 60 = TRL 5-6 = "relevant environment demonstration"
   - Maakt de keuze interpreteerbaar

5. **Presenteer floor sensitivity als scenario**
   - Strikte definitie (floors=65): X% by 2040
   - Moderate definitie (floors=60): 9% by 2040  
   - Loose definitie (floors=55): 17% by 2040
   - Laat lezer kiezen welke definitie passend is

### Lange termijn (indicatief)

6. **Structured expert elicitation**
   - Voor floors als empirische parameters
   - Distributies ipv puntwaarden
   - Vermeidt false precision

7. **Proxy time series voor pillars**
   - Oxford AI Readiness Index → G proxy
   - OECD AI indicators → governance/policy proxy
   - Update floor beliefs naarmate data beschikbaar komt

---

## Research-Backed Referenties

| Bron | Relevantie |
|------|-----------|
| NASA TRL Handbook | Maturity framework voor floors als definitional stage gates |
| CMMI Model | Governance maturity levels (G pillar) |
| ISO/IEC 42001 | AI management system requirements (operationalisatie G) |
| NIST AI RMF | Governance framework specificatie |
| Cooke (1991) | Structured expert judgment voor uncertainty quantification |
| OECD/JRC Handbook | Composite indicator methodology (validatie van onze ablatie aanpak) |
| Kaplan-Meier (1958) | Survival analysis voor right-censoring |

---

## Samenvatting

**De vraag "waarom 60?" heeft twee valide antwoorden:**

1. **Definitional:** "60 = TRL 5-6 = het punt waarop we iets 'echt' noemen ipv 'proof of concept'"
   - Dan is het een spec, geen voorspelling
   - En we tonen sensitivity: wat gebeurt er bij 55 of 65?

2. **Empirisch:** "We schatten dat 60 het minimale niveau is, maar zijn onzeker"
   - Dan moeten we die onzekerheid propageren
   - En resultaat is een range, geen punt

**Wat we NU doen:**
- Eerlijk zeggen: floors=60 is een keuze die de uitkomst domineert
- Multi-horizon rapporteren (geen "never")
- TRL/CMMI mapping toevoegen om 60 interpreteerbaar te maken

**Wat we LATER kunnen doen:**
- Expert elicitation voor uncertainty
- Proxy data voor empirische update

---

**Status:** Framework complete. Ready for content implementation.
