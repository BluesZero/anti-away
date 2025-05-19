from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

class NotificationPopup(QWidget):
    def __init__(self, message="Anti-Away se activó automáticamente."):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(320, 80)

        self.setStyleSheet("""
            QWidget {
                background-color: #262626;
                color: white;
                border-radius: 10px;
            }
            QLabel {
                font-size: 13px;
            }
            QPushButton {
                background: none;
                border: none;
                color: #ccc;
                font-size: 14px;
            }
            QPushButton:hover {
                color: red;
            }
        """)

        label = QLabel(message)
        label.setFont(QFont("Segoe UI", 10))

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(20, 20)
        close_btn.clicked.connect(self.close)

        top = QHBoxLayout()
        top.addWidget(label)
        top.addStretch()
        top.addWidget(close_btn)

        layout = QVBoxLayout(self)
        layout.addLayout(top)

        QTimer.singleShot(6000, self.close)  # Cierra solo después de 6 segundos

    def show(self):
        screen_geometry = self.screen().availableGeometry()
        self.move(screen_geometry.width() - self.width() - 20, screen_geometry.height() - self.height() - 40)
        super().show()
