from typing import List, Optional

from vedro.core import AggregatedResult, Report

__all__ = ("create_report",)


def create_report(aggregated_results: Optional[List[AggregatedResult]] = None) -> Report:
    report = Report()
    if aggregated_results:
        for aggregated_result in aggregated_results:
            report.add_result(aggregated_result)
    return report
