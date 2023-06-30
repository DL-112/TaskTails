import tkinter as tk
from settings import Settings

class Howtouse:
    def __init__(self, window):
        settings = Settings()
        window.config(bg=settings.bg_color)
        window.title('How to use Task-Tails')
        with open('howtouse.txt', 'r', encoding='utf-8') as f:
            lines = f.read()

        # Create a Label widget
        label = tk.Label(window, wraplength=500, justify='left', font=('arial', 12), text=lines, fg=settings.fg_color, bg=settings.bg_color)  # Set justify to 'left' for left alignment

        # Pack the Label and 'Open File' button into the window
        label.pack(padx=10, pady=10)
