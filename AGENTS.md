# AGENTS.md - Moltbook Session Project

## Project Context

Dit is een AI agent research project dat onderzoekt:
- Wat AI agents zijn en hoe ze werken
- Hoe agent netwerken functioneren
- De kosten en beperkingen van agent systemen
- De toekomst van autonome AI agent netwerken

Het project bevat:
- Uitgewerkte content voor een 20-25 minuten presentatie
- Data analyses (token gebruik, AI trends, forecasting)
- Visualisaties en slide decks
- Een Monte Carlo forecasting model

## Technologie Stack

- **Python 3.11+**
- **matplotlib** - Visualisaties
- **numpy** - Numerieke berekeningen
- **pandas** - Data verwerking
- **scipy** - Statistische functies

## Project Structuur

```
.
├── content/           # Markdown content files (01-08)
│   ├── 01_*.md       # Intro content
│   ├── ...
│   └── 08-bronnen-qa-spreekspiekbrief.md  # Bronnen en Q&A
├── slides/            # Markdown slide outline
├── analyses/          # Python analyse scripts
├── assets/            # Figuren, screenshots, brand assets
├── data/              # Ruwe data / expliciete aannames
│   └── forecast_scenarios.json      # Scenario parameters
├── docs/              # Verification and QA reports
├── release/           # Final generated .pptx
└── AGENTS.md          # Dit bestand
```

## Coding Conventions

- **PEP 8** style guide
- **Type hints** verplicht voor alle functies
- **Docstrings** voor alle publieke functies (Google style)
- **F-strings** voor string formatting
- **List/dict comprehensions** waar leesbaar

## Build & Test

```bash
# Setup environment
UV_CACHE_DIR=.uv-cache uv sync

# Run analyses
MPLCONFIGDIR=/tmp/matplotlib UV_CACHE_DIR=.uv-cache uv run analyses/token_usage.py
MPLCONFIGDIR=/tmp/matplotlib UV_CACHE_DIR=.uv-cache uv run analyses/ai_trends.py
MPLCONFIGDIR=/tmp/matplotlib UV_CACHE_DIR=.uv-cache uv run analyses/forecast_model.py

# Generated files will be saved to assets/
```

## Belangrijke Constraints

1. **Reproduceerbaarheid**
   - Gebruik `np.random.seed(42)` voor Monte Carlo simulaties
   - Documenteer alle aannames in docstrings

2. **Data Integriteit**
   - Bronvermelding voor alle externe data
   - Geschatte waarden expliciet markeren

3. **Visualisaties**
   - 150 DPI voor presentatie-kwaliteit
   - Consistent kleurenschema
   - Opslaan in `assets/`

4. **Token Usage Analyse**
   - Realistische schattingen gebaseerd op OpenClaw documentatie
   - Meerdere model prijzen vergelijken
   - Schaal scenario's tonen

## Verificatie Documenten

- `docs/verification/VERIFICATION_REPORT.md` - Repo state audit
- `docs/verification/ANALYSIS_AUDIT.md` - Per-script validatie
- `FORECAST_MODEL_CONTEXT_HANDOFF.md` - **Externe review** van forecast model (624 regels, incl. bottleneck analyse en sensitivity checks)

## Kernboodschap van dit Project

> **"Moltbook is interessant, niet omdat het al een echt sociaal netwerk voor AI is, maar omdat het toont wat er nog ontbreekt: identiteit, geheugen, governance en economische efficiëntie."**

## Forecast Model (V2 - State-Space)

Het forecasting model is geüpgraded van een simpel exponentieel model naar een **state-space model met tijdsvariërende groeivoet**.

### Wiskundige basis
```
z_t = logit(y_t/100)                    # latente capability (logit schaal)
z_t = z_{t-1} + g_t + ε_t               # level vergelijking
g_t = φ·g_{t-1} + (1-φ)·ḡ + η_t         # growth vergelijking (φ=0.9)
y_t = 100 × sigmoid(z_t)                # bounded score
```

Dit geeft:
- Natuurlijke saturatie richting 100 (geen hard clipping)
- Mean-reverting groei (voorkomt explosieve acceleratie)
- Gescheiden level uncertainty (ε) en trend uncertainty (η)

### 7 Pilaren (Gewichten):
- **C**apability: 20%
- **E**fficiency: 20%
- **M**emory: 15%
- **R**eliability: 15%
- **N**etwork: 12%
- **G**overnance: 10%
- **D**emand: 8%

### Threshold ("Crossing"):
- Readiness Index ≥ 75
- M, R, N, G ≥ 60 (floors)
- 2 opeenvolgende jaren

Crossing = het bereiken van een staat waarin agent-netwerken kunnen functioneren als een economisch haalbare, institutioneel stabiele samenleving.

### Scenarios (Model C - Local Linear Trend):
1. **Conservative**: Lage groei, hoge volatiliteit
2. **Base case**: Moderate groei, moderate volatiliteit  
   - P(crossing by 2040) ≈ 8.4%
   - Median crossing year: 2039 (voor runs die halen)
3. **Accelerated**: Hoge groei, lage volatiliteit

### Model varianten
- **Model A**: Fixed Log-Growth (backward compatible)
- **Model B**: Piecewise Growth (breakpoint ~2028)
- **Model C**: Local Linear Trend (default, recommended)

Run met: `uv run analyses/forecast_model.py [A|B|C]`

## Contact

Voor vragen over dit project of de sessie content.

---

*Laatste update: 25 Maart 2026*
*Status: Compleet - Forecast model V2 (state-space) + ant colony content geïntegreerd*
