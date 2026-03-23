# Deel 5: Trends

## Wat de repo nu nog wel claimt

### Stanford HAI

- grote sprongen op moeilijke benchmarks zoals MMMU, GPQA en SWE-bench
- meer dan 280x daling in kost om GPT-3.5-level quality te bereiken tussen november 2022 en oktober 2024

### Epoch

- sterke groei in compute stock
- sterke groei in frontier training compute
- sterke vooruitgang in pre-training efficiency
- chip performance per dollar blijft verbeteren

### MiniMax M2.7 vs Opus 4.6

- MiniMax documenteert M2.7 nu publiek op de eigen modelsite en in de eigen API pricing docs
- officiële list price:
  - M2.7: $0,30 input / $1,20 output per 1M tokens
  - Opus 4.6: $5 input / $25 output per 1M tokens
- officiële vendor benchmarks maken "veel goedkoper en nog competitief" verdedigbaar
- ze maken "in wezen gelijk aan Opus 4.6" nog steeds te sterk

## Wat de repo niet meer claimt

- geen synthetische ECI tijdreeks alsof die uit brondata kwam
- geen te harde "alles is exponentieel" taal
- geen overdreven MiniMax-vs-Opus conclusie
- geen verwarring tussen vendor-reported benchmark claims en een neutraal matched eval sheet

## Veilige trendzin

> "De hardste verdedigbare curve zit vandaag in kosten, compute en efficiency. Capability gaat ook vooruit, maar bounded benchmarks satureren en moeten voorzichtig gelezen worden."

## Veilige MiniMax-zin

> "MiniMax M2.7 is op officiële list prices uitzonderlijk goedkoop en op sommige agentic/coding taken competitief, maar officiële vendor pages plaatsen het nog niet netjes op Opus 4.6-niveau."

## Belangrijke bronnuance

Op de ECI-pagina noemt Epoch in de overview 37 benchmarks, maar in de datasection 42 benchmarks.

Dus:

- liever "dozens of benchmarks"
- niet doen alsof er één perfect hard getal is wanneer de bron zelf varieert
