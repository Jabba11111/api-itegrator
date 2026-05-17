# Tosca-flow — testcase uitvoeren en resultaat in Testersuite

## Twee modellen

| Model | Wat Tosca doet | Wat tester handmatig doet | Geschikt voor |
|---|---|---|---|
| **A. Lookup + PATCH** (aanbevolen) | result wegschrijven per CAS | testrun aanmaken + scenarios/cases via UI toevoegen (geeft SCE-badge) | de meeste situaties |
| **B. Volledig dynamisch** | scenarios én cases toevoegen aan run en daarna result wegschrijven | alleen design (cases in scenarios) bijhouden | als Tosca per-run varieert in welke cases |

Model A gebruikt alleen officiële Bearer/Basic API + één HTML-lookup.
Model B vereist daarnaast de UI-form-POST met sessie-auth en CSRF.

---

## Model A — Lookup + PATCH (aanbevolen)

### Aannames

- De testrun bestaat al (handmatig aangemaakt).
- De gewenste scenarios + cases zijn handmatig via de Testersuite-UI aan
  de run toegevoegd (geeft SCE-badge automatisch).
- Per CAS heeft Tosca de CAS-code beschikbaar (bv. `CAS41`).

### Globale Tosca-buffers

| Buffer | Voorbeeld |
|---|---|
| `TS_API_BASE` | `https://superp.testersuite.nl.api.testersuite.com` |
| `TS_UI_BASE` | `https://superp.testersuite.nl/1` |
| `TS_ENV` | `1` |
| `TS_BASIC` | `<base64(user:pass)>` |
| `TS_RUN_ID` | `92` |
| `TS_OK_STATUS_ID` | `?` (te bepalen, 1=notstarted en 4=notok zijn bekend) |
| `TS_NOTOK_STATUS_ID` | `4` |

### Module 1 — Lijst alle trtcs in de run

| Veld | Waarde |
|---|---|
| Method | `GET` |
| URL | `{TS_UI_BASE}/papi/testscenario/RUN{TS_RUN_ID}/testcases` |
| Header | `Cookie: PHPSESSID={TS_SESSION}` |
| Header | `X-Requested-With: XMLHttpRequest` |

**Response:** HTML met één `<tr>` per trtc:

```html
<tr databaseid="447" relationid="447" businessid="CAS41">
    <a runsce_id="2">SCE3</a>
    <td class="testcase-shortdescription">test voor test scenario</td>
    ...
</tr>
```

**Parse:** voor elk `<tr>` met `databaseid` attribuut:
- `databaseid` → `trtc_id`
- `businessid` → CAS-code (`CAS41`)
- (optioneel) inhoud van `<a runsce_id="…">` → SCE-tekst voor verificatie

**Buffer:** voor de CAS-code die Tosca nu uitvoert, vind de match in de lijst
en sla `trtc_id` op.

**Cache-tip:** doe Module 1 één keer bij het begin van de Tosca-batch en
bewaar de hele mapping `CAS_CODE → trtc_id` als Tosca Data Resource.

### Module 2 — Tosca eigen test

Voer de geautomatiseerde acties uit. Zet aan het einde:

- `TOSCA_RESULT` = `"ok"` of `"notok"`
- `EXEC_STATUS_ID` = `{TS_OK_STATUS_ID}` of `{TS_NOTOK_STATUS_ID}`

### Module 3 — Update resultaat

| Veld | Waarde |
|---|---|
| Method | `PATCH` |
| URL | `{TS_API_BASE}/{TS_ENV}/test-runs/{TS_RUN_ID}/test-cases/{trtc_id}` |
| Header | `Authorization: Basic {TS_BASIC}` |
| Header | `Content-Type: application/vnd.api+json` |
| Header | `Accept: application/vnd.api+json` |
| Body | zie hieronder |

```json
{
  "data": {
    "type": "testRunTestCase",
    "id": "{trtc_id}",
    "attributes": { "status": "{TOSCA_RESULT}" },
    "relationships": {
      "executionStatus": {
        "data": { "id": "{EXEC_STATUS_ID}", "type": "testRunTestCaseStatus" }
      }
    }
  }
}
```

### Volgorde

```
Eenmaal per Tosca-batch:
  └─ Module 1: GET trtcs → cache CAS_CODE → trtc_id mapping

Per testcase in de Tosca ExecutionList:
  ├─ lookup trtc_id uit cache
  ├─ Module 2: Tosca steps → TOSCA_RESULT, EXEC_STATUS_ID
  └─ Module 3: PATCH result
```

