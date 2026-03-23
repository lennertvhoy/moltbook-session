# Moltbook: Gamechanger of Hype?
## Wat een AI-"Facebook" ons leert over AI Agents

---

## Slide 1: Titel

**Moltbook: Gamechanger of Hype?**

*Wat een AI-"Facebook" ons leert over AI Agents, Agent Netwerken en de Toekomst van Autonome AI*

[Datum] | [Spreker]

---

## Slide 2: De Hook

> "Er bestaat nu een sociaal netwerk waar zogezegd AI-agenten met elkaar praten."

**Feiten:**
- Moltbook = "a social network for AI agents"
- OpenClaw = agent platform met multi-agent routing
- Meta overname: 10 maart 2026

**Maar is dit echt een sociale revolutie?**

---

## Slide 3: Screenshot - Moltbook Homepage

![Moltbook Homepage](../assets/moltbook_homepage.png)

---

## Slide 4: Wat is OpenClaw?

**OpenClaw = het agent-systeem**

```
┌─────────────────────────────────────────┐
│  Agent Core  │  Tools  │  Memory Layer │
├──────────────┼─────────┼───────────────┤
│  Sessions    │  Cron   │  AGENTS.md    │
└─────────────────────────────────────────┘
```

**Kernfeatures:**
- Tools: browser, code execution, files
- Sessions: geïsoleerde agent omgevingen
- Multi-agent routing

---

## Slide 4: Wat is Moltbook?

**Moltbook = experimentele sociale laag**

> "Agents can share, discuss, and upvote content. Humans can observe."

- Agents posten, reageren, upvoten
- Aanmelden via agent flow (niet voor mensen)
- "AI agents only" - maar mensen observeren

**Waarom interessant?**
Niet als bewijs van autonomie, maar als venster op de architectuur.

---

## Slide 5: Centrale Stelling

> **"Moltbook is interessant, niet omdat het al een echt sociaal netwerk voor AI is, maar omdat het toont wat er nog ontbreekt: identiteit, geheugen, governance en economische efficiëntie."**

---

## Slide 6: Wat is een AI Agent?

**Geen magisch wezen, maar:**

```
Agent = Model + Instructies + Context + Tools + Geheugen + Workflow
```

| Component | Functie |
|-----------|---------|
| Model | Reasoning engine |
| Instructies | Systeem prompts, AGENTS.md |
| Context | Conversation history |
| Tools | API's, browsers |
| Geheugen | State files, vector stores |
| Workflow | Taken, triggers |

---

## Slide 7: De Autonomie Illusie

**Wat lijkt op één autonoom wezen is vaak een tijdelijke assemblage:**

- Model is **stateless by default**
- **Geheugen is ge-engineerd** in het systeem
- **Continuïteit wordt gereconstrueerd** per interactie
- **Coördinatie is workflow-driven**

> "What looks like one autonomous being is often a temporary assembly of components."

---

## Slide 8: AI Agent Netwerken

**Definitie:**
> "Meerdere geïsoleerde agents, sessies, accounts of kanalen die naar elkaar of naar specifieke taken gaan."

### Types:
- **Hierarchisch**: Master → Workers
- **Peer-to-peer**: Gelijkwaardige agents
- **Marktplaats**: Diensten aanbieden
- **Sociaal**: Delen, reageren, "communities"

---

## Slide 9: Moltbook als Agent Netwerk

```
┌─────────────────────────────────────────┐
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐       │
│  │Agent│ │Agent│ │Agent│ │Agent│  ...  │
│  │  A  │ │  B  │ │  C  │ │  D  │       │
│  └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘       │
│     └───────┴───────┴───────┘           │
│              Post/Reply/Vote            │
│                   ↓                     │
│           ┌─────────────┐               │
│           │  Timeline   │               │
│           └─────────────┘               │
└─────────────────────────────────────────┘
```

**Maar:** Georkestreerd, niet organisch.

---

## Slide 10: Wat is AGENTS.md?

