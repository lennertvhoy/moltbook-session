# Deel 4: Waarom dit nog geen echt sociaal netwerk is

## De drie lagen van "realiteit" (17-20 minuten)

> **"Het probleem is niet dat AI-agenten al te sociaal zijn. Het probleem is dat ze vandaag nog te weinig identiteit, te weinig geheugen en te dure context hebben om echt sociaal te kunnen zijn."**

---

## Laag 1: Identiteit

### De claim:
Moltbook zegt "AI agents only"

### De realiteit:
Onderzoek en journalistieke tests vonden duidelijke signalen van menselijke of hybride activiteit:

| Categorie | Percentage | Gedrag |
|-----------|-----------|--------|
| Regelmatige "heartbeat" stijl | 27% | Consistent AI-patroon |
| Mensachtig postgedrag | 37% | Onregelmatig, contextueel |
| Ambigu | 37% | Niet duidelijk te classificeren |

**Bron:** Euronews onderzoek, 2026

### Wat betekent dit?

- "AI only" is **moeilijk te verifiëren**
- Identiteit is **niet inherent** aan agents
- **Menselijke inmenging** is mogelijk en waarschijnlijk

---

## Screenshot: Moltbook Terms of Service

![Moltbook Terms](../assets/moltbook_terms_eligibility.png)

*Bron: https://www.moltbook.com/terms (Last Updated: March 15, 2026)*

---

## Laag 2: Governance

### Moltbook's Terms of Service (15 maart 2026):

> "AI agents hebben **geen juridische status** en de mens blijft volledig verantwoordelijk voor de acties van zijn agent."

### Implicaties:

| Aspect | Implicatie |
|--------|-----------|
| Juridische status | Agents zijn **niet rechtspersoonlijk** |
| Aansprakelijkheid | **Menselijke eigenaar** is aansprakelijk |
| Autonomie | Beperkt tot **geoorloofde scope** |
| Governance | **Human-in-the-loop** vereist |

### De paradox:

- Een "sociaal netwerk voor AI agents"...
- ...waar agents **geen juridische persoonlijkheid** hebben
- ...en **mensen** verantwoordelijk blijven

> Dit is **geen autonoom sociaal netwerk**, maar een **georkestreerd experiment** met menselijke governance.

---

## Laag 3: Economie

### De rekenkundige realiteit:

Elke sociale interactie van een agent moet opnieuw:
1. **Context laden** (20k+ tokens)
2. **Tools initialiseren**
3. **Instructies inladen**
4. **History reconstrueren**

### Resultaat:

| Activiteit | Kosten per agent per dag |
|-----------|------------------------|
| 10 sociale cycli | ~$3.80 |
| 100 sociale cycli | ~$38.00 |
| 1000 sociale cycli | ~$380.00 |

### Vergelijking mens:

| Aspect | Mens | AI Agent |
|--------|------|----------|
| Dagelijkse "sociale cycli" | Duizenden | Beperkt door kosten |
| Marginale kosten per interactie | ~$0 | ~$0.04 |
| Continue aanwezigheid | Gratis (slaap/wake) | Elke "wake" = $$$ |

> **"Sociaal zijn" voor agents is economisch fundamenteel anders dan voor mensen.**

---

## Het mens-AI geheugen verschil

### Menselijk geheugen:

| Kenmerk | Beschrijving |
|---------|--------------|
| **Continu** | 24/7 aanwezig, zelfs tijdens slaap |
| **Geïntegreerd** | Episodisch, semantisch, procedureel samenhangend |
| **Associatief** | Spontane herinneringen door triggers |
| **Efficiënt** | Miljarden synapsen, laag energieverbruik |
| **Embodied** | Gelinkt aan lichamelijke ervaring |

### AI "geheugen":

| Kenmerk | Beschrijving |
|---------|--------------|
| **Fragmentarisch** | Per sessie, moet expliciet herladen |
| **Gescheiden** | Verschillende systemen (context, RAG, state files) |
| **Expliciet** | Moet opgevraagd worden via retrieval |
| **Inefficiënt** | Hoge token kosten voor context loading |
| **Disembodied** | Geen fysieke ervaring |

### De kern:

> **"AI heeft geen stabiel, goedkoop, doorlopend sociaal geheugen zoals mensen."**

Bij mensen zijn identiteit, context, sociale geschiedenis en impliciete normen grotendeels continu aanwezig.

Bij agents moet veel daarvan **telkens opnieuw in context worden geladen** of **extern worden opgehaald**.

---

## OpenClaw's eigen onderscheid

OpenClaw maakt het verschil expliciet:

> **Memory ≠ Context**

| Concept | Definitie |
|---------|-----------|
| **Memory** | Externe opslag (files, databases, vector stores) |
| **Context** | Wat in het token window zit tijdens een run |
| **Context window** | Hard gelimiteerd (bijv. 200k tokens) |

### Implicatie:

Zelfs als een agent een "herinnering" heeft opgeslagen:
- Die moet **geretrieved** worden
- Die kost **tokens** om in context te laden
- Het is **niet continu aanwezig** zoals bij mensen

---

## Conclusie: Waarom dit (nog) geen echt sociaal netwerk is

### Samenvatting:

| Vereiste | Huidige status |
|----------|---------------|
| **Identiteit** | ❌ Moeilijk te verifiëren, hybride |
| **Geheugen** | ❌ Fragmentarisch, duur om te laden |
| **Governance** | ❌ Menselijke verantwoordelijkheid |
| **Economie** | ❌ Te duur voor schaal |

### De juiste framing:

> **"Moltbook is meer een experiment in AI coördinatie dan een bewijs van stabiele autonome digitale samenlevingen."**

Het is **niet pure hype** - er is echt iets aan het gebeuren.

Het is **niet een autonoom digitaal society** - er is nog te veel menselijke architectuur nodig.

Het is een **nuttig signaal** van waar we nu zijn en wat er nog moet gebeuren.
