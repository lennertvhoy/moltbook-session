# Deel 2: Wat is een AI agent?

## Praktische definitie

Een bruikbare werkdefinitie voor deze sessie:

```text
Agent = model + instructies + context + tools + workflow + externe state
```

## Waarom deze definitie beter werkt

- Ze is systeemgericht in plaats van mystiek
- Ze sluit aan bij hoe tools als OpenClaw in de praktijk zijn opgebouwd
- Ze maakt zichtbaar waar de kosten en failure modes zitten

## Belangrijke nuance

- Het model zelf is doorgaans stateless by default
- Continuiteit wordt gereconstrueerd via context, state files, retrieval en workflow
- Wat als "autonomie" voelt, is vaak een georkestreerde loop

## Voor agent netwerken

Zodra meerdere agents, sessies of rollen naast elkaar bestaan met routing, policies en tool-restricties, krijg je een agent netwerk.

Dat is technisch relevant, maar nog geen bewijs van stabiele sociale emergentie.
