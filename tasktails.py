import tkinter as tk
from second_frame import SecondFrame
from first_frame import FirstFrame
from settings import Settings
import atexit
from block import WebsiteBlocker


class TaskTails():
    def __init__(self):
        self.settings = Settings()

        # Create the main window
        self.root = tk.Tk()
        # self.root.state("zoomed")
        self.root.configure(bg=self.settings.root_color)

        # Declaring databases
        # db_names = ['data.db','data2.db']

        # Set the task-tails logo
        self.root.iconphoto(True, tk.PhotoImage(file='images/logo.png'))
        self.root.title('TaskTails - Your Smart Strict Tool For Your Effective Study')

        # There is no button after this full screen mode
        # self.root.attributes("-fullscreen", True)

        # Create the frames
        # First frame
        frame1 = tk.LabelFrame(self.root, text='Profile', width=self.settings.w1, height=self.settings.h, fg=self.settings.fg_color, bg=self.settings.frame_bg_color)
        frame1.pack(side='left', padx=10, pady=10)
        frame1.pack_propagate(0)
        # tk.Label(frame1, text='This is inside the first frame').pack()

        # Second frame
        frame2 = tk.LabelFrame(self.root, text='You goals and tasks', width=self.settings.w2, height=self.settings.h, fg=self.settings.fg_color, bg=self.settings.frame_bg_color)
        frame2.pack(side='left', padx=10, pady=10)
        frame2.pack_propagate(0)
        # tk.Label(frame2, text='This is inside the second frame').pack()

        # Create first frame object
        FirstFrame(frame1, self.restart)

        # Create second frame object
        SecondFrame(frame2, self.restart)

        # Start the main loop
        self.root.mainloop()

    def restart(self):
        WebsiteBlocker().unblock_websites()
        self.root.destroy()
        TaskTails()

    def cleanup(self):
        WebsiteBlocker().unblock_websites()
        
if __name__ == "__main__":
    tasktails = TaskTails()
    atexit.register(tasktails.cleanup)



