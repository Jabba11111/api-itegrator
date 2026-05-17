# Open vragen — beantwoorden vóór ronde 3

## 1. Base URLs — BEANTWOORD ✅

API: `https://{customer}.testersuite.nl.api.testersuite.com`
UI: `https://{customer}.testersuite.nl/{customer_id}`
Voorbeeld: `customer=superp`, `customer_id=environmentId=1`, `cycle_id=2`, `run_id=2`.

## 2. Auth — BEANTWOORD ✅

Officiële API: HTTP **Basic** (`Authorization: Basic <base64(user:pass)>`).
Niet Bearer. Format: `application/vnd.api+json` (JSON:API).

## 3. Stoplight — beantwoord ✅

- Add test case aan testrun: bevestigd, `POST /{env}/test-runs/{runId}/test-cases`
  met body `{ data: { relationships: { testDesignTestCase: { data: {id, type} } } } }`
- Add test scenario aan testrun: **bestaat niet** officieel volgens jou.

## 3b. Stoplight — nog te zoeken

### Update testresult

Zoek "Update test run test case", "Set result", of `PATCH`-endpoint op
`/test-run-test-cases/{id}` of `/test-runs/{id}/test-cases/{id}`.
Nodig: method, path, body-structuur, toegestane `status`-waarden.

### Test scenario test case (slug `c65d7cb23d459`)

Slug uit jouw eerste paste — wat doet dit endpoint precies? Welke method
+ path, en wat zit er in de response?

## 4. SCE/CAS code → ID mapping — BEANTWOORD ✅

`SCE<nr>` en `CAS<nr>` zitten beide in `attributes.businessId`. Voorbeeld:

- scenario id `1` → `attributes.businessId == "SCE1"`
- testcase id `39` → `attributes.businessId == "CAS39"`

Er is geen documented `filter[businessId]` — match client-side, of
pagineer met `filter[testCycle]` als scope-beperking.

Sample-response staat in [`samples/get-test-scenario-1.json`](samples/get-test-scenario-1.json).

## 4b. Scenario-label in de testrun-weergave <a id="scenario-label"></a>

De officiële add-testcase endpoint accepteert **alleen** een
`testDesignTestCase`-reference, geen scenario. Vraag: wordt het
scenario-label dan automatisch getoond bij die regel in de testrun?

Hypothese: ja, Testersuite leidt het scenario af uit de
`testScenarioTestCase`-relatie van de design-testcase. Te testen op
staging door één keer een case te toevoegen via deze API en in de UI te
kijken of het scenario zichtbaar is.

Als het label niet vanzelf verschijnt, vallen we terug op de UI-add-flow
(form-urlencoded, sessie-auth) — vangst staat klaar in
[devtools-capture-guide.md](devtools-capture-guide.md).

## 5. Status-vocabulaire

Welke `status`-waarden mag een testrun-testcase hebben?
`pass` / `fail` / `blocked` / `not_executed`? Numeriek? Pas zichtbaar
zodra vraag 3b is beantwoord.

## 6. DevTools-vangst — alleen als 3a/3b NIET officieel bestaan

Pas relevant wanneer Stoplight de write-acties niet biedt; dan val ik
terug op de UI-endpoints. Vangst-procedure staat in
[devtools-capture-guide.md](devtools-capture-guide.md).
