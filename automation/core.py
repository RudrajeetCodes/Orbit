import subprocess


class Automation:
    """Handles automated computer actions for Orbit."""

    def open_app(self, target):
        apps = {
            "chrome": "google-chrome",
            "firefox": "firefox",
            "terminal": "gnome-terminal",
            "file_manager": "nautilus",
        }

        command = apps.get(target)

        if command is None:
            return False

        subprocess.Popen(
            [command],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        return True

    def execute(self, action):
        """Execute a structured Orbit action."""

        if not action:
            return False

        if action.get("action") == "open_app":
            return self.open_app(action.get("target"))

        return False
