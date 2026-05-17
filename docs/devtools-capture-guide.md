# DevTools-vangst — handleiding

Voor twee acties is er nog geen officiële API-documentatie en is er ook
geen captured UI-call. Vang ze zelf één keer in DevTools en deel hier de
output — daarna kan ik de templates definitief maken.

## Wat opslaan per call

Voor elke vangst:

- **Request URL** (volledig, met query-string)
- **Request Method** (POST / PATCH / DELETE)
- **Request payload** — tab "Payload" in Chrome DevTools, óf bij
  `application/x-www-form-urlencoded` de form-data key/values
- **Response body** (eerste paar regels is genoeg, vooral het antwoord op
  "wat is het ID van wat ik net heb toegevoegd?")
- **`Content-Type` request-header** (form-urlencoded vs json maakt uit)

Authenticatie-headers (`Cookie: PHPSESSID=…`, CSRF-tokens) hoeven niet
in deze vangst — jij regelt auth zelf.

## Vangst 1 — Testcase toevoegen aan testrun

1. Open een testrun in de UI: `…/testcycle/2/testrun/2/edit`.
2. Open DevTools → tab **Network** → filter `Fetch/XHR`.
3. Voeg via de UI één testcase toe vanuit een scenario:
   - kies scenario `SCE…`
   - kies één testcase `CAS…`
   - klik op "Toevoegen" of equivalent
4. Zoek in de Network-tab de POST/PATCH die op dat moment afgaat
   (niet `listtestscenariostoadd` of `get-testscenarios-testcases-rows`
   — die zijn al bekend en zijn read-calls).
5. Kopieer URL, method, payload, response zoals hierboven.

## Vangst 2 — Resultaat van testcase updaten

1. Zelfde testrun, zelfde DevTools-tab.
2. Markeer een testcase als **Passed** (of Failed / Blocked).
3. Vang de bijbehorende POST/PATCH.
4. Idem voor opmerking-veld als dat separaat verzonden wordt.

## Vangst 3 — Compleet scenario toevoegen (optioneel maar nuttig)

Als je liever in één keer alle CAS van een SCE wilt toevoegen i.p.v.
per stuk: vang de POST die afgaat als je in de UI "scenario toevoegen"
kiest in plaats van losse testcase.

## Plak hier (placeholder)

Vervang dit blok later met de echte vangst:

```
### Add-testcase-to-run
URL:
Method:
Content-Type:
Payload:
Response (relevant deel):

### Update-result
URL:
Method:
Content-Type:
Payload:
Response (relevant deel):
```
