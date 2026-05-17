"""Use-case templates. Each entry produces a request block when rendered.

Two surface kinds:
- "official": Stoplight API. JSON:API format, HTTP Basic auth.
- "ui":       web-app endpoint. form-urlencoded, session auth.
"""

import json as _json
from string import Template
from urllib.parse import urlencode

USECASES = {
    "list-scenarios": {
        "title": "List test scenarios in a cycle",
        "surface": "official",
        "method": "GET",
        "url": "$api_base/$env/test-scenarios?filter[testCycle]=$cycle_id&page[offset]=0",
        "headers": {
            "Authorization": "Basic $basic",
            "Accept": "application/vnd.api+json",
        },
        "body": None, "body_form": None,
        "expected_status": 200,
        "extract": "data[].id, attributes.* -> match SCE-code client-side",
        "status": "official",
        "params": ["api_base", "env", "basic", "cycle_id"],
    },
    "get-scenario": {
        "title": "Get one scenario (incl. testcases via included[])",
        "surface": "official",
        "method": "GET",
        "url": "$api_base/$env/test-scenarios/$scenario_id",
        "headers": {
            "Authorization": "Basic $basic",
            "Accept": "application/vnd.api+json",
        },
        "body": None, "body_form": None,
        "expected_status": 200,
        "extract": "included[type=testCase] -> match CAS-code -> testcase_id",
        "status": "official",
        "params": ["api_base", "env", "basic", "scenario_id"],
    },
    "create-test-run": {
        "title": "Create a test run",
        "surface": "official",
        "method": "POST",
        "url": "$api_base/$env/test-runs",
        "headers": {
            "Authorization": "Basic $basic",
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json",
        },
        "body": {
            "data": {
                "type": "testRun",
                "attributes": {
                    "shortDescription": "$short_description",
                    "longDescription": "$long_description",
                    "startDate": "$start_date",
                    "endDate": "$end_date",
                },
                "relationships": {
                    "testCycle": {
                        "data": {"id": "$cycle_id", "type": "testCycle"}
                    }
                },
            }
        },
        "body_form": None,
        "expected_status": 201,
        "extract": "data.id -> run_id",
        "status": "official",
        "params": ["api_base", "env", "basic", "cycle_id",
                   "short_description", "long_description",
                   "start_date", "end_date"],
    },
    "add-testcase-to-run-official": {
        "title": "Add testcase to testrun (JSON:API relationship — TBD)",
        "surface": "official",
        "method": "POST",
        "url": "$api_base/$env/test-runs/$run_id/relationships/testCases",
        "headers": {
            "Authorization": "Basic $basic",
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json",
        },
        "body": {
            "data": [
                {
                    "type": "testCase",
                    "id": "$testcase_id",
                    "meta": {"scenarioId": "$scenario_id"},
                }
            ]
        },
        "body_form": None,
        "expected_status": 200,
        "extract": "trtc_id (uit response, structuur TBD)",
        "status": "TBD — endpoint vermoed, Stoplight bevestigen",
        "params": ["api_base", "env", "basic", "run_id",
                   "scenario_id", "testcase_id"],
    },
    "update-result-official": {
        "title": "Update testcase result in testrun (TBD)",
        "surface": "official",
        "method": "PATCH",
        "url": "$api_base/$env/test-run-test-cases/$trtc_id",
        "headers": {
            "Authorization": "Basic $basic",
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json",
        },
        "body": {
            "data": {
                "type": "testRunTestCase",
                "id": "$trtc_id",
                "attributes": {
                    "status": "$status",
                    "comment": "$comment",
                    "durationSeconds": "$duration_seconds",
                },
            }
        },
        "body_form": None,
        "expected_status": 200,
        "extract": None,
        "status": "TBD — endpoint vermoed, Stoplight bevestigen",
        "params": ["api_base", "env", "basic", "trtc_id",
                   "status", "comment", "duration_seconds"],
    },
    "list-scenarios-to-add-ui": {
        "title": "List addable scenarios (UI, captured)",
        "surface": "ui",
        "method": "POST",
        "url": "$ui_base/testcycle/$cycle_id/testrun/$run_id/listtestscenariostoadd",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json",
        },
        "body": None, "body_form": {},
        "expected_status": 200,
        "extract": "lijst SCE's",
        "status": "captured",
        "params": ["ui_base", "cycle_id", "run_id"],
    },
    "list-run-testcases-ui": {
        "title": "List testcases in testrun (UI, captured)",
        "surface": "ui",
        "method": "POST",
        "url": "$ui_base/testcycle/$cycle_id/testrun/$run_id/get-testscenarios-testcases-rows",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json",
        },
        "body": None, "body_form": {},
        "expected_status": 200,
        "extract": "rows",
        "status": "captured",
        "params": ["ui_base", "cycle_id", "run_id"],
    },
    "add-testcase-to-run-ui": {
        "title": "Add testcase to testrun (UI fallback)",
        "surface": "ui",
        "method": "POST",
        "url": "$ui_base/testcycle/$cycle_id/testrun/$run_id/$add_action",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json",
        },
        "body": None,
        "body_form": {
            "scenario_id": "$scenario_id",
            "testcase_id": "$testcase_id",
        },
        "expected_status": 200,
        "extract": "testrun_testcase_id",
        "status": "TBD — DevTools capture nodig",
        "params": ["ui_base", "cycle_id", "run_id", "add_action",
                   "scenario_id", "testcase_id"],
    },
    "update-result-ui": {
        "title": "Update testcase result (UI fallback)",
        "surface": "ui",
        "method": "POST",
        "url": "$ui_base/testcycle/$cycle_id/testrun/$run_id/$update_action",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json",
        },
        "body": None,
        "body_form": {
            "testrun_testcase_id": "$testrun_testcase_id",
            "status": "$status",
            "comment": "$comment",
            "duration_seconds": "$duration_seconds",
        },
        "expected_status": 200,
        "extract": None,
        "status": "TBD — DevTools capture nodig",
        "params": ["ui_base", "cycle_id", "run_id", "update_action",
                   "testrun_testcase_id", "status", "comment",
                   "duration_seconds"],
    },
}


def _sub(value, values):
    if isinstance(value, str):
        return Template(value).safe_substitute(values)
    if isinstance(value, dict):
        return {k: _sub(v, values) for k, v in value.items()}
    if isinstance(value, list):
        return [_sub(v, values) for v in value]
    return value


def render(usecase_key, values):
    if usecase_key not in USECASES:
        raise KeyError(f"unknown usecase: {usecase_key}")
    spec = USECASES[usecase_key]
    body = _sub(spec.get("body"), values)
    body_form = _sub(spec.get("body_form"), values)
    body_text = None
    if body is not None:
        body_text = _json.dumps(body, indent=2)
    elif body_form is not None:
        body_text = urlencode(body_form) if body_form else ""
    return {
        "title": spec["title"],
        "surface": spec["surface"],
        "status": spec["status"],
        "method": spec["method"],
        "url": _sub(spec["url"], values),
        "headers": _sub(spec["headers"], values),
        "body_text": body_text,
        "body_is_json": body is not None,
        "expected_status": spec["expected_status"],
        "extract": spec["extract"],
    }
