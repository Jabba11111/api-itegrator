# Use cases

Volgorde = wat Tosca tijdens een testrun nodig heeft.

Notatie:

- `{{api_base}}` = `https://{customer}.testersuite.nl.api.testersuite.com`
- `{{ui_base}}` = `https://{customer}.testersuite.nl/{customer_id}`
- `{{env}}` = `environmentId` (zelfde getal als `{customer_id}` in de UI, bv. `1`)
- `{{basic}}` = `<base64(user:pass)>`
- `{{cycle_id}}`, `{{run_id}}` = numerieke IDs

Auth wordt door jou geleverd — deze docs beschrijven alleen de request-shape.

---

## 1. Lookup scenarios in een testcyclus  *(officieel)*

**Doel:** vind het `scenario_id` dat hoort bij een SCE-code.

**Endpoint:** `GET {{api_base}}/{{env}}/test-scenarios?filter[testCycle]={{cycle_id}}&page[offset]=0`

**Headers:**

```
Authorization: Basic {{basic}}
Accept: application/vnd.api+json
```

**Response:** JSON:API lijst van `testScenario`-objecten, 10 per pagina.

**Mapping SCE → id:** geen ingebouwde `code`-filter. Drie opties:

1. Pagineer en match op `data[].attributes.name` of een vergelijkbaar veld
   (welk veld dat exact is hangt af van jouw Testersuite-config — zie
   open-questions.md).
2. Gebruik `filter[customField_X]=SCE001` als SCE-code als custom field
   is geconfigureerd.
3. Sla over: laat Tosca het numerieke `scenario_id` direct kennen.

---

## 2. Get one scenario (incl. testcases)  *(officieel)*

**Doel:** alle testcases binnen één SCE ophalen — daaruit haal je het
`testcase_id` voor een gegeven CAS-code.

**Endpoint:** `GET {{api_base}}/{{env}}/test-scenarios/{{scenario_id}}`

**Headers:** zelfde als boven.

**Response:** `data` = scenario, `included[]` bevat `testScenarioTestCase`,
`testCase`, en `testCaseStep`-records. Filter `included[]` op
`type==testCase` en match op `code`/`name` om `testcase_id` te vinden.

---

## 3. Create a test run  *(officieel)*

**Doel:** een nieuwe testrun aanmaken (bv. bij het starten van een Tosca-batch).

**Endpoint:** `POST {{api_base}}/{{env}}/test-runs`

**Headers:**

```
Authorization: Basic {{basic}}
Content-Type: application/vnd.api+json
Accept: application/vnd.api+json
```

**Body (JSON:API):**

```json
{
  "data": {
    "type": "testRun",
    "attributes": {
      "shortDescription": "{{short_description}}",
      "longDescription": "{{long_description}}",
      "startDate": "{{start_date}}",
      "endDate": "{{end_date}}"
    },
    "relationships": {
      "testCycle": {
        "data": { "id": "{{cycle_id}}", "type": "testCycle" }
      }
    }
  }
}
```

**Response:** `201` met `data.id` = nieuw `run_id`.

---

## 4. Voeg testcase toe aan testrun via scenario  *(officieel — vermoed, TBD)*

**Vermoede endpoint (JSON:API relationship):**

`POST {{api_base}}/{{env}}/test-runs/{{run_id}}/relationships/testCases`

**Body:**

```json
{
  "data": [
    { "type": "testCase", "id": "{{testcase_id}}",
      "meta": { "scenarioId": "{{scenario_id}}" } }
  ]
}
```

**Onbekend:** of `meta.scenarioId` de juiste manier is om de SCE-koppeling
te leggen, of dat er een aparte `testRunTestScenario`-resource is. De
"Get a test scenario"-response noemt het type `testRunTestScenario` — dus
de relatie bestaat als eigen resource. Te bevestigen in Stoplight.

**Fallback (UI):** zie 4b.

---

## 4b. Voeg testcase toe aan testrun  *(UI fallback)*

**Endpoint:** `POST {{ui_base}}/testcycle/{{cycle_id}}/testrun/{{run_id}}/{{add_action}}`

`{{add_action}}` nog vast te leggen via DevTools-vangst (zie
[devtools-capture-guide.md](devtools-capture-guide.md)).

**Body (form-urlencoded):**

```
scenario_id={{scenario_id}}&testcase_id={{testcase_id}}
```

---

## 5. Update testcase-resultaat in testrun  *(officieel — vermoed, TBD)*

**Vermoede endpoint:** `PATCH {{api_base}}/{{env}}/test-run-test-cases/{{trtc_id}}`

(Resource-naam en path zijn een gok op basis van JSON:API-conventies — te
bevestigen via Stoplight.)

**Body:**

```json
{
  "data": {
    "type": "testRunTestCase",
    "id": "{{trtc_id}}",
    "attributes": {
      "status": "{{status}}",
      "comment": "{{comment}}",
      "durationSeconds": {{duration_seconds}}
    }
  }
}
```

**Fallback (UI):** vergelijkbare structuur als 4b.

---

## 6. Lijst-calls (UI) — verkenning  *(captured)*

| Doel | URL |
|---|---|
| Wat kan ik nog toevoegen? | `POST {{ui_base}}/testcycle/{{cycle_id}}/testrun/{{run_id}}/listtestscenariostoadd` |
| Wat zit er al in? | `POST {{ui_base}}/testcycle/{{cycle_id}}/testrun/{{run_id}}/get-testscenarios-testcases-rows` |

Form-urlencoded, sessie-auth, `X-Requested-With: XMLHttpRequest`.

---

## Welke call hoort bij welk Tosca-moment

```
Tosca StartUp           → 1/2 (lookup)  óf  3 (create run als nog niet bestaat)
Tosca AddToRun (per CAS)→ 4 (officieel) / 4b (UI fallback)
Tosca uitvoer           → 5 (update result)
Tosca rollback          → DELETE op zelfde URL als 4
```
