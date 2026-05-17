# Use cases

Volgorde = wat Tosca tijdens een testrun nodig heeft.

Notatie:

- `{{api_base}}` = officiële Bearer-API base, bv. `https://superp.testersuite.nl.api.testersuite.com`
- `{{ui_base}}` = UI-base, bv. `https://superp.testersuite.nl/1` (`1` = `customer_id`)
- `{{cycle_id}}`, `{{run_id}}` = numerieke IDs (bv. `2` en `2`)
- `{{token}}` = Bearer token (alleen voor `api_base`)

Auth wordt door jou geleverd — deze docs beschrijven alleen de request-shape.

---

## 1. Lookup SCE-code → scenario-id  *(Bearer)*

**Doel:** vertaal `SCE001` naar het interne `scenario_id`.

**Endpoint:** `GET {{api_base}}/test-scenarios?code={{sce_code}}` *(exacte
query-key volgens Stoplight bevestigen; alternatief: `?filter[code]=…`)*

**Headers:**

```
Authorization: Bearer {{token}}
Accept: application/json
```

**Doorgeven:** `data[0].id` → `{{scenario_id}}`.

---

## 2. Lookup CAS-code → testcase-id  *(Bearer)*

**Doel:** binnen een scenario, vertaal `CAS042` naar `testcase_id`.

**Endpoint:** `GET {{api_base}}/test-scenarios/{{scenario_id}}/test-cases?code={{cas_code}}`
*(Stoplight-slug `c65d7cb23d459-test-scenario-test-case`, exacte path bevestigen)*

**Doorgeven:** `data[0].id` → `{{testcase_id}}`.

---

## 3. Lees welke scenarios nog toegevoegd kunnen worden  *(UI)*

**Doel:** UI-keuzelijst opbouwen (debug / verkenning).

**Endpoint:**
`POST {{ui_base}}/testcycle/{{cycle_id}}/testrun/{{run_id}}/listtestscenariostoadd`

**Headers:**

```
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
```

**Body:** form-urlencoded *(payload nog vast te leggen — vermoedelijk leeg
of filter-params)*.

---

## 4. Voeg losse testcase toe aan testrun via scenario  *(UI — vangst nodig)*

**Dit is de kern-actie die Tosca nodig heeft.**

**Endpoint:** `POST {{ui_base}}/testcycle/{{cycle_id}}/testrun/{{run_id}}/{{add-action}}`
— **`{{add-action}}` nog te bepalen** uit
[devtools-capture-guide.md](devtools-capture-guide.md), vangst 1.

**Body (verwacht, form-urlencoded):**

```
scenario_id={{scenario_id}}&testcase_id={{testcase_id}}
```

**Response:** moet het `testrun_testcase_id` opleveren — nodig voor
stap 5/6.

**Waarom via scenario en niet los:** als je puur de `testcase_id` toevoegt
mist het scenario-label in de testrun-weergave. Door zowel `scenario_id`
als `testcase_id` mee te sturen wordt de SCE-naam aan de regel gekoppeld.

---

## 5. Update testcase-resultaat in testrun  *(UI — vangst nodig)*

**Endpoint:** `POST {{ui_base}}/testcycle/{{cycle_id}}/testrun/{{run_id}}/{{update-action}}`
— **vangst 2** uit devtools-capture-guide.

**Body (verwacht):**

```
testrun_testcase_id={{testrun_testcase_id}}&status={{status}}&comment={{comment}}&duration_seconds={{duration_seconds}}
```

Toegestane `status`-waarden nog te bevestigen (vermoeden: `pass`, `fail`,
`blocked`, `not_executed` of numerieke codes).

---

## 6. Verwijder testcase uit testrun (rollback)  *(UI — optioneel)*

Bij setup-fout in Tosca; alleen nuttig als je niet wilt dat een mislukte
case als "blocked" in de run blijft staan.

Endpoint en body volgens dezelfde vangst-procedure.

---

## Welke call hoort bij welk moment in Tosca

```
Tosca StartUp           → 1 (lookup SCE)  → 2 (lookup CAS)
Tosca AddToRun          → 4 (add testcase via scenario)  ← onthoudt testrun_testcase_id
Tosca uitvoer (pass)    → 5 (update result = pass)
Tosca uitvoer (fail)    → 5 (update result = fail, comment = error)
Tosca setup-fout        → 6 (remove)  óf  5 (update = blocked)
```
