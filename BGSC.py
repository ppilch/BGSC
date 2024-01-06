from kivy.lang import Builder
from kivy.core.window import Window

from kivymd.app import MDApp

from players import PlayersManagement
from games import GamesManagement
from options import OptionsManagement
from editgame import EditGameManagement
from db import DBOperations

# This moves MDTextField up, above opened keyboard
Window.keyboard_anim_args = {'d':.2, 't': 'in_out_expo'}
Window.softinput_mode = 'below_target'

dbo = DBOperations()

class BoardGamesScoreCounter(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    p = PlayersManagement()
    g = GamesManagement()
    o = OptionsManagement()
    eg = EditGameManagement()

    def build(self):
        #self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = dbo.get_setting("darkmode")[0][0]
        Builder.load_file('./kv/players.kv')
        Builder.load_file('./kv/messages.kv')
        Builder.load_file('./kv/category_edit.kv')
        return Builder.load_file('./kv/bgsc.kv')
        
    def open_player_screen(self):
        self.p.players_load_screen()
        
    def open_games_screen(self):
        self.g.games_load_screen()
   
    def open_options_screen(self):
        self.o.options_load_screen()    
        
    def open_editgame_screen(self):
        self.eg.editgame_load_screen()
        
if __name__ == '__main__':
    BoardGamesScoreCounter().run()
