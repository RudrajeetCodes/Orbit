class OrbitAgent:
    """Core agent responsible for coordinating Orbit tasks."""

    def __init__(self):
        self.current_task = None

    def set_task(self, task):
        self.current_task = task

    def clear_task(self):
        self.current_task = None

    def plan(self, task=None):
        """Convert a user task into a structured action."""

        if task is not None:
            self.set_task(task)

        if not self.current_task:
            return None

        command = self.current_task.lower().strip()

        if "open chrome" in command:
            return {
                "action": "open_app",
                "target": "chrome"
            }

        return {
            "action": "unknown",
            "target": None
        }
