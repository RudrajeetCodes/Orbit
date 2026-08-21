from automation.core import Automation


class OrbitAgent:
    """Core agent responsible for coordinating Orbit tasks."""

    def __init__(self):
        self.current_task = None
        self.automation = Automation()

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

        command = self.current_task.strip()
        command_lower = command.lower()

        if "open chrome" in command_lower:
            return {
                "action": "open_app",
                "target": "chrome",
            }

        if "open firefox" in command_lower:
            return {
                "action": "open_app",
                "target": "firefox",
            }

        if "open terminal" in command_lower:
            return {
                "action": "open_app",
                "target": "terminal",
            }

        if "open files" in command_lower or "open file manager" in command_lower:
            return {
                "action": "open_app",
                "target": "file_manager",
            }

        if "create a file called " in command_lower:
            target = command.split("create a file called ", 1)[1].strip()

            if target:
                return {
                    "action": "create_file",
                    "target": target,
                }

        if "create a folder called " in command_lower:
            target = command.split("create a folder called ", 1)[1].strip()

            if target:
                return {
                    "action": "create_folder",
                    "target": target,
                }

        if "delete the file " in command_lower:
            target = command[len("delete the file ") :].strip()

            if target:
                return {
                    "action": "delete_file",
                    "target": target,
                }

        if "delete the folder " in command_lower:
            target = command[len("delete the folder ") :].strip()

            if target:
                return {
                    "action": "delete_folder",
                    "target": target,
                }

        if "move " in command_lower and " to " in command_lower:
            source, destination = command.split(" to ", 1)
            source = source[len("move ") :].strip()
            destination = destination.strip()

            if source and destination:
                return {
                    "action": "move",
                    "target": {
                        "source": source,
                        "destination": destination,
                    },
                }

        if "copy " in command_lower and " to " in command_lower:
            source, destination = command.split(" to ", 1)
            source = source[len("copy ") :].strip()
            destination = destination.strip()

            if source and destination:
                return {
                    "action": "copy_file",
                    "target": {
                        "source": source,
                        "destination": destination,
                    },
                }

        if "rename " in command_lower and " to " in command_lower:
            source, destination = command.split(" to ", 1)
            source = source[len("rename ") :].strip()
            destination = destination.strip()

            if source and destination:
                return {
                    "action": "rename_file",
                    "target": {
                        "source": source,
                        "destination": destination,
                    },
                }

        return {
            "action": "unknown",
            "target": None,
        }

    def run(self, task):
        """Plan and execute a user task."""

        action = self.plan(task)

        if action is None:
            return False

        return self.automation.execute(action)