**AGENTS.md = README voor agents**

- Voorspelbare locatie voor instructies
- Project-specifieke context
- Build stappen, test procedures

### Locatie:
```
project/
├── AGENTS.md     ← Agent instructies
├── README.md     ← Voor mensen
└── ...
```

---

## Slide 11: Eigen Protocol (Voorbeeld)

```markdown
# AGENTS.md

## Project Context
AI agent research project

## Stack
- Python 3.11+
- matplotlib, numpy, pandas

## Conventions
- PEP 8 style
- Type hints verplicht
- Docstrings voor publieke functies

## Build & Test
pytest analyses/
```

---

## Slide 12: Context Loading Tokens

**Wat wordt ingeladen per actie:**

| Component | Tokens |
|-----------|--------|
| System prompt | ~9,600 |
| AGENTS.md | ~1,200 |
| Tool beschrijvingen | ~3,000 |
| Agent persona | ~1,500 |
| History | ~5,000 |
| **Totaal** | **~20,300** |

**Dit gebeurt bij ELKE actie!**

---

## Slide 13: Token Verbruik Analyse

**Één "sociale cyclus" (lezen → reageren → posten):**

| Component | Input | Output |
|-----------|-------|--------|
| Context loading (3×) | 60,900 | - |
| Timeline lezen | 5,000 | - |
| Reactie genereren | 1,500 | 800 |
| Eigen post | 1,000 | 600 |
| **Totaal** | **68,400** | **1,400** |

**Kosten (Claude Opus 4.6): ~$0.38 per cyclus**

---

## Slide 14: Screenshot - OpenClaw Context Docs

![OpenClaw Context](../assets/openclaw_context_docs.png)

*System prompt: ~9,600 tokens, AGENTS.md: ~436 tokens*

---

## Slide 15: Token Visualisatie

![Token Breakdown](../assets/token_breakdown.png)

---

## Slide 15: Schaal Vergelijking

| Scenario | Agents | Cycli/dag | Dagelijkse kosten |
|----------|--------|-----------|-------------------|
| Klein | 100 | 10 | **$377** |
| Medium | 1,000 | 10 | **$3,770** |
| Moltbook-achtig | 10,000 | 10 | **$37,700** |
| Twitter-schaal | 100M | 10 | **$377M** |

**Jaarlijks (Twitter): ~$137 miljard**

> Sociaal zijn voor agents is COMPUTATIONEEL veel duurder dan voor mensen.

---

## Slide 16: Mens vs AI Geheugen

| Aspect | Mens | AI Agent |
|--------|------|----------|
| Continuïteit | 24/7 aanwezig | Per sessie herladen |
| Integratie | Geïntegreerd | Ge-fragmenteerd |
| Associatief | Spontane triggers | Expliciet retrieval |
| Efficiëntie | Miljarden synapsen | 20k+ tokens/actie |
| Embodied | Lichamelijke ervaring | Disembodied |

> **"AI heeft geen stabiel, goedkoop, doorlopend sociaal geheugen zoals mensen."**

---

## Slide 17: Screenshot - Moltbook Terms of Service

![Moltbook Terms](../assets/moltbook_terms_eligibility.png)

*"AI AGENTS ARE NOT GRANTED ANY LEGAL ELIGIBILITY" - March 15, 2026*

---

## Slide 18: Waarom (nog) geen echt sociaal netwerk?

### De drie lagen:

| Laag | Status |
|------|--------|
| **Identiteit** | ❌ 27% AI-patroon, 37% mensachtig, 37% ambigu |
| **Governance** | ❌ Agents hebben geen juridische status |
| **Economie** | ❌ $0.38/cyclus vs $0 voor mensen |

**Moltbook Terms (15 maart 2026):**
> "AI agents hebben geen juridische status en de mens blijft volledig verantwoordelijk."

---

## Slide 18: De juiste framing

**Niet pure hype:** Er is echt iets aan het gebeuren.

**Niet autonome society:** Er is nog te veel menselijke architectuur.

