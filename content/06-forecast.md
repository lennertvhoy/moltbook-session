# Deel 6: Forecast Model

> **Van trends naar forecast:** Deel 5 liet zien dat onderliggende voorwaarden (capability, efficiency, compute) snel verbeteren. Maar wanneer leidt dit tot echte doorbraak? Dat hangt af van méér dan losse benchmarks — het vereist samenwerking tussen capabilities, governance, reliability en netwerkeffecten. Dit deel vertaalt die complexiteit naar een voorzichtig forecastmodel.

## 1. Wat we proberen te voorspellen

> **Eerste betekenisvolle bounded-scope emergentie van een Level-3-achtig AI agent netwerk**

Dit betekent concreet:
- **Persistant geheugen** — agents onthouden context over sessies
- **Multi-agent samenwerking** — rolverdeling, coördinatie
- **Cross-system tool use** — beperkte interoperabiliteit
- **Economisch nuttige inzet** — productie, niet alleen demo
- **Voldoende governance/reliability** — voor beperkte deployment met menselijk toezicht

**Niet** wat we voorspellen:
- ❌ Brede volwassen deployability over alle sectoren
- ❌ Cross-vendor ubiquity (agents van verschillende makers werken naadloos samen)
- ❌ Minimale menselijke oversight op schaal
- ❌ Volledige institutionele maturiteit

De vraag is dus: *wanneer werkt een netwerk van agents voor echte, beperkte toepassingen* — niet *wanneer zijn agent-samenlevingen volledig mature*.

---

## 2. Waarom het oude model te streng was

Het vorige model (V1) had drie structurele problemen die het systematisch te laat maakten:

### Harde floors op 60
Elke pillar moest exact ≥ 60 zijn. Dit maakte 59 een totale failure en 60 een succes. In werkelijkheid is "voldoende governance" een gradueel fenomeen.

### "Nooit crossed" bij 2040
91% "never crossed by 2040" betekende in feite "crossed pas ná 2040". De horizon truncatie creëerde een kunstmatig "never".

### Twee-jaar regel + harde floors
De combinatie van strikte floors én "twee opeenvolgende jaren" maakte crossing uitzonderlijk zeldzaam. De meeste faillures waren geen fundamentele onmogelijkheden, maar graduele missers.

**Ablation resultaat:** Zonder harde floors was de crossing probability 47% ipv 9%. De specificatie van de drempels domineerde de uitkomst.

---

## 3. Canoniek model

### 3.1 Wiskundige vorm

We gebruiken een **discrete-time hazard model** met **soft feasibility**:

```
h(t) = h0 × exp(λ_C·z_C + λ_E·z_E + λ_D·z_D + λ_M·z_M) 
       × φ_G(y_G) × φ_N(y_N) × φ_R(y_R)
```

Waarbij:
- **h(t)** = hazard (kans op emergentie in jaar t, gegeven nog niet geëmergeerd)
- **z_i** = latent capability level op logit-schaal
- **y_i** = observed score 0-100
- **φ_i(y_i)** = soft feasibility functie

### 3.2 Soft feasibility

```
φ(y; θ, k) = 1 / (1 + exp(-k × (y - θ) / 10))
```

Dit geeft:
- y = θ → φ = 0.5 (50% feasible)
- y >> θ → φ → 1 (volledig feasible)
- y << θ → φ → 0 (niet feasible)

**Waarom deze vorm?**
- Natuurlijke saturatie (sigmoid)
- Parameters hebben intuïtieve betekenis (θ = inflection point, k = steepness)
- Geen harde clipping (geen 59=fail, 60=pass)

### 3.3 Parameter ranges (niet punten)

