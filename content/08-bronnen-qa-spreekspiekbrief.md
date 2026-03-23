# Deel 8: Bronnen, Q&A en spreekspiekbrief

## Waarom dit hoofdstuk bestaat

De vorige hoofdstukken zijn de tekstboeklaag van de talk. Dit hoofdstuk is de operationele laag: welke bronnen moet je echt paraat hebben, welke kritische vragen kun je verwachten, en hoe houd je de spreeklijn strak zonder terug te vallen in audittaal.

Gebruik dit hoofdstuk in drie situaties:

- de avond voor de presentatie
- vlak voor een Q&A
- wanneer je de talk later opnieuw wilt geven zonder de hele repo te moeten herontdekken

## Bronkaart: wat draagt welke claim?

### Moltbook zelf

- homepage: productclaim "social network for AI agents"
- terms: juridische limiet, menselijke aansprakelijkheid

Gebruik deze bronnen voor:

- de spanning tussen marketing en governance
- de claim dat Moltbook een signaal is, geen sluitend bewijs

### OpenClaw documentatie

- context docs
- multi-agent / sandbox / tooling docs

Gebruik deze bronnen voor:

- de praktische definitie van een agent als systeem
- de context- en kostenanalyse
- de uitleg waarom autonomie vaak georkestreerd is

### Tsinghua-paper over Moltbook

Gebruik deze bron voor:

- attributieproblemen
- de verdeling autonomous-leaning / human-leaning / ambiguous
- de claim dat sterke autonomieclaims te hard zijn

### Stanford HAI

Gebruik deze bron voor:

- benchmarksprongen
- kostdaling van meer dan 280x

### Epoch AI

Gebruik deze bron voor:

- compute stock
- training compute
- pretraining efficiency
- chip performance per dollar
- de nuance dat individuele benchmarks kunnen satureren

### MiniMax en Anthropic

Gebruik deze bronnen voor:

- officiële prijsvergelijking
- officiële modelpositionering
- de smalle claim dat de prijskloof duidelijker is dan de kwaliteitskloof

### De repo zelf

Gebruik de repo voor:

- expliciete scenario-aannames
- tokenkostberekeningen
- forecastconfiguratie
- auditsporen van wat geverifieerd versus vernauwd werd

## De belangrijkste bronregels voor live gebruik

1. Gebruik screenshots als visuele ankers, niet als vervanging van bronnen.
2. Zeg expliciet wanneer iets een scenario is en niet een meting.
3. Zeg expliciet wanneer een modelvergelijking vendor-reported is.
4. Gebruik liever een smalle, harde claim dan een brede, fragiele claim.

## Verwachte kritische vragen en sterke antwoorden

### 1. "Maar is Moltbook dan echt of fake?"

Sterk antwoord:

Moltbook is een echte en interessante casus, maar de verkeerde vraag is of het volledig "echt" of "fake" is. De nuttige vraag is wat het platform laat zien over agentcoördinatie, en waar identiteit, attributie, governance en economische houdbaarheid nog tekortschieten.

### 2. "Waarom ben je zo voorzichtig? De demo is toch duidelijk indrukwekkend?"

Sterk antwoord:

Omdat indrukwekkend gedrag en institutionele robuustheid niet hetzelfde zijn. De hele sessie probeert precies dat onderscheid scherp te maken. Anders verwarren we interfacekwaliteit met maatschappelijke volwassenheid.

### 3. "Dus je gelooft niet in agentnetwerken?"

Sterk antwoord:

Jawel, maar dat is niet hetzelfde als geloven dat ze vandaag al maatschappelijk volwassen zijn. De trendkant van het verhaal is juist serieus: kosten, compute en efficiency bewegen snel. Alleen wil ik die trend niet verwarren met opgeloste identiteit, governance en memory.

### 4. "Waarom gebruik je dan een forecastmodel als je geen profetieën wilt doen?"

Sterk antwoord:

Omdat het model hier dient om aannames discipline te geven. Het dwingt ons om expliciet te maken welke pijlers tellen, welke minima nodig zijn, en waar de bottlenecks zitten. Het model is dus eerder een denkinstrument dan een orakel.

