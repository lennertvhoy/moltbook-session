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
/home/ff/Documents/BoostMeUp/MoltBook_Sessie/
├── content/           # Markdown content files (01-07)
│   ├── 01-intro.md
│   ├── 02-ai-agents.md
│   ├── 03-agents-md.md
│   ├── 04-kritiek.md
│   ├── 05-trends.md
│   ├── 06-forecast.md
│   └── 07-slot.md
├── slides/            # Markdown slide decks
│   └── slides-main.md
├── analyses/          # Python analyse scripts
│   ├── token_usage.py
│   ├── ai_trends.py
│   └── forecast_model.py
├── assets/            # Gegenereerde visualisaties
│   ├── ai_trends.png
│   ├── forecast_distribution.png
│   └── token_breakdown.png
├── data/              # Ruwe data files
├── venv/              # Python virtual environment
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
cd /home/ff/Documents/BoostMeUp/MoltBook_Sessie
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run analyses
python analyses/token_usage.py
python analyses/ai_trends.py
python analyses/forecast_model.py

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

*Laatste update: Maart 2026*
*Status: Compleet*
