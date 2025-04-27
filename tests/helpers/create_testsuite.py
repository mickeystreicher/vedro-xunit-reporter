from socket import gethostname
from typing import Any, Dict, Optional

__all__ = ("create_testsuite", "create_testcase",)


def create_testsuite(testcase: Optional[Dict[str, Any]] = None,
                     params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if params is None:  # pragma: no cover
        params = {}
    testsuite = {
        "@name": "Scenarios",
        "@hostname": gethostname(),
        "@timestamp": "1970-01-01T00:00:00",
        "@time": "0.000",
        "@tests": "0",
        "@failures": "0",
        "@skipped": "0",
        "@errors": "0",
        **params
    }
    if testcase:
        testsuite["testcase"] = testcase
    return {
        "testsuites": {
            "testsuite": testsuite
        }
    }


def create_testcase(params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if params is None:  # pragma: no cover
        params = {}
    return {
        "@name": "subject",
        "@classname": "scenarios.scenario.Scenario",
        "@time": "0.000",
        **params
    }