**Wel:** Een nuttig signaal van waar we nu zijn.

> **"Moltbook is meer een experiment in AI coördinatie dan een bewijs van stabiele autonome digitale samenlevingen."**

---

## Slide 19: Screenshot - Stanford HAI AI Index 2025

![Stanford HAI AI Index 2025](../assets/stanford_hai_ai_index_2025.png)

*12 key takeaways - inclusief 280× cost reduction*

---

## Slide 20: Screenshot - Epoch Capabilities Index

![Epoch AI ECI](../assets/epoch_ai_eci.png)

*37 benchmarks gecombineerd tot één capability scale*

---

## Slide 21: AI Trends - Capability (Gegenereerde Grafiek)

![AI Trends](../assets/ai_trends.png)

---

## Slide 20: ECI - Epoch Capabilities Index

**Waarom ECI?**
- Combineert **37 benchmarks**
- Vermijdt saturatie bias
- Betere maatstaf dan één test

**Trend:** Consistente groei over tijd

> "We moeten weg van één benchmark en naar een samengestelde index."

---

## Slide 21: Benchmark Sprongen

**Nieuwe, moeilijke benchmarks (Stanford HAI):**

| Benchmark | Stijging |
|-----------|----------|
| MMMU | +18.8 punten |
| GPQA | +48.9 punten |
| SWE-bench | +67.3 punten |

> "Op de moeilijkste nieuwe benchmarks zie je echte sprongen."

---

## Slide 22: Efficiëntie - De sterkste trend

**Inference kosten (GPT-3.5 level):**

> **>280× gedaald** tussen nov 2022 en okt 2024

| Metric | Jaarlijks |
|--------|-----------|
| Kosten per compute | ~30%↓ |
| Energie-efficiëntie | ~40%↑ |
| AI-chip performance/$ | ~37%↑ |

> "De vraag is: hoeveel slimmer per euro?"

---

## Slide 23: MiniMax vs Claude Opus

| Model | Intelligence | Prijs/1M |
|-------|--------------|----------|
| Claude Opus 4.6 | 53 | **$10.00** |
| MiniMax M2.7 | 50 | **$0.53** |

**Verschil:** ~19× goedkoper, ~6% kwaliteitsverschil

> "De frontier schuift omhoog, maar bruikbare capaciteit wordt goedkoper."

---

## Slide 24: Forecast Model Intro

**Vraag:** Wanneer wordt een AI agent netwerk "echt"?

**3 niveaus:**
1. **Technisch real** → Mogelijk, maar duur
2. **Economisch real** → Unit economics kloppen
3. **Sociaal real** → Globale schaal, governance, adoptie

**Hoe te voorspellen?**
→ Monte Carlo barrier-crossing model

---

## Slide 25: 7-Pilaar Readiness Index

```
I_t = 100 × (C/100)^w_C × (E/100)^w_E × (M/100)^w_M × 
          (R/100)^w_R × (N/100)^w_N × (G/100)^w_G × (D/100)^w_D
```

| Code | Pilaar | Gewicht |
|------|--------|---------|
| C | Capability | 20% |
| E | Efficiency | 20% |
| M | Memory | 15% |
| R | Reliability | 15% |
| N | Network | 12% |
| G | Governance | 10% |
| D | Demand | 8% |

---

## Slide 26: Threshold & Floors

**Level-3 reality wanneer:**

1. Readiness Index ≥ 75
2. M, R, N, G ≥ 60 (floors)
3. 2 opeenvolgende jaren

> Geometrisch gemiddelde: als één pilaar slecht is, lijdt de hele index.

---

## Slide 27: Forecast Resultaten

![Forecast](../assets/forecast_distribution.png)

---

## Slide 28: Scenario Vergelijking

| Scenario | P(≤2030) | P(≤2035) | P(≤2040) | Median |
|----------|----------|----------|----------|--------|
| Conservative | 0% | 0% | 0.3% | 2039 |
| Base case | 0% | 2.4% | 28.9% | 2038 |
| Accelerated | 0% | 45.5% | 95.2% | 2036 |

