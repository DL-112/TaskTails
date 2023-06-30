import tkinter as tk
from settings import Settings
import json
from tkinter import messagebox
from urllib.parse import urlparse
import re

class Web():
    def __init__(self, frame):

        self.master = frame
        self.master.title('Block Websites')
        self.settings = Settings()
        self.master.config(bg=self.settings.root_color)
        self.sites_to_block = []

        ################################

        # Frame for header
        header_frame = tk.LabelFrame(self.master, text="Enter your website address here", bg=self.settings.bg_color, relief='solid', fg=self.settings.fg_color)
        header_frame.pack(padx=10, pady=10, fill='x')

        # label 'add a website'
        self.add_label = tk.Label(header_frame, font=('ariel', 20), text='Add website url', bg=self.settings.bg_color, fg=self.settings.fg_color)
        self.add_label.pack(side='left')

        # topic name textbox
        self.web_address_box = tk.Entry(header_frame, width=50, font=('ariel', 20), bg=self.settings.root_color, fg=self.settings.fg_color, highlightthickness=0, bd=0)
        self.web_address_box.pack(padx=5, pady=10, side='left')
        self.web_address_box.bind("<Return>", self.pressed_enter)

        # new subtopic button
        self.add_button = tk.Button(header_frame, text='+', font=('bold'), width=8, height=3, bg=self.settings.button_color, highlightthickness=0, bd=0, fg=self.settings.fg_color, command=self.add)
        self.add_button.pack(side="right", padx=15, pady=10)

        ################################

        # Create a canvas and scrollbar
        self.scrollbar = tk.Scrollbar(self.master)  # self.scrollbar
        self.scrollbar.pack(side='right', fill='y')

        self.canvas = tk.Canvas(self.master, bg=self.settings.bg_color, yscrollcommand=self.scrollbar.set, highlightbackground='black')
        self.canvas.pack(fill='x', expand=True, anchor='nw', padx=10)

        # Binding with the canvas with mousewheel
        # self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        self.scrollbar.config(command=self.canvas.yview)

        # Just a Label
        existed = tk.Label(self.canvas, text="Sites to be blocked", font=self.settings.font, bg=self.settings.button_color, fg=self.settings.fg_color)
        existed.pack(padx=10, pady=5, side='top', anchor='w')

        self.update_list()

    def is_valid_url(self, url):
        regex = re.compile(
            r"^(?:http|ftp)s?://"  # http:// or https://
            # domain...
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
            r"localhost|"
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$", re.IGNORECASE)

        return re.match(regex, url) is not None or re.match(regex, "http://" + url) is not None

    def add(self):
        # Get user typed web address from text box
        web_add = self.web_address_box.get()
        web_add = web_add.replace("\n", "")

        # Validate the input as a URL
        if not self.is_valid_url(web_add):
            messagebox.showerror("Error", "Invalid URL provided.")
            return

        # Prepend "http://" if the scheme is missing
        if not web_add.startswith(("http://", "https://")):
            web_add = "http://" + web_add

        parsed_url = urlparse(web_add)

        domain = parsed_url.netloc

        # Load the existing data from the file
        with open("data/sites.json", "r") as file:
            data = json.load(file)

        # Modify the data as needed
        data.append(domain)  # Add a new website to the list

        # Save the modified data back to the file
        with open("data/sites.json", "w") as file:
            json.dump(data, file)

        self.update_list()

    def update_list(self):

        # Remove the existing frames
        frame_to_remove = []
        for key, widget in self.canvas.children.items():
            if isinstance(widget, tk.Frame):
                frame_to_remove.append(widget)

        for frame in frame_to_remove:
            frame.destroy()

        # Read the contents of the file
        with open("data/sites.json", "r") as file:
            data = json.load(file)

        # Create and pack new button widgets for each web address in the list
        for site in data:
            button_frame = tk.Frame(self.canvas, bg=self.settings.frame_bg_color)
            button_frame.pack(side="top", anchor='w', padx=10, pady=5)

            # Displaying web address
            web_address = tk.Label(button_frame, text=site, font=self.settings.font, bg=self.settings.button_color, fg=self.settings.fg_color, height=1, width=30)
            web_address.pack(padx=10, pady=5, side="left", anchor="w")

            # Delete buttons to delete an address
            delete = tk.Button(button_frame, text="delete", font=self.settings.font, bg=self.settings.button_color, fg=self.settings.fg_color, command=lambda site=site: self.delete_list(site))
            delete.pack(padx=10, pady=5, side="left")

    def delete_list(self, site):
        # Remove the newline character from the site address
        site = site.strip()

        # Ask the user to confirm the deletion
        confirm = messagebox.askokcancel(
            "Confirm Deletion", f"Are you sure you want to delete {site}?")

        # Delete the site address if the user confirmed the deletion
        if confirm:

            # Read the JSON data from the file
            with open("data/sites.json", "r") as file:
                json_data = json.load(file)

            # Remove the desired element from the list
            json_data.remove(site)

            # Save the updated JSON data back to the file
            with open("data/sites.json", "w") as file:
                json.dump(json_data, file)

        # Refresh
        self.update_list()

    def pressed_enter(self, event):
        self.add()


