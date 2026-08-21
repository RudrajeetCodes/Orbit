from pathlib import Path
import subprocess
from pathlib import Path


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

    def open_url(self, target):
        """Open a URL using Firefox."""

        if not target:
            return False

        subprocess.Popen(
            ["firefox", target],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        return True

    def create_folder(self, target):
        """Create a new folder."""

        if not target:
            return False

        folder = Path(target)

        if folder.exists():
            return False

        folder.mkdir(parents=True)

        return True

    def delete_folder(self, target):
        """Delete an empty folder."""

        if not target:
            return False

        folder = Path(target)

        if not folder.exists() or not folder.is_dir():
            return False

        folder.rmdir()

        return True

    def create_file(self, target):
        """Create an empty file."""
        file = Path(target)

        if file.exists():
            return False

        file.parent.mkdir(parents=True, exist_ok=True)
        file.touch()

        return True

    def delete_file(self, target):
        """Delete a file."""
        file = Path(target)

        if not file.exists() or not file.is_file():
            return False

        file.unlink()

        return True

    def move(self, source, destination):
        """Move a file or folder."""
        source = Path(source)
        destination = Path(destination)

        if not source.exists() or destination.exists():
            return False

        destination.parent.mkdir(parents=True, exist_ok=True)
        source.rename(destination)

        return True

    def execute(self, action):
        """Execute a structured Orbit action."""

        if not action:
            return False

        if action.get("action") == "open_app":
            return self.open_app(action.get("target"))

        if action.get("action") == "open_url":
            return self.open_url(action.get("target"))

        if action.get("action") == "create_folder":
            return self.create_folder(action.get("target"))

        if action.get("action") == "move":
            target = action.get("target", {})
            return self.move(target.get("source"), target.get("destination"))

        if action.get("action") == "delete_file":
            return self.delete_file(action.get("target"))

        if action.get("action") == "create_file":
            return self.create_file(action.get("target"))

        if action.get("action") == "delete_folder":
            return self.delete_folder(action.get("target"))

        return False
