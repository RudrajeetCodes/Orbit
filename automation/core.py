import shutil
import subprocess
from pathlib import Path


class Automation:
    """Handles automated computer actions for Orbit."""

    def open_app(self, target):
        """Open an application or activate it if already running."""

        apps = {
            "chrome": "google-chrome",
            "firefox": "firefox",
            "brave": "brave-browser",
            "terminal": "gnome-terminal",
            "file_manager": "nautilus",
        }

        command = apps.get(target)

        if command is None:
            return False

        # Reuse an existing window if possible.
        if self.activate_app(target):
            return True

        # Application isn't running, so launch it.
        subprocess.Popen(
            [command],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        return True

    def open_url(self, target, browser="firefox"):
        """Open a URL using the requested browser."""

        if not target:
            return False

        browsers = {
            "chrome": "google-chrome",
            "firefox": "firefox",
            "brave": "brave-browser",
        }

        command = browsers.get(browser.lower())

        if command is None:
            return False

        subprocess.Popen(
            [command, target],
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

    def copy_file(self, target):
        """Copy a file."""
        source = Path(target["source"])
        destination = Path(target["destination"])

        if not source.exists() or not source.is_file():
            return False

        if destination.exists():
            return False

        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

        return True

    def copy_folder(self, target):
        """Copy a folder."""
        source = Path(target["source"])
        destination = Path(target["destination"])

        if not source.exists() or not source.is_dir():
            return False

        if destination.exists():
            return False

        shutil.copytree(source, destination)

        return True

    def rename_file(self, target):
        """Rename a file."""
        source = Path(target.get("source"))
        destination = Path(target.get("destination"))

        if not source.exists() or not source.is_file():
            return False

        if destination.exists():
            return False

        source.rename(destination)

        return True

    def rename_folder(self, target):
        """Rename a folder."""
        source = Path(target.get("source"))
        destination = Path(target.get("destination"))

        if not source.exists() or not source.is_dir():
            return False

        if destination.exists():
            return False

        source.rename(destination)

        return True

    def list_directory(self, target):
        """List the contents of a directory."""
        folder = Path(target)

        if not folder.exists() or not folder.is_dir():
            return False

        return [item.name for item in folder.iterdir()]

    def get_file_info(self, target):
        """Get information about a file or folder."""
        path = Path(target)

        if not path.exists():
            return False

        if path.is_file():
            file_type = "file"
        elif path.is_dir():
            file_type = "folder"
        else:
            file_type = "other"

        return {
            "name": path.name,
            "type": file_type,
            "size": path.stat().st_size,
        }

    def search_files(self, target):
        """Search for files matching a pattern."""
        directory = Path(target.get("directory"))
        pattern = target.get("pattern")

        if not directory.exists() or not directory.is_dir():
            return False

        if not pattern:
            return False

        return [str(path) for path in directory.rglob(pattern) if path.is_file()]

    def click(self, target):
        """Click at the specified screen coordinates using wdotool."""

        if not isinstance(target, dict):
            return False

        x = target.get("x")
        y = target.get("y")

        if x is None or y is None:
            return False

        try:
            subprocess.run(
                [
                    "wdotool",
                    "--backend",
                    "gnome",
                    "mousemove",
                    str(x),
                    str(y),
                ],
                check=True,
            )

            subprocess.run(
                [
                    "wdotool",
                    "--backend",
                    "gnome",
                    "click",
                    "1",
                ],
                check=True,
            )

            return True

        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def type_text(self, text):
        """Type text using ydotool."""

        if not isinstance(text, str) or not text:
            return False

        try:
            subprocess.run(
                ["wdotool", "--backend", "gnome", "type", "--", text],
                check=True,
            )

            return True

        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def press_key(self, key):
        """Press a keyboard key using wdotool."""

        if not isinstance(key, str) or not key:
            return False

        try:
            subprocess.run(
                ["wdotool", "--backend", "gnome", "key", key],
                check=True,
            )

            return True

        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def get_active_window(self):
        """Return information about the currently active window."""

        try:
            result = subprocess.run(
                ["wdotool", "--backend", "gnome", "getactivewindow"],
                capture_output=True,
                text=True,
                check=True,
            )

            window_id = result.stdout.strip()

            if not window_id:
                return False

            name = subprocess.run(
                [
                    "wdotool",
                    "--backend",
                    "gnome",
                    "getwindowname",
                    window_id,
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            return {
                "id": window_id,
                "name": name.stdout.strip(),
            }

        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def is_app_active(self, app_name):
        """Check whether the active window belongs to an application."""

        if not app_name:
            return False

        window = self.get_active_window()

        if not window:
            return False

        aliases = {
            "firefox": ["firefox"],
            "chrome": ["google-chrome", "chrome"],
            "terminal": ["gnome-terminal", "org.gnome.terminal"],
            "files": ["org.gnome.nautilus", "nautilus"],
        }

        candidates = aliases.get(
            app_name.lower(),
            [app_name.lower()],
        )

        try:
            result = subprocess.run(
                [
                    "wdotool",
                    "--backend",
                    "gnome",
                    "getwindowclassname",
                    window["id"],
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            app_id = result.stdout.strip().lower()

            return any(candidate in app_id for candidate in candidates)

        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def activate_app(self, app_name):
        """Activate an existing application window."""

        if not app_name:
            return False

        classes = {
            "firefox": "firefox",
            "chrome": "google-chrome",
            "brave": "brave",
            "terminal": "org.gnome.Terminal",
            "file_manager": "org.gnome.Nautilus",
        }

        app_class = classes.get(
            app_name.lower(),
            app_name,
        )

        try:
            result = subprocess.run(
                [
                    "wdotool",
                    "--backend",
                    "gnome",
                    "search",
                    "--class",
                    app_class,
                    "--ignore-case",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            for line in result.stdout.splitlines():
                parts = line.strip().split(maxsplit=1)

                if not parts:
                    continue

                window_id = parts[0]

                if window_id.isdigit():
                    subprocess.run(
                        [
                            "wdotool",
                            "--backend",
                            "gnome",
                            "windowactivate",
                            window_id,
                        ],
                        check=True,
                    )

                    return True

            return False

        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def execute(self, action):
        """Execute a structured Orbit action."""

        if not action:
            return False

        if action.get("action") == "open_app":
            return self.open_app(action.get("target"))

        if action.get("action") == "open_url":
            return self.open_url(
                action.get("target"),
                action.get("browser", "firefox"),
            )

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

        if action.get("action") == "copy_file":
            return self.copy_file(action.get("target"))

        if action.get("action") == "copy_folder":
            return self.copy_folder(action.get("target"))

        if action.get("action") == "rename_file":
            return self.rename_file(action.get("target"))

        if action.get("action") == "rename_folder":
            return self.rename_folder(action.get("target"))

        if action.get("action") == "list_directory":
            return self.list_directory(action.get("target"))

        if action.get("action") == "get_file_info":
            return self.get_file_info(action.get("target"))

        if action.get("action") == "search_files":
            return self.search_files(action.get("target"))

        if action.get("action") == "click":
            return self.click(action.get("target"))

        if action.get("action") == "click":
            return self.click(action.get("target"))

        if action.get("action") == "type_text":
            return self.type_text(action.get("target"))

        if action.get("action") == "press_key":
            return self.press_key(action.get("target"))

        return False
