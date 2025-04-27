from vedro.core import Dispatcher
from vedro.plugins.director import Director, DirectorPlugin

from vedro_xunit_reporter import XUnitReporter, XUnitReporterPlugin

__all__ = ("registered_plugin",)


def registered_plugin() -> Dispatcher:
    dispatcher = Dispatcher()

    director = DirectorPlugin(Director)
    director.subscribe(dispatcher)

    reporter = XUnitReporterPlugin(XUnitReporter)
    reporter.subscribe(dispatcher)

    return dispatcher
