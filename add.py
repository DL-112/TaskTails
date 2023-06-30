import tkinter as tk
import sqlite3
from settings import Settings

class Add():
    def __init__(self, master, db):
        self.master = master
        self.master.title('Add a Subtopic')
        self.settings = Settings()
        self.master.config(bg=self.settings.root_color)
        self.db = db
        print(db)
    
        ################################

        # Frame
        self.entry_frame = tk.LabelFrame(self.master, bg=self.settings.bg_color, fg=self.settings.fg_color, text="Enter your subtopic name here")
        self.entry_frame.pack(padx=10, pady=10)

        self.entry = tk.Text(self.entry_frame, height=1, width=25, font=('ariel', 15), bg=self.settings.root_color, fg=self.settings.fg_color, highlightthickness=0, bd=0)
        self.entry.pack(padx=10, pady=10)
        self.entry.insert("1.0", "Your subtopic name")

        # Frame for others
        self.frame = tk.LabelFrame(self.master, bg=self.settings.bg_color, text="Enter more details", fg=self.settings.fg_color)
        self.frame.pack(padx=10, pady=(0,10))

        # Adding widgets to the frame
        self.description = tk.Text(self.frame, height=1, width=25, font=('ariel', 15), bg=self.settings.root_color, fg=self.settings.fg_color, highlightthickness=0, bd=0)
        self.description.pack(padx=10, pady=10)
        self.description.insert("1.0", "your description")

        self.time = tk.Text(self.frame, height=1, width=25, font=('ariel', 15), bg=self.settings.root_color, fg=self.settings.fg_color, highlightthickness=0, bd=0)
        self.time.pack(padx=10, pady=(0,10))
        self.time.insert("1.0", "your time plan")

        # Ok
        self.okay = tk.Button(self.frame, text="Ok", height=1, font=('ariel', 15), bg=self.settings.button_color, fg=self.settings.fg_color, highlightthickness=0, bd=0, command=self.ok)
        self.okay.pack(anchor='e')

    def ok(self):

        # Get user typed informations

        self.subtopic_name = self.entry.get("1.0", tk.END)
        self.subtopic_name = self.subtopic_name.replace("\n", "")

        self.description_value = self.description.get("1.0", tk.END)
        self.description_value = self.description_value.replace("\n", "")

        self.time_value = self.time.get("1.0", tk.END)
        self.time_value = self.time_value.replace("\n", "")

        # Create a connection to the database
        conn = sqlite3.connect(self.db)

        # Create a cursor object to execute SQL commands
        c = conn.cursor()

        # Insert data into the tasks table
        data = [(self.subtopic_name, self.description_value, self.time_value, False)]
        c.executemany("INSERT INTO tasks VALUES (?,?,?,?)", data)

        # Commit the changes to the database and close the connection
        conn.commit()
        conn.close()

        # Close the window
        self.master.destroy()
