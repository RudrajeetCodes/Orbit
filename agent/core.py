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
                "target": "chrome",
            }

        if "open firefox" in command:
            return {
                "action": "open_app",
                "target": "firefox",
            }

        if "open terminal" in command:
            return {
                "action": "open_app",
                "target": "terminal",
            }

        if "open files" in command or "open file manager" in command:
            return {
                "action": "open_app",
                "target": "file_manager",
            }

        return {
            "action": "unknown",
            "target": None,
        }
