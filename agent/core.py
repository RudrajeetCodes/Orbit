from pathlib import Path

from automation.core import Automation
from visual.core import VisualAction


class OrbitAgent:
    """Core agent responsible for coordinating Orbit tasks."""

    def __init__(self):
        self.current_task = None
        self.automation = Automation()
        self.visual = VisualAction()

    def resolve_path(self, path):
        """Resolve natural-language filesystem locations."""
        path = path.strip()

        home = Path.home()

        if path.lower() in ("home", "my home", "home directory"):
            return str(home)

        if path.lower().startswith("home/"):
            return str(home / path[5:])

        if path.startswith("~/"):
            return str(Path(path).expanduser())

        if path.startswith("/"):
            return path

        return str(home / path)

    def resolve_url(self, site):
        """Convert a website name or URL into a usable URL."""
        site = site.strip()

        if not site:
            return None

        if site.startswith(("http://", "https://")):
            return site

        site = site.rstrip("/")

        if "." not in site:
            site = f"{site}.com"

        return f"https://{site.lower()}"

    def plan_web_search(self, command):
        """Parse a browser + website + search request."""
        command_lower = command.lower()

        browsers = {
            "chrome": "chrome",
            "brave": "brave",
            "firefox": "firefox",
        }

        browser = None

        for name in browsers:
            if f"open {name}" in command_lower:
                browser = browsers[name]
                break

        if browser is None:
            return None

        if " and search for " not in command_lower:
            return None

        open_positions = [
            i for i in range(len(command_lower)) if command_lower.startswith("open ", i)
        ]

        if len(open_positions) < 2:
            return None

        website_start = open_positions[1] + len("open ")
        search_start = command_lower.index(" and search for ")

        site = command[website_start:search_start].strip().rstrip(",")
        query = command[search_start + len(" and search for ") :].strip()

        if not site or not query:
            return None

        return {
            "action": "web_search",
            "browser": browser,
            "site": site,
            "query": query,
        }

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

        web_search = self.plan_web_search(command)

        if web_search:
            return web_search

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
            prefix = "create a folder called "
            target = command[len(prefix) :].strip()

            parts = target.rsplit(" in ", 1)

            if len(parts) == 2:
                folder_name, parent = parts
                target = str(
                    Path(self.resolve_path(parent.strip())) / folder_name.strip()
                )

            if target:
                return {
                    "action": "create_folder",
                    "target": target,
                }

        if "make a folder called " in command_lower:
            prefix = "make a folder called "
            target = command[len(prefix) :].strip()

            parts = target.rsplit(" in ", 1)

            if len(parts) == 2:
                folder_name, parent = parts
                target = str(
                    Path(self.resolve_path(parent.strip())) / folder_name.strip()
                )

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

            # Remove natural-language item prefixes.
            for prefix in (
                "the folder ",
                "a folder ",
                "the file ",
                "a file ",
            ):
                if source.lower().startswith(prefix):
                    source = source[len(prefix) :].strip()
                    break

            # Resolve source location.
            source_parts = source.rsplit(" in ", 1)

            if len(source_parts) == 2:
                source_name, source_parent = source_parts

                source = str(
                    Path(self.resolve_path(source_parent.strip())) / source_name.strip()
                )
            else:
                source = self.resolve_path(source)

            # Resolve destination.
            destination = self.resolve_path(destination)

            # If destination is an existing directory,
            # move the item into it using its original name.
            destination_path = Path(destination)

            if destination_path.exists() and destination_path.is_dir():
                destination = str(destination_path / Path(source).name)

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

        if self.plan_web_search(task):
            return [self.plan_web_search(task)]

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
            elif action == "web_search":
                success = self.execute_web_search(step)
            else:
                success = self.automation.execute(step)

                # Give the application time to become visible/focused.
                if success and action == "open_app":
                    import time

                    time.sleep(2)

            if not success:
                return False

        return True

    def execute_web_search(self, step):
        """Execute a browser + website + search workflow."""

        browser = step.get("browser")
        site = step.get("site")
        query = step.get("query")

        print("WEB SEARCH: looking for Search")

        if not browser or not site or not query:
            print("WEB SEARCH: Search button not found")
            return False

        print("WEB SEARCH: Search clicked")

        # Open the requested browser.
        if not self.automation.execute(
            {
                "action": "open_app",
                "target": browser,
            }
        ):
            return False

        import time

        time.sleep(2)

        # Open the website in the requested browser.
        url = self.resolve_url(site)

        if not self.automation.execute(
            {
                "action": "open_url",
                "target": url,
                "browser": browser,
            }
        ):
            return False

        time.sleep(3)

        # Find and click the search field using OCR.
        if not self.visual.click_text("Search"):
            return False

        print("WEB SEARCH: typing query")

        # Type the search query.
        if not self.automation.execute(
            {
                "action": "type_text",
                "target": query,
            }
        ):
            print("WEB SEARCH: typing failed")
            return False

        print("WEB SEARCH: query typed")

        print("WEB SEARCH: pressing Return")

        success = self.automation.execute(
            {
                "action": "press_key",
                "target": "Return",
            }
        )

        print("WEB SEARCH: Return result =", success)

        return success

    def run(self, task):
        """Plan and execute a user task."""

        action = self.plan(task)

        if action is None:
            return False

        if action["action"] == "click_text":
            return self.visual.click_text(action["target"])

        if action["action"] == "web_search":
            return self.execute_web_search(action)

        return self.automation.execute(action)
