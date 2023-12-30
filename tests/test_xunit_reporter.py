import unittest
from argparse import ArgumentParser, Namespace
from pathlib import Path
from socket import gethostname
from unittest import IsolatedAsyncioTestCase as TestCase
from unittest.mock import Mock

import xmltodict
from vedro import Config
from vedro.core import AggregatedResult, Dispatcher, ExcInfo
from vedro.core import MonotonicScenarioScheduler as ScenarioScheduler
from vedro.core import (Report, ScenarioResult, StepResult, VirtualScenario,
                        VirtualStep)
from vedro.events import (ArgParsedEvent, ArgParseEvent, CleanupEvent,
                          ConfigLoadedEvent, ScenarioReportedEvent,
                          StartupEvent)
from vedro.plugins.director import Director, DirectorPlugin

from vedro_xunit_reporter import XUnitReporter, XUnitReporterPlugin


class TestXUnitReporter(TestCase):
    maxDiff = None

    def setUp(self):
        if XUnitReporter.report_path.exists():
            XUnitReporter.report_path.unlink()

        self.dispatcher = Dispatcher()

        director = DirectorPlugin(Director)
        director.subscribe(self.dispatcher)

        reporter = XUnitReporterPlugin(XUnitReporter)
        reporter.subscribe(self.dispatcher)

    async def test_no_scenarios(self):
        await self._fire_startup_event()

        await self._fire_cleanup_event()

        xml = self._parse_report_xml()
        self.assertDictEqual(xml, self._create_testsuite())

    async def test_passed_scenario(self):
        await self._fire_startup_event()

        scenario_result = self._create_scenario_result().mark_passed()
        scenario_result.set_started_at(1000).set_ended_at(2000)
        aggregated_result = await self._fire_reported_event(scenario_result)

        await self._fire_cleanup_event([aggregated_result])

        xml = self._parse_report_xml()
        self.assertDictEqual(xml, self._create_testsuite(
            self._create_testcase({"@time": "1000.000"}),
            params={
                "@timestamp": "1970-01-01T00:16:40",
                "@tests": "1",
                "@time": "1000.000"
            }
        ))

    async def test_failed_scenario(self):
        await self._fire_startup_event()

        scenario_result = self._create_scenario_result().mark_failed()
        step_result = self._create_step_result().mark_failed()
        exception = TypeError("error message")
        step_result.set_exc_info(ExcInfo(type(exception), exception, traceback=None))

        scenario_result.add_step_result(step_result)
        aggregated_result = await self._fire_reported_event(scenario_result)

        await self._fire_cleanup_event([aggregated_result])

        xml = self._parse_report_xml()
        self.assertDictEqual(xml, self._create_testsuite(
            self._create_testcase({
                "failure": {
                    "@type": exception.__class__.__name__,
                    "@message": str(exception)
                }
            }),
            params={
                "@tests": "1",
                "@failures": "1",
            }
        ))

    async def test_skipped_test(self):
        await self._fire_startup_event()

        scenario_result = self._create_scenario_result().mark_skipped()
        aggregated_result = await self._fire_reported_event(scenario_result)

        await self._fire_cleanup_event([aggregated_result])

        xml = self._parse_report_xml()
        self.assertDictEqual(xml, self._create_testsuite(
            self._create_testcase({"skipped": None}),
            params={
                "@tests": "1",
                "@skipped": "1"
            }
        ))

    async def _fire_startup_event(self):
        await self.dispatcher.fire(ConfigLoadedEvent(Path(), Config))

        arg_parse_event = ArgParseEvent(ArgumentParser())
        await self.dispatcher.fire(arg_parse_event)

        namespace = Namespace(xunit_report_path=XUnitReporter.report_path)
        arg_parsed_event = ArgParsedEvent(namespace)
        await self.dispatcher.fire(arg_parsed_event)

        startup_event = StartupEvent(ScenarioScheduler([]))
        await self.dispatcher.fire(startup_event)

    async def _fire_reported_event(self, scenario_result):
        aggregated_result = AggregatedResult.from_existing(scenario_result, [scenario_result])
        await self.dispatcher.fire(ScenarioReportedEvent(aggregated_result))
        return aggregated_result

    async def _fire_cleanup_event(self, aggregated_results=None):
        report = Report()
        if aggregated_results:
            for aggregated_result in aggregated_results:
                report.add_result(aggregated_result)
        cleanup_event = CleanupEvent(report)
        await self.dispatcher.fire(cleanup_event)
        return report

    def _parse_report_xml(self):
        with open(XUnitReporter.report_path) as f:
            return xmltodict.parse(f.read(), force_list=False)

    def _create_scenario_result(self):
        scenario = Mock(spec=VirtualScenario)
        scenario.name = "Scenario"
        scenario.subject = "subject"
        scenario.rel_path = Path("./scenarios/scenario.py")
        return ScenarioResult(scenario)

    def _create_step_result(self):
        step = Mock(spec=VirtualStep)
        return StepResult(step)

    def _create_testsuite(self, testcase=None, params=None):
        if params is None:
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

    def _create_testcase(self, params=None):
        if params is None:
            params = {}
        return {
            "@name": "subject",
            "@classname": "scenarios.scenario.Scenario",
            "@time": "0.000",
            **params
        }


if __name__ == "__main__":
    unittest.main()
