from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.metrics import dp
import inspect

from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.app import App, MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.icon_definitions import md_icons
from kivymd.uix.snackbar import Snackbar

from db import *

dbo = DBOperations()

class GamesManagement(MDScreen):

    running_app = None

    def games_load_screen(self):
        print(inspect.currentframe().f_code.co_name)
        self.running_app = MDApp.get_running_app()
        #Workaround from stackoverflow (size not working in .kv)
        self.running_app.root.ids.mdsc_game_order_column.ids.segment_panel.width = (Window.width - dp(60))/2
        self.running_app.root.ids.mdsc_game_order_direction.ids.segment_panel.width = (Window.width - dp(60))/2
                
    def open_games_backdrop(self, the_backdrop):
        print(inspect.currentframe().f_code.co_name)
        the_backdrop.open(-Window.height / 4)
        the_backdrop.left_action_items = [["menu",lambda x: self.running_app.root.ids.nav_drawer.set_state("toggle")]]
        
        