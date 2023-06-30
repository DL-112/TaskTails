import tkinter as tk
from settings import Settings
import sqlite3
from easy_json import get_value
import os
from timer import Timer
from PIL import Image, ImageDraw, ImageTk
from edit import Edit
import platform
from block import WebsiteBlocker
import atexit

class SecondFrame(tk.Frame):
    def __init__(self, frame, restart):
        self.restart = restart

        self.settings = Settings()
        self.frame = frame

        # set the frame color
        self.frame.config(bg=self.settings.frame_bg_color)

        # Declaring databases
        data_path = "data"
        self.db_names = [file for file in os.listdir(data_path) if file.endswith('.db')] 
        self.index = 0

        # left and right tkimag
        self.left_image = self.create_button_picture('back', 70)
        self.right_image = self.create_button_picture('next', 70)
        self.restart_image = self.create_button_picture('restart', 50)

        if get_value('theme', 'data/settings.json') == 'white':
            # left and right tkimag
            self.left_image = self.create_button_picture('white/back', 70)
            self.right_image = self.create_button_picture('white/next', 70)
            self.restart_image = self.create_button_picture('white/restart', 50)

        ### HEADER FRAME
        # Create header frame for the header
        header_frame = tk.Frame(self.frame, bg=self.settings.bg_color, relief='solid')
        header_frame.pack(padx=10, pady=(0,10), fill='x')

        # buttons in the header frame
        self.left_button = tk.Button(header_frame, image=self.left_image, text="", fg=self.settings.fg_color, compound=tk.LEFT, bg=self.settings.bg_color, highlightthickness=0, bd=0, command=self.left_click)
        self.left_button.pack(side="left", padx=15, pady=10)

        # Add a maintopic to the header_frame
        self.maintopic = tk.Label(header_frame, text=self.settings.maintopic, font=('Arial', 20), height=2, bg=self.settings.bg_color, fg=self.settings.fg_color)
        self.maintopic.pack(side="left", padx=15, pady=10)

        self.right_button = tk.Button(header_frame, image=self.right_image, text="", fg=self.settings.fg_color, compound=tk.RIGHT, bg=self.settings.bg_color, highlightthickness=0, bd=0, command=self.right_click)
        self.right_button.pack(side="right", padx=15, pady=10)

        # Frame for Timer
        self.timer_frame = tk.Frame(header_frame, bg = self.settings.button_color, bd=2, highlightthickness=2)
        self.timer_frame.pack(side='right')

        self.restart_button = tk.Button(header_frame, image=self.restart_image, text="", fg=self.settings.fg_color, compound=tk.RIGHT, bg=self.settings.bg_color, highlightthickness=0, bd=0, command=self.pressed_restart_button)
        self.restart_button.pack(side="right", padx=15, pady=10)

        # Starting the timer
        self.timer = None 
        self.start_timer()

        # Create a canvas and scrollbar
        self.scrollbar = tk.Scrollbar(self.frame) # self.scrollbar
        self.scrollbar.pack(side='right', fill='y')

        self.canvas = tk.Canvas(self.frame, bg=self.settings.bg_color, yscrollcommand=self.scrollbar.set, highlightbackground='black')
        self.canvas.pack(fill='both', expand=True, anchor='nw', padx=10)

        # Binding with the canvas with mousewheel
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        self.scrollbar.config(command=self.canvas.yview)

        # Initialize false to edit window
        self.edit_window = None

        ### call, delete and call // temporary fix //
        self.change_db()
        self.canvas.delete("all")
        self.change_db()

    def change_db(self):

        # Create frame for Sub Topics
        subTopic_frame = tk.Frame(self.canvas, bg=self.settings.bg_color, relief='solid')
        subTopic_frame.grid(row=0, column=0, sticky='nsew')

        # Create frame for Checkbox
        complete_frame = tk.Frame(self.canvas, bg=self.settings.bg_color, relief='solid')
        complete_frame.grid(row=0, column=1, sticky='nsew')

        # Configure grid weights to allow frames to expand
        self.canvas.grid_rowconfigure(0, weight=1)
        self.canvas.grid_columnconfigure(0, weight=1)
        self.canvas.grid_columnconfigure(1, weight=1)

        # Set column minimum sizes to keep frames on left and right
        self.canvas.grid_columnconfigure(0, minsize=subTopic_frame.winfo_reqwidth())
        self.canvas.grid_columnconfigure(1, minsize=complete_frame.winfo_reqwidth())

        # Create a connection to the database
        self.db_which = "data/" + self.db_names[self.index]
        self.conn = sqlite3.connect(self.db_which)

        # Create a cursor object to execute SQL commands
        self.c = self.conn.cursor()

        # Select all data from the table
        self.c.execute("SELECT * FROM tasks")

        # Fetch all the rows from the query result
        rows = self.c.fetchall()

        # Display main topic
        maintopic = os.path.basename(self.db_which).replace('_', ' ')
        maintopic = os.path.splitext(maintopic)[0]
        self.maintopic.config(text=maintopic)
        
        # Format the rows into a string
        for row in rows:

            edit_and_task_topic_frame = tk.Frame(subTopic_frame,bg=self.settings.bg_color)
            edit_and_task_topic_frame.pack(side='top',anchor='w')
            
            task_topic = tk.Label(edit_and_task_topic_frame, text=f"{row[0]}", fg=self.settings.fg_color, bg=self.settings.button_color, font=('Arial', 16, 'bold'), bd=10)
            task_topic.pack(side='left', anchor='w', pady=10, padx=10)

            edit_button = tk.Button(edit_and_task_topic_frame, text='Edit', fg=self.settings.fg_color, bg=self.settings.button_color, command=lambda row=row: self.edit_clicked(row))
            edit_button.pack(side='left', anchor='w', pady=10, padx=10)

            description_frame = tk.Frame(subTopic_frame, bg=self.settings.bg_color)
            description_frame.pack(side='top', anchor='w', padx=20, pady=5, fill='x')

            task_description = tk.Label(description_frame, text=f"{row[1]}", fg=self.settings.fg_color, bg=self.settings.bg_color, font=('Arial', 12))
            task_description.grid(row=0, column=0, sticky='w')

            task_time = tk.Label(description_frame, text=f"Time: {row[2]}", fg=self.settings.fg_color, bg=self.settings.bg_color, font=('Arial', 12))
            task_time.grid(row=1, column=0, sticky='w')
            task_time.grid(row=1, column=0, sticky='w')

        # Loop through the database and display Completed or Not Completed
        i = 0
        for row in rows:
            if row[3]:
                completeOrNot = "Completed"
            else:
                completeOrNot = "Not Completed"

            task_complete = tk.Label(complete_frame, text=completeOrNot, fg=self.settings.fg_color, bg=self.settings.bg_color, font=('Arial', 12))
            task_complete.grid(row=i, column=1, sticky='ne', pady=50, padx=(300,0))
            i = i+1
            #complete_maintopic = tk.maintopic(complete_frame, text=completeOrNot, fg=self.settings.fg_color, bg=self.settings.bg_color, font=('Arial', 12))
            #complete_maintopic.grid(row=index, column=1, sticky='e', pady=50, padx=(460,0))
       
        # Associate the frames with the self.canvas
        self.canvas.create_window((0, 0), window=subTopic_frame, anchor='nw')
        self.canvas.create_window((self.canvas.winfo_width(), 0), window=complete_frame, anchor='ne')

        subTopic_frame.update_idletasks()
        complete_frame.update_idletasks()  # necessary to get the correct dimensions of the scrollable frame
        self.canvas.config(scrollregion=self.canvas.bbox('all'))

        # Close the connection to the database
        self.conn.close()

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def right_click(self):
        self.index += 1
        if self.index > len(self.db_names)-1:
            self.index = 0
        self.canvas.delete('all')
        self.change_db()

    def left_click(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.db_names)-1
        self.canvas.delete('all')
        self.change_db()

    def create_button_picture(self, which, image_size):
        # open the image and convert it to RGBA mode
        img = Image.open(f'images/{which}.png').convert('RGBA')

        # Resize the image
        img = img.resize((image_size, image_size), Image.LANCZOS)

        # create a new image with the same size and fill it with white color
        background = Image.new('RGBA', img.size)
        draw = ImageDraw.Draw(background)
        draw.rectangle((0, 0, img.size[0], img.size[1]), fill=self.settings.bg_color)

        # merge the color-filled image with the original image
        result = Image.alpha_composite(background, img)

        # Create a Tkinter image object
        tkimg = ImageTk.PhotoImage(result)

        # now just return the image and create button inside the constructor method
        return tkimg
        
    def start_timer(self):
        self.timer = Timer(self.timer_frame)

    def edit_clicked(self, row):
        # check if there is existing edit window
        # only false value will create a window
        if self.edit_window is None or not self.edit_window.winfo_exists():
            # create a toplevel window under the first frame
            self.edit_window = tk.Toplevel(self.frame)
            Edit(self.edit_window, self.db_which, row, self.restart)
        else:
            self.edit_window.lift()

    def clear_hosts_file(self):
        file_path = self.get_hosts_path()
        lines_to_keep = []
        with open(file_path, "r") as file:
            for line in file:
                if "127.0.0.1" not in line:
                    lines_to_keep.append(line)

        with open(file_path, "w") as file:
            file.writelines(lines_to_keep)

    def get_hosts_path(self):
        system_name = platform.system()
        if system_name == "Linux" or system_name == "Darwin":
            return "/etc/hosts"
        elif system_name == "Windows":
            return r"C:\Windows\System32\drivers\etc\hosts"
        else:
            raise OSError("Unsupported operating system")
        
    def pressed_restart_button(self):
        self.restart()
