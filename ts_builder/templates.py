"""Use-case templates. Each entry produces a request block when rendered.

Two surface kinds:
- "bearer": official Stoplight API, JSON, Authorization: Bearer
- "ui":     web-app endpoint, form-urlencoded, session auth (caller's problem)
"""

from string import Template
from urllib.parse import urlencode

USECASES = {
    "lookup-scenario": {
        "title": "Lookup SCE-code -> scenario_id",
        "surface": "bearer",
        "method": "GET",
        "url": "$api_base/test-scenarios?code=$sce_code",
        "headers": {
            "Authorization": "Bearer $token",
            "Accept": "application/json",
        },
        "body": None,
        "expected_status": 200,
        "extract": "data[0].id -> scenario_id",
        "status": "official (query-key TBD)",
        "params": ["api_base", "token", "sce_code"],
    },
    "lookup-testcase": {
        "title": "Lookup CAS-code -> testcase_id (within scenario)",
        "surface": "bearer",
        "method": "GET",
        "url": "$api_base/test-scenarios/$scenario_id/test-cases?code=$cas_code",
        "headers": {
            "Authorization": "Bearer $token",
            "Accept": "application/json",
        },
        "body": None,
        "expected_status": 200,
        "extract": "data[0].id -> testcase_id",
        "status": "official (path TBD)",
        "params": ["api_base", "token", "scenario_id", "cas_code"],
    },
    "list-scenarios-to-add": {
        "title": "List scenarios still addable to testrun (UI)",
        "surface": "ui",
        "method": "POST",
        "url": "$ui_base/testcycle/$cycle_id/testrun/$run_id/listtestscenariostoadd",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json",
        },
        "body_form": {},
        "expected_status": 200,
        "extract": "lijst met SCE's",
        "status": "captured",
        "params": ["ui_base", "cycle_id", "run_id"],
    },
    "list-run-testcases": {
        "title": "List testcases already in testrun, grouped by SCE (UI)",
        "surface": "ui",
        "method": "POST",
        "url": "$ui_base/testcycle/$cycle_id/testrun/$run_id/get-testscenarios-testcases-rows",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json",
        },
        "body_form": {},
        "expected_status": 200,
        "extract": "rows met scenario+testcase combinaties",
        "status": "captured",
        "params": ["ui_base", "cycle_id", "run_id"],
    },
    "add-testcase-to-run": {
        "title": "Add testcase to testrun via scenario (UI)",
        "surface": "ui",
        "method": "POST",
        "url": "$ui_base/testcycle/$cycle_id/testrun/$run_id/$add_action",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json",
        },
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
    "update-result": {
        "title": "Update testcase result in testrun (UI)",
        "surface": "ui",
        "method": "POST",
        "url": "$ui_base/testcycle/$cycle_id/testrun/$run_id/$update_action",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json",
        },
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
    "remove-testcase": {
        "title": "Remove testcase from testrun (UI, optional)",
        "surface": "ui",
        "method": "POST",
        "url": "$ui_base/testcycle/$cycle_id/testrun/$run_id/$remove_action",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json",
        },
        "body_form": {
            "testrun_testcase_id": "$testrun_testcase_id",
        },
        "expected_status": 200,
        "extract": None,
        "status": "TBD — DevTools capture nodig",
        "params": ["ui_base", "cycle_id", "run_id", "remove_action",
                   "testrun_testcase_id"],
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
    """Render a usecase to a dict of resolved request fields.

    Unknown placeholders are left as `$name` so the output still shows what is missing.
    """
    if usecase_key not in USECASES:
        raise KeyError(f"unknown usecase: {usecase_key}")
    spec = USECASES[usecase_key]
    body = _sub(spec.get("body"), values)
    body_form = _sub(spec.get("body_form"), values)
    body_text = None
    if body is not None:
        import json as _json
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