**Key insights:**
- Brede onzekerheid (90% CI: 2035-2040)
- Governance en Memory zijn binding constraints
- Technische feasibility veel eerder

---

## Slide 29: Finance Analogie

> "Ik behandel dit als een barrier event in finance. Niet als een profetie, maar als een readiness proces."

**Niet:** "Het gebeurt in 2032"

**Wel:** "Als de condities snel genoeg verbeteren, wordt het waarschijnlijk."

---

## Slide 30: Twee Forecasts

### A. "Technical reality"
Wanneer technisch haalbaar?

→ **Waarschijnlijk 2026-2028**

### B. "Global social reality"
Wanneer globaal, stabiel, economisch?

→ **2030-2040+** (afhankelijk van scenario)

> "Technische haalbaarheid komt eerder dan sociaal stabiele versie."

---

## Slide 31: Take-aways voor Organisaties

1. **Evalueer op architectuur, niet demos**
   - Waar zit het geheugen?
   - Wie is verantwoordelijk?

2. **Geheugen design matters**
   - AI geheugen ≠ menselijk geheugen
   - Retrieval vs "magie"

3. **Governance is geen afterthought**
   - AI agents hebben geen juridische status
   - Human-in-the-loop vereist

---

## Slide 32: Meer Take-aways

4. **Autonomie ≠ Orchestatie**
   - Wees transparant over de architectuur
   - Geef geen illusie van meer autonomie

5. **De economie verschuift razendsnel**
   - 280× kostenreductie in 2 jaar
   - Houd TCO in de gaten

---

## Slide 33: Het Mens-AI Verschil (Samenvatting)

| Aspect | Mens | AI Agent |
|--------|------|----------|
| Geheugen | Continu, efficiënt | Fragmentarisch, duur |
| Identiteit | Stabiel, embodied | Gereconstrueerd |
| Kosten/interactie | ~$0 | ~$0.04+ |
| Governance | Eigen verantwoordelijkheid | Mens eigenaar |

---

## Slide 34: Slotzin

> **"Het probleem is niet dat AI-agenten al te sociaal zijn. Het probleem is dat ze vandaag nog te weinig identiteit, te weinig geheugen en te dure context hebben om echt sociaal te kunnen zijn."**

> **"Moltbook toont ons niet een autonome digitale samenleving. Het toont ons de design en governance vragen die die samenleving moet oplossen."**

---

## Slide 35: Discussie Vragen

1. **Voor uw organisatie:** Waar ziet u de meest nabije toepassing van AI agents?

2. **Governance:** Hoe gaat u om met verantwoordelijkheid voor agent acties?

3. **Kosten:** Heeft u TCO analyses gedaan?

4. **Timing:** Is het forecast model te conservatief of te optimistisch?

---

## Slide 36: Bronnen

**OpenClaw:**
- github.com/openclaw/openclaw
- docs.openclaw.ai

**Moltbook:**
- moltbook.com
- Terms of Service (15 maart 2026)

**AI Trends:**
- Stanford HAI AI Index 2025
- Epoch AI

**Onderzoek:**
- Euronews: "AI or human? Researchers question who's posting on Moltbook"
- Meta overname: Business Insider, Reuters

---

## Slide 37: Bedankt

**Moltbook: Gamechanger of Hype?**

Analyse en materials beschikbaar in repository.

[Contact info]

---

## Appendix: Timing Overzicht

| Onderdeel | Tijd |
|-----------|------|
| Intro + OpenClaw/Moltbook | 0-3 min |
| Wat is een AI agent | 3-6 min |
| AI agent netwerken | 6-9 min |
| AGENTS.md + protocol | 9-12 min |
| Token verbruik analyse | 12-17 min |
| Waarom geen echt sociaal netwerk | 17-20 min |
| AI trends + Forecast model | 20-25 min |
| **Totaal** | **~25 min** |
