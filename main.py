from overlay.core import Overlay
from PySide6.QtWidgets import QApplication


def main():
    app = QApplication([])

    overlay = Overlay()
    overlay.show()

    app.exec()


if __name__ == "__main__":
    main()
