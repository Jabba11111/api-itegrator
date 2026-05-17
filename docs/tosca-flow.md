# Tosca-flow — testcase uitvoeren en resultaat in Testersuite

Hoe je in Tosca Tricentis één testcase laat lopen en het resultaat
terugschrijft naar een lopende Testersuite-testrun.

## Aannames

- Tosca Tricentis 14+ met **TBox HTTP Engine**.
- Basic auth wordt door jou geleverd via een Tosca Buffer of vault.
- Per Tosca-suite weet je vooraf: `TEST_CYCLE_ID` en `TEST_RUN_ID`.

## Globale Tosca-buffers

Definieer deze één keer (bv. in een Setup-module of als project-buffers):

| Buffer | Voorbeeldwaarde |
|---|---|
| `TS_API_BASE` | `https://superp.testersuite.nl.api.testersuite.com` |
| `TS_ENV` | `1` |
| `TS_BASIC` | `base64(user:pass)` |
| `TS_CYCLE_ID` | `4` |
| `TS_RUN_ID` | `2` |

Plus per testcase die Tosca uitvoert:

| Buffer | Bron |
|---|---|
| `SCE_CODE` | testdatasheet, bv. `SCE1` |
| `CAS_CODE` | testdatasheet, bv. `CAS2` |
| `TOSCA_RESULT` | `ok` of `notok` (na uitvoer) |

## Vijf HTTP-modules in Tosca

### Module 1 — Lookup scenario (optioneel)

Sla over als het `scenario_id` direct uit het testdatasheet komt.

| Veld | Waarde |
|---|---|
| Method | `GET` |
| URL | `{TS_API_BASE}/{TS_ENV}/test-scenarios?filter[testCycle]={TS_CYCLE_ID}&page[offset]=0` |
| Header | `Authorization: Basic {TS_BASIC}` |
| Header | `Accept: application/vnd.api+json` |

**Verwacht:** `200 OK`, JSON:API pagina.

**Naar buffer (JSONPath):**
`$.data[?(@.attributes.businessId=='{SCE_CODE}')].id` → `SCENARIO_ID`

**Pagineren:** als geen match en `links.next` aanwezig, herhaal met
`page[offset]=10`, `20`, … (Tosca: TestStep-loop).

### Module 2 — Lookup testcase

| Veld | Waarde |
|---|---|
| Method | `GET` |
| URL | `{TS_API_BASE}/{TS_ENV}/test-scenarios/{SCENARIO_ID}` |
| Header | `Authorization: Basic {TS_BASIC}` |
| Header | `Accept: application/vnd.api+json` |

**Naar buffer (JSONPath):**
`$.included[?(@.type=='testCase' && @.attributes.businessId=='{CAS_CODE}')].id` → `TESTCASE_ID`

### Module 3 — Add testcase aan testrun

| Veld | Waarde |
|---|---|
| Method | `POST` |
| URL | `{TS_API_BASE}/{TS_ENV}/test-runs/{TS_RUN_ID}/test-cases` |
| Header | `Authorization: Basic {TS_BASIC}` |
| Header | `Content-Type: application/vnd.api+json` |
| Header | `Accept: application/vnd.api+json` |
| Body | JSON, zie hieronder |

```json
{
  "data": {
    "relationships": {
      "testDesignTestCase": {
        "data": { "id": "{TESTCASE_ID}", "type": "testCase" }
      }
    }
  }
}
```

**Verwacht:** `201 Created`.
**Naar buffer:** `$.data.id` → `TRTC_ID`.

### Module 4 — (Hier voert Tosca zijn eigen test uit)

Voer de geautomatiseerde acties uit. Zet aan het einde:

- `TOSCA_RESULT` = `ok` of `notok`
- Map dat naar `EXEC_STATUS_ID`:
  - `notok` → `4`
  - `ok` → `?` (nog vast te leggen — eenmalig met module 6 hieronder)

### Module 5 — Update resultaat

| Veld | Waarde |
|---|---|
| Method | `PATCH` |
| URL | `{TS_API_BASE}/{TS_ENV}/test-runs/{TS_RUN_ID}/test-cases/{TRTC_ID}` |
| Header | `Authorization: Basic {TS_BASIC}` |
| Header | `Content-Type: application/vnd.api+json` |
| Header | `Accept: application/vnd.api+json` |
| Body | JSON, zie hieronder |

