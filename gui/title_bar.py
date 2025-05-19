from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt

class TitleBar(QWidget):
    def __init__(self, parent, on_close):
        super().__init__(parent)
        self.setFixedHeight(36)
        self.setStyleSheet("background-color: #1e1e1e;")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)

        icon_label = QLabel()
        icon_label.setPixmap(QPixmap("resources/icon.png").scaled(20, 20, Qt.KeepAspectRatio))
        icon_label.setFixedSize(24, 24)

        title_label = QLabel("  Anti-Away")
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        title_label.setStyleSheet("color: white;")

        close_btn = QPushButton("\u2715")
        close_btn.setFixedSize(28, 28)
        close_btn.setStyleSheet("""
            QPushButton {
                background: none;
                color: white;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                background-color: #aa3333;
            }
        """)
        close_btn.clicked.connect(on_close)

        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(close_btn)
