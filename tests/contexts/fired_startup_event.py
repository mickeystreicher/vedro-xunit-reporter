from argparse import ArgumentParser, Namespace
from pathlib import Path

from vedro import Config
from vedro.core import Dispatcher
from vedro.core import MonotonicScenarioScheduler as ScenarioScheduler
from vedro.events import (ArgParsedEvent, ArgParseEvent, ConfigLoadedEvent,
                          StartupEvent)

from vedro_xunit_reporter import XUnitReporter

__all__ = ("fired_startup_event",)


async def fired_startup_event(dispatcher: Dispatcher) -> None:
    await dispatcher.fire(ConfigLoadedEvent(Path(), Config))

    arg_parse_event = ArgParseEvent(ArgumentParser())
    await dispatcher.fire(arg_parse_event)

    namespace = Namespace(xunit_report_path=XUnitReporter.report_path)
    arg_parsed_event = ArgParsedEvent(namespace)
    await dispatcher.fire(arg_parsed_event)

    startup_event = StartupEvent(ScenarioScheduler([]))
    await dispatcher.fire(startup_event)
