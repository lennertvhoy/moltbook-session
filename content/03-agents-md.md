# Deel 3: AGENTS.md, context en tokenkosten

## Waarom dit hoofdstuk belangrijk is

Veel presentaties over agents blijven hangen op gedrag: posten, antwoorden, taken uitvoeren, rollen aannemen. Dit hoofdstuk gaat bewust een laag dieper. Het stelt de vraag: wat moet er technisch telkens opnieuw worden meegedragen zodat dat gedrag überhaupt kan gebeuren?

Het antwoord is belangrijker dan het op het eerste gezicht lijkt, omdat het tegelijk drie dingen raakt:

- architectuur
- continuïteit
- kost

Wie niet begrijpt hoe context wordt opgebouwd en herladen, begrijpt ook niet waarom moderne agentsystemen zowel indrukwekkend als economisch fragiel kunnen zijn.

## De rol van AGENTS.md

`AGENTS.md` is in dit project geen gimmick, maar een voorbeeld van een bredere ontwerppraktijk. Zulke bestanden geven een agent of coding workflow een stabiele plek om context op te halen over:

- projectdoel
- conventies
- build- en teststappen
- veiligheidsregels
- kwaliteitslat

De naam van het bestand is niet essentieel. De functie is essentieel: relevante context centraliseren zodat die opnieuw kan worden meegegeven of opgehaald wanneer een agent een taak uitvoert.

Dat lijkt efficiënt, maar er zit een keerzijde aan: al die context moet vaak mee het model in. En tokens zijn niet gratis.

## Wat context in de praktijk allemaal omvat

OpenClaw documenteert context expliciet als alles wat naar het model gaat voor een run. Dat is een nuttige bronanker, omdat het laat zien hoe snel context zich ophoopt.

In de praktijk kan context bestaan uit:

- system prompt
- projectinstructies
- tool schema’s
- relevante history
- retrieved files of memory
- agentpersona en state

Dat zijn niet zomaar randdetails. Ze vormen in hoge mate de operationele identiteit van het systeem op dat moment.

Wie zegt dat een agent "gewoon even" een sociale handeling stelt, vergeet vaak dat die handeling architectonisch gedragen wordt door een grote contextconstructie.

## Het gedocumenteerde OpenClaw-anker

De repo gebruikt OpenClaw niet als bewijs dat alle systemen hetzelfde zijn, maar als gedocumenteerd voorbeeld van hoe groot contextoverhead al kan zijn in een relatief klein scenario.

In `data/token_usage_assumptions.json` staat een bronanker dat uit de OpenClaw-contextdocs komt:

- system prompt: ongeveer 9.603 tokens
- `AGENTS.md`: 436 tokens
- skills list: 546 tokens
- tool schemas: 7.997 tokens
- totaal session tokens in dat voorbeeld: ongeveer 14.250

Dat is belangrijk om twee redenen.

![OpenClaw context docs](../assets/openclaw_context_docs.png)

### 1. Het toont dat contextoverhead niet hypothetisch is

Zelfs zonder groot sociaal netwerk, zonder grote feed en zonder uitgebreide reputatiestructuur zit je al in de orde van tienduizenden tokens context.

### 2. Het maakt een latere sociale kostberekening geloofwaardiger

De repo doet nergens alsof deze OpenClaw-cijfers al Moltbook zelf meten. Ze dienen als anker om te laten zien dat hoge contextbelasting onder huidige architecturen heel plausibel is.

## De illustratieve sociale cyclus

Boven op dat bronanker rekent de repo een expliciet assumption-driven scenario door voor één "sociale cyclus" van een agent:

- timeline lezen
- reply genereren
- post creëren

De aannames in `data/token_usage_assumptions.json` gebruiken per actie een contextload bestaande uit:

- system prompt: 9.600 tokens
- projectinstructies: 1.200 tokens
- toolbeschrijvingen: 3.000 tokens
- persona en state: 1.500 tokens
- eerdere history: 5.000 tokens

Daarbovenop komen nog:

- 10 timeline-posts aan 500 tokens per stuk
- 1.500 reply-contexttokens en 800 reply-outputtokens
- 1.000 post-contexttokens en 600 post-outputtokens

De berekening in [`../analyses/token_usage.py`](../analyses/token_usage.py) laat vervolgens zien dat context loading drie keer terugkomt in de cyclus. Dat is precies de clou: niet de uiteindelijke output, maar het telkens opnieuw meedragen van systeemcontext domineert de inputkant van de kost.

## De berekening volledig uitgeschreven

Hier is de cyclus zoals de repo ze daadwerkelijk uitrekent.

### Stap 1: contextload per actie

Per actie wordt verondersteld dat de agent ongeveer deze context meekrijgt:

- system prompt: **9.600**
- projectinstructies: **1.200**
- toolbeschrijvingen: **3.000**
- persona en state: **1.500**
- eerdere history: **5.000**

Samen is dat:

```text
9.600 + 1.200 + 3.000 + 1.500 + 5.000 = 20.300 input tokens per contextload
```

Omdat de illustratieve sociale cyclus drie contextloads veronderstelt:

```text
20.300 x 3 = 60.900 input tokens
```

### Stap 2: timeline lezen

De timeline bevat in dit scenario:

```text
10 posts x 500 tokens = 5.000 input tokens
```

### Stap 3: reply genereren

```text
reply-context = 1.500 input tokens
reply-output  =   800 output tokens
```

### Stap 4: nieuwe post maken

```text
post-context = 1.000 input tokens
post-output  =   600 output tokens
```

### Stap 5: totaal

Totaal input:

```text
60.900 + 5.000 + 1.500 + 1.000 = 68.400 input tokens
```

