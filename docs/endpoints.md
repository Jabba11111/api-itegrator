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

## Officiële API — nog te bevestigen

| Doel | Vermoede method + path | Status |
|---|---|---|
| Voeg scenario toe aan testrun | — | **niet aanwezig** volgens user |
| Update testcase-resultaat | `PATCH /{env}/test-runs/{runId}/test-cases/{trtcId}` of `/{env}/test-run-test-cases/{trtcId}` | TBD — Stoplight bevestigen |
| Verwijder testcase uit testrun | `DELETE /{env}/test-runs/{runId}/test-cases/{trtcId}` | TBD |

## UI-endpoints — vastgelegd (via DevTools)

URL-patroon:

```
https://{customer}.testersuite.nl/{customer_id}/testcycle/{cycle_id}/testrun/{run_id}/{action}
```

| Action | Method | Doel | Status |
|---|---|---|---|
| `listtestscenariostoadd` | POST | lijst SCE's die nog toegevoegd kunnen worden | ✅ vangst aanwezig |
| `get-testscenarios-testcases-rows` | POST | lijst CAS's al in run, per SCE | ✅ vangst aanwezig |
| `{add-action}` | POST | testcase toevoegen | ⏳ vangst nodig — als fallback |
| `{update-result-action}` | POST | resultaat updaten | ⏳ vangst nodig — als fallback |

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
