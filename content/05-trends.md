# Deel 5: Trends

## Waarom dit hoofdstuk zo voorzichtig moet zijn

Trendhoofdstukken zijn vaak waar presentaties ontsporen. Er zijn genoeg echte signalen van snelle vooruitgang in AI om een sterke talk te dragen. Maar er is ook een sterke verleiding om al die signalen in één richting te duwen: "alles is exponentieel, dus agent-samenlevingen komen vanzelf heel snel."

Deze repo probeert precies die fout te vermijden.

De juiste vraag is niet: "kunnen we een zo indrukwekkend mogelijke groeicurve tekenen?" De juiste vraag is: "welke trends zijn vandaag echt bronmatig en methodologisch stevig genoeg om in deze discussie te gebruiken?"

Het antwoord is: de hardste signalen zitten vooral in **economie, compute en efficiency**. Capability gaat ook vooruit, maar is moeilijker te lezen, vooral omdat benchmarks kunnen satureren of van samenstelling veranderen.

## 1. Wat Stanford HAI veilig laat zien

De Stanford HAI-bron die in deze repo gebruikt wordt, ondersteunt twee soorten claims die wél stevig genoeg zijn voor deze sessie.

### Benchmarksprongen

Er zijn duidelijke sprongen op moeilijke benchmarks, waaronder:

- MMMU
- GPQA
- SWE-bench

De Stanford HAI AI Index 2025 rapporteert dat binnen **één jaar** na introductie van deze benchmarks (2023→2024) frontier-modellen substantiële verbeteringen lieten zien:

- MMMU: **+18,8 punten**
- GPQA: **+48,9 punten**  
- SWE-bench: **+67,3 punten**

**Belangrijke caveat:** Deze cijfers vertegenwoordigen de verbetering van het beste beschikbare frontier-model op elk moment, niet één specifiek model. De sprongen komen door nieuwere modelgeneraties (GPT-4 → GPT-4V, Gemini 1.0 → 1.5, etc.) en verbeterde prompting-technieken. Het zijn geen vergelijkingen tussen twee specifieke modellen.

### Kostdaling

De tweede sterke claim is economischer en voor deze sessie eigenlijk nog belangrijker: Stanford HAI vat samen dat de kost om GPT-3.5-niveau te bereiken tussen **november 2022** en **oktober 2024** met meer dan **280x** gedaald is.

Dat soort kostdaling raakt direct aan de haalbaarheid van agentische systemen. Een samenleving van agents wordt niet alleen bepaald door wat modellen kunnen, maar ook door wat het kost om dat gedrag vaak en op schaal te laten draaien.

![Stanford HAI AI Index 2025](../assets/stanford_hai_ai_index_2025.png)

Deze screenshot gebruik je best als overzichtsanker, niet als losse bron om alle exacte cijfers uit af te lezen. De repo neemt er twee dingen uit mee die stevig genoeg zijn: benchmarksprongen en kostdaling.

## 2. Wat Epoch veilig laat zien

Epoch is in deze repo vooral nuttig als bron voor infrastructuur- en efficiencytrends.

De veilige signalen uit `data/ai_trends_metrics.json` zijn:

- compute stock groeit ongeveer **3,3x per jaar**
- frontier training compute groeit ongeveer **5x per jaar**
- pre-training efficiency verbetert ongeveer **3x per jaar**
- chip performance per dollar stijgt ongeveer **37% per jaar**

Dat is precies het soort trend dat je nodig hebt om een nuchtere maar krachtige these te bouwen:

> zelfs als capabilitymetingen soms lastig te interpreteren zijn, verbeteren de onderliggende economische en infrastructurele voorwaarden nog steeds hard.

Voor agentnetwerken is dat cruciaal. Lagere kosten, betere chips en efficiëntere training veranderen rechtstreeks wat economisch mogelijk wordt.

![Epoch ECI](../assets/epoch_ai_eci.png)

De ECI-screenshot is nuttig omdat ze laat zien waarom composietmetrics bestaan: individuele benchmarks raken na verloop van tijd verzadigd. Maar ze is ook precies waarom we voorzichtig blijven. De pagina geeft intern al variatie in benchmarktelling, dus de goede houding is methodologisch respect zonder overdreven exactheid.

## 3. Waarom we geen "alles is exponentieel"-taal meer gebruiken

Een eerdere zwakte van dit project was dat trendmateriaal te makkelijk in een algemene exponentiële story terechtkwam. Dat is nu bewust teruggesneden.

Daar zijn goede redenen voor.

### Benchmarks kunnen satureren

