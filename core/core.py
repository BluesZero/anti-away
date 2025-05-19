import ctypes
import pyautogui
import time

def get_idle_duration_seconds():
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
        millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
        return millis / 1000.0
    return 0

def simulate_mouse_activity(interval, should_run):
    while should_run():
        pyautogui.moveRel(1, 0, duration=0.1)
        pyautogui.moveRel(-1, 0, duration=0.1)
        time.sleep(interval)
