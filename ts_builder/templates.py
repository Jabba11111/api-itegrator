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
        "title": "Add testcase to testrun (officieel, kopieert design naar run)",
        "surface": "official",
        "method": "POST",
        "url": "$api_base/$env/test-runs/$run_id/test-cases",
        "headers": {
            "Authorization": "Basic $basic",
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json",
        },
        "body": {
            "data": {
                "relationships": {
                    "testDesignTestCase": {
                        "data": {"id": "$design_testcase_id", "type": "testCase"}
                    }
                }
            }
        },
        "body_form": None,
        "expected_status": 201,
        "extract": "data.id -> trtc_id (testRunTestCase id, andere ID-ruimte!)",
        "status": "official — let op: design_testcase_id != trtc_id",
        "params": ["api_base", "env", "basic", "run_id", "design_testcase_id"],
    },
    "get-testruntestcase": {
        "title": "Get one testRunTestCase (read result)",
        "surface": "official",
        "method": "GET",
        "url": "$api_base/$env/test-runs/$run_id/test-cases/$trtc_id",
        "headers": {
            "Authorization": "Basic $basic",
            "Accept": "application/vnd.api+json",
        },
        "body": None, "body_form": None,
        "expected_status": 200,
        "extract": "attributes.status (string), relationships.executionStatus.data.id (FK)",
        "status": "bevestigd (vangst gedeeld)",
        "params": ["api_base", "env", "basic", "run_id", "trtc_id"],
    },
    "update-result-official": {
        "title": "Update testcase result in testrun (PATCH testRunTestCase)",
        "surface": "official",
        "method": "PATCH",
        "url": "$api_base/$env/test-runs/$run_id/test-cases/$trtc_id",
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
                    "status": "$status"
                },
                "relationships": {
                    "executionStatus": {
                        "data": {
                            "id": "$execution_status_id",
                            "type": "testRunTestCaseStatus"
                        }
                    }
                }
            }
        },
        "body_form": None,
        "expected_status": 200,
        "extract": None,
        "status": "endpoint-pad bevestigd; body-shape vermoed (JSON:API convention)",
        "params": ["api_base", "env", "basic", "run_id", "trtc_id",
                   "status", "execution_status_id"],
    },
    "ui-login-get": {
        "title": "Login pagina ophalen (CSRF + initial PHPSESSID)",
        "surface": "ui",
        "method": "GET",
        "url": "$ui_origin/login",
        "headers": {
            "Accept": "text/html",
        },
        "body": None, "body_form": None,
        "expected_status": 200,
        "extract": "Set-Cookie: PHPSESSID=...  |  HTML: <input name='csrft' value='...'>",
        "status": "captured",
        "params": ["ui_origin"],
    },
    "ui-login-post": {
        "title": "Login (krijgt definitieve PHPSESSID)",
        "surface": "ui",
        "method": "POST",
        "url": "$ui_origin/login",
        "headers": {
            "Cookie": "PHPSESSID=$initial_phpsessid",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "$ui_origin",
            "Referer": "$ui_origin/login",
            "X-Requested-With": "XMLHttpRequest",
        },
        "body": None,
        "body_form": {
            "redirect": "",
            "csrft": "$csrf",
            "username": "$username",
            "password": "$password",
        },
        "expected_status": 200,
        "extract": "Set-Cookie: PHPSESSID=<new>  | response is JSON",
        "status": "captured",
        "params": ["ui_origin", "initial_phpsessid", "csrf", "username", "password"],
    },
    "ui-list-run-trtcs": {
        "title": "List trtcs in run (UI, HTML) — voor lookup CAS->trtc_id",
        "surface": "ui",
        "method": "GET",
        "url": "$ui_base/papi/testscenario/RUN$run_id/testcases",
        "headers": {
            "Cookie": "PHPSESSID=$phpsessid",
            "X-Requested-With": "XMLHttpRequest",
        },
        "body": None, "body_form": None,
        "expected_status": 200,
        "extract": "parse HTML: <tr databaseid=trtc_id businessid=CAS-code runsce_id=...>",
        "status": "captured",
        "params": ["ui_base", "run_id", "phpsessid"],
    },
    "ui-edit-testrun-add": {
        "title": "Add case via scenario aan run (UI form-POST, voorbeeld 1 nieuwe entry)",
        "surface": "ui",
        "method": "POST",
        "url": "$ui_base/testcycle/$cycle_id/testrun/$run_id/edit",
        "headers": {
            "Cookie": "PHPSESSID=$phpsessid",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "$ui_origin",
            "Referer": "$ui_base/testcycle/$cycle_id/testrun/$run_id/edit",
            "X-Requested-With": "XMLHttpRequest",
        },
        "body": None,
        "body_form": {
            "opentab": "testcases",
            "csrft": "$csrf",
            "autoFillTesters": "1",
            "2": "$run_short_description",
            "3": "$run_long_description",
            "5": "",
            "6": "",
            "7": "$tester_usr_id",
            "8": "$start_date",
            "9": "$end_date",
            "12": "0",
            "13": "0",
            "testruntestscenariotestcases[]": "",
            "testruntestscenariotestcases[new__$new_key][relationId]": "",
            "testruntestscenariotestcases[new__$new_key][testscenarioId]": "$design_scenario_id",
            "testruntestscenariotestcases[new__$new_key][testcaseId]": "$design_testcase_id",
            "testruntestscenariotestcases[new__$new_key][testerId]": "USR1",
            "testruntestscenariotestcases[new__$new_key][resetStatus]": "0",
        },
        "expected_status": 302,
        "extract": "nieuwe trtc_id volgt uit GET ui-list-run-trtcs",
        "status": "captured — form-save model, bij meerdere cases ook bestaande entries meesturen",
        "params": ["ui_base", "ui_origin", "cycle_id", "run_id",
                   "phpsessid", "csrf", "run_short_description",
                   "run_long_description", "tester_usr_id",
                   "start_date", "end_date", "new_key",
                   "design_scenario_id", "design_testcase_id"],
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
