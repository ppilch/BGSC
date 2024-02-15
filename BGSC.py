from kivy.lang import Builder
from kivy.core.window import Window
import inspect

from kivymd.app import MDApp

from players import PlayersManagement
from games import GamesManagement
from options import OptionsManagement
from editgame import EditGameManagement
from db import DBOperations
from initial_load import InitialLoad

# This moves MDTextField up, above opened keyboard
Window.keyboard_anim_args = {'d':.2, 't': 'in_out_expo'}
Window.softinput_mode = 'below_target'

class BoardGamesScoreCounter(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    p = PlayersManagement()
    g = GamesManagement()
    o = OptionsManagement()
    eg = EditGameManagement()
    dbo = DBOperations()
    il = InitialLoad()

    def on_start(self):
        print(inspect.currentframe().f_code.co_name)
        self.open_games_screen()

    def build(self):
        print(inspect.currentframe().f_code.co_name)
        #self.theme_cls.material_style = "M3"
        self.dbo.create_all_objects()
        self.il.initial_load()
        self.theme_cls.theme_style = self.dbo.get_setting("darkmode")
        Builder.load_file('./kv/players.kv')
        Builder.load_file('./kv/games.kv')
        Builder.load_file('./kv/messages.kv')
        Builder.load_file('./kv/category_edit.kv')
        return Builder.load_file('./kv/bgsc.kv')
        
    def open_player_screen(self):
        print(inspect.currentframe().f_code.co_name)
        self.p.players_load_screen()
        
    def open_games_screen(self):
        print(inspect.currentframe().f_code.co_name)
        self.g.games_load_screen()
   
    def open_options_screen(self):
        print(inspect.currentframe().f_code.co_name)
        self.o.options_load_screen()    
        
    def open_editgame_screen(self):
        print(inspect.currentframe().f_code.co_name)
        self.eg.editgame_load_screen()
        
if __name__ == '__main__':
    BoardGamesScoreCounter().run()
