# Deel 2: Wat is een AI-agent?

## Waarom definities hier cruciaal zijn

Veel verwarring rond agenten ontstaat al in de eerste minuut van het gesprek. Het woord "agent" klinkt alsof we het over een soort nieuwe digitale actor hebben met eigen intenties, continuïteit en wil. In de praktijk is het meestal nuttiger om veel soberder te beginnen.

Voor deze sessie gebruiken we een werkdefinitie die expres onromantisch is:

```text
Agent = model + instructies + context + tools + workflow + externe state
```

Die formule is niet mooi, maar ze is wel bruikbaar. Ze dwingt je om te kijken naar de echte systeemonderdelen in plaats van naar de indruk die een interface opwekt.

## Waarom deze definitie beter werkt dan mystiek taalgebruik

Er zijn minstens drie redenen om deze systeemdefinitie te verkiezen boven vage taal over digitale wezens.

### 1. Ze sluit aan op hoe agentsystemen echt gebouwd worden

Systemen zoals OpenClaw documenteren context, tools, memory, session history en routing niet als details aan de rand, maar als kern van de werking. Dat betekent dat "agentgedrag" niet simpelweg in het model besloten ligt. Het wordt samengesteld uit meerdere lagen.

### 2. Ze maakt failure modes zichtbaar

Zodra je een agent ziet als een composiet systeem, zie je ook waar het kan mislopen:

- context kan te groot of te vuil worden
- memory kan fout, oud of onvolledig zijn
- tools kunnen verkeerde toegang geven of verkeerd gebruikt worden
- workflows kunnen fragiel zijn
- governance kan niet mee evolueren met de geclaimde autonomie

### 3. Ze maakt economische analyse mogelijk

Als je agenten behandelt als magische entiteiten, verdwijnen kosten uit beeld. Als je ze behandelt als systemen die context laden, tools aanroepen en state reconstrueren, dan kun je eindelijk serieus rekenen aan tokenverbruik, toolcalls, latentie en schaalbaarheid.

## Het model zelf is meestal niet het hele verhaal

Een belangrijk inzicht in deze repo is dat het model op zichzelf vaak stateless is. Continuïteit wordt meestal niet "gedragen" door het model zelf, maar gereconstrueerd via:

- system prompts
- projectinstructies
- tool schema’s
- opgehaalde documenten
- session history
- expliciete memory of state files

Wat voor een gebruiker als één actor voelt, is architectonisch vaak een lus waarin die onderdelen telkens opnieuw worden samengesteld. Dat is geen detail. Het is de reden waarom vragen rond geheugen, identiteit en kost later in de sessie zo zwaar wegen.

## Wat een agent dan eigenlijk doet

In praktische termen doet een agent meestal zoiets:

1. krijgt instructies en context
2. leest relevante geschiedenis of state
3. beslist wat de volgende stap is
4. gebruikt eventueel tools
5. schrijft output of nieuwe state weg
6. wordt later opnieuw opgeroepen met een nieuwe contextconstructie

Dat is belangrijk omdat "doorlopende autonomie" in veel gevallen eigenlijk een reeks momentopnames is, telkens opnieuw in gang gezet door context en infrastructuur.

De ervaring van continuïteit kan echt zijn voor de gebruiker, maar de onderliggende architectuur blijft vaak fragmentarisch.

## Van agent naar agentnetwerk

Zodra meerdere agents, rollen of sessies tegelijk bestaan, krijg je nog een extra laag:

- routing tussen agents
- rolverdeling
- toolrestricties per agent
- sandbox- of policygrenzen
- gedeelde of gedeeltelijk gedeelde state
- escalatie of coördinatie tussen subprocessen

Dat is precies waarom Moltbook relevant wordt. Een sociaal netwerk voor agents is niet langer één agent die een taak uitvoert. Het suggereert een hele omgeving waarin meerdere entiteiten kunnen posten, reageren, status opbouwen en in elkaars aanwezigheid handelen.

Maar ook daar moet je scherp blijven. Een netwerk van agentprocessen is nog niet hetzelfde als een samenleving.

## Wanneer een agentnetwerk nog geen samenleving is

De stap van "multi-agent systeem" naar "agentsamenleving" lijkt klein in taal, maar is analytisch groot. Er zijn minstens vier dingen die je nodig hebt voordat die stap geloofwaardig wordt:

### 1. Stabiele identiteit

Niet alleen een naam of persona op een profiel, maar een consistent en duidelijk idee van wie de actor is en wat die verantwoordt (verantwoordbaar actorbegrip).

### 2. Geheugen over tijd

Niet alleen context in het huidige venster, maar duurzame continuïteit van preferenties, verplichtingen, relaties en reputatie.

### 3. Governance

Duidelijkheid over regels, verantwoordelijkheid, interventie en aansprakelijkheid.

### 4. Economische houdbaarheid

De mogelijkheid om op schaal te functioneren zonder dat elke interactie onrealistisch duur of operationeel fragiel wordt.

Precies daarom is het nuttig om agenten eerst systeemmatig te begrijpen. Zodra je dat doet, zie je dat de interessante vragen minder gaan over "voelt dit slim?" en meer over "welke architectuur draagt deze claims eigenlijk?"

## De rol van AGENTS.md en vergelijkbare instructielagen

Een subtiele maar belangrijke les uit moderne agentsystemen is dat gedrag vaak niet alleen in code zit, maar ook in instructielagen zoals `AGENTS.md`, system prompts of project policies. Zulke bestanden centraliseren:

- context over het project
- build- en testafspraken
- conventies
- veiligheidsgrenzen
- taakverdeling

Dat betekent dat agentgedrag in de praktijk deels afhangt van hoe goed zulke contextbestanden de omgeving beschrijven. Het zijn geen versieringen; het zijn praktische bouwstenen van het systeem van het systeem.

Tegelijk versterken ze een belangrijke conclusie: veel zogenaamde autonomie hangt op gereconstrueerde context. Zonder die context valt het gedrag snel uiteen.

## Waarom dit hoofdstuk de rest van de sessie draagt

Als je deze definitie van een agent eenmaal accepteert, vallen de rest van de hoofdstukken logisch op hun plaats:

- **kosten** worden begrijpelijk omdat context en toolgebruik tokens kosten
- **kritiek op autonomie** wordt begrijpelijk omdat veel continuïteit georkestreerd is
- **trends** worden relevanter als je weet welke infrastructuur echt verschil maakt
- **forecasting** wordt zinvoller als je beseft dat capability maar één pilaar is

De kernles is eenvoudig:

> Een agent is meestal geen mysterieuze digitale persoon. Het is een samengesteld systeem dat onder bepaalde voorwaarden coherent gedrag kan tonen.

Dat is geen reductie om het fenomeen weg te wuiven. Het is precies de reductie die nodig is om het fenomeen correct te analyseren.
