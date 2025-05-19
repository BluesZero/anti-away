from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QSpinBox, QHBoxLayout,
    QCheckBox, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QColor, QPalette, QCursor

from gui.title_bar import TitleBar
from gui.popup import NotificationPopup
from core import get_idle_duration_seconds, simulate_mouse_activity
from config import load_config, save_config
import threading

class AntiAwayApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Anti-Away")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(400, 420)

        # Estilo general de la aplicación
        self.setStyleSheet("""
            QWidget {
                background-color: #2a2a2e;
                color: #ffffff;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel {
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton {
                background-color: #444;
                color: white;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #666;
            }
            QPushButton:pressed {
                background-color: #888;
            }
            QPushButton:disabled {
                background-color: #333;
                color: #aaa;
            }
            QSpinBox {
                background-color: #393943;
                color: white;
                border: 1px solid #666;
                padding: 6px;
                font-size: 14px;
                border-radius: 4px;
            }
            QCheckBox {
                font-size: 13px;
                padding-top: 6px;
            }
            QFrame {
                background-color: #3a3a3e;
                height: 1px;
            }
        """)

        self.config = load_config()
        self.running = False

        self.init_ui()

        # Animación de aparición de la ventana
        self.setWindowOpacity(0.0)
        self.fade_in = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in.setDuration(800)
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.setEasingCurve(QEasingCurve.InOutQuad)
        QTimer.singleShot(100, self.fade_in.start)

        # Verifica inactividad del usuario cada 10 segundos
        self.inactivity_timer = QTimer()
        self.inactivity_timer.timeout.connect(self.check_user_inactivity)
        self.inactivity_timer.start(10000)

        # Iniciar automáticamente si está habilitado
        if self.config["auto_start"]:
            self.start()

    def init_ui(self):
        # Barra de título personalizada
        self.title_bar = TitleBar(self, self.close)

        # Etiqueta de estado (activo/inactivo)
        self.status_label = QLabel("Estado: Inactivo")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Arial", 14))

        # Inputs para intervalo de simulación
        self.interval_label = QLabel("Intervalo de simulación:")

        self.minutes_input = QSpinBox()
        self.minutes_input.setRange(0, 59)
        self.minutes_input.setSuffix(" min")
        self.minutes_input.setFixedWidth(120)

        self.seconds_input = QSpinBox()
        self.seconds_input.setRange(0, 59)
        self.seconds_input.setSuffix(" seg")
        self.seconds_input.setFixedWidth(120)

        interval_inputs = QHBoxLayout()
        interval_inputs.setSpacing(10)
        interval_inputs.addWidget(self.minutes_input)
        interval_inputs.addWidget(self.seconds_input)

        # Checkbox para autoinicio
        self.auto_start_checkbox = QCheckBox("Iniciar automáticamente")
        self.auto_start_checkbox.setChecked(self.config["auto_start"])

        # Selector de tiempo de inactividad
        self.inactivity_spin = QSpinBox()
        self.inactivity_spin.setRange(1, 60)
        self.inactivity_spin.setSuffix(" min de inactividad")
        self.inactivity_spin.setFixedWidth(220)
        self.inactivity_spin.setValue(self.config.get("inactivity_trigger", 4))

        # Checkbox para activar por inactividad
        self.inactivity_checkbox = QCheckBox("Activar por inactividad")
        self.inactivity_checkbox.setChecked(self.config.get("enable_auto_trigger", True))

        # Inicializa valores de tiempo
        total = self.config["interval"]
        self.minutes_input.setValue(total // 60)
        self.seconds_input.setValue(total % 60)

        # Botones de control
        self.start_button = QPushButton("▶ Iniciar")
        self.stop_button = QPushButton("■ Detener")
        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.start_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.stop_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.start_button.setMinimumHeight(48)
        self.stop_button.setMinimumHeight(48)
        self.start_button.setFixedWidth(160)
        self.stop_button.setFixedWidth(160)

        # Layout general
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(self.title_bar)
        layout.addWidget(self.status_label)
        layout.addWidget(QFrame())

        # Tarjeta de configuración
        settings_card = QWidget()
        settings_card.setStyleSheet("background-color: #323238; border-radius: 12px;")
        settings_layout = QVBoxLayout(settings_card)
        settings_layout.setContentsMargins(20, 20, 20, 20)
        settings_layout.setSpacing(12)

        settings_layout.addWidget(self.interval_label)
        settings_layout.addLayout(interval_inputs)
        settings_layout.addWidget(self.auto_start_checkbox)
        settings_layout.addWidget(self.inactivity_spin)
        settings_layout.addWidget(self.inactivity_checkbox)

        layout.addWidget(settings_card)
        layout.addWidget(QFrame())

        # Botones inferiores
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)

        layout.addStretch()

    # Permite mover la ventana sin bordes arrastrando
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPosition().toPoint()

    # Ejecuta el movimiento del mouse en segundo plano
    def simulate(self):
        interval = self.config["interval"]
        simulate_mouse_activity(interval, lambda: self.running)

    # Inicia la simulación
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
            self.config["enable_auto_trigger"] = self.inactivity_checkbox.isChecked()
            save_config(self.config)

            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)

            thread = threading.Thread(target=self.simulate, daemon=True)
            thread.start()

    # Detiene la simulación
    def stop(self):
        self.running = False
        self.status_label.setText("Estado: Inactivo")
        self.animate_status_label("#ff6666")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    # Cambia el color del texto de estado
    def animate_status_label(self, color_hex):
        color = QColor(color_hex)
        palette = self.status_label.palette()
        palette.setColor(QPalette.WindowText, color)
        self.status_label.setPalette(palette)

    # Verifica el tiempo de inactividad y activa si se supera el umbral
    def check_user_inactivity(self):
        idle_time = get_idle_duration_seconds()
        threshold = self.inactivity_spin.value() * 60
        print(f"[DEBUG] Idle time: {idle_time:.1f}s / Threshold: {threshold}s")
        if (
            self.config.get("enable_auto_trigger", True)
            and idle_time >= threshold
            and not self.running
        ):
            self.start()
            self.show_activation_popup()

    # Muestra una notificación cuando se activa automáticamente
    def show_activation_popup(self):
        self.popup = NotificationPopup("💡 Anti-Away se ha activado automáticamente por inactividad.")
        self.popup.show()
