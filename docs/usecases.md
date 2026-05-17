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

**Mapping SCE → id:** `SCE<nr>` zit in `data[i].attributes.businessId` (bv.
`"SCE1"`). Geen ingebouwde `filter[businessId]` — pagineren tot je een match
op `businessId` hebt, of het `scenario_id` direct uit Tosca aandragen.

---

## 2. Get one scenario (incl. testcases)  *(officieel)*

**Doel:** alle testcases binnen één SCE ophalen — daaruit haal je het
`testcase_id` voor een gegeven CAS-code.

**Endpoint:** `GET {{api_base}}/{{env}}/test-scenarios/{{scenario_id}}`

**Headers:** zelfde als boven.

**Response:** `data` = scenario, `included[]` bevat `testScenarioTestCase`,
`testCase`, en `testCaseStep`-records.

**Mapping CAS → id:** filter `included[]` op `type=="testCase"` en match
`attributes.businessId == "{{cas_code}}"`. Het `id`-veld van die record is
`testcase_id`.

Zie [`samples/get-test-scenario-1.json`](samples/get-test-scenario-1.json)
voor een echte response.

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

## 4. Voeg testcase toe aan testrun  *(officieel — BEVESTIGD)*

**Endpoint:** `POST {{api_base}}/{{env}}/test-runs/{{run_id}}/test-cases`

(Stoplight-slug: `468d6afc8761f-add-test-case`. Beschrijving: *"Copies a
test design test case and adds it to a test run."* — de testcase wordt
gekopieerd; je krijgt een nieuw `testRunTestCase`-record terug.)

**Headers:**

```
Authorization: Basic {{basic}}
Content-Type: application/vnd.api+json
Accept: application/vnd.api+json
```

**Body:**

```json
{
  "data": {
    "relationships": {
      "testDesignTestCase": {
        "data": { "id": "{{testcase_id}}", "type": "testCase" }
      }
    }
  }
}
```

**Response (201):** `data.id` = `trtc_id` (nodig voor stap 5).
`data.type = "testRunTestCase"`.

**Belangrijke open vraag:** de body bevat **geen scenario-veld**. De
oorspronkelijke wens (scenario-naam zichtbaar bij de case in de testrun)
hangt af van of Testersuite zelf het scenario afleidt uit de design-case
(via `testScenarioTestCase`-relatie). Te valideren in een staging-run —
zie [open-questions.md](open-questions.md#scenario-label).

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

## 5. Update testcase-resultaat in testrun  *(officieel, pad bevestigd)*

**Endpoint-pad:** `PATCH {{api_base}}/{{env}}/test-runs/{{run_id}}/test-cases/{{trtc_id}}`

Pad bevestigd via een echte respons op `GET` op dezelfde URL — zie
[`samples/get-testruntestcase-425.json`](samples/get-testruntestcase-425.json).
Per JSON:API-conventie is `PATCH` op dezelfde URL de update-call.

**Body (vermoed, JSON:API):**

```json
{
  "data": {
    "type": "testRunTestCase",
    "id": "{{trtc_id}}",
    "attributes": {
      "status": "{{status}}"
    },
    "relationships": {
      "executionStatus": {
        "data": { "id": "{{execution_status_id}}", "type": "testRunTestCaseStatus" }
      }
    }
  }
}
```

**Statusveld — twee niveaus:**

- `attributes.status` is een string. Geobserveerde waarde: `"notok"`.
  Overige waarden vermoedelijk `"ok"`, `"pending"`, `"blocked"` —
  bevestigen door de UI-status door te klikken en `GET` op de testcase
  te herhalen.
- `relationships.executionStatus.data.id` verwijst naar een
  `testRunTestCaseStatus`-resource. `id=4` = "notok". De andere IDs zijn
  nog onbekend.

**Onzeker:** of Testersuite alleen `attributes.status` accepteert,
alleen het FK-relationship, of beide tegelijk. Beste eerste poging:
beide meesturen.

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
