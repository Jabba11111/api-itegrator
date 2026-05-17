# Open vragen — beantwoorden vóór ronde 3

## 1. Base URLs — BEANTWOORD ✅

API: `https://{customer}.testersuite.nl.api.testersuite.com`
UI: `https://{customer}.testersuite.nl/{customer_id}`
Voorbeeld: `customer=superp`, `customer_id=environmentId=1`, `cycle_id=2`, `run_id=2`.

## 2. Auth — BEANTWOORD ✅

Officiële API: HTTP **Basic** (`Authorization: Basic <base64(user:pass)>`).
Niet Bearer. Format: `application/vnd.api+json` (JSON:API).

## 3. Stoplight-pagina's die ik nog nodig heb

De volgende drie pagina's bestaan vermoedelijk; check op
https://testersuite.stoplight.io/docs/api en plak de Request/Response.

### a) Voeg scenario óf testcase toe aan een testrun

Zoek pagina's zoals:

- "Add test scenario to test run"
- "Add test case to test run"
- of relationship-endpoints: `POST /test-runs/{id}/relationships/testScenarios`
  / `…/relationships/testCases`

Wat ik specifiek nodig heb:

- exacte path
- body-structuur (JSON:API `data` array of object?)
- of de `scenario_id` als `meta.scenarioId`, als aparte
  `testRunTestScenario`-resource, of via een ander veld meekomt — want
  dat is de hele crux (jouw eis: "scenario-naam moet bij de case staan")

### b) Update testresult

Zoek "Update test run test case", "Set result", of vergelijkbaar.
Pad-vermoedens: `PATCH /test-run-test-cases/{id}` of
`/test-runs/{id}/test-cases/{id}`.

### c) Test scenario test case (slug `c65d7cb23d459`)

Dit slug suggereert een endpoint voor de scenario↔testcase relatie zelf.
Welke method + path, en welke velden bevat het response?

## 4. Hoe linkt een SCE-code aan een scenario-record?

`filter[code]` bestaat **niet** op `/test-scenarios`. Wat zit er wél in
`attributes`? Drie scenario's:

- Het is een naam-veld (`attributes.name` of `attributes.shortDescription`).
- Het is een custom field (`attributes.customField19` o.i.d.) → dan kun
  je `filter[customField_19]=SCE001` gebruiken.
- Het is een dedicated veld (`attributes.code`).

Antwoord helpt me bepalen of we client-side moeten matchen of of er een
filter-truc is. Een voorbeeld-response van `GET /1/test-scenarios/1` is
genoeg.

## 5. Status-vocabulaire

Welke `status`-waarden mag een testrun-testcase hebben?
`pass` / `fail` / `blocked` / `not_executed`? Numeriek? Pas zichtbaar
zodra vraag 3b is beantwoord.

## 6. DevTools-vangst — alleen als 3a/3b NIET officieel bestaan

Pas relevant wanneer Stoplight de write-acties niet biedt; dan val ik
terug op de UI-endpoints. Vangst-procedure staat in
[devtools-capture-guide.md](devtools-capture-guide.md).
