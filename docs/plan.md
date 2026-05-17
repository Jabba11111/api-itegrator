# Plan

## Doel

Vanuit Tosca Tricentis, tijdens een lopende testrun in Testersuite:

1. Een testcase (`CAS<nr>`) toevoegen aan de testrun, **via** het scenario
   waar die case in hoort (`SCE<nr>`), zodat in de testrun de scenario-naam
   bij de case staat.
2. Het resultaat van die case (pass/fail/blocked) wegschrijven in de testrun.

Authenticatie is door jou opgelost — dit plan beschrijft alleen de
request-shapes (method, URL, headers, body) per call.

## Belangrijke vondsten uit Stoplight

- **Auth = Basic** (`Authorization: Basic <base64(user:pass)>`), niet Bearer.
- **URL-patroon**: `https://{customer}.testersuite.nl.api.testersuite.com/{environmentId}/<resource>`.
  De `{environmentId}` is dezelfde `1` die in de UI-URL staat (`/1/testcycle/2/...`).
- **JSON:API** — alle requests/responses zijn `application/vnd.api+json`,
  met de structuur `{ "data": { "type", "id", "attributes", "relationships" } }`.
- **`POST /{env}/test-runs` bestaat officieel**. Een test run heeft van
  zichzelf relationships `testScenarios` en `testCases` — er is dus zeer
  waarschijnlijk een JSON:API relationship-endpoint om scenarios/cases aan
  een bestaande run toe te voegen, zonder UI-endpoints.

Dit zou kunnen betekenen dat we de UI-endpoints helemaal **niet nodig
hebben**. Dat hangt af van twee Stoplight-pagina's die ik nog niet heb
gezien — zie [open-questions.md](open-questions.md).

## Twee API-werelden — herziene status

| Wereld | Base URL | Auth | Format | Status voor ons doel |
|---|---|---|---|---|
| Officiële API | `https://{customer}.testersuite.nl.api.testersuite.com` | Basic | JSON:API | Bevestigd voor lookup + test run create. Toevoegen aan run en resultaat: **misschien** ook hier, te bevestigen. |
| UI / web-app | `https://{customer}.testersuite.nl/{customer_id}/…` | sessie | form-urlencoded | Fallback als de officiële API de write-acties niet biedt. |

## Lookup SCE-code → scenario_id — herzien

Er is **geen `?code=` filter** op `/test-scenarios`. Wat wel kan:

- `filter[testCycle]={cycle_id}` — geeft alle scenarios binnen een
  testcyclus, met `page[offset]` pagineren.
- `filter[customField_*]=…` — alleen als de SCE-code als custom field
  geconfigureerd is in jouw Testersuite-instance.

Mogelijke aanpakken (volgorde van voorkeur):

1. **Direct via ID:** als jouw Tosca-test al het numerieke scenario_id kent
   (niet de SCE-code), sla de lookup over.
2. **Custom field filter:** als SCE-code een custom field is (bv. customField19),
   gebruik `?filter[customField19]=SCE001`.
3. **Lijst + client-side filter:** haal `GET /test-scenarios?filter[testCycle]={cycle_id}&page[offset]=…`,
   pagineren, en in Tosca/JSON-pad de juiste record op `code` matchen.

Idem voor CAS-code → testcase_id.

## Stappen in de Tosca-runtime — herzien (ronde 3)

```
Per CAS die Tosca uitvoert:

1. (optioneel) lookup scenario   GET  /{env}/test-scenarios?filter[testCycle]=…
                                   match attributes.businessId == "SCE<nr>"
2. (optioneel) lookup testcase   GET  /{env}/test-scenarios/{scenario_id}
                                   filter included[] op type=testCase,
                                   match attributes.businessId == "CAS<nr>"
3. add testcase to run           POST  /{env}/test-runs/{run_id}/test-cases
                                   body: testDesignTestCase relationship  ✅ OFFICIEEL
4. Tosca voert uit
5. update result                 PATCH /{env}/test-runs/{run_id}/test-cases/{trtc_id}
                                   body: attributes.status + executionStatus FK  ✅ PAD
```

Stap 3 officieel bevestigd. Stap 5 pad bevestigd (zelfde URL als GET);
body-shape per JSON:API-conventie, body wel nog te valideren tegen
echte response.

**Belangrijke vraag bij stap 3:** of het scenario-label automatisch
verschijnt naast de toegevoegde case in de testrun-weergave (zie
[open-questions.md](open-questions.md#scenario-label)). Als niet, dan UI
fallback voor stap 3 inzetten.

## Wat dit project oplevert

Onveranderd:

- **`docs/`** — specificatie naast Tosca.
- **`ts_builder/` (Python CLI)** — Tosca-klare request-blokken.
- **`index.html` (statische builder)** — zelfde, browser-versie.

## Volgordeplan

| Ronde | Wat | Status |
|---|---|---|
| 1 | Scaffold + docs met TBD | ✅ |
| 2 | Basic auth + JSON:API + environmentId verwerkt; nieuwe usecases (create-test-run) | ✅ deze commit |
| 3 | Stoplight: bevestig of "add scenario aan run" en "update result" officieel bestaan | ⏳ wacht op input |
| 4 | Templates dichtschroeven, voorbeeld-curls valideren tegen jouw account | — |
