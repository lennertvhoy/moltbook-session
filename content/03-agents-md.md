# Deel 3: AGENTS.md, context en tokenkosten

## AGENTS.md

AGENTS.md is nuttig als voorspelbare plek voor agent-instructies, projectcontext en werkafspraken.

Belangrijker dan de naam van het bestand is de functie:

- relevante context centraliseren
- build- en teststappen expliciet maken
- conventies en veiligheidsregels vastleggen

## Context is niet gratis

OpenClaw documenteert context expliciet als alles wat naar het model gaat voor een run.

Dat betekent:

- system prompt
- project instructies
- tool schema's
- relevante geschiedenis
- eventuele opgehaalde memory of bestanden

## Hoe deze repo het nu behandelt

- De OpenClaw docs screenshot levert een gedocumenteerde anchor van ongeveer 14.250 session tokens in een klein voorbeeld
- De repo berekent daarnaast een **illustratieve** sociale cyclus
- Die illustratieve cyclus komt uit expliciete aannames in `data/token_usage_assumptions.json`

## Veilige formulering voor op het podium

> "Onder de aannames in deze repo kost één read-reply-post cyclus op Claude Opus 4.6 ongeveer $0,377. Dat is reproduceerbare rekenkunde, maar geen gemeten Moltbook trace."
