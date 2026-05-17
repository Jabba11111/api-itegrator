# Endpoints — inventaris en status

## Twee oppervlakken

| Soort | Base URL | Auth | Content-Type |
|---|---|---|---|
| Officiële API | `https://{customer}.testersuite.nl.api.testersuite.com` | Basic | `application/vnd.api+json` |
| UI / web-app | `https://{customer}.testersuite.nl/{customer_id}` | sessie (PHPSESSID) | `application/x-www-form-urlencoded` |

**Auth-header officieel:** `Authorization: Basic <base64(user:pass)>`.

## Officiële API — bevestigd (uit Stoplight)

URL = `{api_base}/{environmentId}/<path>`. De `{environmentId}` is dezelfde
`1` die in de UI-URL als eerste path-segment staat.

| Endpoint | Method | Path | Stoplight-slug |
|---|---|---|---|
| Retrieve all test scenarios | GET | `/{env}/test-scenarios` | `c8e3fae5e8e81-retrieve-all` |
| Get one test scenario | GET | `/{env}/test-scenarios/{id}` | `154d1c8cdb722-get-a-test-scenario` |
| Test scenario ↔ test case | ? | (slug) | `c65d7cb23d459-test-scenario-test-case` |
| Test scenario (resource) | ? | (slug) | `273a0d26ebfde-test-scenario` |
| Create a test run | POST | `/{env}/test-runs` | `6d3ae0aeb118b-create-a-test-run` |
| **Add test case to run** | POST | `/{env}/test-runs/{runId}/test-cases` | `468d6afc8761f-add-test-case` |

Query-parameters op `Retrieve all`:

- `filter[customField_*]` — bv. `filter[customField19]=1`
- `filter[testCycle]` — testcyclus-id, leeg = Masterlist
- `page[offset]` — paginering (10 per pagina)

**Niet aanwezig:** `filter[code]` of `filter[name]`. Lookup op SCE-code
gaat dus niet direct via query — zie `plan.md` voor de drie alternatieven.

## Officiële API — pad bevestigd via vangst

| Doel | Method + path | Status |
|---|---|---|
| Get one testRunTestCase | `GET /{env}/test-runs/{runId}/test-cases/{trtcId}` | ✅ vangst gedeeld |
| Update testcase-resultaat | `PATCH /{env}/test-runs/{runId}/test-cases/{trtcId}` | ✅ pad zelfde URL, body-shape per JSON:API-conventie |
| Verwijder testcase uit testrun | `DELETE /{env}/test-runs/{runId}/test-cases/{trtcId}` | vermoed (zelfde URL) |
| Voeg scenario toe aan testrun | — | niet aanwezig officieel |
| List testRunTestCaseStatus waarden | `GET /{env}/test-run-test-case-statuses` of via included | vermoed, TBD |

## ID-ruimtes in Testersuite

Vier verschillende numerieke ID-ruimtes — verwarring leidt tot 404 / verkeerde scope.

| Soort | Voorbeeld | Waar |
|---|---|---|
| design `testCase` id | `2` | `attributes.businessId="CAS2"` |
| design `testScenario` id | `3` | `attributes.businessId="SCE3"` |
| `testRunTestCase` id (trtc) | `447` | `databaseid="447"` in HTML, `id` na POST |
| `testRunTestScenario` id (runsce) | `2` | `runsce_id="2"` in HTML — run-interne koppeling |

Let op: `runsce_id` en design `testScenario` id zijn **verschillende reeksen**.
In de HTML hierboven heeft de SCE3-badge `runsce_id="2"` (niet 3).

Vijf statuswaarden, gezien in een `progress`-response van Testersuite:
`notstarted`, `started`, `ok`, `notok`, `skipped`.

| `attributes.status` | `executionStatus.id` |
|---|---|
| `"notstarted"` | `1` |
| `"started"` | ? |
| `"ok"` | ? |
| `"notok"` | `4` |
| `"skipped"` | ? |

Alleen `notok ↔ 4` is bevestigd via een vangst. De vier andere
ID-mappings zijn snel te achterhalen door één case per status door te
klikken in de UI en `GET /{env}/test-runs/{run}/test-cases/{trtc}` te
doen — zie open-questions.

## UI-endpoints — vastgelegd (via DevTools)

URL-patroon:

```
https://{customer}.testersuite.nl/{customer_id}/testcycle/{cycle_id}/testrun/{run_id}/{action}
```

| Action | Method | Doel | Status |
|---|---|---|---|
| `listtestscenariostoadd` | POST | popup 1: lijst SCE's die nog toegevoegd kunnen worden | ✅ vangst |
| `get-testscenarios-testcases-rows` | POST | popup 2: lijst CAS's per gekozen SCE | ✅ vangst |
| `papi/testscenario/RUN{run_id}/testcases` | GET | **lijst alle trtc's in run met SCE-badge** (HTML) | ✅ vangst |
| `{add-testscenario-or-cases}` | POST | submit die scenarios+cases aan run koppelt | ✅ vangst — `POST /testcycle/{c}/testrun/{r}/edit` (volledige form-save met CSRF) |
| `{update-action}` | POST/PATCH | resultaat updaten | (officieel mogelijk, zie boven) |

Content-Type van UI-calls is `application/x-www-form-urlencoded; charset=UTF-8`.

## Bekende voorbeeld-IDs

- `customer` = `superp`
- `environmentId` (UI: customer_id) = `1`
- `cycle_id` = `2`
- `run_id` = `2`

Voorbeeld werkende URLs:

```
GET  https://superp.testersuite.nl.api.testersuite.com/1/test-scenarios?filter[testCycle]=2
GET  https://superp.testersuite.nl.api.testersuite.com/1/test-scenarios/1
POST https://superp.testersuite.nl.api.testersuite.com/1/test-runs

POST https://superp.testersuite.nl/1/testcycle/2/testrun/2/listtestscenariostoadd
```
