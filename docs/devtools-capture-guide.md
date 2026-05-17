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



https://superp.testersuite.nl/1/testcycle/2/testrun/2/listtestscenariostoadd
Request Method
POST
Status Code
200 OK
Remote Address
109.235.75.203:443
Referrer Policy
strict-origin-when-cross-origin
cache-control
no-store, no-cache, must-revalidate
connection
Keep-Alive
content-length
3483
content-security-policy
base-uri 'self'; script-src 'self'; worker-src 'self' blob:; object-src 'none';
content-security-policy-report-only
default-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; base-uri 'self'; script-src 'self'; worker-src 'self' blob:; object-src 'none'; frame-src 'none'; frame-ancestors 'none'; form-action 'self'
content-type
application/json; charset=utf-8
date
Sun, 17 May 2026 20:30:59 GMT
expires
Thu, 19 Nov 1981 08:52:00 GMT
keep-alive
timeout=10, max=97
pragma
no-cache
referrer-policy
strict-origin-when-cross-origin
server
Apache
set-cookie
refreshToken=4f22b51576c30c99bb9362356a2c0770ce60d6240a29a8cf4d464ee6490b5f45f505bfd19379b785d8faf2e2826f01c36f8e9ece18d13f00325c5421480d681a; path=/; secure; HttpOnly; SameSite=Lax
strict-transport-security
max-age=31536000; includeSubDomains
x-content-type-options
nosniff
x-frame-options
SAMEORIGIN
accept
*/*
accept-encoding
gzip, deflate, br, zstd
accept-language
nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7
connection
keep-alive
content-length
183
content-type
application/x-www-form-urlencoded; charset=UTF-8
cookie
PHPSESSID=d28065f0d755ed92fecb4a07e111d8af; refreshToken=4f22b51576c30c99bb9362356a2c0770ce60d6240a29a8cf4d464ee6490b5f45f505bfd19379b785d8faf2e2826f01c36f8e9ece18d13f00325c5421480d681a
host
superp.testersuite.nl
origin
https://superp.testersuite.nl
referer
https://superp.testersuite.nl/1/testcycle/2/testrun/2/edit
sec-ch-ua
"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"
sec-ch-ua-mobile
?0
sec-ch-ua-platform
"Windows"
sec-fetch-dest
empty
sec-fetch-mode
cors
sec-fetch-site
same-origin
user-agent
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36
x-requested-with
XMLHttpRequest



Request URL
https://superp.testersuite.nl/1/testcycle/2/testrun/2/get-testscenarios-testcases-rows
Request Method
POST
Status Code
200 OK
Remote Address
109.235.75.203:443
Referrer Policy
strict-origin-when-cross-origin
cache-control
no-store, no-cache, must-revalidate
connection
Keep-Alive
content-security-policy
base-uri 'self'; script-src 'self'; worker-src 'self' blob:; object-src 'none';
content-security-policy-report-only
default-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; base-uri 'self'; script-src 'self'; worker-src 'self' blob:; object-src 'none'; frame-src 'none'; frame-ancestors 'none'; form-action 'self'
content-type
application/json; charset=utf-8
date
Sun, 17 May 2026 20:30:59 GMT
expires
Thu, 19 Nov 1981 08:52:00 GMT
keep-alive
timeout=10, max=98
pragma
no-cache
referrer-policy
strict-origin-when-cross-origin
server
Apache
set-cookie
refreshToken=4f22b51576c30c99bb9362356a2c0770ce60d6240a29a8cf4d464ee6490b5f45f505bfd19379b785d8faf2e2826f01c36f8e9ece18d13f00325c5421480d681a; path=/; secure; HttpOnly; SameSite=Lax
strict-transport-security
max-age=31536000; includeSubDomains
transfer-encoding
chunked
x-content-type-options
nosniff
x-frame-options
SAMEORIGIN
accept
*/*
accept-encoding
gzip, deflate, br, zstd
accept-language
nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7
connection
keep-alive
content-length
83
content-type
application/x-www-form-urlencoded; charset=UTF-8
cookie
PHPSESSID=d28065f0d755ed92fecb4a07e111d8af; refreshToken=4f22b51576c30c99bb9362356a2c0770ce60d6240a29a8cf4d464ee6490b5f45f505bfd19379b785d8faf2e2826f01c36f8e9ece18d13f00325c5421480d681a
host
superp.testersuite.nl
origin
https://superp.testersuite.nl
referer
https://superp.testersuite.nl/1/testcycle/2/testrun/2/edit
sec-ch-ua
"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"
sec-ch-ua-mobile
?0
sec-ch-ua-platform
"Windows"
sec-fetch-dest
empty
sec-fetch-mode
cors
sec-fetch-site
same-origin
user-agent
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36
x-requested-with
XMLHttpRequest
