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

## 3b. Update-result pad — BEANTWOORD ✅

Pad bevestigd: `/{env}/test-runs/{run_id}/test-cases/{trtc_id}`.
GET bevestigd via vangst, PATCH op zelfde URL per JSON:API-conventie.

Open sub-vragen voor de PATCH:

- Officiële Stoplight-pagina (slug)?
- Mag `attributes.status` direct gezet worden, of moet het via de
  `executionStatus`-relationship?
- Volledige lijst van toegestane `executionStatus`-IDs (`1` t/m ?) met
  bijbehorende `attributes.status`-strings.

## 5. Status-vocabulaire — gedeeltelijk beantwoord

Geobserveerd: `attributes.status = "notok"` ↔ `executionStatus.id = 4`.

Nog nodig: de overige `testRunTestCaseStatus`-records. Snelste manier:

- Klik in de UI een testcase door naar `ok` / `blocked` / `pending` etc.
- Run de CLI `python3 -m ts_builder --curl get-testruntestcase env=1 run_id=92 trtc_id=425 basic=…`
- Noteer welke `executionStatus.id` bij welke string hoort.

Of, als er een endpoint is: `GET /{env}/test-run-test-case-statuses`.

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
