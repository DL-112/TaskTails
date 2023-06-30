import tkinter as tk 
from settings import Settings
import tkinter.messagebox as mbox
from block import WebsiteBlocker
from easy_json import get_value

class Timer:
	def __init__(self, master):
		self.settings = Settings()
		self.master = master
		self.running = False
		self.pause = False
		self.break_interval = False
		self.study_interval = True

		# study timer
		self.study_timer_string = '0:0:0 |'
		self.study_seconds = 0
		self.study_minutes = 0
		self.study_hours = 0
		self.total_s_time = 0

		# break timer
		self.break_timer_string = '0:0'
		self.break_seconds = 0
		self.break_minutes = 0
		self.total_b_time = 0

		self.timer_string = self.study_timer_string + " | " + self.break_timer_string

		self.study_label = tk.Label(self.master, text='Study', fg=self.settings.fg_color, bg=self.settings.button_color)
		self.study_label.grid(row=0, column=0, sticky='ew')

		self.break_label = tk.Label(self.master, text='Break', fg=self.settings.fg_color, bg=self.settings.button_color)
		self.break_label.grid(row=0, column=1, sticky='ew')

		self.study_timer_label = tk.Label(self.master, text=self.study_timer_string, fg=self.settings.fg_color, bg=self.settings.button_color, font=("Helvetica", 24))
		self.study_timer_label.grid(row=1, column=0)

		self.break_timer_label = tk.Label(self.master, text=self.break_timer_string, fg=self.settings.fg_color, bg=self.settings.button_color, font=("Helvetica", 24))
		self.break_timer_label.grid(row=1, column=1)

		self.start_button = tk.Button(self.master,text='Start', command=self.clicked_start, fg=self.settings.fg_color, bg=self.settings.button_color, highlightthickness=0, bd=0)
		self.start_button.grid(row=2, column=0, sticky='ew')

		self.pause_button = tk.Button(self.master, text='Pause', command=self.clicked_pause, fg=self.settings.fg_color, bg=self.settings.button_color, highlightthickness=0, bd=0)
		self.pause_button.grid(row=2, column=1, sticky='ew')
		self.pause_button.config(state='disable')

		# Object to block
		self.web_blocker = WebsiteBlocker()

	def update_timer(self):
		if self.study_interval:
			if not self.pause:

				self.study_seconds += 1
				self.total_s_time += 1
				if self.study_seconds >= 60:
					self.study_seconds = 0
					self.study_minutes += 1
				if self.study_minutes >= 60:
					self.study_minutes = 0
					self.study_hours += 1

				self.study_timer_string = f"{self.study_hours}:{self.study_minutes}:{self.study_seconds} |"
				self.study_timer_label.config(text=self.study_timer_string)

				if self.running and self.total_s_time != self.settings.study_time: # check for time's up
					self.master.after(1000, self.update_timer)

				elif self.running and self.total_s_time == self.settings.study_time:
					self.total_s_time = 0
					mbox.showinfo("Time's up!", "Now, take a break!")
					if get_value('website_blocking', 'data/settings.json') == True:
						self.web_blocker.unblock_websites()
					self.study_timer_label.config(text='0:0:0 |')
					self.break_interval = True
					self.study_interval = False
					self.cancel()
					self.running = True
					self.update_timer()

			else:
				self.pause = False
				print('paused')

		elif self.break_interval:
			if not self.pause:
				self.break_seconds += 1
				self.total_b_time += 1
				if self.break_seconds >= 60:
					self.break_seconds = 0
					self.break_minutes += 1

				self.break_timer_string = f"{self.break_minutes}:{self.break_seconds}"
				self.break_timer_label.config(text=self.break_timer_string)

				if self.running and self.total_b_time != self.settings.break_time: # check for time's up
					self.master.after(1000, self.update_timer)

				if self.running and self.total_b_time == self.settings.break_time:
					self.total_b_time = 0
					mbox.showinfo("Time's up", "Now, get back to study!")
					if get_value('website_blocking', 'data/settings.json') == True:
						self.web_blocker.block_websites()
					self.break_timer_label.config(text='0:0')
					self.break_interval = False
					self.study_interval = True
					self.cancel()
					self.running = True
					self.update_timer()

			else:
				self.pause = False
				print('paused')

	def clicked_start(self):
		websites = self.web_blocker.load_websites_from_json()
		if websites and get_value('website_blocking', 'data/settings.json'):
			self.web_blocker.block_websites()
			self.running = True
			self.start_button.config(state='disable')
			self.pause_button.config(state='active')
			self.update_timer()

		elif get_value('website_blocking', 'data/settings.json') == False:
			self.running = True
			self.start_button.config(state='disable')
			self.pause_button.config(state='active')
			self.update_timer()

		else:
			mbox.showinfo("No Websites Found", "Please choose which websites to block first.")

	def clicked_pause(self):
		self.running = False
		self.pause = True
		self.start_button.config(state='active')
		self.pause_button.config(state='disable')

	def cancel(self):
		self.running = False
		self.pause = False
		self.study_seconds = 0
		self.study_minutes = 0
		self.study_hours = 0
		self.break_seconds = 0
		self.break_minutes = 0
