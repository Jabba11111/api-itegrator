# Use cases

Volgorde = wat Tosca tijdens een testrun nodig heeft.

In alle voorbeelden:

- `{{base_url}}` = `https://{customer}.testersuite.nl.api.testersuite.com`
  (vervang `{customer}` door je eigen subdomein, bv. `superp`)
- `{{token}}` = Bearer access token
- `{{cycle_id}}`, `{{run_id}}` = numerieke IDs van de testcyclus en de testrun

---

## 1. Lookup SCE-code → scenario-id

**Doel:** vertaal een SCE-code (bv. `SCE001`) naar het interne `scenario_id`.

**Endpoint:** `GET {{base_url}}/test-scenarios?code={{sce_code}}` *(TBD bevestigen)*

**Headers:**

```
Authorization: Bearer {{token}}
Accept: application/json
```

**Response (verwacht):**

```json
{ "data": [ { "id": 123, "code": "SCE001", "name": "..." } ] }
```

**Doorgeven aan volgende call:** `data[0].id` → `{{scenario_id}}`

---

## 2. Lookup CAS-code → testcase-id

**Doel:** binnen een scenario, vertaal een CAS-code (bv. `CAS042`) naar `testcase_id`.

**Endpoint:** `GET {{base_url}}/test-scenarios/{{scenario_id}}/test-cases?code={{cas_code}}` *(TBD bevestigen)*

**Headers:** zelfde als hierboven.

**Response (verwacht):**

```json
{ "data": [ { "id": 9876, "code": "CAS042", "name": "..." } ] }
```

**Doorgeven:** `data[0].id` → `{{testcase_id}}`

---

## 3. Voeg scenario toe aan testrun

**Doel:** alle testcases uit een SCE in één keer aan een lopende testrun koppelen.

**Endpoint:** `POST {{base_url}}/test-runs/{{run_id}}/scenarios` **(TBD — bestaat dit officieel?)**

**Fallback (UI-endpoint):** `POST https://superp.testersuite.nl/{{customer_id}}/testrun/listtestscenariostoadd`
— vereist sessie-auth (PHPSESSID), niet Bearer.

**Body:**

```json
{ "scenario_id": {{scenario_id}} }
```

**Response:** lijst van toegevoegde testcase-IDs.

---

## 4. Voeg losse testcase toe aan testrun via scenario

**Doel:** specifieke CAS aan testrun koppelen, mét scenario-naam zichtbaar.

**Endpoint:** `POST {{base_url}}/test-runs/{{run_id}}/test-cases` **(TBD)**

**Body:**

```json
{
  "scenario_id": {{scenario_id}},
  "testcase_id": {{testcase_id}}
}
```

**Response:** het aangemaakte `testrun_testcase_id` (nodig voor stap 5).

---

## 5. Update testcase-resultaat in testrun

**Doel:** Tosca-uitvoer (pass/fail/blocked + opmerking + duur) terugschrijven.

**Endpoint:** `PATCH {{base_url}}/test-runs/{{run_id}}/test-cases/{{testrun_testcase_id}}` **(TBD)**

**Body:**

```json
{
  "status": "{{status}}",
  "comment": "{{comment}}",
  "duration_seconds": {{duration_seconds}}
}
```

Toegestane `status`-waarden: `pass`, `fail`, `blocked`, `not_executed` *(TBD bevestigen)*.

---

## 6. Verwijder testcase uit testrun (rollback)

**Doel:** als Tosca de case niet kon uitvoeren door een setup-fout.

**Endpoint:** `DELETE {{base_url}}/test-runs/{{run_id}}/test-cases/{{testrun_testcase_id}}` **(TBD)**

**Response:** `204 No Content`.
