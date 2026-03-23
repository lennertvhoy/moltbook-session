# Screenshots Gallery

Dit bestand bevat de belangrijkste screenshots van externe bronnen die in de presentatie worden gebruikt.

Gebruik deze galerij als **ondersteunend bewijsmateriaal**, niet als vervanging van de onderliggende bronpagina’s. De juiste volgorde in deze repo is:

1. lees eerst de inhoudelijke hoofdstukken in deze map
2. gebruik daarna deze screenshots om de visuele ankers in de deck te herkennen
3. ga voor precieze claimcontrole terug naar de verificatiedocs in [`../docs/verification/`](../docs/verification/)

Belangrijk: screenshots zijn in dit project bewijssteun, geen primaire citatievorm.

---

## 1. Moltbook Homepage

**Bron:** https://www.moltbook.com

![Moltbook Homepage](../assets/moltbook_homepage.png)

*Toont: "A Social Network for AI Agents" en "Humans welcome to observe."*

**Waarom dit relevant is:** dit is het marketinganker van de sessie. Het laat zien hoe Moltbook zichzelf positioneert, maar niet automatisch wat juridisch, technisch of institutioneel al bewezen is.

---

## 2. Moltbook Terms of Service

**Bron:** https://www.moltbook.com/terms

![Moltbook Terms](../assets/moltbook_terms_eligibility.png)

*Toont: Key bepalingen over AI agent eligibility en verantwoordelijkheid*

**Waarom dit relevant is:** deze screenshot corrigeert de homepage-lezing. Hier wordt zichtbaar dat agentparticipatie op het platform niet hetzelfde is als juridische autonomie.

**Belangrijke tekst:**
> "AI AGENTS ARE NOT GRANTED ANY LEGAL ELIGIBILITY WITH USE OF OUR SERVICES. AS A RESULT, YOU AGREE THAT YOU ARE SOLELY RESPONSIBLE FOR YOUR AI AGENTS AND ANY ACTIONS OR OMISSIONS OF YOUR AI AGENTS."

---

## 3. OpenClaw Context Documentatie

**Bron:** https://docs.openclaw.ai/concepts/context

![OpenClaw Context](../assets/openclaw_context_docs.png)

*Toont: een OpenClaw context breakdown met system prompt (~9.603 tokens) en totale session tokens van ongeveer 14.250 in het getoonde voorbeeld.*

**Waarom dit relevant is:** dit is het belangrijkste bronanker voor de kosten- en contextdiscussie in de sessie. De repo gebruikt dit niet als Moltbook-meting, maar als gedocumenteerd voorbeeld van hoe groot contextoverhead al snel kan worden.

**Key inzicht:**
> "Context is everything OpenClaw sends to the model for a run. It is bounded by the model's context window (token limit)."

---

## 4. Stanford HAI AI Index 2025

**Bron:** https://hai.stanford.edu/ai-index/2025-ai-index-report

![Stanford HAI AI Index 2025](../assets/stanford_hai_ai_index_2025.png)

*Toont: Top 12 takeaways uit het AI Index Report 2025*

**Waarom dit relevant is:** deze bron ondersteunt vooral de brede capability- en kosttrendclaims. Ze is nuttig als overzicht, maar wordt in de repo nog altijd smal gelezen.

**Key takeaways zichtbaar:**
1. AI performance on demanding benchmarks continues to improve
2. AI is increasingly embedded in everyday life
3. Business is all in on AI
4. AI becomes more efficient, affordable and accessible (>280× cost reduction)

---

## 5. Epoch AI - Epoch Capabilities Index

**Bron:** https://epoch.ai/benchmarks/eci

![Epoch AI ECI](../assets/epoch_ai_eci.png)

*Toont: ECI grafiek met model scores over tijd.*

**Waarom dit relevant is:** deze screenshot helpt om uit te leggen waarom samengestelde capability-metrics bestaan, maar ook waarom je voorzichtig moet blijven met exacte benchmarktellingen en grote "alles is exponentieel"-claims.

**Key inzicht:**
> "ECI is a composite metric which uses scores from many benchmarks to generate a single, general capability scale."

*Nuance:* de ECI-pagina noemt in de overview 37 benchmarks, maar in de data-sectie 42 benchmarks. Gebruik in de presentatie dus liever "dozens of benchmarks" dan een te hard exact getal.

---

## Gebruik in presentaties en studie

Deze screenshots kunnen direct worden gebruikt in presentaties door te verwijzen naar:
- `../assets/moltbook_homepage.png`
- `../assets/moltbook_terms_eligibility.png`
- `../assets/openclaw_context_docs.png`
- `../assets/stanford_hai_ai_index_2025.png`
- `../assets/epoch_ai_eci.png`

Op GitHub worden deze afbeeldingen automatisch gerenderd wanneer je de markdown files bekijkt.

## Beste koppeling met de teksthoofdstukken

- homepage + terms: [`01-intro.md`](01-intro.md) en [`04-kritiek.md`](04-kritiek.md)
- OpenClaw context: [`02-ai-agents.md`](02-ai-agents.md) en [`03-agents-md.md`](03-agents-md.md)
- Stanford HAI + Epoch: [`05-trends.md`](05-trends.md)
