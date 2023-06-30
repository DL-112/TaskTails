import tkinter as tk
from settings import Settings 

class Aboutus:
    def __init__(self, window):
        # Set the window title
        settings = Settings()
        window.title("About Us")
        window.config(bg=settings.bg_color)
        
        # Add a label for your names
        names_label = tk.Label(window, text="Developed by Wai Yan Htut and his team", font=("Arial", 18, "bold"), fg=settings.fg_color, bg=settings.bg_color, padx=10)
        names_label.pack()
        
        # Add a label for the description
        description_label = tk.Label(window, text="\nAs students, we utilize languages such as C, C++, JavaScript, Java, and Python to develop software solutions and automation scripts.", fg=settings.fg_color, bg=settings.bg_color)
        description_label.pack()
        
        # Add a label for the program information
        program_label = tk.Label(window, text="While our programs may have certain imperfections, we believe they will greatly benefit your study endeavors.", fg=settings.fg_color, bg=settings.bg_color)
        program_label.pack(padx=10)
        
        # Add a label for contact information
        contact_label = tk.Label(window, text="\nContact us for feedbacks and bug reports:", font=("Arial", 12), fg=settings.fg_color, bg=settings.bg_color)
        contact_label.pack()

        wyh = tk.Text(window, wrap="none", height=1, width=23, borderwidth=0, highlightthickness=0, fg=settings.fg_color, bg=settings.bg_color)
        wyh.insert("1.0", "waiyanhtut354@gmail.com")
        wyh.config(state='disabled')
        wyh.pack()

        github = tk.Text(window, wrap="none", height=1, width=44, borderwidth=0, highlightthickness=0, fg=settings.fg_color, bg=settings.bg_color)
        github.insert("1.0", "Github: https://github.com/DL-112/TaskTails")
        github.config(state='disabled')
        github.pack()

        contribute = tk.Label(window, text='\nIf you want to contribute this project on github, Go ahead.\nWe appreciate it very much.', fg=settings.special_text_color, bg=settings.bg_color)
        contribute.pack()

