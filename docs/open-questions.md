# Open vragen — beantwoorden vóór ronde 2

## 1. Base URLs — BEANTWOORD

| Wereld | Patroon |
|---|---|
| Officiële API | `https://{customer}.testersuite.nl.api.testersuite.com` |
| UI | `https://{customer}.testersuite.nl/{customer_id}` |

Voorbeeld: `customer=superp`, `customer_id=1`, `cycle_id=2`, `run_id=2`.

Verwerkt in CLI defaults en `index.html`.

**Sub-vraag (mini):** zit er een versie-prefix (`/v1/`, `/api/`) tussen
de API-base en de resource-paden? Bij voorkeur uit Stoplight "Servers"-sectie.

## 2. Stoplight-bodies <a id="stoplight-bodies"></a>

De vier Stoplight-pagina's zijn voor mij gated (403 zonder login). Plak
hieronder per pagina de "Request" + "Response"-secties, of schroef in
[`usecases.md`](usecases.md) zelf de query-keys aan.

**Pagina's:**

- `c8e3fae5e8e81-retrieve-all` — retrieve all test scenarios
- `154d1c8cdb722-get-a-test-scenario` — get a test scenario
- `c65d7cb23d459-test-scenario-test-case` — scenario↔testcase
- `273a0d26ebfde-test-scenario` — test-scenario resource

Specifiek nodig:

- Exacte query-key om op `code` te filteren (`?code=…` vs `?filter[code]=…`)
- Exact path voor testcases-binnen-scenario
- Response-veldnamen (`id` vs `scenario_id`, `data` vs `result`, etc.)

## 3. DevTools-vangst van write-acties

Twee calls die we nog niet hebben — vang ze één keer in DevTools volgens
[`devtools-capture-guide.md`](devtools-capture-guide.md):

- **Add-testcase-to-run** (klik "Toevoegen" op een CAS in een testrun)
- **Update-result** (markeer een CAS als Passed / Failed)

## 4. Status-vocabulaire

Welke waarden accepteert Testersuite voor het resultaat van een testcase?
Vermoeden: `pass`, `fail`, `blocked`, `not_executed`. Of zijn het
numerieke codes (1/2/3)? Bevestigen via vangst 2.

## 5. Authenticatie — door jou opgelost

Jij regelt zelf hoe je een Bearer-token verkrijgt en hoe je een
PHPSESSID-sessie krijgt voor de UI-calls. Deze repo neemt daar geen
positie in en stopt geen auth-flow in de templates — alleen het
`Authorization: Bearer …` header-veld voor Bearer-calls.
