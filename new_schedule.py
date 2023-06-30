import tkinter as tk
from tkinter import messagebox
import sqlite3
from settings import Settings
import os
from add import Add
from easy_json import edit_value

class New():
    def __init__(self, frame, restart):
        self.restart = restart
        self.master = frame
        self.master.title('Modify Your Shedules')
        self.settings = Settings()
        self.master.config(bg=self.settings.root_color)

        ###############################
        self.restart_json = "data/restart.json"

        # Frame for header
        header_frame = tk.LabelFrame(self.master, text="Enter your schedule name here", bg=self.settings.bg_color, relief='solid', fg=self.settings.fg_color)
        header_frame.pack(padx=10, pady=10, fill='x')

        # label 'add a shedule'
        self.add_topic = tk.Label(header_frame, font=('ariel', 20), text='Add Shedule', bg=self.settings.bg_color, fg=self.settings.fg_color)
        self.add_topic.pack(side='left')

        # topic name textbox
        self.topic_namebox = tk.Entry(header_frame, width=50, font=('ariel', 20), bg=self.settings.root_color, fg=self.settings.fg_color, highlightthickness=0, bd=0)
        self.topic_namebox.pack(padx=10, pady=10, side='left')
        self.topic_namebox.bind("<Return>", self.pressed_enter)

        # new subtopic button
        self.new_topic = tk.Button(header_frame, text='+', font=('bold'), width=8, height=3, bg=self.settings.button_color, highlightthickness=0, bd=0, fg=self.settings.fg_color, command=self.create)
        self.new_topic.pack(side="right", padx=15, pady=10)

        ###############################

        # Create a canvas and scrollbar
        self.scrollbar = tk.Scrollbar(self.master)  # self.scrollbar
        self.scrollbar.pack(side='right', fill='y')

        self.canvas = tk.Canvas(self.master, bg=self.settings.bg_color, yscrollcommand=self.scrollbar.set, highlightbackground='black')
        self.canvas.pack(fill='x', expand=True, anchor='nw', padx=10)

        # Binding with the canvas with mousewheel
        # self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        self.scrollbar.config(command=self.canvas.yview)

        # Just a Label
        existed = tk.Label(self.canvas, text="Existing Data Bases < press the name to add more elements >", font=self.settings.font, bg=self.settings.button_color, fg=self.settings.fg_color)
        existed.pack(padx=10, pady=5, side='top', anchor='w')

        # Initialize false to window
        self.new_subtopic_window = None

        # Display existing databases
        self.update_db_button()

    # def on_mousewheel(self, event):
    #    self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def create(self):
        # Get user typed topic name from text box
        self.topic_name = self.topic_namebox.get()
        self.topic_name = self.topic_name.replace("\n", "")

        # Replace spaces with underscores
        self.topic_name = self.topic_name.replace(" ", "_")

        # Create a database with the given name in the "data" folder
        db_path = os.path.join("data", f"{self.topic_name}.db")
        if not os.path.exists(db_path):
            
            # Replace back
            self.topic_name = self.topic_name.replace("_", " ")

            # Making sure
            confirm = messagebox.askokcancel("Create Schedule", f"Create a new schedule called {self.topic_name}?")

            if confirm:
                conn = sqlite3.connect(db_path)

                # Create a cursor object to execute SQL commands
                c = conn.cursor()

                # Create the tasks table if it doesn't exist
                c.execute('''CREATE TABLE IF NOT EXISTS tasks
                            (subtopic text, 
                            description text, 
                            time text, 
                            completed bool)''')
                
                conn.commit()
                conn.close()

                # Replace again Lol
                self.topic_name = self.topic_name.replace(" ", "_")

                # Add the new database name to the list and update the label in the GUI
                self.db_names.append(self.topic_name)
                self.restart()
        else:
            # Database file already exists, show an error message
            messagebox.showerror(
                "Error", f"Database '{self.topic_name}' already exists.")

    def update_db_button(self):

        # Declaring databases
        data_path = "data"
        self.db_names = [file for file in os.listdir(
            data_path) if file.endswith('.db')]

        # Remove the existing frames
        frame_to_remove = []
        for key, widget in self.canvas.children.items():
            if isinstance(widget, tk.Frame):
                frame_to_remove.append(widget)

        for frame in frame_to_remove:
            frame.destroy()

        # Create and pack new button widgets for each database name in the list
        for db in self.db_names:

            button_frame = tk.Frame(
                self.canvas, bg=self.settings.frame_bg_color)
            button_frame.pack(side="top", anchor='w', padx=10, pady=5)

            # Adding a new subtopic to a database
            db_button = tk.Button(button_frame, text=db, font=self.settings.font, bg=self.settings.button_color, fg=self.settings.fg_color, command=lambda db=db: self.add_subtopic(db))
            db_button.pack(padx=10, pady=5, side="left", anchor="w")

            # Delete buttons to delete a database
            delete = tk.Button(button_frame, text="delete", font=self.settings.font, bg=self.settings.button_color, fg=self.settings.fg_color, command=lambda db=db: self.delete_db(db))
            delete.pack(padx=10, pady=5, side="left")

    def delete_db(self, database):

        # Remove the newline character from the database name
        database = database.strip()

        # Ask the user to confirm the deletion
        confirm = messagebox.askokcancel(
            "Confirm Deletion", f"Are you sure you want to delete {database}?")

        # Delete the database if the user confirmed the deletion
        if confirm:

            # Delete the database if it exists
            path = os.path.join("data", database)
            try:
                os.remove(path)
                self.restart()
            except FileNotFoundError:
                print(f"File {path} not found.")
                return

    def add_subtopic(self, db):

        path_to_pass = os.path.join("data", db)
        # check if there is existing new subtopic window
        # only false value will create a window
        if self.new_subtopic_window is None or not self.new_subtopic_window.winfo_exists():
            # create a toplevel window under the first frame
            self.new_subtopic_window = tk.Toplevel(self.master)
            new_subtopic_gui = Add(self.new_subtopic_window, path_to_pass)
        else:
            self.new_subtopic_window.lift()

    def pressed_enter(self, event):
        self.create()