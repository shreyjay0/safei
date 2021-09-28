import os,time,sys
from tkinter import Message
import pyautogui
import wmi
import win32gui, win32con
import ctypes
import threading
import tkinter.simpledialog, winsound
from win10toast import ToastNotifier as toast

def linux_light_off():
    #xset dpms force off
    pass

def get_input_to_setup(title, description):
    tkinter.Tk().withdraw()
    return tkinter.simpledialog.askstring(title, description)

def reminder(reminder, title):
    winsound.PlaySound("*",winsound.SND_ALIAS)
    return ctypes.windll.user32.MessageBoxW(0, reminder, title,1)

def notification(title, notif_msg, t):
    notif = toast()
    notif.show(title, notif_msg, t)

def wait_for_ten_minutes():
    pass

def wmlib():
    return wmi.WMI(namespace='wmi')

def current_brightness():
    return wmlib().WmiMonitorBrightness()[0].CurrentBrightness

def waiting_period(t):
    now = get_time()
    while get_time() - now < t:
        turn_off()
        pyautogui.moveTo(2,2)

def set_brightness(b):
    wmlib().WmiMonitorBrightnessMethods()[0].WmiSetBrightness(b, 0)
    wait(0.2)

def wait(t):
    time.sleep(t)

def turn_off():
    set_brightness(0)
    win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SYSCOMMAND, win32con.SC_MONITORPOWER, 2)

def turn_on():
    SC_MONITORPOWER = 0xF170
    return win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SYSCOMMAND,SC_MONITORPOWER, -1)

def get_time():
    return time.localtime().tm_sec + (time.localtime().tm_min * 60) + (time.localtime().tm_hour * 60)

def start_protection():
    brightness_start = current_brightness()
    brightness = brightness_start
    while brightness >= 10 :    
        brightness -= 10
        set_brightness(brightness)
    brightness_mid = current_brightness()
    return brightness_start, brightness_mid

def end_protection(brightness_start, brightness_mid):
    pyautogui.click(button="middle")
    brightness = brightness_mid
    while brightness < brightness_start:    
        brightness += 10
        set_brightness(brightness)

def main_win(t):
    b_start, b_end = start_protection()
    print("turning off")
    # notification("METIME 😎 - SAFEI 😊","Dimming lights now! Get rest.",10)
    turn_off()
    waiting_period(t)
    turn_on()
    # notification("METIME over 😁 - SAFEI 😊","Dimming lights now! Get rest.",10)
    print("System is now open to use")
    end_protection(b_start, b_end)

# using threading
# def test(): 
#     turn_off()
#     t = threading.Timer(4, turn_on())
#     t.start()
#     turn_on()
#     t.cancel()

def format_time_input(time_in_hhmm):
    return int(time_in_hhmm.split(":")[0]) * 3600 + int(time_in_hhmm.split(":")[1]) * 60

def check_num(input):
    if input == "" and input != None:
        return False
    try:
        input.isnumeric()
        return True
    except:
        exit()

def check_time(input):
    try:
        time.strptime(input,"%H:%M")
        return True
    except:
        return False

def main_lin():
    pass

def start_config(breaks):
    extend_req_count = 0
    #10 minute reminder
    while reminder("This is a reminder to tell you that the screen would be blackened out in 10 minutes. Please make sure you complete your tasks quickly and get it ready to save if it's urgent. We'll send you another notification in another 8 minutes. \n\nPress cancel if you'd like to extend the timing for the start of MeTime by 10 minutes", "METIME 😎 REMINDER - SAFEI 😊") != 1: #rejects
        extend_req_count += 1
        wait(10)
        if extend_req_count == 3:
            break
    if extend_req_count < 3:
        wait(5) #after acceptance
        while reminder("This is a final reminder to tell you that the screen would be blackened out in another 2 minutes. It is advised to minimise all tabs before the MeTime starts. Please make sure you're ready to stop for a while you take rest. Also, you should save it if it's urgent. \n\nPress cancel if you'd like to extend the timing for the start of MeTime by another 5 minutes. Take rest!", "URGENT REMINDER - SAFEI 😊") != 1:
            extend_req_count += 1
            wait(5) #rejection
            if extend_req_count == 3:
                break
        if extend_req_count < 3: main_win(breaks) #acceptance


if sys.platform[:3] == "win":
    interval = ""
    while not check_time(interval) and interval != None:
        interval = get_input_to_setup("Setup - SAFEI 😊", "After what time period are you willing to take breaks? (in hours as \"HH:MM\")")
    if interval : interval_bg = format_time_input(interval)
    else: exit()    
    breaks = ""
    while not check_num(breaks):
        breaks = get_input_to_setup("Setup - SAFEI 😊", "What is your preferred break duration? (in minutes)")
    if not breaks:
        exit()
    go = True
    while True:
        wait(interval)
        start_config(breaks)

elif sys.platform[:5] == "linux": 
    main_lin()

