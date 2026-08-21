class OrbitAgent:
    """Core agent responsible for coordinating Orbit tasks."""

    def __init__(self):
        self.current_task = None

    def set_task(self, task):
        self.current_task = task

    def clear_task(self):
        self.current_task = None
