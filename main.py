from tasktails import TaskTails
import platform
import os
import sys
import ctypes
import tkinter as tk
from easy_json import edit_value
from settings import Settings

settings = Settings()

def check_root():
    if platform.system() == "Linux":
        if os.getuid() != 0:
            return False
        else:
            return True
    
    elif platform.system() == "Windows":
        if not ctypes.windll.shell32.IsUserAnAdmin():
            return False
        else:
            return True

def request_admin_access():
    if platform.system() == "Linux":
        root.destroy()
        args = ['sudo', sys.executable, "tasktails.py"] + sys.argv + [os.environ]
        # Relaunch the script with sudo
        edit_value('website_blocking', True, 'data/settings.json')
        os.execlpe('sudo', *args)

    elif platform.system() == "Windows":
        root.destroy()
        script = "tasktails.py"
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script, None, 1)
        edit_value('website_blocking', True, 'data/settings.json')

def press_yes():
    if check_root() != True:
        request_admin_access()
    else:
        root.destroy()
        edit_value('website_blocking', True, 'data/settings.json')
        TaskTails()

def press_no():
    root.destroy()
    edit_value('website_blocking', False, 'data/settings.json' )
    TaskTails()

root = tk.Tk()
root.configure(bg=settings.root_color)

root.iconphoto(True, tk.PhotoImage(file='images/logo.png'))
root.title('Task Tails')

question = tk.Label(root, text='proceed with site blocking feature?\n(You have to permit admin access to modify "host" file)', bg=settings.root_color, fg=settings.fg_color)
question.grid(row=0, columnspan=2, padx=5, pady=5)

yes = tk.Button(root, text='yes', command=press_yes, bg=settings.button_color, fg=settings.fg_color, highlightthickness=0)
yes.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
no = tk.Button(root, text='no', command=press_no, bg=settings.button_color, fg=settings.fg_color, highlightthickness=0)
no.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

root.mainloop()