| Parameter | Type | Range/Best Guess | Bron |
|-----------|------|------------------|------|
| **h0** (baseline hazard) | Calibratie | [0.01, 0.10] per jaar | Historische analogies |
| **λ_C, λ_E, λ_D** (capability loadings) | Gewichten | ~0.3 elk, som = 1 | Normalisatie |
| **λ_M** (memory loading) | Gewicht | ~0.2 | Expert judgment |
| **θ_G** (governance inflection) | Expert judgment | 35-50 (best: 40) | Wat is "voldoende"? |
| **θ_N** (network inflection) | Expert judgment | 40-55 (best: 45) | Wat is "bruikbaar"? |
| **θ_R** (reliability inflection) | Expert judgment | 45-60 (best: 50) | Wat is "betrouwbaar genoeg"? |
| **k_G, k_N, k_R** (steepness) | Expert judgment | 0.08-0.15 | Hoe "scharp" is de drempel? |

**Belangrijk:** Waar geen directe data is, gebruiken we ranges en expliciteren we de onzekerheid. Geen schijnprecisie.

### 3.4 Wat is empirisch vs expert judgment

| Component | Status | Hoe te kalibreren |
|-----------|--------|-------------------|
| C (Capability) | **Empirisch** | Epoch ECI, benchmark trends |
| E (Efficiency) | **Empirisch** | Stanford HAI kostendaling |
| D (Demand) | **Proxy** | Investeringen, adoptie surveys |
| M (Memory) | **Expert** | Geen directe metrics, expert ranges |
| N (Network) | **Expert** | Geen directe metrics, expert ranges |
| R (Reliability) | **Expert** | Incident rates als proxy, maar grotendeels expert |
| G (Governance) | **Expert** | Policy indices als proxy, maar grotendeels expert |

---

## 4. Wat het model voorspelt (en niet)

### Wél
- **Time-to-event distributie** — P(emergentie ≤ t) voor elke t
- **Uncertainty ranges** — 90% confidence intervals, niet enkele jaren
- **Sensitivity** — hoeveel uitkomst verandert bij parameter variatie
- **Empirisch vs expert** — expliciet onderscheid

### Niet
- ❌ "De doorbraak komt in 2033"
- ❌ "60% kans tegen 2035"
- ❌ "Dit is hoe het zeker gaat"

### Output formaat

```
Jaar    P(emergentie ≤ jaar)    P(nog niet)
2030    5%                      95%
2032    15%                     85%
2035    40%                     60%
2040    70%                     30%
...     ...                     ...

Median (indicatief): jaar waar P = 50%
90% interval: [jaar bij P=5%, jaar bij P=95%]
```

**Let op:** Deze cijfers zijn illustratief van het formaat, niet de model output. De daadwerkelijke distributie hangt af van de gekalibreerde parameters.

---

## 5. Strengere latere mijlpaal (kanttekening)

Bovenstaand model voorspelt **bounded-scope emergentie**. Een striktere, latere mijlpaal is **broad viability**:

- Cross-vendor interoperabiliteit
- Institutionele trust en mature governance
- Routine deployment met beperkt toezicht
- Economische schaal en impact

Deze vereist scherpere drempels (hogere θ, sterkere k) en waarschijnlijk extra tijd voor institutionele ontwikkeling.

Wij rapporteren deze als **secundaire mijlpaal**, niet als hoofdvoorspelling.

---

## 6. Open onzekerheden

1. **Geen historische precedent** — We hebben geen Level-3 agent netwerken gezien. Alle analogies (cloud, mobile) zijn imperfect.

2. **Expert judgment domineert** — Voor governance, network, en reliability hebben we geen sterke empirische ankers. De ranges zijn breed.

3. **Regime shifts** — Governance en network kunnen discontinu veranderen (crisis, standaardisatie). Dit model neemt geleidelijke dynamiek aan.

4. **Breakthrough risico** — Een GPT-4-achtig moment voor agents is niet gemodelleerd. Smooth hazard vs discontinu potentieel.

---

## 7. Samenvatting

Het canonieke model voorspelt **eerste bounded-scope emergentie** van nuttige agent netwerken — niet volledige mature deployability.

Het gebruikt:
- **Soft feasibility** ipv harde floors
- **Time-to-event** ipv "jaar X of nooit"
- **Parameter ranges** ipv schijnprecisie
- **Expliciete onzekerheid** over empirisch vs expert components

De hoofdvoorspelling is een **distributie over tijd**, niet een enkel jaar.
