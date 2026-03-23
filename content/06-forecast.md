# Deel 6: Forecast model

## Waarom er überhaupt een forecast in zit

Na alle kritiek op hype en overclaims kan een forecast-sectie tegenintuïtief lijken. Als de sessie juist voorzichtig wil zijn, waarom dan een model bouwen dat over 2030, 2035 of 2040 praat?

Het antwoord is dat een goed forecast-model hier niet dient om de toekomst vast te leggen, maar om aannames te disciplineren.

Zonder model blijven veel discussies vaag:

- "capability gaat snel"
- "governance loopt achter"
- "economics verbeteren nog wel"

Met een model word je gedwongen om te zeggen:

- welke factoren tellen mee
- hoe zwaar ze wegen
- welke minima je noodzakelijk vindt
- wat een doorbraak eigenlijk betekent
- hoe schokken en onzekerheid meegenomen worden

In deze repo is het forecastmodel dus bewust geen profetie, maar een gestructureerde manier om onenigheid zichtbaar te maken.

## Wat het model precies is

Het model in [`../analyses/forecast_model.py`](../analyses/forecast_model.py) is een **Monte Carlo barrier-crossing model**. Dat klinkt technischer dan het is.

Concreet doet het drie dingen:

1. het simuleert de ontwikkeling van zeven pijlers tussen 2026 en 2040
2. het combineert die pijlers tot een readiness index
3. het checkt of een scenario een drempel haalt én tegelijk aan minimale voorwaarden voldoet

De output is dus niet "de waarheid over de toekomst", maar een kansverdeling onder expliciete aannames.

## De formele logica van het model

Onder de motorkap gebeurt het volgende:

1. voor elke pijler wordt een startwaarde in 2026 gekozen
2. elk jaar krijgt die pijler een lognormale groeistap
3. er is ook een kans op een negatieve schok
4. alle pijlers worden begrensd tussen 0 en 100
5. de readiness index wordt berekend als een **gewogen geometrisch gemiddelde**
6. crossing gebeurt pas wanneer threshold én floors gehaald worden gedurende twee opeenvolgende jaren

Dat gewogen geometrische gemiddelde is belangrijk. Het betekent dat lage pijlers relatief zwaarder doorwegen dan in een gewone som. Dat past inhoudelijk bij deze use case: één fundamentele zwakte mag niet te makkelijk overschreeuwd worden door één heel sterke pijler.

## De zeven pijlers

Het model gebruikt zeven pijlers die samen de readiness van een echte agentsamenleving moeten benaderen:

- **C**apability
- **E**fficiency
- **M**emory
- **R**eliability
- **N**etwork
- **G**overnance
- **D**emand

Hun gewichten staan expliciet in `data/forecast_scenarios.json`:

- Capability: **20%**
- Efficiency: **20%**
- Memory: **15%**
- Reliability: **15%**
- Network: **12%**
- Governance: **10%**
- Demand: **8%**

Dat is al een inhoudelijke stellingname. Ze zegt dat capability belangrijk is, maar niet dominant genoeg om de rest te overrulen. Dat past bij de centrale these van de repo: een samenleving van agents hangt niet alleen af van slimmer worden, maar ook van infrastructuur, coördinatie, geheugen en bestuurbaarheid.

## Thresholds, floors en opeenvolgende jaren

Het model verklaart een scenario niet "klaar" zodra één gemiddelde score toevallig hoog uitvalt. Er zijn drie voorwaarden:

### 1. Een readiness threshold

De samengestelde index moet minstens **75** halen.

### 2. Floors op vier cruciale pijlers

Memory, Reliability, Network en Governance moeten elk minstens **60** halen.

### 3. Twee opeenvolgende jaren

De voorwaarden moeten **twee opeenvolgende jaren** gelden, zodat het model geen eenmalige lucky spike als echte doorbraak interpreteert.

Dat is een sterke ontwerpkeuze. Ze verhindert dat het model zichzelf trakteert op valse precisie.

## Waarom de floors inhoudelijk zo belangrijk zijn

De floors zijn in feite het morele en institutionele hart van het model.

Ze zeggen: zelfs als capability en efficiency indrukwekkend stijgen, noem je het nog geen echte readiness wanneer:

- geheugen te zwak blijft
- betrouwbaarheid te grillig blijft
- netwerkcoördinatie te fragiel blijft
- governance achterblijft

Dat past perfect bij de rest van de talk. De bottlenecks die in de kritiekhoofdstukken centraal staan, worden hier niet alleen retorisch genoemd maar ook structureel ingebouwd.

## De drie scenario’s

Het model rekent met drie scenariofamilies:

### Conservative

- lagere groei
- hogere volatiliteit
- zwaardere negatieve schokken

### Base case

- gematigde groei
- gematigde volatiliteit
- plausibele maar niet extreme negatieve schokken

### Accelerated

- hogere groei
- lagere volatiliteit
- mildere negatieve schokken

Belangrijk is dat deze scenario’s geen geobserveerde waarheid coderen. Ze coderen verschillende veronderstellingen over hoe snel de zeven pijlers vooruitgaan en hoe kwetsbaar ze zijn voor terugslag.

## De scenario-inputs concreet gemaakt

De JSON in [`../data/forecast_scenarios.json`](../data/forecast_scenarios.json) maakt de aannames volledig auditbaar. Voor de base case zijn de startpunten in 2026:

- Capability: **55**
- Efficiency: **45**
- Memory: **30**
- Reliability: **28**
- Network: **20**
- Governance: **25**
- Demand: **50**

En de gemiddelde jaarlijkse groeiverwachtingen (`growth_mu`) zijn:

- Capability: **0,18**
- Efficiency: **0,28**
- Memory: **0,14**
- Reliability: **0,16**
- Network: **0,15**
- Governance: **0,08**
- Demand: **0,12**

