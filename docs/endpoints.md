# Endpoints — inventaris en status

| # | Endpoint | Bron | Status | Auth |
|---|---|---|---|---|
| 1 | `GET /test-scenarios` | Stoplight "retrieve all test scenarios" | officieel | Bearer |
| 2 | `GET /test-scenarios/{id}` | Stoplight "get a test scenario" | officieel | Bearer |
| 3 | `GET /test-scenarios/{id}/test-cases` | Stoplight "scenario-testcase" | officieel | Bearer |
| 4 | `POST /test-runs/{run_id}/scenarios` | — | **TBD** (vermoedelijk officieel) | Bearer? |
| 5 | `POST /test-runs/{run_id}/test-cases` | — | **TBD** | Bearer? |
| 6 | `PATCH /test-runs/{run_id}/test-cases/{id}` | — | **TBD** | Bearer? |
| 7 | `DELETE /test-runs/{run_id}/test-cases/{id}` | — | **TBD** | Bearer? |
| 8 | `POST /testrun/listtestscenariostoadd` | DevTools (UI) | UI-only | sessie (PHPSESSID) |
| 9 | `POST /testrun/get-testscenarios-testcases-rows` | DevTools (UI) | UI-only | sessie (PHPSESSID) |

## Base URLs

| Soort | URL | Wanneer gebruiken |
|---|---|---|
| Officiële API | `https://{{customer}}.testersuite.nl.api.testersuite.com` | endpoints 1–7 (Bearer) |
| UI | `https://superp.testersuite.nl/{{customer_id}}/` | endpoints 8–9 (alleen als 4–7 niet bestaan) |

**Patroon:** de officiële API hangt onder `api.testersuite.com` met de
klant-subdomein als prefix. Voorbeeld: `https://superp.testersuite.nl.api.testersuite.com`.
De resource-paden onder die base staan in de [Stoplight-docs](https://stoplight.io/) —
zie [open-questions](open-questions.md) punt 2 voor wat ik nog moet uitvinden over
de testrun-endpoints.

## Auth

- **Bearer**: `Authorization: Bearer <token>` — voor de officiële API.
- **Sessie**: `Cookie: PHPSESSID=…` — alleen UI-endpoints. Verkrijgen via login-flow, niet geschikt voor gescripte Tosca-runs zonder extra werk.

## Beslisboom

```
Bestaan endpoint 4–7 officieel?
├─ Ja  → alles via Bearer, klaar.
├─ Nee → endpoints 8–9 (UI) gebruiken
│         └─ Bearer werkt daar niet → sessie-login flow toevoegen aan builder
└─ Onbekend → eerst Stoplight checken (zie open-questions.md)
```
