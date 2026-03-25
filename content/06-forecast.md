# Deel 6: Forecast Model

> **Van trends naar forecast:** Deel 5 liet zien dat onderliggende voorwaarden (capability, efficiency, compute) snel verbeteren. Maar wanneer leidt dit tot echte doorbraak? Dit deel vertaalt die complexiteit naar een voorzichtig forecastmodel.

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

## 2. Het model: opzet en aannames

### 2.1 Wiskundige basis

Het model gebruikt een **latent capability** benadering met logit-transformatie:

```
z_t = logit(y_t/100) = log(y_t / (100 - y_t))

State equations (local linear trend):
    z_t = z_{t-1} + g_t + ε_t      (level, ε_t ~ N(0, sigma))
    g_t = φ×g_{t-1} + (1-φ)×ḡ + η_t  (growth, η_t ~ N(0, sigma_g))

y_t = 100 × sigmoid(z_t)          (transform back)
```

**Wat dit betekent in gewone taal:** We transformeren scores (0-100) naar een schaal waar groei natuurlijk vertraagt naarmate we 100 naderen. Dit voorkomt dat het model onrealistisch snel naar perfectie schiet.

### 2.2 De zeven pilaren

| Pijler | Code | Gewicht | Focus |
|--------|------|---------|-------|
| Capability | C | 20% | Wat agents kunnen |
| Efficiency | E | 20% | Kost per capaciteit |
| Memory | M | 15% | Duurzaam geheugen |
| Reliability | R | 15% | Betrouwbaarheid |
| Network | N | 12% | Interoperabiliteit |
| Governance | G | 10% | Regels & verantwoording |
| Demand | D | 8% | Marktbehoefte |

### 2.3 Drempels (thresholds)

Het model gebruikt **twee criteria**:

1. **Readiness Index ≥ 75** — gewogen gemiddelde van alle pilaren
2. **Vier "floor" pilaren ≥ 60** — Memory, Reliability, Network, Governance moeten allemaal minimaal 60 halen

Daarnaast moeten beide criteria **twee opeenvolgende jaren** worden gehaald voordat "crossing" wordt geregistreerd.

**Belangrijk:** Deze floors zijn harde drempels (59 = failure, 60 = pass). Dit is een bewuste keuze voor dit model, maar het betekent dat de uitkomst gevoelig is voor deze specifieke drempelwaarden.

---

## 3. Scenario's

### 3.1 Drie scenario's

| Scenario | Beschrijving | Kenmerk |
|----------|--------------|---------|
| **Conservative** | Lage groei, hogere volatiliteit, meer shocks | Veel obstakels |
| **Base case** | Moderate groei, moderate volatiliteit | Balans |
| **Accelerated** | Hoge groei, lagere volatiliteit, minder shocks | Gunstige omstandigheden |

### 3.2 Voorbeeld: Base case startwaarden (2026)

| Pijler | Start | Groei/jaar | Opmerking |
|--------|-------|------------|-----------|
| Capability | 55 | +18% | Sterkste start |
| Efficiency | 45 | +28% | Snelste groei |
| Memory | 30 | +14% | Moet van ver komen |
| Reliability | 28 | +16% | Moet van ver komen |
| Network | 20 | +15% | Laagste start |
| Governance | 25 | +12% | Institutionele traagheid |
| Demand | 50 | +12% | Moderate groei |

**Let op:** Deze waarden zijn expliciete aannames (expert judgment), geen empirische metingen.

---

## 4. Wat het model voorspelt (en niet)

### Wél
- **Crossing probability** — kans dat de drempels worden gehaald vóór 2040
- **Scenario vergelijking** — hoe verschillende aannames leiden tot verschillende uitkomsten
- **Sensitivity** — welke parameters de uitkomst het sterkst beïnvloeden

### Niet
- ❌ "De doorbraak komt in 2033"
- ❌ "60% kans tegen 2035"
- ❌ "Dit is hoe het zeker gaat"

### Typische output (voorbeeld, illustratief)

In de base case:
- Crossing probability vóór 2040: ~8-9%
- "Never crosses" in de simulatie: ~91%

**Interpretatie:** Dit betekent niet dat emergentie onmogelijk is. Het betekent dat onder de huidige aannames (lage startwaarden voor M, R, N, G + harde floors + sigmoid saturatie), het model een lage waarschijnlijkheid berekent.

---

## 5. Belangrijkste inzichten uit het model

### 5.1 Floors binden meer dan de headline threshold

Sensitivity analyse toont:
- Floor 60 → 50: crossing probability stijgt van ~8% naar ~27%
- Floor 60 → 70: crossing probability daalt van ~8% naar ~1%
- Threshold 75 → 70: minimaal effect (~8% → ~8.5%)

**Conclusie:** De vier floor-pilaren (Memory, Reliability, Network, Governance) zijn de echte "poortwachters" — niet het gewogen gemiddelde van 75.

### 5.2 Sigmoid saturatie remt hoogwaardige groei

Doordat het model logit/sigmoid gebruikt:
- Groei van 20→30 gaat relatief snel
- Groei van 80→90 gaat veel langzamer
- Dit maakt het halen van floor 60 vanuit start 20-30 uitdagend

### 5.3 Governance groeit het langzaamst

In alle scenario's heeft Governance (G) de laagste groeirate (4-12%/jaar). Dit reflecteert institutionele traagheid: regels en verantwoordingskaders ontwikkelen zich langzamer dan technische capability.

---

## 6. Strengere latere mijlpaal (kanttekening)

Bovenstaand model voorspelt **bounded-scope emergentie** — bruikbare agentnetwerken in beperkte domeinen. Een striktere, latere mijlpaal is **broad viability**:

- Cross-vendor interoperabiliteit
- Institutionele trust en mature governance
- Routine deployment met beperkt toezicht
- Economische schaal en impact

Deze zou hogere drempels vereisen (bijv. floors op 70-75 in plaats van 60) en waarschijnlijk extra tijd voor institutionele ontwikkeling.

Wij rapporteren deze als **secundaire mijlpaal**, niet als hoofdvoorspelling.

---

## 7. Open onzekerheden

1. **Geen historische precedent** — We hebben geen Level-3 agent netwerken gezien. Alle analogies (cloud, mobile) zijn imperfect.

2. **Expert judgment domineert** — Voor governance, network, en reliability hebben we geen sterke empirische ankers. De ranges zijn breed.

3. **Harde floors zijn normatief** — De keuze voor floor=60 (niet 55 of 65) bepaalt veel van de uitkomst.

4. **Breakthrough risico** — Een GPT-4-achtig moment voor agents is niet gemodelleerd. Smooth growth vs discontinu potentieel.

---

## 8. Samenvatting

Het forecast model voorspelt **eerste bounded-scope emergentie** van nuttige agent netwerken — niet volledige mature deployability.

Het gebruikt:
- **Logit/sigmoid transformatie** voor natuurlijke saturatie
- **Harde floors** (60) voor vier kritieke pilaren
- **Time-to-crossing** (binair: ja/nee per simulatie)
- **Expliciete onzekerheid** over empirisch vs expert components

De hoofdvoorspelling is een **crossing probability**, niet een enkel jaartal.

Het belangrijkste inzicht: **floors binden eerder dan de headline threshold**. Governance, Memory, Reliability en Network zijn de werkelijke bottlenecks — niet het gemiddelde van alle pilaren.
