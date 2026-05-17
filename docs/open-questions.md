# Open vragen — beantwoorden vóór ronde 2

## 1. Base URL voor de officiële Bearer-API — BEANTWOORD

Patroon: `https://{customer}.testersuite.nl.api.testersuite.com`
Voorbeeld: `https://superp.testersuite.nl.api.testersuite.com`

Verwerkt als default in CLI en HTML builder.

**Sub-vraag (nog open):** zit er een versie-prefix (`/v1/`, `/api/`) tussen de
base en de resource-paden? Dat blijkt uit de Stoplight "Servers"-sectie of uit
één voorbeeld-request.

## 2. Bestaan Testrun/Testresult endpoints officieel?

**Vraag:** is er een Stoplight-pagina voor:

- "Voeg scenario toe aan testrun"
- "Voeg testcase toe aan testrun"
- "Update testresultaat"
- "Verwijder testcase uit testrun"

Als ja: deel de links (of plak de URL/method/body uit Stoplight).

**Wat ik doe per antwoord:**

- Ja, officieel → ik werk `docs/endpoints.md` en `docs/usecases.md` bij met
  exacte paths/bodies en `{{TBD}}` valt weg.
- Nee, alleen UI → ik bouw in de Python CLI een sessie-login-mode bij (POST naar
  `/login`, PHPSESSID-cookie hergebruiken). De HTML-versie krijgt dan een
  waarschuwing dat sessie-auth in de browser CORS-issues geeft.
- Hybride → mix van de twee.

## 3. Voorbeeld-IDs voor werkende curl's

**Vraag:** één echte set:

- `cycle_id`
- `run_id`
- één `SCE`-code + bijbehorend `scenario_id`
- één `CAS`-code + bijbehorend `testcase_id`

(Geen geheimen — alleen de IDs. Een wegwerp/staging-token mag, anders zet ik
`$TS_TOKEN` als placeholder in de curls.)

**Wat ik doe:** elke curl in de docs wordt een copy-paste die je in een
staging-omgeving direct kunt draaien om de spec te valideren.

## 4. (klein) Status-vocabulaire

**Vraag:** welke statuswaarden accepteert Testersuite voor een testresultaat?
Vermoeden: `pass`, `fail`, `blocked`, `not_executed`. Bevestigen of corrigeren.
