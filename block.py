import json
from tkinter import messagebox
import platform

class WebsiteBlocker:
    def __init__(self):
        self.hosts_path = self.get_hosts_path()
        self.ip_address = "127.0.0.1"
        self.file_path = "data/sites.json"

    def block_websites(self):
        websites = self.load_websites_from_json()
        for website in websites:
            self.block(website)

    def unblock_websites(self):
        websites = self.load_websites_from_json()
        for website in websites:
            self.unblock(website)

    def block(self, website):
        # Open the hosts file in append mode
        with open(self.hosts_path, "a") as file:
            file.write(f"{self.ip_address} {website}\n")

        print(f"{website} blocked!")

    def unblock(self, website):      
        # Read the hosts file into memory
        with open(self.hosts_path, "r") as file:
            lines = file.readlines()

        # Remove the blocked website entry
        with open(self.hosts_path, "w") as file:
            for line in lines:
                if not line.startswith(f"{self.ip_address} {website}"):
                    file.write(line)

        print(f"{website} unblocked!")

    def get_hosts_path(self):
        system_name = platform.system()
        if system_name == "Linux" or system_name == "Darwin":
            return "/etc/hosts"
        elif system_name == "Windows":
            return r"C:\Windows\System32\drivers\etc\hosts"
        else:
            raise OSError("Unsupported operating system")

    def load_websites_from_json(self):
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            raise Exception("JSON file not found.")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error decoding JSON file.")

        return None
