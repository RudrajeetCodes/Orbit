class Automation:
    """Handles automated computer actions for Orbit."""

    def __init__(self):
        self.actions = []

    def add_action(self, action):
        self.actions.append(action)

    def clear(self):
        self.actions.clear()

    def get_actions(self):
        return self.actions
