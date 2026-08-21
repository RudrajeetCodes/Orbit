class Overlay:
    """Handles Orbit's visual guidance overlay."""

    def __init__(self):
        self.visible = False

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def toggle(self):
        self.visible = not self.visible
