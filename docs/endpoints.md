# Endpoints — inventaris en status

## Twee oppervlakken

| Soort | Base URL | Voorbeeld |
|---|---|---|
| Officiële API (Bearer) | `https://{customer}.testersuite.nl.api.testersuite.com` | `https://superp.testersuite.nl.api.testersuite.com` |
| UI / web-app (sessie) | `https://{customer}.testersuite.nl/{customer_id}` | `https://superp.testersuite.nl/1` |

## Officiële API — gedocumenteerd op Stoplight

| Endpoint | Stoplight-slug | Gebruikt voor |
|---|---|---|
| `GET /test-scenarios` (retrieve all) | `c8e3fae5e8e81-retrieve-all` | lijst alle SCE's, filter op `code` |
| `GET /test-scenarios/{id}` | `154d1c8cdb722-get-a-test-scenario` | één SCE ophalen |
| `… test-scenario-test-case` | `c65d7cb23d459-test-scenario-test-case` | testcases binnen een SCE |
| `… test-scenario` (collection) | `273a0d26ebfde-test-scenario` | CRUD op SCE-resource |

Exacte paths, query-parameters en response-schemas komen uit de Stoplight-
pagina's — die zijn gated (login-required), dus ik kan ze niet automatisch
inlezen. Plak de relevante "Request" en "Response"-secties in
[open-questions.md](open-questions.md#stoplight-bodies) en ik vul ze in.

## UI-endpoints — vastgelegd via DevTools

URL-patroon:

```
https://{customer}.testersuite.nl/{customer_id}/testcycle/{cycle_id}/testrun/{run_id}/{action}
```

| Action | Method | Doel | Status |
|---|---|---|---|
| `listtestscenariostoadd` | POST | lijst SCE's die nog aan testrun toegevoegd kunnen worden | ✅ vangst aanwezig |
| `get-testscenarios-testcases-rows` | POST | lijst CAS's die al in de testrun zitten, gegroepeerd per SCE | ✅ vangst aanwezig |
| `{add-action}` | POST | losse testcase toevoegen aan testrun via scenario | ⏳ vangst nodig |
| `{update-result-action}` | POST/PATCH | resultaat van een testcase in de testrun updaten | ⏳ vangst nodig |

`Content-Type` van de UI-calls is `application/x-www-form-urlencoded`,
geen JSON. Response is wel `application/json`.

Zie [devtools-capture-guide.md](devtools-capture-guide.md) voor hoe je de
twee ⏳ vangsten maakt.

## Bekende voorbeeld-IDs (uit jouw vangst)

- `customer` = `superp`
- `customer_id` = `1`
- `cycle_id` = `2`
- `run_id` = `2`

Voorbeeld-URL die werkt in jouw account:

```
POST https://superp.testersuite.nl/1/testcycle/2/testrun/2/listtestscenariostoadd
```
