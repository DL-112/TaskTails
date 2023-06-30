import sqlite3
import tkinter as tk
from settings import Settings
from tkinter import messagebox

class Edit():
    def __init__(self, master, db, tuple, restart):
        self.restart = restart

        # Create setting object
        self.settings = Settings()

        self.master = master
        self.master.title('Edit your Subtopic')
        self.master.config(bg=self.settings.root_color)

        # Declaring databases 
        self.database = db # This is a location string
        self.tuple = tuple # This is a data tuple

        ################################

        # Frame
        self.entry_frame = tk.LabelFrame(self.master, bg=self.settings.bg_color, text="Change your subtopic name", fg=self.settings.fg_color)
        self.entry_frame.pack(padx=10, pady=10)

        self.entry = tk.Text(self.entry_frame, height=1, width=25, font=('ariel', 15), bg=self.settings.root_color, fg=self.settings.fg_color, highlightthickness=0, bd=0)
        self.entry.pack(padx=10, pady=10)
        self.entry.insert("1.0", self.tuple[0])

        # Frame for others
        self.frame = tk.LabelFrame(self.master, bg=self.settings.bg_color, text="Change other details", fg=self.settings.fg_color)
        self.frame.pack(padx=10, pady=(0,10))

        # Adding widgets to the frame
        self.description = tk.Text(self.frame, height=1, width=25, font=('ariel', 15), bg=self.settings.root_color, fg=self.settings.fg_color, highlightthickness=0, bd=0)
        self.description.pack(padx=10, pady=10)
        self.description.insert("1.0", self.tuple[1])

        self.time = tk.Text(self.frame, height=1, width=25, font=('ariel', 15), bg=self.settings.root_color, fg=self.settings.fg_color, highlightthickness=0, bd=0)
        self.time.pack(padx=10, pady=(0,10))
        self.time.insert("1.0", self.tuple[2])

        self.var = tk.IntVar()

        if(tuple[3]):
            self.var.set(1)
        else:
            self.var.set(2)

        self.completed = tk.Radiobutton(self.frame, selectcolor=self.settings.bg_color, text="Completed", variable=self.var, value=1, font=self.settings.font,  fg=self.settings.special_text_color, bg=self.settings.input_color, highlightthickness=0, bd=0)
        self.completed.pack(padx=10, pady=10, anchor='w')

        self.not_completed = tk.Radiobutton(self.frame, selectcolor=self.settings.bg_color, text="Not Completed", variable=self.var, value=2, font=self.settings.font,  fg=self.settings.special_text_color, bg=self.settings.input_color, highlightthickness=0, bd=0)
        self.not_completed.pack(padx=10, pady=(0,10), anchor='w')

        #######################
        # Frame for buttons
        self.button_frame = tk.Frame(self.frame, background=self.settings.bg_color)
        self.button_frame.pack(fill='x')

        # Delete
        self.delete = tk.Button(self.button_frame, text="Delete", height=1, font=('ariel', 15), fg=self.settings.fg_color, bg=self.settings.button_color, command=self.delete)
        self.delete.pack(side='left', padx=5, pady=5)  # Place on the left side

        # Ok
        self.okay = tk.Button(self.button_frame, text="Ok", height=1, font=('ariel', 15), fg=self.settings.fg_color, bg=self.settings.button_color, command=self.ok)
        self.okay.pack(side='right', padx=5, pady=5)  # Place on the right side

        ##################################

    def handle_selection(self):
        if self.var.get() == 1:
            self.compledted_or_not = True
        elif self.var.get() == 2:
            self.compledted_or_not = False

    def ok(self):

        # Get user typed informations

        self.subtopic_name = self.entry.get("1.0", tk.END)
        self.subtopic_name = self.subtopic_name.replace("\n", "")

        self.description_value = self.description.get("1.0", tk.END)
        self.description_value = self.description_value.replace("\n", "")

        self.time_value = self.time.get("1.0", tk.END)
        self.time_value = self.time_value.replace("\n", "")

        self.handle_selection()

        # Create a connection to the database
        conn = sqlite3.connect(self.database)

        # Create a cursor object to execute SQL commands
        c = conn.cursor()

        # Construct the query using the existing tuple values
        query = "UPDATE tasks SET subtopic=?, description=?, time=?, completed=? WHERE subtopic=? AND description=? AND time=? AND completed=?"

        # Insert data into the tasks table
        data = (self.subtopic_name, self.description_value, self.time_value, self.compledted_or_not)

        # Execute the query with the existing and new tuples as parameters
        c.execute(query, (data[0], data[1], data[2], data[3], self.tuple[0], self.tuple[1], self.tuple[2], self.tuple[3]))

        # Commit the changes to the database and close the connection
        conn.commit()
        conn.close()

        self.master.destroy()
        self.restart()

    def delete(self):
        # Display a messagebox to confirm the deletion
        confirm = messagebox.askokcancel("Confirm Deletion", "Are you sure you want to delete this subtopic?")

        if confirm:
            # Create a connection to the database
            conn = sqlite3.connect(self.database)

            # Create a cursor object to execute SQL commands
            c = conn.cursor()

            # Delete the subtopic from the database
            c.execute("DELETE FROM tasks WHERE subtopic=? AND description=? AND time=? AND completed=?", self.tuple)

            # Commit the changes to the database and close the connection
            conn.commit()
            conn.close()
