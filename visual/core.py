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

        return self.automation.click({
            "x": x,
            "y": y,
        })