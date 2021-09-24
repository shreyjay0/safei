import os,time,sys
import pyautogui
import wmi
import win32gui, win32con
import ctypes
import threading
import tkinter

def linux_light_off():
    #xset dpms force off
    pass
def get_intervals():
    tkinter.Tk().withdraw()
    return tkinter.simpledialog.askstring("Setup - SAFEI 😊", "After what time period are you willing to take breaks? (in hours)")

def get_break_time():
    tkinter.Tk().withdraw()
    return tkinter.simpledialog.askstring("Setup - SAFEI 😊", "What is your preferred break duration? (in minutes)")

def ten_minute_reminder():
    return ctypes.windll.user32.MessageBoxW(0, "This is a reminder to tell you that the screen would be blackened out in 10 minutes. Please make sure you complete your tasks quickly and get it ready to save if it's urgent. We'll send you another notification in another 8 minutes. \n\nPress cancel if you'd like to extend the timing for the start of MeTime by 10 minutes", "METIME 😎 REMINDER - SAFEI 😊",1)

def two_minute_reminder():
    return ctypes.windll.user32.MessageBoxW(0, "This is a final reminder to tell you that the screen would be blackened out in another 2 minutes. It is advised to minimise all tabs before the MeTime starts. Please make sure you're ready to stop for a while you take rest. Also, you should save it if it's urgent. \n\nPress cancel if you'd like to extend the timing for the start of MeTime by 10 minutes. Take rest!", "URGENT REMINDER - SAFEI 😊",1)

def wait_for_ten_minutes():
    pass

def wmlib():
    return wmi.WMI(namespace='wmi')

def current_brightness():
    return wmlib().WmiMonitorBrightness()[0].CurrentBrightness

def waiting_period(now):
    while get_time() - now < 10:
        turn_off()
        pyautogui.moveTo(2,2)

def set_brightness(b):
    wmlib().WmiMonitorBrightnessMethods()[0].WmiSetBrightness(b, 0)
    wait(0.2)

def wait(t):
    time.sleep(t)

def turn_off():
    SC_MONITORPOWER = 0xF170
    return win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SYSCOMMAND,SC_MONITORPOWER, 2)

def turn_on():
    SC_MONITORPOWER = 0xF170
    return win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SYSCOMMAND,SC_MONITORPOWER, -1)

def get_time():
    return time.localtime().tm_sec + (time.localtime().tm_min * 60) + (time.localtime().tm_hour * 60)

def start_protection():
    brightness_start = current_brightness()
    brightness = brightness_start
    while brightness > 10 :    
        brightness -= 10
        set_brightness(brightness)
    turn_off()
    brightness_mid = current_brightness()
    return brightness_start, brightness_mid

def end_protection(brightness_start, brightness_mid):
    pyautogui.click(button="middle")
    brightness = brightness_mid
    while brightness < brightness_start:    
        brightness += 10
        set_brightness(brightness)

def main_win():
    b_start, b_end = start_protection()
    now = get_time()
    waiting_period(now)
    turn_off()
    end_protection(b_start, b_end)

# using threading
# def test(): 
#     turn_off()
#     t = threading.Timer(4, turn_on())
#     t.start()
#     turn_on()
#     t.cancel()

def main_lin():
    pass

if sys.platform[:3] == "win":
    interval = get_intervals()
    breaks= get_break_time()
    if ten_minute_reminder() == 1: #accepts
        # wait(10)
        if two_minute_reminder() == 1:
            main_win()
        else:
            wait(600)
    else: #when user rejects
        wait(600)

elif sys.platform[:5] == "linux": 
    main_lin()

#pythonw.exe .\safei.py