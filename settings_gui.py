import tkinter as tk 
from tkinter import filedialog
from settings import Settings
from easy_json import get_value, edit_value
import os

class Settings_GUI():
	def __init__(self, master, restart):

		self.restart = restart

		master.title('Settings')
		self.settings = Settings()
		master.config(bg=self.settings.root_color)

		self.settings_json = "data/settings.json"
		self.restart_json = "data/restart.json"

		### Profile picture
		# Frame for profile picture
		profile_frame = tk.Frame(master, bg=self.settings.bg_color)
		profile_frame.pack(padx=10, pady=(10,0), fill='x')

		# the profile picture label
		pp_text = get_value('pp_location', self.settings_json) # get picture location
		if pp_text == 'images/newuser.png': # the default newuser picture
			pp_text = "Select an image for profile picture>>"

		else:
			pp_text = os.path.basename(pp_text) # show only the basename

		# PROFILE
		profile_title = tk.Label(profile_frame, text="Profile Picture", font=self.settings.font, bg=self.settings.button_color, fg=self.settings.fg_color)
		profile_title.grid(row=0, column=0, sticky='w', padx=5, pady=5)

		# the profile picture label
		self.pp_label = tk.Label(profile_frame, text=pp_text, font=self.settings.font, bg=self.settings.button_color, fg=self.settings.fg_color)
		self.pp_label.grid(row=1, column=0, sticky='ew', padx=5, pady=5)

		# the profile picture button
		pp_dir_button = tk.Button(profile_frame, text="Select profile picture", font=self.settings.font, command=self.ask_profile_picture, bg=self.settings.button_color, fg=self.settings.fg_color)
		pp_dir_button.grid(row=1, column=1, sticky='ew', padx=(66,5), pady=5)

		### username
		# Frame for username
		username_frame = tk.Frame(master, bg=self.settings.bg_color)
		username_frame.pack(padx=10, pady=(10,0), fill='x')

		# the username previously stored
		self.username = self.settings.username

		# NAME
		name_title = tk.Label(username_frame, text='Username', font=self.settings.font, bg=self.settings.button_color, fg=self.settings.fg_color)
		name_title.grid(row=0, column=0, sticky='w', padx=5, pady=5)

		# username textbox
		self.username_box = tk.Entry(username_frame, width=30, font=self.settings.font, bg=self.settings.root_color, fg=self.settings.fg_color, highlightthickness=0, bd=0)
		self.username_box.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
		self.username_box.bind("<Return>", self.pressed_enter)

		# username changing button
		username_changing_button = tk.Button(username_frame, text='Change', font=self.settings.font, command=self.ask_new_username, bg=self.settings.button_color, fg=self.settings.fg_color)
		username_changing_button.grid(row=1, column=1, sticky='ew', padx=5, pady=5)

		# reminder label
		reminder1 = tk.Label(username_frame, text='(You can change your name by over-writting the existing name and click "change")\n', bg=self.settings.bg_color, fg=self.settings.special_text_color)
		reminder1.grid(row=2, column=0, sticky='w', columnspan=2, padx=5, pady=5)

		# inserting the name in the text box
		self.username_box.insert(tk.END, self.username)


		### Themes
		# Frame for theme
		theme_frame = tk.Frame(master,bg=self.settings.bg_color)
		theme_frame.pack(padx=10, pady=(10,0), fill='x')

		theme_title = tk.Label(theme_frame, text='Available Themes', font=self.settings.font, bg=self.settings.button_color, fg=self.settings.fg_color)
		theme_title.grid(row=0, column=0, sticky='w', padx=10, pady=10)

		#themes = tk.Label(theme_frame, text='Themes', font=self.settings.font, fg=self.settings.fg_color, bg=self.settings.button_color)
		#themes.grid(row=1, column=0, sticky='w', padx=10, pady=10)

 		# assign selected theme with tkinter's stringvar
		self.selected_theme = tk.StringVar(value=get_value('theme', self.settings_json)) 

		## List of available themes
		theme_row_number = 2
		theme_column_number = 0
		for theme in self.settings.available_themes:
			tk.Radiobutton(theme_frame, selectcolor=self.settings.bg_color, command=self.select_theme, variable=self.selected_theme, value=theme, text=theme, font=self.settings.font,  fg=self.settings.special_text_color, bg=self.settings.input_color, highlightthickness=0, bd=0).grid(row=theme_row_number, column=theme_column_number, sticky='w', padx=10, pady=5)	
			
			if(theme_row_number==4):
				theme_row_number = 2
				theme_column_number+=1
			else:
				theme_row_number += 1

		### TIMER
		# Frame for timer
		timer_frame = tk.Frame(master, bg=self.settings.bg_color)
		timer_frame.pack(padx=10, pady=10, fill='x')

		timer_title = tk.Label(timer_frame, text='Timer', font=self.settings.font, bg=self.settings.button_color, fg=self.settings.fg_color)
		timer_title.grid(row=0, column=0, sticky='w', padx=10, pady=10)

 		# assign selected timer with tkinter's stringvar
		self.selected_timer = tk.IntVar(value=get_value('timer', self.settings_json)) 

		## LIST OF AVAILABLE TIMER FOR STUDY INTERVAL AND BREAK TIME
		timer_row_number = 1
		for timer in self.settings.available_timers:
			tk.Radiobutton(timer_frame, selectcolor=self.settings.bg_color, command=self.select_timer, variable=self.selected_timer, value=timer, text=f"Study for {timer} minutes straight and take a break for " + str(self.settings.available_timers[timer]) + " minutes", font=self.settings.font, fg=self.settings.special_text_color, bg=self.settings.input_color, highlightthickness=0, bd=0).grid(row=timer_row_number, column=0, sticky='w', padx=10, pady=5)
			timer_row_number += 1


		# reminder label
		apply_changes_button = tk.Button(master, text='Apply Changes', font=self.settings.font, bg=self.settings.button_color, fg=self.settings.fg_color, command=self.restart)
		apply_changes_button.pack(fill='x')

	def ask_profile_picture(self):
		# get dir using filedialog from tkinter
		pp_dir = filedialog.askopenfilename(title="Select a picture", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
		# if the user successfully chose a location, the label will change to its location.
		if pp_dir:
			filename = os.path.basename(pp_dir)
			self.pp_label.config(text=filename)
			edit_value('pp_location', pp_dir, self.settings_json)
			self.restart()
		else:
			pass
		
	def ask_new_username(self):
		### GET USER TYPED VALUE FROM TEXT BOX
		self.username = self.username_box.get()
		self.username = self.username.replace("\n", "") # I don't know why but, it comes with new line characters sometimes. So I replaced it with empty string.
		edit_value('name', self.username, self.settings_json)
		self.restart()


	### THESE FUNCTIONS TRIGGERED ON RADIO BUTTON SWITCHING
	def select_theme(self):
		edit_value('theme', self.selected_theme.get(), self.settings_json)
		  
	def select_timer(self):
		edit_value('timer', self.selected_timer.get(), self.settings_json)

	def pressed_enter(self, event):
		self.ask_new_username()