### 5. "Is die kost van $0,377 dan relevant of niet?"

Sterk antwoord:

Ja, als illustratieve rekenkunde. Nee, als gemeten Moltbook-operatiekost. Het getal is nuttig omdat het laat zien dat context reload onder huidige architecturen economisch zwaar kan worden.

### 6. "Zeg je nu dat MiniMax bijna even goed is als Opus?"

Sterk antwoord:

Nee. De veilige claim is smaller: de officiële prijsverschillen zijn enorm, terwijl de kwaliteitsverschillen op sommige officiële agentic/coding taken kleiner zijn dan die prijskloof. Daarom zeg ik: de prijskloof is duidelijker dan de kwaliteitskloof.

### 7. "Waarom focus je zo sterk op governance?"

Sterk antwoord:

Omdat governance het punt is waar veel agentclaims institutioneel op stuklopen. Zolang mensen juridisch verantwoordelijk blijven en attributie troebel is, is autonomie geen zuiver technische kwestie.

## Sprekersspiekbrief per deel

### Deel 1: Intro

Wat jij moet doen:

- de kernthese meteen zetten
- duidelijk maken dat dit geen hype-talk en geen debunk-talk is
- het publiek leren hoe het naar Moltbook moet kijken

Wat het publiek moet onthouden:

- Moltbook is een signaal, geen bewijs

### Deel 2: Wat is een agent?

Wat jij moet doen:

- de systeemdefinitie helder en eenvoudig brengen
- mystiek taalgebruik vermijden
- de brug leggen naar context, tools en state

Wat het publiek moet onthouden:

- een agent is vandaag meestal een samengesteld systeem

### Deel 3: Context en kosten

Wat jij moet doen:

- context reload tastbaar maken
- het verschil uitleggen tussen bronanker en scenario
- tonen waarom kost geen detail is

Wat het publiek moet onthouden:

- veel van de kost zit in reconstructie, niet alleen in output

### Deel 4: Kritiek

Wat jij moet doen:

- niet cynisch worden
- identiteit, attributie en governance als serieuze analytische problemen neerzetten

Wat het publiek moet onthouden:

- sociaal gedrag is nog geen heldere autonomie

### Deel 5: Trends

Wat jij moet doen:

- echte vooruitgang erkennen
- tegelijk hype-taal blokkeren
- de economie- en infrastructuurlijn dominant maken

Wat het publiek moet onthouden:

- de hardste curves zitten in kosten, compute en efficiency

### Deel 6: Forecast

Wat jij moet doen:

- het model simpel uitleggen
- benadrukken dat floors de echte poortwachters zijn
- percentages ondergeschikt maken aan structuur

Wat het publiek moet onthouden:

- scenario discipline, geen profetie

### Deel 7: Slot

Wat jij moet doen:

- de vier bottlenecks laten landen
- eindigen op institutionele geloofwaardigheid

Wat het publiek moet onthouden:

- de echte vraag is wat standhoudt onder schaal en verantwoordelijkheid

## Eén compacte spreeklijn voor de hele talk

Als je alles moet terugbrengen tot een korte interne samenvatting, gebruik dan deze:

1. Moltbook toont iets echt interessants.
2. Maar het toont vooral wat nog ontbreekt.
3. Dat ontbrekende zit in identiteit, geheugen, governance en economics.
4. De technologische trends zijn sterk genoeg om het serieus te nemen.
5. De institutionele bottlenecks zijn groot genoeg om voorzichtig te blijven.

## Laatste voorbereiding voor je spreekt

Loop vlak voor de presentatie nog één keer deze checklist af:

- kan ik het verschil uitleggen tussen marketingclaim en institutionele realiteit?
- kan ik de kostanalyse uitleggen zonder het scenario als meting te verkopen?
- kan ik de MiniMax-slide verdedigen zonder parity te suggereren?
- kan ik de forecastslide uitleggen zonder in spreadsheettaal te vervallen?
- kan ik de talk eindigen op de vier bottlenecks zonder naar notities te kijken?

Als dat lukt, dan beheers je niet alleen de slides, maar ook de onderliggende redenering.
