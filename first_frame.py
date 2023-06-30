import tkinter as tk 
from settings import Settings
from settings_gui import Settings_GUI
from PIL import Image, ImageTk, ImageDraw
from easy_json import edit_value, get_value
from new_schedule import New
from sites import Web
from aboutus import Aboutus
from howtouse import Howtouse

class FirstFrame():
    def __init__(self, frame, restart):
        self.restart = restart
        
        self.frame = frame
        self.settings = Settings()

        # set the frame's color
        self.frame.config(bg=self.settings.bg_color)

        self.image_path = self.settings.image_path
        self.image_size = 100
        self.username = self.settings.username

        self.profile_frame = tk.Frame(frame, bg=self.settings.bg_color, width=self.settings.w1, height=self.settings.h1)
        self.profile_frame.pack(pady=20)
        self.profile_frame.pack_propagate(0)

        # Making profile button
        self.profile_image = self.create_profile_image() # I tried to directly pass it. It didn't work
        self.profile_button = tk.Button(self.profile_frame, image=self.profile_image, text="", compound=tk.LEFT, bg=self.settings.bg_color, highlightthickness=0, bd=0, padx=5)
        self.profile_name = tk.Label(self.profile_frame, text=self.username, fg=self.settings.fg_color, bg=self.settings.bg_color, padx=5, font='unicode')

        # Grid in place
        self.profile_button.grid(row=0, column=0)
        self.profile_name.grid(row=0, column=1)


        # Create a frame for navigation
        self.nav_frame = tk.Frame(frame, bg=self.settings.bg_color, width=self.settings.w1, height=self.settings.h2)
        self.nav_frame.pack()
        self.nav_frame.pack_propagate(0)        


        # 4 buttons and 1 label in the nav frame
        self.settings_bt = tk.Button(self.nav_frame, text='Settings', width=self.settings.w1, fg=self.settings.fg_color, bg=self.settings.button_color, highlightthickness=0, bd=0, height=2, command=self.create_settings_window).pack(pady=(0,2.5), padx=10)
        self.howtouse = tk.Button(self.nav_frame, text='How to use?', width=self.settings.w1, fg=self.settings.fg_color, bg=self.settings.button_color, highlightthickness=0, bd=0, height=2, command=self.howtouse).pack(pady=2.5, padx=10)
        self.create_new_schedule = tk.Button(self.nav_frame,text='My Schedules', width=self.settings.w1, bg=self.settings.button_color, highlightthickness=0, bd=0, fg=self.settings.fg_color, height=2, command=self.new_schedule).pack(pady=2.5, padx=10)
        self.block_sites = tk.Button(self.nav_frame, text='Block websites', width=self.settings.w1, fg=self.settings.fg_color, bg=self.settings.button_color, highlightthickness=0, bd=0, height=2, command=self.site_window).pack(pady=2.5, padx=10)
        self.aboutus = tk.Button(self.nav_frame, text='About us', width=self.settings.w1, fg=self.settings.fg_color, bg=self.settings.button_color, highlightthickness=0, bd=0, height=2, command=self.aboutus).pack(pady=2.5, padx=10)

        self.copy_right = tk.Label(self.nav_frame, text="Copyright © WYH, AMM", width=self.settings.w1, fg="#fd971f", bg=self.settings.button_color).pack(side='bottom', padx=10)


        # Initialize false to settings window
        self.settings_window = None
        self.schedule = None
        self.site = None
        self.aboutus_window = None 
        self.htu_window = None

    def create_profile_image(self):

        try:
            if(get_value('pp_location', 'data/settings.json') == 'images/white/newuser.png' and get_value('theme', 'data/settings.json') != 'white'):
                edit_value('pp_location', 'images/newuser.png', 'data/settings.json')
            if(get_value('pp_location', 'data/settings.json') == 'images/newuser.png' and get_value('theme', 'data/settings.json') == 'white'):
                edit_value('pp_location', 'images/white/newuser.png', 'data/settings.json')
            # Open the image
            img = Image.open(get_value('pp_location', 'data/settings.json'))

        except FileNotFoundError: # if file not found, automatically set to new user image
            if get_value('theme', 'data/settings.json') == 'white':
                edit_value('pp_location', 'images/white/newuser.png', 'data/settings.json')
                img = Image.open('images/white/newuser.png')

            else:
                edit_value('pp_location', 'images/newuser.png', 'data/settings.json')
                img = Image.open('images/newuser.png')

        if self.image_path == 'images/newuser.png' or self.image_path == 'images/white/newuser.png':
            # Resize the image
            img = img.resize((self.image_size, self.image_size), Image.LANCZOS)

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

        else:
            # Resize the image 
            img = img.resize((self.image_size, self.image_size), Image.LANCZOS)

            # Create a Tkinter image object
            tkimg = ImageTk.PhotoImage(img)

            # now just return the image and create button inside the constructor method
            return tkimg

    def create_settings_window(self):
        # check if there is existing settings window
        # only false value will create a window
        if self.settings_window is None or not self.settings_window.winfo_exists():
            # create a toplevel window under the first frame
            self.settings_window = tk.Toplevel(self.frame)
            Settings_GUI(self.settings_window, self.restart)
        else:
            self.settings_window.lift()

    def new_schedule(self):
        # check if there is existing schedule window
        # only false value will create a window
        if self.schedule is None or not self.schedule.winfo_exists():
            # create a toplevel window under the first frame
            self.schedule = tk.Toplevel(self.frame)
            Schedule = New(self.schedule, self.restart)
        else:
            self.schedule.lift()

    def site_window(self):
        # check if there is existing schedule window
        # only false value will create a window
        if self.site is None or not self.site.winfo_exists():
            # create a toplevel window under the first frame
            self.site = tk.Toplevel(self.frame)
            Site = Web(self.site)
        else:
            self.site.lift()

    def aboutus(self):
        if self.aboutus_window is None or not self.aboutus_window.winfo_exists():
            # create a toplevel window under the first frame
            self.aboutus_window = tk.Toplevel(self.frame)
            Aboutus(self.aboutus_window)
        else:
            self.aboutus_window.lift()

    def howtouse(self):
        if self.htu_window is None or not self.htu_window.winfo_exists():
            # create a toplevel window under the first frame
            self.htu_window = tk.Toplevel(self.frame)
            Howtouse(self.htu_window)
        else:
            self.htu_window.lift()