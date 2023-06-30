from PIL import ImageGrab
from easy_json import get_value, edit_value

class Settings():
    def __init__(self):
        # GET THE DIMENSIONS OF THE SCREEN
        self.screen_width, self.screen_height = ImageGrab.grab().size
        self.w1, self.w2, self.h, self.h1, self.h2 = self.get_dimensions()

        self.settings_json = "data/settings.json"

        ### AVAILABLE_THEMEES
        self.available_themes = {'blue': ['#1B4965', '#FDF0D5', '#0C0A3E', '#003049', '#1C4966', '#fffb00', '#303841'], 
                                'light blue': ['#4598ca', '#ffffff', '#0a4c76', '#10659a', '#1C4966', 'yellow', '#303841'],
                                'red': ['#710627', '#ffffff', '#780000','#9E1946', '#1C4966', '#FFA500', '#303841'],
                                'black': ['#303841', '#ffffff', '#1e1f29', '#6e6e6e', '#1e1f29', '#FFA500', '#303841'],
                                'white': ['#FDFDFD','#474747','#CBBBEB','#A1EAFB','#ACE5F6','#A7226E','#FECFF3']}

        self.theme = self.available_themes[get_value('theme', self.settings_json)]

        ### RELATED ATTRIBUTES FROM THEMES
        self.bg_color = self.theme[0]
        self.fg_color = self.theme[1]
        self.root_color = self.theme[2]
        self.button_color = self.theme[3]
        self.input_color = self.theme[4]
        self.special_text_color = self.theme[5]
        self.frame_bg_color = self.theme[6]
        self.font = 'arial, 12'

        ### FOR FIRST FRAME
        
        # username
        self.username = get_value('name', self.settings_json)
        # profile image path
        self.image_path = get_value('pp_location', self.settings_json)
        # button height
        self.button_height = 3


        ### FOR SECOND FRAME
        self.maintopic = "Main Topic"


        ### AVAILABLE_TIMERS
        # ALL INTEGERS ARE IN MINUTES
        self.available_timers = {30: 5, 60: 10, 90: 15, 120: 20}
        self.study_interval = get_value('timer', self.settings_json)
        self.break_interval = self.available_timers[self.study_interval]

        self.study_time = self.study_interval * 60
        self.break_time = self.break_interval * 60


    def get_dimensions(self):
        w1, w2 = int((self.screen_width - 50) * 1/5), int((self.screen_width - 50) * 4/5)
        h = self.screen_height - 50
        h1 = 150
        h2 = h - h1
        return w1, w2, h, h1, h2
