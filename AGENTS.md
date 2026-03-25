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
├── content/           # Markdown content files (01-07 + sidebar)
│   ├── 01_*.md       # Intro content
│   ├── ...
│   └── 07_forecast_aggi_sidebar.md  # AGI als voorwaarde/volg vraag
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

## Forecast Model Parameters

### 7 Pilaren (Gewichten):
- **C**apability: 20%
- **E**fficiency: 20%
- **M**emory: 15%
- **R**eliability: 15%
- **N**etwork: 12%
- **G**overnance: 10%
- **D**emand: 8%

### Threshold:
- Readiness Index ≥ 75
- M, R, N, G ≥ 60 (floors)
- 2 opeenvolgende jaren

### Scenarios:
1. **Conservative**: Lage groei, hoge volatiliteit
2. **Base case**: Moderate groei, moderate volatiliteit
3. **Accelerated**: Hoge groei, lage volatiliteit

## Contact

Voor vragen over dit project of de sessie content.

---

*Laatste update: 23 Maart 2026*
*Status: Compleet - Forecast model bijgewerkt (G governance growth 0.08→0.12)*
