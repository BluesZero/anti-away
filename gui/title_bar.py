from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout
from PySide6.QtGui import QFont, QPixmap, QCursor, QIcon
from PySide6.QtCore import Qt

class TitleBar(QWidget):
    def __init__(self, parent, on_close):
        super().__init__(parent)
        self.setFixedHeight(44)
        self.setStyleSheet("""
            QWidget {
                background-color: #1b1b1e;
                border-bottom: 1px solid #2e2e33;
            }
            QLabel {
                color: #ffffff;
                font-family: 'Segoe UI';
                font-size: 15px;
                font-weight: bold;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(10)

        icon_label = QLabel()
        icon_label.setPixmap(QPixmap("resources/icon.png").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon_label.setFixedSize(28, 28)

        title_label = QLabel("Anti-Away")

        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addStretch()

        # Minimize button
        minimize_btn = QPushButton()
        minimize_btn.setIcon(QIcon("resources/minimize.png"))
        minimize_btn.setIconSize(QPixmap("resources/minimize.png").scaled(18, 18).size())
        minimize_btn.setFixedSize(32, 32)
        minimize_btn.setCursor(QCursor(Qt.PointingHandCursor))
        minimize_btn.setStyleSheet("""
            QPushButton {
                background-color: #2a2a2e;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #444;
            }
        """)
        minimize_btn.clicked.connect(parent.showMinimized)

        # Close button
        close_btn = QPushButton()
        close_btn.setIcon(QIcon("resources/close.png"))
        close_btn.setIconSize(QPixmap("resources/close.png").scaled(18, 18).size())
        close_btn.setFixedSize(32, 32)
        close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #2a2a2e;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #e04343;
            }
        """)
        close_btn.clicked.connect(on_close)

        layout.addWidget(minimize_btn)
        layout.addWidget(close_btn)
