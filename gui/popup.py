from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, QTimer

class NotificationPopup(QDialog):
    def __init__(self, message):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                border: 1px solid #888;
                border-radius: 8px;
            }
            QLabel {
                color: white;
                font-size: 13px;
            }
            QPushButton {
                background-color: #3a3a3a;
                color: white;
                padding: 4px 10px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        self.setFixedSize(260, 100)

        layout = QVBoxLayout()
        self.label = QLabel(message)
        self.label.setWordWrap(True)

        self.button = QPushButton("Cerrar")
        self.button.clicked.connect(self.close)

        layout.addWidget(self.label)
        layout.addWidget(self.button, alignment=Qt.AlignRight)
        self.setLayout(layout)

        self.move_to_bottom_right()
        QTimer.singleShot(7000, self.close)

    def move_to_bottom_right(self):
        screen = self.screen().availableGeometry()
        self.move(screen.width() - self.width() - 20, screen.height() - self.height() - 20)