De base case zegt dus impliciet:

- capability en efficiency bewegen relatief snel
- memory en reliability verbeteren, maar trager
- governance blijft de traagste structurele pijler
- networkcoördinatie begint zwak en blijft onzeker

## Wat het model nu laat zien

De verificatiedocs in deze repo vatten de huidige base-case output als volgt samen:

- kans om tegen **2040** de voorwaarden te halen: ongeveer **28,1%**
- mediane crossing year in de base case: **2038**

Dat zijn bruikbare uitkomsten, maar alleen zolang je ze correct leest.

De juiste lezing is niet:

- "de doorbraak komt in 2038"

De juiste lezing is:

- "onder deze aannames ontstaat een niet-dominante maar reële kans tegen 2040, en die uitkomst wordt vooral beperkt door de moeilijkste floors"

## De forecastgrafiek inline gelezen

![Forecast distribution](../assets/forecast_distribution.png)

Deze figuur heeft vier panelen en elk paneel doet ander werk.

### Linksboven: readiness trajectories

Hier zie je per scenario de mediane indexontwikkeling, met bandbreedte tussen het 25e en 75e percentiel. Dit paneel is nuttig om het verschil in structureel tempo tussen `Conservative`, `Base case` en `Accelerated` te zien.

### Rechtsboven: kans op crossing per jaar

Hier wordt zichtbaar hoe de cumulatieve kans oploopt dat een scenario tegen een bepaald jaar alle voorwaarden haalt. Dit is vaak het meest intuïtieve paneel voor een publiek, maar ook het paneel dat het makkelijkst verkeerd gelezen wordt als voorspelling.

### Linksonder: crossing-year distribution

Deze boxplots tonen enkel de runs die effectief een crossing halen. Daardoor zie je meteen hoe breed de spreiding blijft, zelfs binnen geslaagde scenario’s.

### Rechtsonder: audit notes

Dit paneel is eigenlijk het methodologische geweten van de figuur. Het vermeldt:

- mediane crossing year
- 90%-interval onder crossings
- threshold sensitivity
- floor sensitivity
- de interpretatieregel dat assumption error belangrijker is dan sampling noise

Dat paneel maakt expliciet dat de grafiek niet bedoeld is als kristallen bol.

## Waarom assumption error belangrijker is dan simulation error

Monte Carlo-modellen kunnen heel precies lijken omdat ze duizenden runs genereren en nette grafieken opleveren. Maar in dit type model is **assumption error** belangrijker dan **simulation error**.

Met andere woorden:

- extra simulaties maken je output statistisch gladder
- betere aannames maken je output inhoudelijk betekenisvoller

Deze repo benoemt dat expliciet, en terecht. Het gevaar van forecastslides is niet dat de random seed onstabiel is. Het gevaar is dat men vergeet hoe normatief de inputkeuzes zelf zijn.

## De belangrijkste uitkomst: floors binden eerder dan thresholds

De sterkste les uit de huidige parameterisatie is niet het mediane jaar, maar de gevoeligheidsanalyse.

De repo test:

- thresholds van **70**, **75** en **80**
- floors van **55**, **60** en **65**

De conclusie is dat de uitkomst weinig verschuift wanneer je alleen de headline threshold aanpast, maar merkbaar verschuift wanneer je de floors aanscherpt of verlaagt.

Dat is een waardevol inzicht, omdat het precies laat zien waar de werkelijke bottlenecks zitten. Het gaat minder om "hoe optimistisch ben je over capability in het algemeen?" en meer om "denk je dat memory, reliability, network en governance tegelijk voldoende robuust worden?"

Dat is ook waarom de presentatie de forecastslide nu framed als:

> scenario discipline, geen profetie

## Waarom het resultaat inhoudelijk interessant is

Het mooiste aan deze analyse is niet dat ze een jaar produceert, maar dat ze laat zien waar optimisme stukloopt.

Je zou intuïtief kunnen denken dat de hele discussie vooral draait om de headline threshold van 75. Maar de simulatie suggereert iets anders:

- capability kan stijgen
- efficiency kan stijgen
- demand kan aanwezig blijven

en toch loopt het systeem vast zolang memory, reliability, network en governance niet tegelijk voldoende sterk worden.

Dat maakt de forecast onverwacht consistent met de rest van de repo. Ze eindigt niet in "meer modelkracht lost alles op", maar in "de bottlenecks blijven institutioneel en architectonisch."

## Hoe je deze slide op het podium moet lezen

De beste manier om dit hoofdstuk mondeling over te brengen is niet door percentages op te dreunen. Het publiek hoeft geen modeloperator te worden. Het publiek moet vooral onthouden:

- het model maakt aannames expliciet
- capability alleen is niet genoeg
- floors zijn de echte poortwachters
- governance en memory zijn geen bijzaak

De cijfers zijn ondersteunend. De hoofdboodschap is structureel.

## Wat dit model dus wél toevoegt

Een goed gelezen forecastmodel helpt om het gesprek te disciplineren:

- het dwingt tot definities
- het maakt bottlenecks expliciet
- het maakt scenario’s vergelijkbaar
- het toont waar gevoeligheid echt zit

Het helpt níét om de toekomst te fixeren.

## Wat je na dit hoofdstuk moet onthouden

De compacte samenvatting van dit hoofdstuk is:

> De juiste les van het model is niet wanneer agent-samenlevingen "aankomen", maar welke barrières eerst weg moeten voordat zo’n claim überhaupt geloofwaardig wordt.

Of nog scherper:

> Floors op memory, reliability, network en governance zijn in deze repo belangrijker dan de headline threshold zelf.

Dat maakt de forecast geen kristallen bol, maar een bruikbaar verlengstuk van de rest van de sessie.