Een benchmark meet vaak een taak of taakcluster binnen een bepaald bereik. Als modellen dat bereik steeds beter beheersen, dan kan de benchmark zijn onderscheidend vermogen verliezen. De curve zegt dan minder over "algemene intelligentie" dan mensen graag denken.

### Samengestelde indices vragen voorzichtigheid

Epoch’s ECI is juist interessant omdat de organisatie zelf erkent dat individuele benchmarks kunnen satureren. Daarom probeert ECI bredere capability-beweging te vatten via een composiet. Maar ook daar moet je voorzichtig blijven in de formulering.

### Broninconsistentie bestaat

De ECI-pagina noemt in de overview **37 benchmarks**, maar in de datasection **42 benchmarks**. Dat is geen ramp, maar wel een signaal dat je niet moet doen alsof één exact benchmarkaantal een heilig feit is wanneer de bron zelf varieert.

Vandaar de bewust smallere formulering in deze repo:

- liever **"dozens of benchmarks"**
- liever **"sterke capability-signalen"**
- niet: **"hier is een perfecte, eenduidige exponentiële capabilitycurve"**

## 4. Wat de deck wél durft concluderen

De kernzin van de trendslide is daarom bewust smal:

> De hardste verdedigbare curve zit vandaag in kosten, compute en efficiency. Capability gaat ook vooruit, maar bounded benchmarks satureren en moeten voorzichtig gelezen worden.

Die zin is sterk omdat ze twee dingen tegelijk doet:

- ze erkent echte vooruitgang
- ze verhindert overselling

Voor een live talk is dat een betere positie dan sensationele claims die bij de eerste kritische vraag uit elkaar vallen.

## De samengestelde trendgrafiek volledig gelezen

![AI trends](../assets/ai_trends.png)

De grafiek in [`../assets/ai_trends.png`](../assets/ai_trends.png) vat de hele trendredenering van de repo samen. Ze heeft drie panelen.

### Paneel 1: benchmarksprongen

Links staan drie puntverbeteringen uit de Stanford HAI-samenvatting (periode **2023→2024**):

- MMMU: **+18,8** percentagepunten
- GPQA: **+48,9** percentagepunten
- SWE-bench: **+67,3** percentagepunten

**Wat dit wel zegt:** Frontier AI-systemen maakten binnen één jaar na introductie van deze benchmarks grote sprongen, door betere modellen en prompting-technieken.

**Wat dit niet zegt:** Het zijn geen vergelijkingen tussen twee specifieke modellen. Het toont de progressie van het beste beschikbare resultaat op elk moment. Het beweert ook niet dat capability als geheel in één nette exponentiële curve past.

### Paneel 2: kostdaling

In het midden staat een **genormaliseerde** kostcurve. Dat is belangrijk: de repo heeft hier niet een volledige ruwe tijdreeks gedigitaliseerd. Ze heeft een logische lijn geconstrueerd tussen twee bronpunten:

- startpunt: een relatieve kostindex van **280**
- eindpunt: een relatieve kostindex van **1**

Daaruit bouwt `analyses/ai_trends.py` met een geometrische interpolatie een visuele curve over de maanden tussen **2022-11** en **2024-10**.

De reden hiervoor is methodologisch: de repo wil de richting en schaalorde van de kostdaling tonen zonder te doen alsof er een volledig originele tussenliggende dataset is.

### Paneel 3: compute en efficiency

Rechts staan de jaarfactoren uit Epoch’s trend snapshot:

- global compute stock: **3,3x/jaar**
- training compute: **5,0x/jaar**
- pretraining efficiency: **3,0x/jaar**
- chip performance per dollar: **1,37x/jaar**

Dit is het sterkste infrastructuurpaneel in de hele deck. Het ondersteunt de these dat economie en infrastructuur de hardste verdedigbare curves zijn.

## 5. MiniMax M2.7 versus Claude Opus 4.6

Dit is het meest gevoelige deel van het trendhoofdstuk, en terecht. Modelvergelijkingen zien er op slides vaak scherper uit dan ze analytisch zijn.

De situatie in deze repo is nu als volgt.

### Wat nu wél veilig is

MiniMax documenteert **M2.7** publiek op de eigen modelsite en in de eigen API-pricingdocs. Dat maakt het model voldoende reëel en actueel om te bespreken.

De officiële list prices zijn:

- **MiniMax M2.7**: $0,30 input / $1,20 output per 1M tokens
- **MiniMax M2.7 highspeed**: $0,60 input / $2,40 output per 1M tokens
- **Claude Opus 4.6**: $5 input / $25 output per 1M tokens

