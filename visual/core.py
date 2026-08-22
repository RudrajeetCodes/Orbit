from automation.core import Automation
from vision.vision_module import capture_screen, find_text_center


class VisualAction:
    """High-level actions that use screen vision."""

    def __init__(self):
        self.automation = Automation()

    def click_text(self, target):
        """Find visible text and click its center."""
        if not target:
            return False

        screenshot = capture_screen()
        position = find_text_center(screenshot, target)

        if position is None:
            return False

        x, y = position

        return self.automation.click(
            {
                "x": x,
                "y": y,
            }
        )

    def type_text(self, text):
        """Type text using the currently focused application."""
        if not text:
            return False

        return self.automation.type_text(text)

    def click_and_type(self, target, text):
        """Click visible text and type into the resulting focused field."""
        if not target or not text:
            return False

        if not self.click_text(target):
            return False

        return self.type_text(text)
