# testersuite-tosca-builder

Genereert kant-en-klare HTTP-requestblokken voor Testersuite die je 1-op-1 in
Tosca HTTP-modules kunt plakken. Geen runtime, geen client: puur templating.

## Wat het levert

Per use case één blok met:

- Method + URL (met `{placeholders}` voor IDs)
- Headers (`Authorization: Bearer …`, `Accept: application/json`, evt. `Content-Type`)
- JSON body-template (Tosca-vriendelijk, variabelen tussen `{{…}}`)
- Verwachte response + welke velden door te geven aan de volgende call
- `curl`-voorbeeld om los te testen vóór je het in Tosca zet

## Twee leveringsvormen

- **Python CLI** — `python -m ts_builder <usecase> --key=value …` → blok op stdout
- **Statische HTML** — `index.html` openen in browser → formulier + output panel,
  geen server nodig

Beide lezen dezelfde templates uit `ts_builder/templates.py`.

## Status

Eerste oplevering: docs + scaffold met `{{TBD}}` op de plekken waar de officiële
endpoint of base URL nog bevestigd moet worden. Zie
[`docs/open-questions.md`](docs/open-questions.md) voor wat er nog beantwoord
moet zijn vóór de tweede oplevering.

## Plan en use cases

Beslisplan en flow per Tosca-stap: [`docs/plan.md`](docs/plan.md).
Use cases met exacte request-shape: [`docs/usecases.md`](docs/usecases.md).

**Officiële API (HTTP Basic + JSON:API, bevestigd via Stoplight):**

1. List scenarios in cycle — `GET /{env}/test-scenarios?filter[testCycle]=…`
2. Get one scenario incl. testcases — `GET /{env}/test-scenarios/{id}`
3. Create a test run — `POST /{env}/test-runs`
4. Add testcase to testrun — `POST /{env}/test-runs/{id}/relationships/testCases` *(vermoed, TBD)*
5. Update result — `PATCH /{env}/test-run-test-cases/{id}` *(vermoed, TBD)*

**UI fallback (form-urlencoded + sessie):**

- `POST {ui_base}/testcycle/{cy}/testrun/{rn}/listtestscenariostoadd` *(captured)*
- `POST {ui_base}/testcycle/{cy}/testrun/{rn}/get-testscenarios-testcases-rows` *(captured)*
- Add / update / remove — vangst nodig als de officiële endpoints (4/5) niet bestaan.

## Quickstart

```bash
# CLI
python -m ts_builder lookup-scenario --code=SCE001 --token=$TS_TOKEN

# HTML
open index.html
```