Dat prijsverschil is helder en hard. Het is niet subtiel.

De officiële vendorpagina’s geven ook benchmarkclaims die het mogelijk maken om te zeggen dat M2.7 op sommige agentic/coding taken competitief is. MiniMax noemt onder meer:

- **56,22%** op SWE-Pro
- **57,0%** op Terminal Bench 2
- **55,6%** op VIBE-Pro
- **1495** GDPval-AA Elo
- **97%** skill adherence

Anthropic positioneert Opus 4.6 als premium frontier-model en noemt onder meer:

- **65,4%** op Terminal-Bench 2.0
- **72,7%** op OSWorld

De veilige samenvatting daarvan is:

> De prijskloof is duidelijker dan de kwaliteitskloof.

## De MiniMax-analyse volledig uitgelegd

De vergelijking in deze repo is bewust smal. Ze vertrekt van officiële vendorpagina’s, niet van een perfect neutrale benchmarksheet.

### Officiële prijsdata

- MiniMax M2.7: **$0,30 input / $1,20 output**
- MiniMax M2.7 highspeed: **$0,60 input / $2,40 output**
- Claude Opus 4.6: **$5 input / $25 output**

Daaruit volgt:

- input is ongeveer **16,7x** goedkoper bij MiniMax M2.7 dan bij Opus 4.6
- output is ongeveer **20,8x** goedkoper

Dat deel van de vergelijking is relatief hard.

### Officiële kwaliteitsdata

De meest rechtstreeks vergelijkbare officiële taak in de repo is Terminal Bench:

- MiniMax M2.7: **57,0%**
- Claude Opus 4.6: **65,4%**

Daarbovenop rapporteert MiniMax ook:

- SWE-Pro: **56,22%**
- VIBE-Pro: **55,6%**
- GDPval-AA Elo: **1495**
- skill adherence: **97%**

Anthropic rapporteert daarnaast voor Opus 4.6:

- OSWorld: **72,7%**
- context window: **1M tokens in beta**

### Waarom dit nog steeds geen parity-slide is

Er zijn drie redenen waarom deze repo parity vermijdt:

1. de cijfers komen uit vendor-eigen publicaties
2. niet alle taken zijn één-op-één gematcht
3. MiniMax’s eigen MMClaw-noot verwijst naar **Sonnet 4.6**, niet Opus 4.6

De goede conclusielijn is dus:

- MiniMax M2.7 is economisch uitzonderlijk agressief geprijsd
- de prestaties zijn serieus genoeg om relevant te zijn
- de vergelijking rechtvaardigt **competitief op sommige taken**, niet **gelijkwaardig overall**

### Wat we expliciet niet zeggen

We zeggen niet:

- dat MiniMax "in wezen gelijk" is aan Opus 4.6
- dat vendorcijfers samen al een neutrale matched eval vormen
- dat MiniMax’s MMClaw-verwijzing een vergelijking met Opus 4.6 bewijst

Die laatste nuance is belangrijk. MiniMax zegt op de eigen pagina dat M2.7 op MMClaw "approaching the latest **Sonnet 4.6**" zit, niet Opus 4.6.

### Waarom deze nuancering juist sterk is

Een zwakke deck probeert parity te suggereren en verliest geloofwaardigheid. Een sterke deck laat zien dat:

- prijsverschillen hard te documenteren zijn
- kwaliteitsvergelijkingen lastiger zijn
- je toch al iets relevants kunt leren uit de combinatie

Het relevante punt voor de talk is dus niet dat MiniMax Opus zou evenaren. Het relevante punt is dat de markt steeds vaker modellen produceert waarvan de economische positie veel scherper verschilt dan de kwaliteitspositie.

Dat is strategisch belangrijk voor iedereen die agentische workflows wil bouwen.

## 6. Wat je na dit hoofdstuk moet onthouden

Als je één mentale samenvatting wilt, gebruik dan deze:

### Hardste signalen

- kosten dalen sterk
- compute groeit sterk
- efficiency verbetert sterk

### Reële maar moeilijkere signalen

- capability gaat vooruit
- benchmarkinterpretatie vraagt meer voorzichtigheid

### Verleidelijke maar te harde claims

- "alles is exponentieel"
- "één benchmark vertelt het hele verhaal"
- "MiniMax is gewoon Opus aan dumpprijzen"

De sterke versie van dit hoofdstuk is dus niet hype en ook niet defaitisme. Ze is:

> de onderliggende economie en infrastructuur bewegen snel genoeg om agentnetwerken serieus te nemen, maar capabilityverhalen vragen nog steeds methodologische discipline.
