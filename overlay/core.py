"""Orbit's visual status and guidance overlay."""

from __future__ import annotations

from agent.core import OrbitAgent
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class AgentWorker(QThread):
    finished = Signal(bool)

    def __init__(self, agent, command):
        super().__init__()
        self.agent = agent
        self.command = command

    def run(self):
        result = self.agent.run_steps(self.command)
        self.finished.emit(result)


class Overlay(QWidget):
    """Orbit's floating bottom command dock."""

    def __init__(self):
        super().__init__()

        self.agent = OrbitAgent()
        self.worker = None

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setFixedSize(620, 72)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Ask Orbit to do something...")
        self.input.setFont(QFont("Segoe UI", 12))
        self.input.setFixedHeight(46)

        self.run_button = QPushButton("➜")
        self.run_button.setFixedSize(46, 46)
        self.run_button.setFont(QFont("Segoe UI", 16))

        self.status = QLabel("● Ready")
        self.status.setFont(QFont("Segoe UI", 10))

        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(10)
        input_layout.addWidget(self.input)
        input_layout.addWidget(self.run_button)

        layout = QVBoxLayout()
        layout.setContentsMargins(14, 10, 14, 8)
        layout.setSpacing(2)
        layout.addLayout(input_layout)
        layout.addWidget(self.status)

        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                background-color: rgba(20, 20, 24, 235);
                border: 1px solid rgba(255, 255, 255, 35);
                border-radius: 18px;
            }

            QLineEdit {
                background-color: rgba(255, 255, 255, 12);
                color: white;
                border: 1px solid rgba(255, 255, 255, 25);
                border-radius: 13px;
                padding: 0 14px;
            }

            QLineEdit:focus {
                border: 1px solid rgba(120, 170, 255, 120);
            }

            QPushButton {
                background-color: rgba(255, 255, 255, 20);
                color: white;
                border: none;
                border-radius: 13px;
            }

            QPushButton:hover {
                background-color: rgba(255, 255, 255, 35);
            }

            QLabel {
                color: rgba(255, 255, 255, 150);
                background: transparent;
                border: none;
            }
        """)

        self.run_button.clicked.connect(self.run_command)
        self.input.returnPressed.connect(self.run_command)

    def show_status(self, title: str, message: str):
        self.status.setText(f"{title}  {message}")

    def position_dock(self):
        screen = QApplication.primaryScreen()

        if not screen:
            return

        geometry = screen.availableGeometry()

        x = geometry.x() + (geometry.width() - self.width()) // 2
        y = geometry.y() + geometry.height() - self.height() - 50

        self.move(x, y)

    def run_command(self):
        command = self.input.text().strip()

        if not command:
            return

        self.run_button.setEnabled(False)
        self.input.setEnabled(False)

        self.show_status("Orbit", "● Working...")

        self.worker = AgentWorker(self.agent, command)
        self.worker.finished.connect(self.command_finished)
        self.worker.start()

    def command_finished(self, success):
        if success:
            self.show_status("Orbit", "✓ Task completed")
        else:
            self.show_status("Orbit", "✗ Task failed")

        self.run_button.setEnabled(True)
        self.input.setEnabled(True)
        self.input.clear()
        self.input.setFocus()

    def showEvent(self, event):
        super().showEvent(event)
        self.position_dock()
        self.input.setFocus()

    def hide_overlay(self):
        self.hide()

    def toggle(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.position_dock()
