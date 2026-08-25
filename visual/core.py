from automation.core import Automation
from vision.vision_module import (
    capture_screen,
    find_text_center,
    mask_regions,
)


class VisualAction:
    """High-level actions that use screen vision."""

    def __init__(self):
        self.automation = Automation()
        self.excluded_regions = []

    def set_excluded_regions(self, regions):
        """Set screen regions that visual OCR should ignore."""
        self.excluded_regions = list(regions or [])

    def click_text(self, target):
        """Find visible text and click its center."""
        if not target:
            return False

        screenshot = capture_screen()

        print("VisualAction excluded regions:", self.excluded_regions)

        if self.excluded_regions:
            screenshot = mask_regions(
                screenshot,
                self.excluded_regions,
            )
            screenshot.save("/tmp/orbit-click-debug.png")

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
