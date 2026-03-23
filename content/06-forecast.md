# Deel 6: Forecast model

## Wat dit model is

- een scenario-tool
- een Monte Carlo barrier-crossing model
- een manier om aannames zichtbaar te maken

## Wat dit model niet is

- geen data-gedreven voorspelling van één exact jaar
- geen profetie
- geen vervanging voor inhoudelijke discussie over definities en thresholds

## Belangrijke aanscherping in deze repo

- scenario-inputs staan nu expliciet in `data/forecast_scenarios.json`
- het model draait reproduceerbaar via `uv`
- threshold sensitivity en floor sensitivity worden gerapporteerd
- de repo zegt expliciet dat assumption error belangrijker is dan simulation error

## Praktische boodschap

In de huidige parameterisatie blijken de floor constraints belangrijker dan de headline threshold.

Dat is precies het soort inzicht dat je wilt:

- niet "het antwoord is 2038"
- wel "de uitkomst hangt sterk af van governance, memory, reliability en network floors"
