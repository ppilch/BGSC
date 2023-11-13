from kivymd.app import MDApp

import inspect
from db import *

dbo = DBOperations()

class OptionsManagement():
    
    running_app = None
    
    def options_load_screen(self):
        print(inspect.currentframe().f_code.co_name)
        self.running_app = MDApp.get_running_app()

    def change_darkmode(self, switch):
        print(inspect.currentframe().f_code.co_name)
        if switch.active == True:
            self.running_app.theme_cls.theme_style = "Dark"
            dbo.update_setting("darkmode", "Dark")
        else:
            self.running_app.theme_cls.theme_style = "Light"
            dbo.update_setting("darkmode", "Light")
        
