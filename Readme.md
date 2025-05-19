# Anti-Away

**Anti-Away** es una aplicación de escritorio que simula actividad del mouse en intervalos definidos para evitar que Microsoft Teams (u otros programas) te pongan como "ausente" automáticamente. También puede activarse tras un periodo de inactividad detectado del usuario.

Este software ha sido desarrollado con fines de comodidad personal y productividad. Anti-Away puede ser útil en situaciones como:

- Evitar bloqueos de pantalla durante presentaciones o reuniones largas.
- Mantener procesos activos en segundo plano sin interrupciones automáticas.
- Prevenir suspensiones del sistema en entornos controlados.

**No está diseñado para ser utilizado como medio para evadir responsabilidades laborales ni engañar a sistemas de control de productividad sin consentimiento.**

⚠️ El uso indebido de esta herramienta en entornos laborales o institucionales puede violar políticas internas. El usuario es responsable de verificar y respetar las normas de su entorno.

> Anti-Away es una herramienta neutral. El uso ético y responsable depende exclusivamente del usuario.
---

## 🚀 Características

- Interfaz moderna con PySide6
- Barra de título personalizada
- Configuración de intervalos en minutos y segundos
- Activación automática tras X minutos de inactividad
- Configuración persistente en `config.json`
- Movimiento de ventana personalizada (sin bordes del sistema)

---

## 🧱 Requisitos

Instala las dependencias ejecutando:

```bash
pip install -r requirements.txt
```

---

## ▶️ Cómo usar

1. Ejecuta la aplicación:

```bash
python main.py
```

2. Define el intervalo de simulación (minutos y segundos)
3. Marca la opción de "Iniciar automáticamente" si deseas que se active al arrancar
4. Puedes establecer cuántos minutos de inactividad se requieren para que se active automáticamente

---

## 📁 Estructura del proyecto

```
anti_away/
├── main.py
├── config.py
├── requirements.txt
├── config.json
├── core/
│   ├── __init__.py
│   └── core.py
├── gui/
│   ├── __init__.py
│   ├── app_window.py
│   └── title_bar.py
└── resources/
    └── icon.png
```

---

## 🧊 Compilación a .exe (opcional)

Usa PyInstaller:

```bash
pyinstaller --onefile --noconsole --icon=resources/icon.ico main.py
```

---

## 🛠 Dependencias principales

- [PySide6](https://doc.qt.io/qtforpython/) - UI moderna
- [pyautogui](https://pyautogui.readthedocs.io/) - Simula movimiento de mouse
- [pywin32](https://github.com/mhammond/pywin32) - Detecta inactividad del sistema (solo Windows)

---

## 📄 Licencia

MIT License

---

Hecho con 💻 por [Tu Nombre Aquí]
