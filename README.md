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

## Use cases

Volledige beschrijving in [`docs/usecases.md`](docs/usecases.md).

1. Lookup SCE-code → scenario-id
2. Lookup CAS-code → testcase-id (binnen een scenario)
3. Voeg scenario toe aan testrun
4. Voeg losse testcase toe aan testrun via scenario
5. Update testcase-resultaat in testrun (pass/fail/blocked)
6. Verwijder testcase uit testrun (rollback)

## Quickstart

```bash
# CLI
python -m ts_builder lookup-scenario --code=SCE001 --token=$TS_TOKEN

# HTML
open index.html
```
