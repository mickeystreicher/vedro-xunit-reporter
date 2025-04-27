from pathlib import Path
from unittest.mock import Mock

from vedro.core import ScenarioResult, StepResult, VirtualScenario, VirtualStep

__all__ = ("create_scenario_result", "create_step_result",)


def create_scenario_result() -> ScenarioResult:
    scenario = Mock(spec=VirtualScenario)
    scenario.name = "Scenario"
    scenario.subject = "subject"
    scenario.rel_path = Path("./scenarios/scenario.py")
    return ScenarioResult(scenario)


def create_step_result() -> StepResult:
    step = Mock(spec=VirtualStep)
    return StepResult(step)
