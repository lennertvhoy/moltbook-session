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

## Forecast Model (Canoniek)

**Wat we voorspellen:** Eerste betekenisvolle bounded-scope emergentie van Level-3-achtige AI agent netwerken.

**Niet:** Brede volwassen deployability, cross-vendor ubiquity, of volledige institutionele maturiteit.

### Wiskundige vorm

Discrete-time hazard met soft feasibility:
```
h(t) = h0 × exp(λ_C·z_C + λ_E·z_E + λ_D·z_D + λ_M·z_M) 
       × φ_G(y_G) × φ_N(y_N) × φ_R(y_R)

φ(y; θ, k) = 1 / (1 + exp(-k × (y - θ) / 10))
```

**Output:** Time-to-event distributie (survival curve), niet "jaar X of nooit".

### Parameters

| Component | Status | Voorbeeld ranges |
|-----------|--------|------------------|
| C, E (Capability, Efficiency) | Empirisch | Uit Stanford HAI, Epoch |
| D (Demand) | Proxy | Investeringen, adoptie |
| M, N, R, G | Expert judgment | Ranges, geen punten |

**Belangrijk:** Output is distribution met expliciete uncertainty, geen schijnprecisie.

### Historische context

- **V1 (oud):** Harde floors op 60, "91% never crosses by 2040", te streng
- **Audit:** Floors domineerden uitkomst (38pp effect); horizon truncatie creëerde kunstmatig "never"
- **Huidig (canoniek):** Soft feasibility, time-to-event framing, expliciete onzekerheid

### Rauwe audit documenten

Volledige ablaties, V2 specificaties, en research notities staan in:
`docs/model_audit/` (niet canoniek, wel beschikbaar voor referentie)

## Contact

Voor vragen over dit project of de sessie content.

---

*Laatste update: 25 Maart 2026*
*Status: Compleet - Forecast model V2 (state-space) + ant colony content geïntegreerd*
