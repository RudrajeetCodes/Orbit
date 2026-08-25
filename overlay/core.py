"""Orbit's visual status and guidance overlay."""

from __future__ import annotations

from agent.core import OrbitAgent
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QColor, QFont, QPainter, QPen
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
        self.setObjectName("dock")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.agent = OrbitAgent()
        self.worker = None

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setFixedSize(620, 88)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Ask Orbit to do something...")
        self.input.setFont(QFont("Segoe UI", 12))
        self.input.setFixedHeight(46)

        self.run_button = QPushButton("➜")
        self.run_button.setFixedSize(46, 46)
        self.run_button.setFont(QFont("Segoe UI", 16))

        self.status = QLabel("● Ready")
        self.status.setFont(QFont("Segoe UI", 10))
        self.brand = QLabel("◉ Orbit")
        self.brand.setObjectName("brand")
        self.brand.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))

        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(10)

        input_layout.addWidget(self.brand)
        input_layout.addWidget(self.input, 1)
        input_layout.addWidget(self.run_button)

        layout = QVBoxLayout()
        layout.setContentsMargins(14, 10, 14, 8)
        layout.setSpacing(2)
        layout.addLayout(input_layout)

        # Main dock layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(14, 10, 14, 8)
        main_layout.setSpacing(14)

        # Orbit branding
        self.brand.setFixedWidth(78)

        # Right side: input + status
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(2)

        # Input row
        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(10)

        input_layout.addWidget(self.input, 1)
        input_layout.addWidget(self.run_button)

        right_layout.addLayout(input_layout)

        # Status
        status_layout = QHBoxLayout()
        status_layout.setContentsMargins(2, 0, 0, 0)
        status_layout.addWidget(self.status)
        status_layout.addStretch()

        right_layout.addLayout(status_layout)

        # Put everything together
        main_layout.addWidget(self.brand)
        main_layout.addLayout(right_layout, 1)

        self.setLayout(main_layout)

        self.setStyleSheet("""
        /* =========================
        ORBIT MAIN DOCK
        ========================= */

        QWidget#dock {
            background-color: rgba(58, 58, 64, 245);
            border: 1px solid rgba(255, 255, 255, 70);
            border-radius: 22px;
        }


        /* =========================
        COMMAND INPUT
        ========================= */

        QLabel#brand {
            color: white;
            background: transparent;
            border: none;
            padding: 0 4px;
        }

        QLineEdit {
            background-color: rgba(42, 42, 48, 235);
            color: #ffffff;

            border: 1px solid rgba(255, 255, 255, 45);
            border-radius: 15px;

            padding-left: 16px;
            padding-right: 16px;

            selection-background-color: rgba(130, 130, 140, 120);
        }

        QLineEdit:hover {
            background-color: rgba(48, 48, 54, 240);
            border: 1px solid rgba(255, 255, 255, 65);
        }

        QLineEdit:focus {
            background-color: rgba(45, 45, 51, 245);
            border: 1px solid rgba(255, 255, 255, 110);
        }

        QLineEdit::placeholder {
            color: rgba(255, 255, 255, 135);
        }


        /* =========================
        RUN BUTTON
        ========================= */

        QPushButton {
            background-color: rgba(78, 78, 86, 245);
            color: #ffffff;

            border: 1px solid rgba(255, 255, 255, 65);
            border-radius: 15px;

            font-size: 18px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: rgba(92, 92, 100, 250);
            border: 1px solid rgba(255, 255, 255, 90);
        }

        QPushButton:pressed {
            background-color: rgba(68, 68, 75, 250);
        }

        QPushButton:disabled {
            background-color: rgba(70, 70, 76, 180);
            color: rgba(255, 255, 255, 80);
        }


        /* =========================
        STATUS
        ========================= */

        QLabel {
            background: transparent;
            border: none;
            color: rgba(255, 255, 255, 175);
        }
    """)

        self.run_button.clicked.connect(self.run_command)
        self.input.returnPressed.connect(self.run_command)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Grey floating dock background
        painter.setBrush(QColor(58, 58, 64, 245))

        # Subtle light border
        painter.setPen(QPen(QColor(255, 255, 255, 70), 1))

        rect = self.rect().adjusted(1, 1, -1, -1)

        painter.drawRoundedRect(rect, 22, 22)

    def show_status(self, title: str, message: str):
        self.status.setText(f"{title}  {message}")

    def position_dock(self):
        screen = QApplication.primaryScreen()

        if not screen:
            return

        geometry = screen.availableGeometry()

        x = geometry.x() + (geometry.width() - self.width()) // 2
        y = geometry.y() + geometry.height() - self.height() - 60

        self.move(x, y)

    def run_command(self):
        command = self.input.text().strip()

        if not command:
            return

        self.run_button.setEnabled(False)
        self.input.setEnabled(False)

        self.show_status("Orbit", "● Working...")

        screen = QApplication.primaryScreen()
        geometry = screen.availableGeometry()

        dock_x = geometry.x() + (geometry.width() - self.width()) // 2
        dock_y = geometry.y() + (geometry.height() - self.height()) // 2

        self.agent.visual.set_excluded_regions(
            [
                (
                    dock_x,
                    dock_y,
                    dock_x + self.width(),
                    dock_y + self.height(),
                )
            ]
        )

        print(
            "Orbit excluded region:",
            (
                dock_x,
                dock_y,
                dock_x + self.width(),
                dock_y + self.height(),
            ),
        )

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
