from vedro.core import AggregatedResult, Dispatcher, ScenarioResult
from vedro.events import ScenarioReportedEvent

__all__ = ("fired_reported_event",)


async def fired_reported_event(dispatcher: Dispatcher,
                               scenario_result: ScenarioResult) -> AggregatedResult:
    aggregated_result = AggregatedResult.from_existing(scenario_result, [scenario_result])
    await dispatcher.fire(ScenarioReportedEvent(aggregated_result))
    return aggregated_result
