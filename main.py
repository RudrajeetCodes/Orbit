from agent.core import OrbitAgent
from overlay.core import Overlay
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication


def main():
    app = QApplication([])

    agent = OrbitAgent()
    overlay = Overlay()

    command = input("You: ")

    result = agent.run(command)

    if result:
        overlay.show_status("Orbit", "✓ Task completed")
    else:
        overlay.show_status("Orbit", "✗ Task failed")

    print("Orbit:", result)

    QTimer.singleShot(2000, overlay.hide_overlay)
    QTimer.singleShot(2100, app.quit)

    app.exec()


if __name__ == "__main__":
    main()
