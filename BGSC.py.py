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

class BoardGamesScoreCounter(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    p = PlayersManagement()
    
    def build(self):
        self.theme_cls.theme_style = "Light"
        #self.theme_cls.theme_style = "Dark"
        Builder.load_file('./kv/players.kv')
        return Builder.load_file('./kv/bgsc.kv')
        
if __name__ == '__main__':
    BoardGamesScoreCounter().run()
