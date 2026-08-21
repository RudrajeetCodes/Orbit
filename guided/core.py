class GuidedMode:
    """Provides step-by-step guidance for Orbit tasks."""

    def __init__(self):
        self.steps = []

    def add_step(self, step):
        self.steps.append(step)

    def clear(self):
        self.steps.clear()

    def get_steps(self):
        return self.steps
