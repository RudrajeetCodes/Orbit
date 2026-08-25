from automation.core import Automation
from visual.core import VisualAction


class GuidedMode:
    """Provides step-by-step execution for Orbit tasks."""

    def __init__(self):
        self.steps = []
        self.automation = Automation()
        self.visual = VisualAction()

    def add_step(self, step):
        self.steps.append(step)

    def clear(self):
        self.steps.clear()

    def get_steps(self):
        return self.steps

    def execute(self):
        """Execute all stored steps in order."""

        results = []

        for step in self.steps:
            if not step:
                results.append(False)
                continue

            action = step.get("action")
            target = step.get("target")

            if action == "click_text":
                result = self.visual.click_text(target)

            elif action == "type_text":
                result = self.visual.type_text(target)

            elif action == "click_and_type":
                result = self.visual.click_and_type(
                    target.get("target"),
                    target.get("text"),
                )

            else:
                result = self.automation.execute(step)

            results.append(result)

            # Stop if a step fails.
            if not result:
                return False

        return True
