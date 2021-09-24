import ctypes
import tkinter.simpledialog

class ui: 
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
