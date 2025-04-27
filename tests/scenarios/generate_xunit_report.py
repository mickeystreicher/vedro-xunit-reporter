from contexts import (fired_reported_event, fired_startup_event,
                      registered_plugin)
from helpers import (create_exc_info, create_report, create_scenario_result,
                     create_step_result, create_testcase, create_testsuite,
                     parse_report_xml)
from vedro.events import CleanupEvent
from vedro_fn import given, scenario, then, when


@scenario()
async def generate_empty_xunit_report():
    with given:
        dispatcher = registered_plugin()
        await fired_startup_event(dispatcher)

        report = create_report()
        event = CleanupEvent(report)

    with when:
        await dispatcher.fire(event)

    with then:
        xml = parse_report_xml()
        assert xml == create_testsuite()


@scenario()
async def generate_xunit_report_for_passed_scenario():
    with given:
        dispatcher = registered_plugin()
        await fired_startup_event(dispatcher)

        aggregated_result = await fired_reported_event(
            dispatcher,
            create_scenario_result()
            .mark_passed()
            .set_started_at(1000)
            .set_ended_at(2000)
        )

        report = create_report([aggregated_result])
        event = CleanupEvent(report)

    with when:
        await dispatcher.fire(event)

    with then:
        xml = parse_report_xml()
        assert xml == create_testsuite(
            create_testcase({
                "@time": "1000.000"
            }),
            params={
                "@timestamp": "1970-01-01T00:16:40",
                "@tests": "1",
                "@time": "1000.000"
            }
        )


@scenario()
async def generate_xunit_report_for_failed_scenario():
    with given:
        dispatcher = registered_plugin()
        await fired_startup_event(dispatcher)

        exc_info = create_exc_info(TypeError("error message"))
        step_result = create_step_result().mark_failed()
        step_result.set_exc_info(exc_info)

        scenario_result = create_scenario_result().mark_failed()
        scenario_result.add_step_result(step_result)
        aggregated_result = await fired_reported_event(dispatcher, scenario_result)

        report = create_report([aggregated_result])
        event = CleanupEvent(report)

    with when:
        await dispatcher.fire(event)

    with then:
        xml = parse_report_xml()
        assert xml == create_testsuite(
            create_testcase({
                "failure": {
                    "@type": exc_info.value.__class__.__name__,
                    "@message": str(exc_info.value)
                }
            }),
            params={
                "@tests": "1",
                "@failures": "1",
            }
        )


@scenario()
async def generate_xunit_report_for_skipped_scenario():
    with given:
        dispatcher = registered_plugin()
        await fired_startup_event(dispatcher)

        aggregated_result = await fired_reported_event(
            dispatcher,
            create_scenario_result()
            .mark_skipped()
        )

        report = create_report([aggregated_result])
        event = CleanupEvent(report)

    with when:
        await dispatcher.fire(event)

    with then:
        xml = parse_report_xml()
        assert xml == create_testsuite(
            create_testcase({
                "skipped": None
            }),
            params={
                "@tests": "1",
                "@skipped": "1"
            }
        )
