from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.image import Image
 
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.icon_definitions import md_icons
from players import *
from options import *
from db import *
 
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
 