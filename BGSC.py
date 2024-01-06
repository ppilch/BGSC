from kivy.lang import Builder

from kivymd.app import MDApp
from players import PlayersManagement
from options import OptionsManagement
from db import DBOperations
dbo = DBOperations()

class BoardGamesScoreCounter(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    p = PlayersManagement()
    o = OptionsManagement()

    def build(self):
        #self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = dbo.get_setting("darkmode")[0][0]
        Builder.load_file('./kv/players.kv')
        return Builder.load_file('./kv/bgsc.kv')
        
    def open_player_screen(self):
        self.p.players_load_screen()
      
    def open_options_screen(self):
        self.o.options_load_screen()    
   
   
if __name__ == '__main__':
    BoardGamesScoreCounter().run()
