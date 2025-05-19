import sys
from PySide6.QtWidgets import QApplication
from gui.app_window import AntiAwayApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AntiAwayApp()
    window.show()
    sys.exit(app.exec())
