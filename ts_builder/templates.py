"""Use-case templates. Each entry produces a request block when rendered."""

from string import Template

USECASES = {
    "lookup-scenario": {
        "title": "Lookup SCE-code -> scenario_id",
        "method": "GET",
        "url": "$base_url/test-scenarios?code=$sce_code",
        "headers": {
            "Authorization": "Bearer $token",
            "Accept": "application/json",
        },
        "body": None,
        "expected_status": 200,
        "extract": "data[0].id -> scenario_id",
        "status": "official",
        "params": ["base_url", "token", "sce_code"],
    },
    "lookup-testcase": {
        "title": "Lookup CAS-code -> testcase_id (within scenario)",
        "method": "GET",
        "url": "$base_url/test-scenarios/$scenario_id/test-cases?code=$cas_code",
        "headers": {
            "Authorization": "Bearer $token",
            "Accept": "application/json",
        },
        "body": None,
        "expected_status": 200,
        "extract": "data[0].id -> testcase_id",
        "status": "official",
        "params": ["base_url", "token", "scenario_id", "cas_code"],
    },
    "add-scenario-to-run": {
        "title": "Add scenario to testrun",
        "method": "POST",
        "url": "$base_url/test-runs/$run_id/scenarios",
        "headers": {
            "Authorization": "Bearer $token",
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        "body": {"scenario_id": "$scenario_id"},
        "expected_status": 201,
        "extract": "data[].id -> testrun_testcase_ids",
        "status": "TBD",
        "params": ["base_url", "token", "run_id", "scenario_id"],
    },
    "add-testcase-to-run": {
        "title": "Add single testcase to testrun via scenario",
        "method": "POST",
        "url": "$base_url/test-runs/$run_id/test-cases",
        "headers": {
            "Authorization": "Bearer $token",
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        "body": {
            "scenario_id": "$scenario_id",
            "testcase_id": "$testcase_id",
        },
        "expected_status": 201,
        "extract": "data.id -> testrun_testcase_id",
        "status": "TBD",
        "params": ["base_url", "token", "run_id", "scenario_id", "testcase_id"],
    },
    "update-result": {
        "title": "Update testcase result in testrun",
        "method": "PATCH",
        "url": "$base_url/test-runs/$run_id/test-cases/$testrun_testcase_id",
        "headers": {
            "Authorization": "Bearer $token",
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        "body": {
            "status": "$status",
            "comment": "$comment",
            "duration_seconds": "$duration_seconds",
        },
        "expected_status": 200,
        "extract": None,
        "status": "TBD",
        "params": [
            "base_url", "token", "run_id", "testrun_testcase_id",
            "status", "comment", "duration_seconds",
        ],
    },
    "remove-testcase": {
        "title": "Remove testcase from testrun (rollback)",
        "method": "DELETE",
        "url": "$base_url/test-runs/$run_id/test-cases/$testrun_testcase_id",
        "headers": {
            "Authorization": "Bearer $token",
            "Accept": "application/json",
        },
        "body": None,
        "expected_status": 204,
        "extract": None,
        "status": "TBD",
        "params": ["base_url", "token", "run_id", "testrun_testcase_id"],
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
    return {
        "title": spec["title"],
        "status": spec["status"],
        "method": spec["method"],
        "url": _sub(spec["url"], values),
        "headers": _sub(spec["headers"], values),
        "body": _sub(spec["body"], values),
        "expected_status": spec["expected_status"],
        "extract": spec["extract"],
    }
