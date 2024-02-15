from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.metrics import dp
import inspect

from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, IconLeftWidget, IconRightWidget, OneLineIconListItem, ImageLeftWidget
from kivymd.app import App, MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.icon_definitions import md_icons
from kivymd.uix.snackbar import Snackbar

from db import *
from datatable_operations import DataTableOperations

dbo = DBOperations()

class IconListItem(OneLineIconListItem):
    icon = StringProperty()

#class GamesManagement(MDScreen):
class GamesManagement:

    def __init__(self):
        self.running_app = MDApp.get_running_app()
        self.name_filter = "-1"
        self.favorite_icon_filter = "-1"
        self.order_direction = "ASC"

    def games_load_screen(self):
        print(inspect.currentframe().f_code.co_name)
        self.running_app = MDApp.get_running_app()
        #Workaround from stackoverflow (size not working in .kv)
        self.reload_games()
                
    def open_games_backdrop(self, the_backdrop):
        print(inspect.currentframe().f_code.co_name)
        the_backdrop.open(-2 * self.running_app.root.ids.txt_game_search.height)
        the_backdrop.left_action_items = [["menu",lambda x: self.running_app.root.ids.nav_drawer.set_state("toggle")]]
    
    def clear_games_list(self):
        print(inspect.currentframe().f_code.co_name)
        self.running_app.root.ids.list_games.clear_widgets()
        
    def reload_games(self):
        print(inspect.currentframe().f_code.co_name)
        self.clear_games_list()
        #set default values for parameters
        #get games from db
        games = dbo.get_game('-1', self.name_filter, self.favorite_icon_filter, 'name', self.order_direction)
        for game in games:
            item_game_id = game[0]
            item_game_name = game[1]
            item_favorite_icon = game[2]
            item_game_image = game[3]
            left_picture = ImageLeftWidget(
                source = f"images/{item_game_image}",
                width = dp(40)
            )
            game_list_item = Game(
                game_id = item_game_id,
                name = item_game_name,
                favorite_icon = item_favorite_icon,
                text = item_game_name,
                on_release = lambda game_list_item: self.open_screen_edit_game(game_list_item)
            )
            right_icon = IconRightWidget(
                icon = item_favorite_icon,
                width = dp(40),
                on_release = lambda right_icon: self.add_game_to_favorites(right_icon, right_icon.parent.parent)
            )
            game_list_item.add_widget(left_picture)
            game_list_item.add_widget(right_icon)
            self.running_app.root.ids.list_games.add_widget(game_list_item)
        self.refresh_filter_text()
            
    def open_screen_edit_game(self, game):
        print(inspect.currentframe().f_code.co_name)
        Game.global_game_id = game.game_id
        self.running_app.root.ids.scr_mngr.current = 'editgame'
        self.running_app.root.ids.scr_mngr.transition.direction = "left"
    
    def create_new_game(self):
        print(inspect.currentframe().f_code.co_name)
        #this sets global_game_id to -1 which is then used in eg.editgame_load_screen
        game = Game(
            game_id = -1,
            name = "",
            favorite_icon = "star-outline"
        )
        self.running_app.root.ids.scr_mngr.current = 'editgame'
        self.running_app.root.ids.scr_mngr.transition.direction = "left"
    
    def add_game_to_favorites(self, right_icon, parent_game):
        print(inspect.currentframe().f_code.co_name)
        if right_icon.icon == "star-outline":
            right_icon.icon = "star"
        else:
            right_icon.icon = "star-outline"
        dbo.upsert_game(parent_game.game_id, parent_game.name, right_icon.icon)
    
    def filter_games_by_name(self, name_filter):
        print(inspect.currentframe().f_code.co_name)
        if name_filter == "":
            self.name_filter = "-1"
        else:
            self.name_filter = name_filter
        self.reload_games()
        
    def filter_games_by_favorite(self, favorite_icon):
        print(inspect.currentframe().f_code.co_name)
        if favorite_icon == "star-off-outline":
            self.running_app.root.ids.ico_favorite_filter.icon = "star"
            self.favorite_icon_filter = "star"
        if favorite_icon == "star":
            self.running_app.root.ids.ico_favorite_filter.icon = "star-outline"
            self.favorite_icon_filter = "star-outline"
        if favorite_icon == "star-outline":
            self.running_app.root.ids.ico_favorite_filter.icon = "star-off-outline"
            self.favorite_icon_filter = "-1"
        self.reload_games()
    
    def change_sorting_order(self, order_icon):
        print(inspect.currentframe().f_code.co_name)
        self.running_app.root.ids.ico_game_sorting_order.icon = "sort-alphabetical-ascending" if order_icon == "sort-alphabetical-descending" else "sort-alphabetical-descending"
        self.order_direction = "DESC" if order_icon == "sort-alphabetical-ascending" else "ASC"
        self.reload_games()
        
    def refresh_filter_text(self):
        print(inspect.currentframe().f_code.co_name)
        # name_filter
        if self.name_filter == "-1":
            name_filter = ""
        else:
            name_filter = "game name = *" + self.name_filter + "*"
        # favorite_icon_filter
        if self.favorite_icon_filter == "star":
            favorite_icon_filter = "favorites = yes"
        elif self.favorite_icon_filter == "star-outline":
            favorite_icon_filter = "favorites = no"
        else:
            favorite_icon_filter = ""
        # joining_comma
        if favorite_icon_filter != "" and name_filter != "":
            joining_comma = ", "
        else:
            joining_comma = ""
        # all_filters
        all_filters = name_filter + joining_comma + favorite_icon_filter
        if all_filters == "":
             all_filters = "none"
        self.running_app.root.ids.bkdp_games.header_text = "Filter: " + all_filters
        
class Game(OneLineAvatarIconListItem):
    
    def __init__(
            self,
            game_id = None,
            name = None,
            favorite_icon = None,
            **kwargs
        ):
        super().__init__(**kwargs)
        self.game_id = game_id
        self.name = name
        self.favorite_icon = favorite_icon
        Game.global_game_id = game_id
        
    dto = DataTableOperations()
        