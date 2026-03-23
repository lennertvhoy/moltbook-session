# Moltbook Session - AI Agents & Agent Networks

Een complete 20-25 minuten sessie over AI agents, OpenClaw, Moltbook en de toekomst van AI agent netwerken.

## Snelle Start

```bash
# Setup
cd /home/ff/Documents/BoostMeUp/MoltBook_Sessie
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run analyses
python analyses/token_usage.py
python analyses/ai_trends.py
python analyses/forecast_model.py
```

## Inhoud

### Content Files (`content/`)
| Bestand | Onderwerp | Tijd |
|---------|-----------|------|
| `01-intro.md` | Hook, OpenClaw, Moltbook | 0-3 min |
| `02-ai-agents.md` | Wat is een AI agent, agent netwerken | 3-9 min |
| `03-agents-md.md` | AGENTS.md, protocol, token analyse | 9-17 min |
| `04-kritiek.md` | Waarom dit nog geen echt sociaal netwerk is | 17-20 min |
| `05-trends.md` | AI trend grafieken en analyse | 20-22 min |
| `06-forecast.md` | Monte Carlo forecasting model | 22-25 min |
| `07-slot.md` | Conclusie en take-aways | 25 min |

### Analyses (`analyses/`)
- **`token_usage.py`** - Token verbruik analyse voor één "sociale cyclus"
  - Context loading breakdown
  - Kosten vergelijking per model
  - Schaal scenario's
  
- **`ai_trends.py`** - AI capability en efficiency trends
  - Epoch Capabilities Index
  - Benchmark sprongen
  - Inference kosten daling
  - MiniMax vs Claude Opus vergelijking
  
- **`forecast_model.py`** - Monte Carlo forecasting model
  - 7-pilaar readiness index
  - Drie scenario's (Conservative, Base, Accelerated)
  - 10,000 simulaties per scenario

### Visualisaties (`assets/`)

**Gegenereerde Analyses:**
- `token_breakdown.png` - Token usage visualisaties
- `ai_trends.png` - AI trends dashboard
- `forecast_distribution.png` - Forecast resultaten

**Screenshots van Bronnen:**
- `moltbook_homepage.png` - Moltbook homepage
- `moltbook_terms_eligibility.png` - Moltbook Terms of Service
- `openclaw_context_docs.png` - OpenClaw context documentatie
- `stanford_hai_ai_index_2025.png` - Stanford HAI AI Index 2025
- `epoch_ai_eci.png` - Epoch Capabilities Index

Zie ook: `content/00-screenshots-gallery.md` voor een overzicht van alle screenshots.

### Presentatie (`slides/`)
- `slides-main.md` - 37 slides met sprekersnotities

## Kernboodschap

> **"Moltbook is interessant, niet omdat het al een echt sociaal netwerk voor AI is, maar omdat het toont wat er nog ontbreekt: identiteit, geheugen, governance en economische efficiëntie."**

### Belangrijkste Inzichten

1. **Token verbruik:** ~$0.38 per "sociale cyclus" (vs $0 voor mensen)
2. **Geheugen:** AI heeft geen stabiel, goedkoop, doorlopend sociaal geheugen
3. **Forecast:** Median arrival 2036-2039 afhankelijk van scenario
4. **Bottleneck:** Niet meer alleen ruwe intelligentie, maar continuïteit, coördinatie, governance en kosten

## Forecast Resultaten (Samenvatting)

| Scenario | P(≤2035) | P(≤2040) | Median |
|----------|----------|----------|--------|
| Conservative | 0% | 0.3% | 2039 |
| Base case | 2.4% | 28.9% | 2038 |
| Accelerated | 45.5% | 95.2% | 2036 |

*Level-3 reality = globaal, stabiel, economisch levensvatbaar agent netwerk*

## Bronnen

- **Stanford HAI AI Index 2025**
- **Epoch AI**
- **OpenClaw Documentatie** (docs.openclaw.ai)
- **Moltbook** (moltbook.com)
- **Euronews onderzoek** (AI vs Human op Moltbook)

## Licentie

Dit project is voor educatieve doeleinden.

---

*Gemaakt: Maart 2026*