```json
{
  "data": {
    "type": "testRunTestCase",
    "id": "{TRTC_ID}",
    "attributes": { "status": "{TOSCA_RESULT}" },
    "relationships": {
      "executionStatus": {
        "data": { "id": "{EXEC_STATUS_ID}", "type": "testRunTestCaseStatus" }
      }
    }
  }
}
```

**Verwacht:** `200 OK`.

### Module 6 — Read result (debug)

Eenmalig nodig om de `EXEC_STATUS_ID` voor `"ok"` vast te stellen:

| Veld | Waarde |
|---|---|
| Method | `GET` |
| URL | `{TS_API_BASE}/{TS_ENV}/test-runs/{TS_RUN_ID}/test-cases/{TRTC_ID}` |
| Header | `Authorization: Basic {TS_BASIC}` |
| Header | `Accept: application/vnd.api+json` |

Zet één case in de UI op "OK", run deze module, en lees
`$.data.relationships.executionStatus.data.id` af.

## Volgorde in een Tosca testrun

```
[Setup eenmaal per Tosca-batch]
  └─ vul TS_* buffers

[Per testcase in de Tosca ExecutionList]
  ├─ Module 1: Lookup scenario  → SCENARIO_ID
  ├─ Module 2: Lookup testcase  → TESTCASE_ID
  ├─ Module 3: Add to run       → TRTC_ID
  ├─ Module 4: Tosca steps      → TOSCA_RESULT
  └─ Module 5: PATCH result
```

## Optimalisaties

- **Cache de lookups.** Doe Module 1+2 één keer aan het begin voor álle
  CAS in je batch en bewaar de mapping `CAS_CODE → TESTCASE_ID` in een
  Tosca Data Resource. Tijdens uitvoer alleen Module 3 + 5.
- **Idempotency.** Als Module 3 een `409 Conflict` geeft, bestaat de
  case al in de run. Roep dan `GET /test-runs/{run}/test-cases` aan om
  de bestaande `TRTC_ID` op te halen voor Module 5.

## Valkuil: drie soorten ID's door elkaar

Testersuite gebruikt drie verschillende numerieke ID-ruimtes. Verwar ze niet:

| Soort | Voorbeeld | Waar te vinden |
|---|---|---|
| **design testCase id** | `39`, `40` | `GET /test-scenarios/{sid}` → `included[type=testCase].id` |
| **testRunTestCase id (trtc_id)** | `425` | `POST /test-runs/{run}/test-cases` response `data.id` |
| **CAS-code (businessId)** | `CAS39`, `CAS2` | `attributes.businessId` op beide bovenstaande resources |

**De Module-3-body verwacht de design id**, niet de trtc_id. Een trtc_id
in `testDesignTestCase.data.id` zetten geeft **HTTP 404**.

```
testDesignTestCase.data.id  →  design testCase id (uit included[])
                               ↑
                               NIET de id die je terugkrijgt uit een eerdere add-call
```

## Foutafhandeling per call

| HTTP-code | Betekenis | Actie |
|---|---|---|
| `200/201` | OK | door |
| `400` | bad request | log body, stop run |
| `401` | auth fout | stop run, check `TS_BASIC` |
| `404` | resource niet gevonden | check ID-soort (design vs trtc!), log, markeer skipped |
| `409` | al toegevoegd | lookup bestaande TRTC_ID |
| `5xx` | server fout | retry 2× met backoff |

## Open punt: scenario-label

De `testRunTestCase` heeft géén `testScenario`-relationship terug. Of
het scenario-label automatisch in de testrun-UI verschijnt na een
API-add, is niet uit de response af te leiden — alleen visueel te
checken na een echte testcall. Zie open-questions.md.

Als blijkt dat het label niet verschijnt: fallback naar UI-flow
(`{ui_base}/testcycle/{cy}/testrun/{rn}/{add-action}`) met
form-urlencoded en sessie-auth. Daarvoor is nog één DevTools-vangst
nodig.
