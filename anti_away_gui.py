import sys
import threading
import time
import json
import ctypes
import pyautogui

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QSpinBox, QHBoxLayout, QCheckBox, QFrame, QMessageBox, QDialog
)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QFont, QColor, QPalette, QCursor, QPixmap, QIcon

CONFIG_FILE = "config.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"interval": 300, "auto_start": False}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def get_idle_duration_seconds():
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
        millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
        return millis / 1000.0
    return 0

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

        # Desaparece automáticamente tras 7 segundos
        QTimer.singleShot(7000, self.close)

    def move_to_bottom_right(self):
        screen = QApplication.primaryScreen().availableGeometry()
        self.move(screen.width() - self.width() - 20, screen.height() - self.height() - 20)

class AntiAwayApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Anti-Away")
        self.setWindowIcon(QIcon("icon.png"))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(400, 360)

        self.setStyleSheet("""
            QWidget { background-color: #2a2a2e; color: #ffffff; }
            QLabel { font-size: 14px; }
            QPushButton {
                background-color: #3e3e44;
                color: white;
                border: none;
                padding: 10px 18px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #5c5c66;
            }
            QPushButton:pressed {
                background-color: #70707a;
            }
            QPushButton:disabled {
                background-color: #2f2f33;
                color: #999999;
            }
            QSpinBox {
                background-color: #383840;
                color: white;
                border: 1px solid #666;
                padding: 4px;
                font-size: 14px;
            }
            QCheckBox {
                font-size: 13px;
            }
            QFrame {
                background-color: #3a3a3e;
                height: 1px;
            }
        """)

        self.config = load_config()
        self.running = False

        self.init_ui()

        self.setWindowOpacity(0.0)
        self.fade_in = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in.setDuration(800)
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.setEasingCurve(QEasingCurve.InOutQuad)
        QTimer.singleShot(100, self.fade_in.start)

        # Verificar inactividad cada 10 segundos
        self.inactivity_timer = QTimer()
        self.inactivity_timer.timeout.connect(self.check_user_inactivity)
        self.inactivity_timer.start(10000)

        if self.config["auto_start"]:
            self.start()

    def init_ui(self):
        self.title_bar = QWidget()
        self.title_bar.setStyleSheet("background-color: #1e1e1e;")
        self.title_bar.setFixedHeight(36)

        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(10, 0, 10, 0)

        icon_label = QLabel()
        icon_label.setPixmap(QPixmap("icon.png").scaled(20, 20, Qt.KeepAspectRatio))
        icon_label.setFixedSize(24, 24)

        title_label = QLabel("  Anti-Away")
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        title_label.setStyleSheet("color: white;")

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(28, 28)
        close_btn.clicked.connect(self.close)
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

        title_layout.addWidget(icon_label)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(close_btn)

        self.status_label = QLabel("Estado: Inactivo")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Arial", 14))

        self.interval_label = QLabel("Intervalo de simulación:")

        self.minutes_input = QSpinBox()
        self.minutes_input.setRange(0, 59)
        self.minutes_input.setPrefix("Min: ")
        self.minutes_input.setFixedWidth(100)

        self.seconds_input = QSpinBox()
        self.seconds_input.setRange(0, 59)
        self.seconds_input.setPrefix("Seg: ")
        self.seconds_input.setFixedWidth(100)

        total_seconds = self.config["interval"]
        self.minutes_input.setValue(total_seconds // 60)
        self.seconds_input.setValue(total_seconds % 60)

        self.auto_start_checkbox = QCheckBox("Iniciar automáticamente")
        self.auto_start_checkbox.setChecked(self.config["auto_start"])

        self.inactivity_spin = QSpinBox()
        self.inactivity_spin.setRange(1, 60)
        self.inactivity_spin.setSuffix(" min de inactividad")
        self.inactivity_spin.setValue(self.config.get("inactivity_trigger", 4))
        self.inactivity_spin.setFixedWidth(220)
        

        self.start_button = QPushButton("▶ Iniciar")
        self.stop_button = QPushButton("■ Detener")
        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.start_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.stop_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 10)
        layout.addWidget(self.title_bar)
        layout.addWidget(self.status_label)

        layout.addWidget(QFrame())

        settings_layout = QVBoxLayout()
        settings_layout.addWidget(self.interval_label)

        interval_inputs = QHBoxLayout()
        interval_inputs.addWidget(self.minutes_input)
        interval_inputs.addWidget(self.seconds_input)
        settings_layout.addLayout(interval_inputs)

        layout.addLayout(settings_layout)
        layout.addWidget(self.auto_start_checkbox)

        layout.addWidget(self.inactivity_spin)

        layout.addWidget(QFrame())

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)

        layout.addStretch()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPosition().toPoint()

    def simulate_activity(self, interval):
        while self.running:
            pyautogui.moveRel(1, 0, duration=0.1)
            pyautogui.moveRel(-1, 0, duration=0.1)
            time.sleep(interval)

    def animate_status_label(self, color_hex):
        color = QColor(color_hex)
        palette = self.status_label.palette()
        palette.setColor(QPalette.WindowText, color)
        self.status_label.setPalette(palette)

    def start(self):
        if not self.running:
            minutes = self.minutes_input.value()
            seconds = self.seconds_input.value()
            interval = minutes * 60 + seconds

            if interval < 1:
                QMessageBox.warning(self, "Intervalo inválido", "Debes seleccionar al menos 1 segundo.")
                return

            self.running = True
            self.status_label.setText("Estado: Activo")
            self.animate_status_label("#00ff66")
            self.config["interval"] = interval
            self.config["auto_start"] = self.auto_start_checkbox.isChecked()
            self.config["inactivity_trigger"] = self.inactivity_spin.value()
            save_config(self.config)

            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)

            thread = threading.Thread(target=self.simulate_activity, args=(interval,), daemon=True)
            thread.start()

    def stop(self):
        self.running = False
        self.status_label.setText("Estado: Inactivo")
        self.animate_status_label("#ff6666")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def check_user_inactivity(self):
        idle_time = get_idle_duration_seconds()
        inactivity_threshold = self.config.get("inactivity_trigger", 4) * 60  # minutos a segundos
        if idle_time >= inactivity_threshold and not self.running:
            self.start()
            self.show_activation_popup()


    def show_activation_popup(self):
        self.popup = NotificationPopup("🛡️ Anti-Away se ha activado automáticamente por 4 minutos de inactividad.")
        self.popup.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AntiAwayApp()
    window.show()
    sys.exit(app.exec())
