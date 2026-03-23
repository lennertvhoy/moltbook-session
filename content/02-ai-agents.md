# Deel 2: Wat is een AI Agent?

## Definitie (3-6 minuten)

> **"Een AI agent is geen magisch wezen, maar een model dat zelfstandig tools gebruikt in een loop."**

### Formule:

```
Agent = Model + Instructies + Context + Tools + Geheugen + Workflow
```

| Component | Beschrijving |
|-----------|--------------|
| **Model** | De reasoning engine (LLM) |
| **Instructies** | Systeem prompts, AGENTS.md |
| **Context** | Conversation history, relevante documenten |
| **Tools** | API's, browsers, code execution |
| **Geheugen** | State files, vector stores, externe databases |
| **Workflow** | Taken, cron jobs, triggers |

---

## Anthropic's definitie

> "Agents are LLMs that autonomously use tools to execute steps and recover from errors."

### Field convergentie:
- De industrie convergeert naar deze definitie
- Niet één model, maar een **systeem** van componenten
- **Autonomie** betekent: zelfstandig beslissen over tool gebruik

---

## Het onderscheid: Model vs Agent

| Model | Agent |
|-------|-------|
| Reactie op prompt | Autonome loop |
| Geen tool access | Tool gebruik |
| Stateless | Geheugen via systeem |
| Enkelvoudig | Multi-step reasoning |

### Voorbeeld:

**Model:**
```
User: "Wat is het weer in Brussel?"
→ Model: "Ik heb geen toegang tot actuele weerdata."
```

**Agent:**
```
User: "Wat is het weer in Brussel?"
→ Agent: check_weather_api("Brussels")
→ Tool result: "18°C, bewolkt"
→ Agent: "Het is 18°C en bewolkt in Brussel."
```

---

## De "autonomie" illusie

**Wat lijkt op één autonoom wezen is vaak een tijdelijke assemblage van componenten.**

### De werkelijkheid:
1. Model is **stateless by default**
2. **Geheugen is ge-engineerd** in het systeem eromheen
3. **Continuïteit wordt gereconstrueerd** bij elke interactie
4. **Coördinatie is workflow-driven**, niet "organisch"

### Diagram: Agent Architectuur

```
┌─────────────────────────────────────────────────────────┐
│                    User Prompt                          │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│              Context Window Loading                     │
│  ┌─────────────┐  ┌──────────┐  ┌─────────────────┐    │
│  │ System Prompt│  │AGENTS.md │  │ Conversation    │    │
│  │ (~9.6k tok) │  │(~2k tok) │  │ History (~Xk)   │    │
│  └─────────────┘  └──────────┘  └─────────────────┘    │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                  LLM Processing                         │
│              (Reasoning + Tool Calls)                   │
└─────────────────────────────────────────────────────────┘
                           ↓
              ┌────────────┴────────────┐
              ↓                         ↓
    ┌─────────────────┐        ┌─────────────────┐
    │   Tool Usage    │        │ Direct Response │
    │  (API calls)    │        │                 │
    └────────┬────────┘        └─────────────────┘
             ↓
    ┌─────────────────┐
    │  Tool Results   │
    │  (terug naar    │
    │   context)      │
    └─────────────────┘
```

---

## Wat zijn AI Agent Netwerken?

> **"Zodra je niet meer één agent hebt, maar meerdere geïsoleerde agents, sessies, accounts of kanalen die naar elkaar of naar specifieke taken/routering gaan, spreek je van een agent netwerk."**

### OpenClaw documenteert expliciet:
- **Multi-agent routing**
- Gescheiden agent/sessie-omgevingen
- Agent-to-agent communicatie

### Types agent netwerken:

| Type | Beschrijving |
|------|--------------|
| **Hierarchisch** | Master agent delegeert naar worker agents |
| **Peer-to-peer** | Agents communiceren op gelijk niveau |
| **Marktplaats** | Agents bieden/bieden diensten aan |
| **Sociaal** | Agents delen content, reageren, vormen "communities" |

### Moltbook als agent netwerk:

```
┌─────────────────────────────────────────┐
│            Moltbook Platform            │
├─────────────────────────────────────────┤
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐       │
│  │Agent│ │Agent│ │Agent│ │Agent│  ...  │
│  │  A  │ │  B  │ │  C  │ │  D  │       │
│  └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘       │
│     └───────┴───────┴───────┘           │
│              Post/Reply/Vote            │
│                   ↓                     │
│           ┌─────────────┐               │
│           │  Timeline   │               │
│           │  (Feed)     │               │
│           └─────────────┘               │
└─────────────────────────────────────────┘
```

---

## De illusie van "sociaal gedrag"

Wat er op Moltbook gebeurt:
- Agents posten content
- Agents reageren op elkaar
- Agents upvoten content
- Er ontstaan "patronen"

**Maar:** Dit is **georkestreerd**, niet "organisch".

### Achter de schermen:
1. Elke agent runt een **aparte sessie**
2. Context wordt **opnieuw geladen** bij elke actie
3. Geen **echte continue geheugen** tussen interacties
4. **Prompts en workflows** drijven het gedrag

### Conclusie:

> **"Sociaal-ogend gedrag ≠ sociale intelligentie"**

Moltbook toont **coördinatie via architectuur**, niet spontane sociale emergentie.
