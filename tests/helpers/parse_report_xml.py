from typing import Any, Dict

import xmltodict

from vedro_xunit_reporter import XUnitReporter

__all__ = ("parse_report_xml",)


def parse_report_xml() -> Dict[str, Any]:
    with open(XUnitReporter.report_path) as f:
        return xmltodict.parse(f.read(), force_list=False)
