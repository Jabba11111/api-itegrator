# Plan

## Doel

Vanuit Tosca Tricentis, tijdens een lopende testrun in Testersuite:

1. Een testcase (`CAS<nr>`) toevoegen aan de testrun, **via** het scenario
   waar die case in hoort (`SCE<nr>`), zodat in de testrun de scenario-naam
   bij de case staat.
2. Het resultaat van die case (pass/fail/blocked) wegschrijven in de testrun.

Authenticatie is door jou opgelost — dit plan beschrijft alleen de
request-shapes (method, URL, headers, body) per call.

## Twee API-werelden, één flow

Testersuite heeft twee gescheiden HTTP-oppervlakken:

| Wereld | Base URL | Geschikt voor |
|---|---|---|
| Officiële API (Bearer) | `https://{customer}.testersuite.nl.api.testersuite.com` | **Lezen** van scenarios en testcases. Stoplight-gedocumenteerd. |
| UI / web-app (sessie) | `https://{customer}.testersuite.nl/{customer_id}/…` | **Schrijven** naar testruns (toevoegen, resultaten). Niet publiek gedocumenteerd; bekend uit DevTools. |

Voor de gevraagde flow (toevoegen aan testrun + resultaat updaten) zijn de
write-acties op dit moment alleen via de UI-wereld bekend. De Bearer-API
biedt lookup (codes → IDs).

## Stappen in de Tosca-runtime

Per CAS die Tosca uitvoert:

```
[Tosca] → genereer request → [Testersuite]                tool van deze repo
─────────────────────────────────────────────────────     ─────────────────
1. lookup scenario  GET   ……/test-scenarios?code=SCE…     ts-builder lookup-scenario
2. lookup testcase  GET   ……/test-scenarios/{id}/...      ts-builder lookup-testcase
3. add to testrun   POST  …/testrun/{run_id}/add-…        ts-builder add-testcase-to-run
4. (Tosca voert uit, krijgt pass/fail)
5. update result    POST/PATCH …/testrun/{run_id}/…       ts-builder update-result
```

Stap 1 en 2 staan officieel beschreven (Stoplight). Stap 3 en 5 zijn de twee
calls die we nog moeten **vastleggen via DevTools** — zie
[devtools-capture-guide.md](devtools-capture-guide.md).

## Bekende endpoints (vandaag)

Uit jouw DevTools-vangst:

```
POST https://superp.testersuite.nl/1/testcycle/2/testrun/2/listtestscenariostoadd
POST https://superp.testersuite.nl/1/testcycle/2/testrun/2/get-testscenarios-testcases-rows
```

Patroon:

```
https://{customer}.testersuite.nl/{customer_id}/testcycle/{cycle_id}/testrun/{run_id}/{action}
```

Concrete waarden in jouw voorbeeld: `customer=superp`, `customer_id=1`,
`cycle_id=2`, `run_id=2`.

Beide zijn **lees**-calls (lijsten ophalen). De daadwerkelijke add- en
update-acties zijn nog niet vastgelegd.

## Wat dit project oplevert

- **`docs/`** — specificatie die je naast Tosca kunt leggen.
- **`ts_builder/` (Python CLI)** — `python -m ts_builder <usecase> key=value …`
  print het Tosca-klare request-blok op stdout.
- **`index.html` (statische builder)** — zelfde, maar als formuliertje in de
  browser, geen Python nodig.

Beide vullen placeholders in en produceren een blok met method, URL,
headers, body en een copy-paste `curl`. Geen runtime-call, geen client —
zodat dit project niet hoeft te weten wat jouw auth-flow is.

## Volgordeplan

| Ronde | Wat | Status |
|---|---|---|
| 1 | Scaffold + docs met `{{TBD}}` op de write-acties | ✅ deze commit |
| 2 | Stoplight-bodies inlezen + DevTools-vangst van add/update | ⏳ wacht op input |
| 3 | Templates dichtschroeven, `{{TBD}}` weghalen, voorbeeld-curls validéren | — |
| 4 | (optioneel) batch-mode in CLI: één Tosca-run = één commando | — |

## Wat ik van jou nodig heb voor ronde 2

Zie [open-questions.md](open-questions.md). Korte versie:

1. Drie Stoplight-pagina's: paste de "Request" en "Response"-secties voor:
   - retrieve-all test scenarios
   - get-a-test-scenario
   - test-scenario-test-case
2. DevTools-vangst van twee acties in de UI:
   - klik op **"Toevoegen"** bij een scenario/testcase in een testrun
   - markeer een testcase als **Passed / Failed** in een testrun
   (zie [devtools-capture-guide.md](devtools-capture-guide.md))
3. Vocabulaire voor resultaatstatus: welke waarden mag `status` hebben?
