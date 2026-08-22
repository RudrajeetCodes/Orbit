"""Orbit's visual status and guidance overlay."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget


class Overlay(QWidget):
    """Display Orbit status and guidance."""

    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setFixedSize(420, 130)

        self.title_label = QLabel()
        self.message_label = QLabel()

        self.title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.message_label.setFont(QFont("Segoe UI", 12))

        self.title_label.setStyleSheet("color: white;")
        self.message_label.setStyleSheet("color: white;")

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.message_label)

        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                background-color: rgba(20, 20, 20, 220);
                border-radius: 15px;
            }
        """)

        self.hide()

    def show_status(self, title: str, message: str):
        """Display a status message on the overlay."""
        self.title_label.setText(title)
        self.message_label.setText(message)

        # Position the overlay near the top-center of the screen.
        screen = QApplication.primaryScreen()
        if screen:
            geometry = screen.availableGeometry()
            x = geometry.x() + (geometry.width() - self.width()) // 2
            y = geometry.y() + 40
            self.move(x, y)

        self.show()

    def hide_overlay(self):
        """Hide the overlay."""
        self.hide()

    def toggle(self):
        """Toggle overlay visibility."""
        if self.isVisible():
            self.hide()
        else:
            self.show()