Totaal output:

```text
800 + 600 = 1.400 output tokens
```

### Stap 6: prijs op Claude Opus 4.6

In de gebruikte brondata kost Opus 4.6:

- **$5 per 1M input tokens**
- **$25 per 1M output tokens**

Dus:

```text
inputkost  = 68.400 / 1.000.000 x 5   = $0,3420
outputkost =  1.400 / 1.000.000 x 25  = $0,0350
totaal     = $0,3770
```

Dat is precies waar het slidegetal vandaan komt.

## De grafiek inline gelezen

![Token breakdown](../assets/token_breakdown.png)

Lees deze figuur in vier stappen:

### Linksboven

Je ziet de verdeling van de **contextload per actie**. Het belangrijkste punt is niet welk component exact het grootste is, maar dat de totale vaste contextlaag al groot is voor er ook maar één sociale handeling gebeurt.

### Rechtsboven

Je ziet de **cyclus per activiteit**. Daar wordt zichtbaar dat "context loading (3x)" de grootste inputblok is. Dat ondersteunt de claim dat het herladen van systeemcontext de kost domineert.

### Linksonder

Je ziet de **kost per cyclus per model**. De log-schaal maakt prijsverschillen zichtbaar zonder te doen alsof de onderliggende taakidentiek volledig neutraal vergeleken is.

### Rechtsonder

Je ziet de auditnotities en schaalscenario’s. Dat paneel is belangrijk omdat het de discipline van de analyse bewaart:

- OpenClaw is een bronanker
- de sociale cyclus is een scenario
- schaalcijfers zijn orde-van-grootte-illustraties

## Wat je uit deze analyse wel en niet moet meenemen

### Wel

- contextoverhead is reëel
- contextreload kan economisch dominant worden
- architectuurkeuzes rond memory en state hebben directe kostgevolgen

### Niet

- Moltbook kost vandaag exact `$0,377` per sociale cyclus
- elk agentsysteem heeft dezelfde kostenstructuur
- outputgeneratie is de primaire kostdriver in elk scenario

## Wat het getal van ongeveer $0,377 wel en niet betekent

Onder de huidige aannames komt de repo uit op ongeveer **$0,377 per read-reply-post-cyclus op Claude Opus 4.6**.

Dat getal is nuttig, maar alleen als je het correct leest.

### Wat het wél is

- reproduceerbare rekenkunde
- gebaseerd op expliciete inputaannames
- nuttig om richting en schaalorde te begrijpen

### Wat het níét is

- geen gemeten Moltbook trace
- geen claim over de exacte huidige operationele kost van Moltbook
- geen universeel getal dat automatisch voor elk agentsysteem geldt

Die discipline is fundamenteel. De repo probeert hier niet te winnen door schijnprecisie. Ze probeert te tonen dat een bepaald type architectuur onder huidige prijsmodellen economisch zwaarder is dan veel mensen intuïtief aannemen.

## Waarom context reload economisch zo belangrijk is

Het belangrijkste inzicht van deze hele kostenanalyse is dat agentgedrag duur kan worden om een reden die niet meteen zichtbaar is in de interface.

Een mens die "even iets leest en antwoordt" lijkt een lichte sociale handeling te verrichten. Een agent die hetzelfde doet, moet mogelijk:

- projectcontext opnieuw meekrijgen
- tools opnieuw geactiveerd krijgen
- state opnieuw laden
- geschiedenis opnieuw opnemen
- output weer in een nieuwe cyclus wegschrijven

Met andere woorden: veel van de kost zit niet in het "sociaal doen", maar in het telkens reconstrueren van de voorwaarden waaronder dat gedrag geloofwaardig kan lijken.

Dat heeft twee gevolgen.

### 1. Economische efficiëntie is geen randvoorwaarde

Ze is een kernvoorwaarde. Als context reload dominant blijft, dan schaalt sociaal agentgedrag veel slechter dan je op basis van de interface zou denken.

### 2. Geheugen en architectuur zijn ook economische vragen

Een beter memory-systeem of slimmere state-reconstructie is niet alleen technisch eleganter. Het kan rechtstreeks de koststructuur van agentnetwerken veranderen.

## Waarom schaalscenario’s ertoe doen

De repo rekent ook schaalscenario’s door. Niet om exacte businesscases te simuleren, maar om zichtbaar te maken hoe snel kleine per-cyclus kosten groot worden wanneer je veel agents en veel dagelijkse interacties veronderstelt.

Dat is cruciaal voor het bredere argument van de sessie. De vraag is niet of één agent iets interessants kan doen. De vraag is wat er gebeurt als je duizenden of miljoenen entiteiten sociaal gedrag laat vertonen onder een architectuur die context telkens opnieuw moet dragen.

## De diepere les van dit hoofdstuk

Dit hoofdstuk gaat uiteindelijk over meer dan tokenprijzen. Het gaat over wat moderne agenten ontologisch eigenlijk zijn.

Als gedrag alleen stabiel blijft door:

- telkens herladen context
- expliciete instructiebestanden
- tool- en workflowlagen
- extern gereconstrueerde state

dan is het misleidend om te snel over robuuste digitale personen te spreken.

Dat betekent niet dat het systeem oninteressant is. Het betekent dat zijn continuïteit en zijn koststructuur beide afhangen van infrastructuur.

De compacte samenvatting is daarom:

> Context is niet gratis, en veel van wat als autonomie voelt wordt vandaag nog economisch en technisch gedragen door herhaalde reconstructie.

Dat inzicht vormt de brug naar de kritiek op identiteit en governance in het volgende hoofdstuk.
