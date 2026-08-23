from automation.core import Automation
from visual.core import VisualAction


class OrbitAgent:
    """Core agent responsible for coordinating Orbit tasks."""

    def __init__(self):
        self.current_task = None
        self.automation = Automation()
        self.visual = VisualAction()

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
        if "open brave" in command_lower:
            return {
                "action": "open_app",
                "target": "brave",
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
            target = command[len("create a file called ") :].strip()

            if target:
                return {
                    "action": "create_file",
                    "target": target,
                }

        if "make a file called " in command_lower:
            target = command[len("make a file called ") :].strip()

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

        if "make a folder called " in command_lower:
            target = command.split("make a folder called ", 1)[1].strip()

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

        if "remove the file " in command_lower:
            target = command[len("remove the file ") :].strip()

            if target:
                return {
                    "action": "delete_file",
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

        if "list the files in " in command_lower:
            target = command[len("list the files in ") :].strip()

            if target:
                return {
                    "action": "list_directory",
                    "target": target,
                }

        if "show information about " in command_lower:
            target = command[len("show information about ") :].strip()

            if target:
                return {
                    "action": "get_file_info",
                    "target": target,
                }

        if "find " in command_lower and " files in " in command_lower:
            parts = command.split(" files in ", 1)

            pattern_name = parts[0][5:].strip()
            directory = parts[1].strip()

            if pattern_name and directory:
                if pattern_name.lower() == "python":
                    pattern = "*.py"
                elif pattern_name.lower() == "text":
                    pattern = "*.txt"
                elif pattern_name.lower() == "markdown":
                    pattern = "*.md"
                else:
                    pattern = f"*.{pattern_name}"

                return {
                    "action": "search_files",
                    "target": {
                        "directory": directory,
                        "pattern": pattern,
                    },
                }

        if command_lower.startswith("click "):
            target = command[6:].strip()

            if target:
                return {
                    "action": "click_text",
                    "target": target,
                }

        return {
            "action": "unknown",
            "target": None,
        }

    def plan_steps(self, task):
        """Convert a multi-step task into a list of structured actions."""

        if not task or not isinstance(task, str):
            return []

        parts = [part.strip() for part in task.split(" and ") if part.strip()]

        steps = []

        for part in parts:
            action = self.plan(part)

            if action is None:
                continue

            if action["action"] == "unknown":
                return []

            steps.append(action)

        return steps

    def run_steps(self, task):
        """Plan and execute a multi-step Orbit task."""

        steps = self.plan_steps(task)

        if not steps:
            return False

        for step in steps:
            action = step["action"]

            if action == "click_text":
                success = self.visual.click_text(step["target"])
            else:
                success = self.automation.execute(step)

                # Give the application time to become visible/focused.
                if success and action == "open_app":
                    import time

                    time.sleep(2)

            if not success:
                return False

        return True

    def run(self, task):
        """Plan and execute a user task."""

        action = self.plan(task)

        if action is None:
            return False

        if action["action"] == "click_text":
            return self.visual.click_text(action["target"])

        return self.automation.execute(action)