---

## Model B — Volledig dynamisch (zwaarder, alleen als nodig)

Als Tosca ook scenarios + cases aan de run moet kunnen toevoegen.
Vereist mimicry van de UI-edit-form. Zie
[`samples/ui-edit-testrun-submit.json`](samples/ui-edit-testrun-submit.json).

### Extra modules

#### Module A — Haal edit-form op (voor CSRF en huidige state)

| Veld | Waarde |
|---|---|
| Method | `GET` |
| URL | `{TS_UI_BASE}/testcycle/{TS_CYCLE_ID}/testrun/{TS_RUN_ID}/edit` |
| Header | `Cookie: PHPSESSID={TS_SESSION}` |

**Parse uit HTML:**
- CSRF-token (uit een `<input name="csrft" value="…">` of `<meta>`)
- Bestaande `testruntestscenariotestcases[…]` entries (loop door alle form-velden)
- Run-metadata (naam, descriptions, dates, tester)

#### Module B — Submit met nieuwe entries

| Veld | Waarde |
|---|---|
| Method | `POST` |
| URL | `{TS_UI_BASE}/testcycle/{TS_CYCLE_ID}/testrun/{TS_RUN_ID}/edit` |
| Header | `Cookie: PHPSESSID={TS_SESSION}` |
| Header | `Content-Type: application/x-www-form-urlencoded` |
| Header | `Origin: {TS_UI_BASE_ORIGIN}` |
| Header | `Referer: {TS_UI_BASE}/testcycle/{TS_CYCLE_ID}/testrun/{TS_RUN_ID}/edit` |
| Body | volledige form-body met alle bestaande velden plus nieuwe entries |

**Nieuwe entry per CAS toe te voegen:**

```
testruntestscenariotestcases[new__<random_hex>][relationId]=
testruntestscenariotestcases[new__<random_hex>][testscenarioId]=<design SCE-id>
testruntestscenariotestcases[new__<random_hex>][testcaseId]=<design CAS-id>
testruntestscenariotestcases[new__<random_hex>][testerId]=USR1
testruntestscenariotestcases[new__<random_hex>][resetStatus]=0
```

`<random_hex>` mag elke string zijn die nog niet als key gebruikt is
binnen deze POST (bv. een uuid zonder streepjes).

**Verwacht:** `302` redirect (volg de location niet, het was succesvol).

#### Module C — Refresh om nieuwe trtc_id te vinden

Run Module 1 (uit Model A) opnieuw. Nieuwe rijen verschijnen met
toegekende `databaseid` (= nieuwe trtc_id).

### Foutgevoeligheden Model B

- **CSRF rotates** per sessie en kan tijdens lange runs verlopen
- **Sessie-cookie** (`PHPSESSID`) verloopt na inactiviteit
- **Race-conditions** als anderen tegelijk de testrun bewerken
- **Brittle:** bij UI-update aan Testersuite-zijde kan de form-structuur
  veranderen → Tosca-flow breekt zonder waarschuwing

---

## Valkuil: vier soorten ID's

Verwar ze niet:

| Soort | Voorbeeld | Waar te vinden |
|---|---|---|
| **design testCase id** | `41` | `included[type=testCase].id` of `[testcaseId]=41` |
| **design testScenario id** | `3` | `[testscenarioId]=3`, of `attributes.businessId=="SCE3"` |
| **testRunTestCase id (trtc_id)** | `447` | `databaseid="447"` in HTML, `id` in API response |
| **testRunTestScenario id (runsce_id)** | `2` | `runsce_id="2"` in HTML (run-interne SCE-instantie) |

Voor PATCH gebruik je altijd `trtc_id`. Voor de UI-form-POST gebruik
je de design IDs. `runsce_id` zie je alleen ter info.

---

## Foutafhandeling per call

| HTTP-code | Betekenis | Actie |
|---|---|---|
| `200/201` | OK | door |
| `302` | redirect na form-submit | succes, volg location niet |
| `400` | bad request / form-validatie | log body, stop |
| `401/403` | auth / sessie-issue | refresh sessie of stop |
| `404` | resource niet gevonden | check ID-soort (design vs trtc!) |
| `409` | conflict (al toegevoegd) | gebruik bestaande trtc |
| `5xx` | server fout | retry 2× met backoff |
