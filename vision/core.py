class VisionSystem:
    """Handles screen and UI understanding for Orbit."""

    def __init__(self):
        self.last_frame = None

    def capture(self):
        return self.last_frame

    def analyze(self, frame):
        self.last_frame = frame
        return {}
