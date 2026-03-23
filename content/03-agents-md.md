# Deel 3: AGENTS.md en Eigen Protocol

## Wat is AGENTS.md? (9-12 minuten)

> **"AGENTS.md is een voorspelbare plek om instructies en context aan coding agents te geven — een soort README voor agents."**

### Officiële definitie:

AGENTS.md is bedoeld als:
- Voorspelbare locatie voor agent instructies
- Project-specifieke context en conventies
- Build stappen, test procedures, coding styles

### Locatie:
```
project-root/
├── AGENTS.md          ← Hier
├── README.md           (voor mensen)
├── src/
├── tests/
└── ...
```

---

## De nuance: Context engineering

Anthropic waarschuwt:
> "Te veel tools en te veel context zijn een veelvoorkomende failure mode. Context moet informatief maar strak blijven."

### Balans:
- **Genoeg context** om de taak te begrijpen
- **Niet te veel** om token gebruik te beheersen
- **Relevant** voor de specifieke taak

---

## Een eigen protocol

Hier is een realistisch AGENTS.md voorbeeld dat ik zou gebruiken:

```markdown
# AGENTS.md

## Project Context

Dit is een AI agent research project. We onderzoeken:
- Wat AI agents zijn en hoe ze werken
- Hoe agent netwerken functioneren  
- De kosten en beperkingen van agent systemen

## Technologie Stack

- Python 3.11+
- matplotlib, numpy, pandas voor analyses
- Jupyter notebooks voor exploratie

## Coding Conventions

- PEP 8 style guide
- Type hints verplicht
- Docstrings voor alle publieke functies
- Tests voor analyse functies

## Build & Test

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Tests
pytest analyses/

# Run analyses
python analyses/token_usage.py
python analyses/ai_trends.py
python analyses/forecast_model.py
```

## Belangrijke Constraints

- Alle analyses moeten reproduceerbaar zijn
- Gebruik Monte Carlo simulaties met vaste seeds
- Documenteer alle aannames
- Visualisaties opslaan in assets/
```

---

## Screenshot: OpenClaw Context Documentatie

![OpenClaw Context](../assets/openclaw_context_docs.png)

*Bron: https://docs.openclaw.ai/concepts/context*

> "Context is everything OpenClaw sends to the model for a run. It is bounded by the model's context window (token limit)."

---

## Wat wordt er allemaal ingeladen?

Bij elke OpenClaw run wordt niet alleen de user prompt meegeteld, maar ook:

| Component | Geschatte tokens |
|-----------|-----------------|
| System prompt | ~9.600 tokens |
| Tool beschrijvingen | ~2.000-5.000 tokens |
| Skills | ~1.000-3.000 tokens |
| Workspace files (AGENTS.md) | ~500-2.000 tokens |
| Conversation history | Variabel (0-10k+) |
| Tool results | Variabel |
| Attachments | Variabel |

### Totaal voor context loading:
**~15.000 - 30.000 tokens** vóór de eigenlijke taak begint.

---

## Token verbruik analyse

### Scenario: Één "sociale cyclus" op Moltbook

Stel een agent die:
1. **Leest** zijn timeline (10 posts bekijken)
2. **Genereert** een reactie op 1 post
3. **Post** een eigen update

#### Stap 1: Context loading (per actie)
```
System prompt:        9.600 tokens
AGENTS.md:            1.200 tokens  
Tool descriptions:    3.000 tokens
Agent persona:        1.500 tokens
Previous history:     5.000 tokens
───────────────────────────────
Subtotal (fixed):    20.300 tokens
```

#### Stap 2: Timeline lezen (10 posts)
```
10 posts × 500 tokens = 5.000 tokens (input)
```

#### Stap 3: Reactie genereren
```
Context (relevant posts):  1.500 tokens
Generated response:          800 tokens (output)
```

#### Stap 4: Eigen post maken
```
Context (inspiratie):      1.000 tokens
Generated post:              600 tokens (output)
```

### Totale token verbruik per cyclus:

| Component | Input tokens | Output tokens |
|-----------|-------------|---------------|
| Context loading (3×) | 60.900 | - |
| Timeline lezen | 5.000 | - |
| Reactie genereren | 1.500 | 800 |
| Eigen post | 1.000 | 600 |
| **Totaal** | **68.400** | **1.400** |

### Kosten berekening (Claude Opus 4.6 pricing):

| Rate | Kosten |
|------|--------|
| Input: $5 / 1M tokens | $0.342 |
| Output: $25 / 1M tokens | $0.035 |
| **Totaal per cyclus** | **~$0.38** |

---

## Vergelijking: Mens vs AI

| Aspect | Mens | AI Agent |
|--------|------|----------|
| **Context loading** | Continu aanwezig | 20k+ tokens per actie |
| **"Sociale cyclus" kosten** | ~$0 (energie) | ~$0.38 |
| **Geheugen** | Geïntegreerd, efficiënt | Ge-fragmenteerd, expliciet |
| **Identiteit** | Stabiel, embodied | Gereconstrueerd per sessie |

### Op schaal:

| Scenario | Aantal agents | Cycli/dag | Dagelijkse kosten |
|----------|--------------|-----------|------------------|
| Klein netwerk | 100 | 10 | **$380** |
| Moltbook-achtig | 10.000 | 10 | **$38.000** |
| Twitter-schaal | 100M | 10 | **$380M** |

> **"Sociaal zijn" is voor agents computationeel veel duurder dan voor mensen.**

---

## OpenClaw tooling voor transparantie

OpenClaw biedt expliciete tooling:

| Command | Functie |
|---------|---------|
| `/status` | Huidige context status |
| `/context list` | Welke files zijn geladen |
| `/context detail` | Token count per component |
| `/usage tokens` | Token gebruik inzicht |

Dit maakt het mogelijk om **kostenbewust** te werken.
