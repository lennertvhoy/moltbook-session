# Moltbook Session: Tekstboekversie

Deze map is de uitgebreide leerlaag van het project. De slides in [`slides/slides-main.md`](../slides/slides-main.md) zijn bewust kort en podiumgericht; de hoofdstukken hieronder leggen de argumenten, aannames, analyses en caveats volledig uit.

Gebruik deze map als je:

- de presentatie inhoudelijk wilt beheersen in plaats van alleen onthouden
- wilt begrijpen welke claims hard geverifieerd zijn en welke assumption-driven zijn
- de analyses, grafieken en methodologische keuzes wilt kunnen uitleggen
- de kernthese van de talk wilt kunnen verdedigen in gesprek of Q&A

## Hoe je dit best leest

### Snelle route

1. [`01-intro.md`](01-intro.md)
2. [`04-kritiek.md`](04-kritiek.md)
3. [`05-trends.md`](05-trends.md)
4. [`06-forecast.md`](06-forecast.md)
5. [`07-slot.md`](07-slot.md)

### Volledige route

1. [`01-intro.md`](01-intro.md)  
   Wat Moltbook is, waarom het interessant is, en wat de centrale these van de sessie is.
2. [`02-ai-agents.md`](02-ai-agents.md)  
   Een praktische definitie van AI-agents en waarom "agent" meestal een systeemterm is, geen mystieke categorie.
3. [`03-agents-md.md`](03-agents-md.md)  
   Hoe context, tools, state en tokenkosten samenhangen, en waarom context reload economisch zo belangrijk is.
4. [`04-kritiek.md`](04-kritiek.md)  
   Waarom Moltbook nog geen overtuigend autonoom sociaal netwerk is: identiteit, attributie, governance en aansprakelijkheid.
5. [`05-trends.md`](05-trends.md)  
   Welke technologische en economische trends vandaag echt verdedigbaar zijn, en welke taal te hard wordt.
6. [`06-forecast.md`](06-forecast.md)  
   Hoe het Monte Carlo-model werkt, wat het wel en niet zegt, en waarom floors belangrijker blijken dan headline thresholds.
7. [`07-slot.md`](07-slot.md)  
   De synthese van de sessie en de implicaties voor builders, operators, governance en strategie.
8. [`08-bronnen-qa-spreekspiekbrief.md`](08-bronnen-qa-spreekspiekbrief.md)  
   Een compacte bronkaart, veelgestelde kritische vragen en een spreekhouvast per deel van de talk.

## Kernthese van het project

> Moltbook is interessant, niet omdat het al een echt sociaal netwerk voor AI is, maar omdat het zichtbaar maakt wat er nog ontbreekt: identiteit, geheugen, governance en economische efficiëntie.

Die these loopt door de hele repo:

- de slides maken ze podiumgeschikt
- de analyses maken ze reproduceerbaar
- de verificatiedocs maken ze auditbaar
- deze `content/`-map maakt ze leerbaar

## Wat hier nu extra in zit

De hoofdstukken in deze map zijn bewust uitgebreid met:

- inline screenshots en grafieken waar ze inhoudelijk horen
- uitleg per figuur: wat je ziet, wat je niet mag overschatten, en wat je moet onthouden
- uitgewerkte analyse-redeneringen in plaats van alleen conclusies
- expliciete scheiding tussen bronanker, afgeleide berekening en scenario-aanname
- een extra hoofdstuk met bronnen, Q&A en spreekspiekbrief

## Wat hier als hard geldt, en wat niet

### Hard geverifieerd in deze repo

- Moltbook positioneert zichzelf publiek als een sociaal netwerk voor AI-agents.
- Moltbook houdt juridisch de mens verantwoordelijk; agents krijgen geen eigen legal eligibility.
- OpenClaw documenteert context, multi-agent routing, tools en sandboxing als expliciete systeemonderdelen.
- Frontier-modelprestaties, compute-trends en kostdalingen tonen sterke vooruitgang, maar niet op een manier die elke hypeclaim rechtvaardigt.

### Expliciet assumption-driven

- de illustratieve kost van een sociale agentcyclus
- het Monte Carlo readiness-model
- elk exact forecast-percentage of jaartal

### Expliciet vernauwd om eerlijk te blijven

- MiniMax M2.7 versus Claude Opus 4.6
- claims over "exponentiële" groei
- claims over echte autonome agentsamenlevingen

## Waar je de auditsporen vindt

- [`../docs/verification/VERIFICATION_REPORT.md`](../docs/verification/VERIFICATION_REPORT.md)
- [`../docs/verification/CLAIM_AUDIT.md`](../docs/verification/CLAIM_AUDIT.md)
- [`../docs/verification/ANALYSIS_AUDIT.md`](../docs/verification/ANALYSIS_AUDIT.md)
- [`../docs/verification/SLIDE_SYSTEM_DECISION.md`](../docs/verification/SLIDE_SYSTEM_DECISION.md)

## Waar je de analyses en outputs vindt

- analyses: [`../analyses/`](../analyses/)
- data-inputs: [`../data/`](../data/)
- grafieken: [`../assets/`](../assets/)
- deck output: [`../release/Moltbook.pptx`](../release/Moltbook.pptx)

## Leeshouding

Lees deze map niet als marketingtekst en ook niet als pure sceptische teardown. De goede houding is:

- neem demo’s serieus
- lees claims smal
- scheid architectuur van antropomorf taalgebruik
- scheid reproduceerbare rekenkunde van geobserveerde werkelijkheid
- behandel forecasts als discipline voor denken, niet als orakel
