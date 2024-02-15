#Kivy modules
from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.widget import Widget
from kivy.input.providers.mouse import MouseMotionEvent
from kivy.clock import Clock
from functools import partial
import inspect
from time import sleep

#KivyMD modules
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, OneLineListItem, IconLeftWidget, IconRightWidget, OneLineIconListItem
from kivymd.app import App, MDApp
from kivymd.uix.button import MDFlatButton, MDIconButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.icon_definitions import md_icons
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.tooltip.tooltip import MDTooltip
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.segmentedcontrol import MDSegmentedControlItem, MDSegmentedControl
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton

#My modules
from db import *
from messages import Messages
from datatable_operations import DataTableOperations
from games import GamesManagement, Game#, CountingMethod#, Round, Category
from mdcolors import MDColors
from helpers import Helpers as h

dbo = DBOperations()
msg = Messages()

class MyToggleButton(MDFlatButton, MDToggleButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background_down = self.theme_cls.primary_color
       
class TooltipMDIconButton(MDIconButton, MDTooltip):
    pass
    
class ListDialog(MDBoxLayout):
    pass

class ItemConfirm(OneLineListItem):
    divider = None

class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''

class CategoryEdit(MDBoxLayout):
    pass

class IconListItem(OneLineIconListItem):
    icon = StringProperty()
 

class EditGameManagement:
        
    #def __init__(self):
#        self.running_app = MDApp.get_running_app()

    dto = DataTableOperations()

    running_app = None
    menu = None
    dialog = None
    drp_menu_categories = None
    category_edit_dialog = None
    category_edit_content_cls = None
    game = None
    counting_method = None
    category = None
    categories_temp = None
    changed = 0
    
    def editgame_load_screen(self):
        print(inspect.currentframe().f_code.co_name)
        self.running_app = MDApp.get_running_app()
        self.fill_editgame_widgets(-1,-1, Game.global_game_id, 1, 'name', 'ASC')

    def go_back_to_games(self):
        print(inspect.currentframe().f_code.co_name)
        if self.changed == 0:
            self.running_app.root.ids.scr_mngr.transition.direction = "right"
            self.running_app.root.ids.scr_mngr.current = 'games'
        else:
            self.show_dialog_confirm_changes("go_back_to_games")

    #def 

    def show_dialog_confirm_changes(self, caller, selected_counting_method = None):
        print(inspect.currentframe().f_code.co_name)
        changes_dialog = MDDialog(
            title = "Save changes?",
            buttons = [
                MDFlatButton(text="CANCEL", on_release = lambda x: self.confirm_changes_decision(changes_dialog, caller, "CANCEL")),
                MDFlatButton(text="DISCARD", on_release = lambda x: self.confirm_changes_decision(changes_dialog, caller, "DISCARD", selected_counting_method)),
                MDFlatButton(text="SAVE", on_release = lambda x: self.confirm_changes_decision(changes_dialog, caller, "SAVE", selected_counting_method))
            ]
        )
        changes_dialog.open()
    
    def change_counting_method_decide_if_show_dialog(self, caller, selected_counting_method):
        print(inspect.currentframe().f_code.co_name)
        print(f"self.changed = {self.changed}")
        if self.changed == 1:
            self.show_dialog_confirm_changes(caller, selected_counting_method)
        else:
            self.select_counting_method(selected_counting_method)
    
    def confirm_changes_decision(self, dialog, caller, decision, selected_counting_method = None):
        print(inspect.currentframe().f_code.co_name)
        if decision == "SAVE":
            self.save_counting_method()
        if decision == "SAVE" or decision == "DISCARD":
            if caller == "go_back_to_games":
                self.running_app.root.ids.scr_mngr.transition.direction = "right"
                self.running_app.root.ids.scr_mngr.current = 'games'
            if caller == "change_counting_method":
                self.select_counting_method(selected_counting_method)
            self.counting_method_changed(0)
        if decision == "SAVE" or decision == "DISCARD" or decision == "CANCEL":
            dialog.dismiss()

    def fill_editgame_widgets(self, counting_method_id, counting_method_name, game_id, default_only, order_col, order_dir):
        print(inspect.currentframe().f_code.co_name)
        ###game
        if game_id == -1:
            game = Game(
                game_id = -1,
                name = "",
                favorite_icon = "star-outline"
                )
        else:
            game_db = dbo.get_game(game_id, '-1', '-1', 'name', 'ASC')
            game = Game(
                game_id = game_db[0][0],
                name = game_db[0][1],
                favorite_icon = game_db[0][2]
                )
        #fields of game
        self.running_app.root.ids.txt_game_name.text = game.name
        self.running_app.root.ids.ico_favorite_game.icon = game.favorite_icon
        self.running_app.root.ids.ico_favorite_game.tooltip_text = self.set_favorite_icon_tooltip(game.favorite_icon)
        
        ###counting_method
        if game_id == -1:
            self.counting_method = CountingMethod(
                counting_method_id = -1,
                name = "",
                game_id = -1,
                default_icon = "checkbox-marked-circle-outline",
                scoring_type_rivcoop = "rivalisation",
                scoring_type_highlow = "highest",
                scoring_type_updown = "up",
                scoring_type_endround = "end",
                scoring_type_defrounds = "defined",
                game_end_condition = "Manual",
                points_on_start = "0",
                score_ending_the_game = "",
                number_of_rounds = "1",
                round_name = "Game end",
                notes = ""
            )
        else:
            counting_method_db = dbo.get_counting_method(counting_method_id, counting_method_name, game_id, default_only, order_col, order_dir)
            self.counting_method = CountingMethod(
                counting_method_id = counting_method_db[0][0],
                name = counting_method_db[0][1],
                game_id = counting_method_db[0][2],
                default_icon = counting_method_db[0][3],
                scoring_type_rivcoop = counting_method_db[0][4],
                scoring_type_highlow = counting_method_db[0][5],
                scoring_type_updown = counting_method_db[0][6],
                scoring_type_endround = counting_method_db[0][7],
                scoring_type_defrounds = counting_method_db[0][8],
                game_end_condition = counting_method_db[0][9],
                points_on_start = counting_method_db[0][10],
                score_ending_the_game = counting_method_db[0][11],
                number_of_rounds = counting_method_db[0][12],
                round_name = counting_method_db[0][13],
                notes = counting_method_db[0][14]
            )
       
        #fields of counting_method
        self.running_app.root.ids.txt_counting_method.text = self.counting_method.name
        self.running_app.root.ids.ico_counting_method_default.icon = self.counting_method.default_icon
        
        self.set_active_togglebutton(self.counting_method.scoring_type_rivcoop)
        self.set_active_togglebutton(self.counting_method.scoring_type_highlow)
        self.set_active_togglebutton(self.counting_method.scoring_type_updown)
        self.set_active_togglebutton(self.counting_method.scoring_type_endround)
        self.set_active_togglebutton(self.counting_method.scoring_type_defrounds)

        self.running_app.root.ids.drp_game_end_condition.text = self.counting_method.game_end_condition
        self.running_app.root.ids.txt_points_on_start.text = str(self.counting_method.points_on_start)
        self.running_app.root.ids.txt_score_ending_the_game.text = str(self.counting_method.score_ending_the_game)
        self.running_app.root.ids.txt_number_of_rounds.text = str(self.counting_method.number_of_rounds)
        self.running_app.root.ids.txt_round_name.text = self.counting_method.round_name
        self.running_app.root.ids.txt_counting_method_notes.text = str(self.counting_method.notes)

        ###game_color
        self.running_app.root.ids.box_counting_method_colors.clear_widgets()
        game_color_db = dbo.get_game_color(-1,self.counting_method.counting_method_id,"id","ASC")
        selected_colors = []
        for game_color in game_color_db:
            selected_colors.append(game_color[1])
        self.save_colors_on_screen(selected_colors)
        ###category
        self.counting_method.categories = []
        if game_id == -1:
            category = Category(
                category_id = -1,
                name = "Points",
                order_no = 1,
                counting_method_id = -1
            )
            self.counting_method.categories.append(category) 
        else:
            category_db = dbo.get_category(-1, self.counting_method.counting_method_id, 0, "order_no", "ASC")
            for cat in category_db:
                category = Category(
                    category_id = cat[0],
                    name = cat[1],
                    order_no = cat[2],
                    counting_method_id = cat[3]
                )
                self.counting_method.categories.append(category) 
        #field of category
        category_names = ""
        category_names = ', '.join(str(x.text) for x in self.counting_method.categories)
        self.running_app.root.ids.txt_categories.text = category_names

        # reset change indicator
        self.counting_method_changed(0)

    def get_active_togglebutton(self, button1, button2):
        print(inspect.currentframe().f_code.co_name)
        if self.running_app.root.ids[f"btn_{button1}"].state == "down":
            return button1
        elif self.running_app.root.ids[f"btn_{button2}"].state == "down":
            return button2
    
    def set_active_togglebutton(self, db_value):
        print(inspect.currentframe().f_code.co_name)
        self.running_app.root.ids[f"btn_{db_value}"].state = "down"
        self.running_app.root.ids[f"btn_{db_value}"].md_bg_color = self.running_app.theme_cls.bg_dark
    
    def set_favorite_icon_tooltip(self, icon_name):
        print(inspect.currentframe().f_code.co_name)
        if icon_name == "star":
            return "Remove game from favorites"
        else:
            return "Add game to favorites"
    
    def delete_counting_method(self, counting_method_id, game_id, dialog):
        print(inspect.currentframe().f_code.co_name)
        dbo.delete_counting_method_soft(counting_method_id)
        self.counting_method_changed(0)
        dialog.dismiss()
        counting_method_number = dbo.get_counting_method_number(game_id)
        if counting_method_number > 0:
            self.fill_editgame_widgets(counting_method_id, "", game_id, 1, "id", "ASC")
            msg.show_snackbar_OK("Counting method deleted")
        else:
            dbo.delete_game_soft(game_id)
            self.running_app.root.ids.scr_mngr.transition.direction = "right"
            self.running_app.root.ids.scr_mngr.current = 'games'
            
    def change_favorites(self):
        print(inspect.currentframe().f_code.co_name)
        current_icon = self.running_app.root.ids.ico_favorite_game.icon
        if current_icon == "star":
            self.running_app.root.ids.ico_favorite_game.icon = "star-outline"
            self.running_app.root.ids.ico_favorite_game.tooltip_text = "Add game to favorites"
        else:
            self.running_app.root.ids.ico_favorite_game.icon = "star"
            self.running_app.root.ids.ico_favorite_game.tooltip_text = "Remove game from favorites"
        self.counting_method_changed(1)
    
    def change_default_counting_method(self):
        print(inspect.currentframe().f_code.co_name)
        self.running_app.root.ids.ico_counting_method_default.icon = "checkbox-marked-circle-outline"
        self.counting_method_changed(1)
    
    def validate_number_of_rounds(self):
        print(inspect.currentframe().f_code.co_name)
        return
        if self.running_app.root.ids.txt_number_of_rounds.text in {"None","","-"}:
            self.running_app.root.ids.txt_number_of_rounds.error = True
        elif int(self.running_app.root.ids.txt_number_of_rounds.text) < 1:
            self.running_app.root.ids.txt_number_of_rounds.error = True
        
    def validate_all_fields(self, validation_bitmask):
        print(inspect.currentframe().f_code.co_name)
        '''
        pow(2, 0) -   1 - Game name
        pow(2, 1) -   2 - Counting method name
        pow(2, 2) -   4 - Points on start
        pow(2, 3) -   8 - Score ending the game
        pow(2, 4) - 16 - Number of rounds
        pow(2, 5) - 32 - Round Name
        pow(2, 6) - 64 - Categories
        '''
        dialog_title = ""
        dialog_message = ""
        if (1 & validation_bitmask == 1) and self.running_app.root.ids.txt_game_name.text == "":
            dialog_title = "Invalid value in field 'Game name'"
            dialog_message = "Please provide a text for field 'Game name'."
            self.running_app.root.ids.txt_game_name.error = True
        elif (2 & validation_bitmask == 2) and self.running_app.root.ids.txt_counting_method.text == "":
            dialog_title = "Invalid value in field 'Counting method name'"
            dialog_message = "Please provide a text for field Counting method name'."
            self.running_app.root.ids.txt_counting_method.error = True
        elif (4 & validation_bitmask == 4) and self.running_app.root.ids.txt_points_on_start.text in {"","-"}:
            dialog_title = "Invalid value in field 'Points on start'."
            dialog_message = "Please provide integer value for field 'Points on start'."
            self.running_app.root.ids.txt_points_on_start.error = True
        elif (8 & validation_bitmask == 8) and self.running_app.root.ids.txt_score_ending_the_game.text in {"-"}:
            dialog_title = "Invalid value in field 'Score ending the game'."
            dialog_message = "Please provide integer value for field 'Score ending the game' or leave this field empty."
            self.running_app.root.ids.txt_score_ending_the_game.error = True
        elif (8 & validation_bitmask == 8) and self.running_app.root.ids.txt_score_ending_the_game.text in {""} and self.running_app.root.ids.drp_game_end_condition.text == "Points":
            dialog_title = "Invalid value in field 'Score ending the game'."
            dialog_message = "When end game condition is set to 'Points' then value for field 'Score ending the game' can't be empty empty."
            self.running_app.root.ids.txt_score_ending_the_game.error = True
        elif (16 & validation_bitmask == 16) and self.running_app.root.ids.txt_number_of_rounds.text in {"","-"}:
            dialog_title = "Invalid value in field 'Number of rounds'"
            dialog_message = "Please provide integer value (minimum 1) for field 'Number of rounds'."
            self.running_app.root.ids.txt_number_of_rounds.error = True
        elif (16 & validation_bitmask == 16) and int(self.running_app.root.ids.txt_number_of_rounds.text) < 1:
            dialog_title = "Invalid value in field 'Number of rounds'"
            dialog_message = "Please provide integer value (minimum 1) for field 'Number of rounds'."
            self.running_app.root.ids.txt_number_of_rounds.error = True
        elif (32 & validation_bitmask == 32) and self.running_app.root.ids.txt_round_name.text == "":
            dialog_title = "Invalid value in field 'Round name'"
            dialog_message = "Please provide a text for field 'Round name'."
            self.running_app.root.ids.txt_round_name.error = True
        elif (64 & validation_bitmask == 64) and self.running_app.root.ids.txt_categories.text == "":
            dialog_title = "Invalid value in field 'Categories'"
            dialog_message = "Please provide at least one item in field 'Categories'."
            self.running_app.root.ids.txt_categories.error = True
        if dialog_message != "":
            msg.show_simple_information(dialog_title, dialog_message)
            return "failure"
        else:
            return "success"
        
    def open_drp_game_end_conditions(self):
        print(inspect.currentframe().f_code.co_name)
        menu_list = [
            {
                "viewclass":"OneLineListItem",
                "text": "Manual",
                "on_release" : lambda x = "Manual" : self.drp_item_selected_game_end_condition(x)
            },
            {
                "viewclass":"OneLineListItem",
                "text":"Rounds",
                "on_release" : lambda x = "Rounds" : self.drp_item_selected_game_end_condition(x)
            },
            {
                "viewclass":"OneLineListItem",
                "text":"Points",
                "on_release" : lambda x = "Points" : self.drp_item_selected_game_end_condition(x)
            },
            {
                "viewclass":"OneLineListItem",
                "text":"Rounds or Points",
                "on_release" : lambda x = "Rounds or Points" : self.drp_item_selected_game_end_condition(x)
            },
            {
                "viewclass":"OneLineListItem",
                "text":"Time",
                "on_release" : lambda x = "Time" : self.drp_item_selected_game_end_condition(x)
            }
            ]
        self.menu = MDDropdownMenu(
            caller = self.running_app.root.ids.drp_game_end_condition,
            items = menu_list,
            width_mult = 4
        )
        self.menu.open()
        
    def drp_item_selected_game_end_condition(self, item_text):
        print(inspect.currentframe().f_code.co_name)
        self.running_app.root.ids.drp_game_end_condition.text = item_text
        self.menu.dismiss()
    
    def show_confirm_delete_dialog(self):
        print(inspect.currentframe().f_code.co_name)
        confirm_delete_dialog = MDDialog(
            title = "Confirm delete",
            text = "Do you want to delete this counting method? Whole game will be deleted if this is the last counting method.",
            buttons=[
                MDFlatButton(text='CANCEL', on_release = lambda x: confirm_delete_dialog.dismiss()),
                MDFlatButton(text='DELETE', on_release = lambda x: self.delete_counting_method(self.counting_method.counting_method_id, self.counting_method.game_id, confirm_delete_dialog)),
                ]
            )
        confirm_delete_dialog.open()
      
    def show_counting_method_dialog(self):
        print(inspect.currentframe().f_code.co_name)
        dialog_list = ListDialog()
        #new blank
        list_item = \
            counting_method_new = CountingMethod(
                counting_method_id = -10,
                name = "New (blank)",
                #game_id is mandatory and doesn't natter here so passing global so that it is not changed when CountingMethod is instatiated.
                game_id = CountingMethod.global_game_id,
                default_icon = "checkbox-blank-circle-outline",
                on_release = lambda counting_method_new: self.change_counting_method_decide_if_show_dialog("change_counting_method", counting_method_new)
            )
        left_icon = IconLeftWidget(
            icon = "plus-box-outline"
            )
        counting_method_new.font_style = "Caption"
        counting_method_new.tooltip = counting_method_new.name
        counting_method_new.add_widget(left_icon)
        dialog_list.ids.md_list.add_widget(counting_method_new)
        #new copy
        list_item = \
            counting_method_new = CountingMethod(
                counting_method_id = -11,
                name = "New (copy)",
                #game_if is mandatory and doesn't natter here so passing global so that it is not changed when CountingMethod is instatiated.
                game_id = CountingMethod.global_game_id,
                default_icon = "",
                on_release = lambda counting_method_new: self.change_counting_method_decide_if_show_dialog("change_counting_method", counting_method_new)
            )
        left_icon = IconLeftWidget(
            icon = "plus-box-multiple-outline"
            )
        counting_method_new.font_style = "Caption"
        counting_method_new.tooltip = counting_method_new.name
        counting_method_new.add_widget(left_icon)
        dialog_list.ids.md_list.add_widget(counting_method_new)
        
        counting_method_db = dbo.get_counting_method('-1', '-1', CountingMethod.global_game_id, 0, 'id', 'ASC')
        for i in range(len(counting_method_db)):
            counting_method_list_item = CountingMethod(
                counting_method_id = counting_method_db[i][0],
                name = counting_method_db[i][1],
                game_id = counting_method_db[i][2],
                default_icon = counting_method_db[i][3],
                on_release = lambda counting_method_list_item: self.change_counting_method_decide_if_show_dialog("change_counting_method", counting_method_list_item)
            )
            left_icon = IconLeftWidget(
            icon = counting_method_list_item.default_icon
            )
            counting_method_list_item.font_style = "Caption"
            counting_method_list_item.tooltip = counting_method_list_item.name
            counting_method_list_item.add_widget(left_icon)
            dialog_list.ids.md_list.add_widget(counting_method_list_item)
        
        self.dialog = MDDialog(
            title = "Select counting method",
            type = "custom",
            content_cls = dialog_list,
            size_hint_x = None,
            size_hint_y = None,
            width = Window.width - dp(24),
            buttons=[
                MDFlatButton(text='CANCEL', on_release = lambda x: self.dialog.dismiss()),
                ]
            )
        self.dialog.open()

    def select_counting_method(self, counting_method):
        print(inspect.currentframe().f_code.co_name)
        ### if new (blank)
        if counting_method.counting_method_id == -10:
            print(">new (blank)")
            self.counting_method.counting_method_id = -1
            #fields of counting_method
            self.running_app.root.ids.txt_counting_method.text = ""
            self.running_app.root.ids.ico_counting_method_default.icon = "checkbox-blank-circle-outline"
            self.set_active_togglebutton("rivalisation")
            self.set_active_togglebutton("highest")
            self.set_active_togglebutton("up")
            self.set_active_togglebutton("end")
            self.set_active_togglebutton("defined")
            self.running_app.root.ids.drp_game_end_condition.text = "Manual"
            self.running_app.root.ids.txt_points_on_start.text = "0"
            self.running_app.root.ids.txt_score_ending_the_game.text = ""
            self.running_app.root.ids.txt_number_of_rounds.text = "1"
            self.running_app.root.ids.txt_round_name.text = "Game end"
            self.running_app.root.ids.txt_counting_method_notes.text = ""
            #game_color
            self.save_colors_on_screen([])
            #category class
            category = Category(
                category_id = -1,
                name = "Points",
                order_no = 1,
                counting_method_id = -1
            )
            self.counting_method.categories = []
            self.counting_method.categories.append(category) 
            #category field
            category_names = ""
            category_names = ', '.join(str(x.text) for x in self.counting_method.categories)
            self.running_app.root.ids.txt_categories.text = category_names
            self.counting_method_changed(0)
        ### if new (copy)
        elif counting_method.counting_method_id == -11:
            print(">new (copy)")
            self.counting_method.counting_method_id = -1
            self.running_app.root.ids.txt_counting_method.text = "Copy of " + self.running_app.root.ids.txt_counting_method.text
            for cat in self.counting_method.categories:
                cat.category_id = -1
            self.counting_method_changed(1)
        ### else (selected counting method)
        else:
            print(">else")
            self.fill_editgame_widgets(
                counting_method_id = counting_method.counting_method_id,
                counting_method_name = '-1',
                game_id = counting_method.game_id,
                default_only = 0,
                order_col = 'name',
                order_dir = 'ASC')
            self.counting_method_changed(0)
        self.dialog.dismiss()
        
    def counting_method_changed(self, changed):
        print(inspect.currentframe().f_code.co_name)
        self.changed = changed

    def save_counting_method(self):
        print(inspect.currentframe().f_code.co_name)
        validation_result = self.validate_all_fields(pow(2, 0)+pow(2, 1)+pow(2, 2)+pow(2, 3)+pow(2, 4)+pow(2, 5)+pow(2, 6))
        if validation_result == "failure":
            return
        else:
            self.counting_method.game_id = dbo.upsert_game(
                Game.global_game_id
            ,   self.running_app.root.ids.txt_game_name.text
            ,   self.running_app.root.ids.ico_favorite_game.icon
            )
            self.counting_method.counting_method_id = dbo.upsert_counting_method(
                self.counting_method.counting_method_id
            ,   self.running_app.root.ids.txt_counting_method.text
            ,   self.counting_method.game_id
            ,   self.running_app.root.ids.ico_counting_method_default.icon
            ,   self.get_active_togglebutton("rivalisation","cooperation")
            ,   self.get_active_togglebutton("lowest","highest")
            ,   self.get_active_togglebutton("up","down")
            ,   self.get_active_togglebutton("rounds","end")
            ,   self.get_active_togglebutton("undefined","defined")
            ,   self.running_app.root.ids.drp_game_end_condition.text
            ,   self.running_app.root.ids.txt_points_on_start.text
            ,   self.running_app.root.ids.txt_score_ending_the_game.text
            ,   self.running_app.root.ids.txt_number_of_rounds.text
            ,   self.running_app.root.ids.txt_round_name.text
            ,   h.replace_quotes(None, self.running_app.root.ids.txt_counting_method_notes.text)
            )
            dbo.merge_category_list(self.counting_method.counting_method_id, self.counting_method.categories)
            dbo.merge_game_colors(self.counting_method.counting_method_id, self.counting_method.colors)
            msg.show_snackbar_OK("Counting method saved")
            # reset change indicator
            self.counting_method_changed(0)


    ##############################
    ########## Edit category ##########
    def open_dialog_category(self):
        print(inspect.currentframe().f_code.co_name)
        self.categories_temp = self.counting_method.categories
        self.category_edit_content_cls = CategoryEdit()
        self.category_edit_dialog = MDDialog(
            title = "Edit categories",
            type = "custom",
            content_cls = self.category_edit_content_cls,
            buttons=[
                MDFlatButton(text='CANCEL', on_release = lambda x: self.category_edit_dialog.dismiss()),
                MDFlatButton(text='OK', on_release=lambda x:self.save_categories())
                ]
            )
        self.category_edit_content_cls.ids.txt_category_order.text = self.get_next_category_order_no()
        self.category_edit_dialog.open()
        
    def open_drp_category(self):
        print(inspect.currentframe().f_code.co_name)
        self.drp_menu_categories = None
        menu_list=[]
        new_category = Category(-1, "", 0, -1)
        list_item = \
            {
                "viewclass":"IconListItem",
                "text": "Add new",
                "icon": "plus",
                "on_release" : lambda x = new_category : self.drp_item_selected_category(self.drp_menu_categories, x)
            }
        menu_list.append(list_item)
        for category in self.categories_temp:
            list_item = \
                {
                    "viewclass":"Category",
                    "text": category.name,
                    "on_release" : lambda x = category : self.drp_item_selected_category(self.drp_menu_categories, x)
                }
            menu_list.append(list_item)
        self.drp_menu_categories = MDDropdownMenu(
            caller = self.category_edit_content_cls.ids.drp_category_edit,
            items = menu_list,
            width_mult = 4
        )
        self.drp_menu_categories.open()
       
    def drp_item_selected_category(self, drp_menu, item):
        print(inspect.currentframe().f_code.co_name)
        if str(item.text) == "":    #[+ Add New] is clicked
            self.category = None
            self.category_edit_content_cls.ids.txt_category_name.text = ""
            self.category_edit_content_cls.ids.txt_category_order.text = self.get_next_category_order_no()
        else:
            self.category = item
            self.category_edit_content_cls.ids.txt_category_name.text = str(item.name)
            self.category_edit_content_cls.ids.txt_category_order.text = str(item.order_no)
        drp_menu.dismiss()
    
    def save_category(self):
        print(inspect.currentframe().f_code.co_name)
        
        if self.category_edit_content_cls.ids.txt_category_name.text == "":
            self.set_validation_category_name()
            self.category_edit_content_cls.ids.txt_category_name.error = True
            return
        
        if self.category == None:
            saving_type = "new"
        else:
            saving_type = "existing"
        ### common actions before ###
        # convert entered order_no into insertable
        order_no_entered = self.category_edit_content_cls.ids.txt_category_order.text
        if order_no_entered == "":
            order_no_new = self.get_next_category_order_no()
        elif int(order_no_entered) < 1:
            order_no_new = 1
        elif int(order_no_entered) > int(self.get_next_category_order_no()):
            if saving_type == "new":
                order_no_new = int(self.get_next_category_order_no())
            else:
                order_no_new = int(self.get_next_category_order_no()) - 1
        else:
            order_no_new = order_no_entered
            
        ### new category logic ###
        if saving_type == "new":
            print(">new category logic")
            order_no_prev = 1000
            #min_category_id = min(self.counting_method.categories, key=lambda x: int(x.category_id))
            new_cat = Category(
                category_id = int(self.get_next_category_id()),
                name=self.category_edit_content_cls.ids.txt_category_name.text,
                order_no=int(order_no_new),
                counting_method_id=self.counting_method.counting_method_id
            )
            self.category = new_cat
            
        ### existing category logic ###
        else:
            # catch previous order_no if there was one
            print(">existing category logic")
            #for cat in self.counting_method.categories:
            order_no_prev = self.category.order_no
            self.category.name = self.category_edit_content_cls.ids.txt_category_name.text
            self.category.order_no = int(order_no_new)
        
        ### common actions after ###
        # renumerate categories with higher order_no
        if int(order_no_new) > int(order_no_prev):
            for cat in self.counting_method.categories:
                if int(cat.order_no) > int(order_no_prev) and int(cat.order_no) <= int(order_no_new):
                    if cat.category_id != self.category.category_id:
                        cat.order_no = int(cat.order_no) - 1
        if int(order_no_new) <= int(order_no_prev):
            for cat in self.counting_method.categories:
                if int(cat.order_no) <= int(order_no_prev) and int(cat.order_no) >= int(order_no_new):
                    if cat.category_id != self.category.category_id:
                        cat.order_no = int(cat.order_no) + 1
        
        # add to the temp list finally
        if saving_type == "new":
            self.categories_temp.append(new_cat)
        # sort, clear gui
        self.categories_temp = sorted(self.categories_temp, key=lambda x: int(x.order_no))
        self.category_edit_content_cls.ids.txt_category_name.text = ""
        self.category_edit_content_cls.ids.txt_category_order.text = self.get_next_category_order_no()
        self.category = None
        self.counting_method_changed(1)
        msg.show_snackbar_OK("Category added to list")
    
    def delete_category(self):
        print(inspect.currentframe().f_code.co_name)
        #self.category is set to None after opening dialog and after saving a category in dialog
        if self.category == None:
            self.category_edit_content_cls.ids.txt_category_name.text = ""
            self.category_edit_content_cls.ids.txt_category_order.text = self.get_next_category_order_no()
            return
        #self.category is set when a category is selected in drop down
        order_no_deleted = self.category.order_no
        cat_to_delete = None
        for cat in self.categories_temp:
            cat_index = self.categories_temp.index(cat)
            # get category to delete it later - to avoid impact on the loop
            if cat.category_id == self.category.category_id:
                cat_to_delete = cat
            # reiterate higher order_no's
            elif int(cat.order_no) > int(order_no_deleted):
                cat.order_no = int(cat.order_no) - 1
                self.categories_temp[cat_index] = cat
        # delete the category and reset fields
        if cat_to_delete != None:
            self.categories_temp.remove(cat_to_delete)
            self.category_edit_content_cls.ids.txt_category_name.text = ""
            self.category_edit_content_cls.ids.txt_category_order.text = self.get_next_category_order_no()
            self.category = None
        self.counting_method_changed(1)
        msg.show_snackbar_OK("Category removed from list")
    
    #save categories from popup to the editgame screen
    def save_categories(self):
        print(inspect.currentframe().f_code.co_name)
        category_names = ""
        category_names = ', '.join(str(x.text) for x in self.categories_temp)
        self.running_app.root.ids.txt_categories.text = category_names
        self.counting_method.categories = self.categories_temp
        self.categories_temp = None
        self.category_edit_dialog.dismiss()
        
    def set_validation_category_name(self):
        print(inspect.currentframe().f_code.co_name)
        self.category_edit_content_cls.ids.txt_category_name.required = True
        
    def get_next_category_id(self):
        print(inspect.currentframe().f_code.co_name)
        max_n = 0
        # check class
        for cat in self.counting_method.categories:
            n = int(cat.category_id)
            if n > max_n:
                max_n = n
        # check temp variable
        for cat in self.categories_temp:
            n = int(cat.category_id)
            if n > max_n:
                max_n = n
        #check db
        n = int(dbo.get_category(-1, -1, -1, "id", "DESC")[0][0])
        if n > max_n:
            max_n = n
        #return max of all above
        return str(max_n + 1)
    
    def get_next_category_order_no(self):
        print(inspect.currentframe().f_code.co_name)
        max_n = 0
        for cat in self.categories_temp:
            n = int(cat.order_no)
            if n > max_n:
                max_n = n
        return str(max_n + 1)
    
    ########## Edit category ##########
    ##############################
    
    ##############################
    ##########   Edit colors   ##########
    def open_dialog_mdcolors(self):
        print(inspect.currentframe().f_code.co_name)
        current_colors_list = []
        for color_item in self.running_app.root.ids.box_counting_method_colors.children:
            current_colors_list.append(color_item.text_color)
            
        colors_cls = MDColors()
        color_dialog = MDDialog(
            title = "Available player colors",
            type = "custom",
            content_cls = colors_cls,
            buttons=[
                MDFlatButton(text='CANCEL', on_release = lambda x: color_dialog.dismiss()),
                MDFlatButton(text='OK', on_release=lambda x:self.save_selected_colors(color_dialog, colors_cls))
                ]
            )
        for color in colors_cls.colors_dict.items():
            color_button = MDIconButton(
                id = "ico_dialog_" + color[0],
                icon = "checkbox-marked-circle" if color[1] in current_colors_list else "checkbox-blank-circle",
                theme_icon_color = "Custom",
                icon_color = color[1],
                on_release = lambda x: self.pres_color(x)
            )
            #colors_cls.ids.lay_mdcolors_edit.add_widget(color_button)
            colors_cls.ids.lay_mdcolors_edit.add_widget(color_button)
        color_dialog.open()
        
    def pres_color(self, pressed_icon):
        print(inspect.currentframe().f_code.co_name)
        pressed_icon.icon = "checkbox-marked-circle" if pressed_icon.icon == "checkbox-blank-circle" else "checkbox-blank-circle"
    
    #pass colors from db/dialog and save them on screen (keeping the dictionary order)
    def save_colors_on_screen(self, selected_colors_names):
        print(inspect.currentframe().f_code.co_name)
        mdcolors = MDColors()
        self.counting_method.colors = []
        self.running_app.root.ids.box_counting_method_colors.clear_widgets()
        if selected_colors_names == []:
            selected_color = MDIcon(
                icon = "circle-off-outline",
                theme_text_color = "Secondary",
            )
            self.running_app.root.ids.box_counting_method_colors.add_widget(selected_color)
        else:
            for game_color in mdcolors.colors_dict.keys():
                if game_color in selected_colors_names:
                    selected_color = MDIcon(
                        icon = "checkbox-blank-circle",
                        theme_text_color = "Custom",
                        text_color = mdcolors.colors_dict.get(game_color)
                    )
                    self.running_app.root.ids.box_counting_method_colors.add_widget(selected_color)
        self.counting_method.colors = selected_colors_names
        
    def save_selected_colors(self, color_dialog, colors_cls):
        selected_colors = []
        for color in list(reversed(colors_cls.ids["lay_mdcolors_edit"].children)):
            if color.icon == "checkbox-marked-circle":
                selected_colors.append(str(color.id).replace("ico_dialog_",""))
        self.save_colors_on_screen(selected_colors)
        self.counting_method_changed(1)
        color_dialog.dismiss()
        
    ##########   Edit colors   ##########
    ##############################
    
class CountingMethod(OneLineIconListItem):
    
    global_counting_method_id = -1
    global_game_id = -1
    
    def __init__(
            self,
            counting_method_id,
            name,
            game_id,
            default_icon,
            scoring_type_rivcoop = None,
            scoring_type_highlow = None,
            scoring_type_updown = None,
            scoring_type_endround = None,
            scoring_type_defrounds = None,
            game_end_condition = None,
            points_on_start = None,
            score_ending_the_game = None,
            number_of_rounds = None,
            round_name = None,
            notes = None,
            colors = {},    #dictionary
            categories = [],    #list
            **kwargs
        ):
        super().__init__(**kwargs)
        self.counting_method_id = counting_method_id
        self.name = name
        self.game_id = game_id
        self.default_icon = default_icon
        self.scoring_type_rivcoop = scoring_type_rivcoop
        self.scoring_type_highlow = scoring_type_highlow
        self.scoring_type_updown = scoring_type_updown
        self.scoring_type_endround = scoring_type_endround
        self.scoring_type_defrounds = scoring_type_defrounds
        self.game_end_condition = game_end_condition
        self.points_on_start = points_on_start
        self.score_ending_the_game = score_ending_the_game
        self.number_of_rounds = number_of_rounds
        self.round_name = round_name
        self.notes = notes
        self.colors = colors
        self.categories = categories
        self.text = name
        CountingMethod.global_counting_method_id = self.counting_method_id
        CountingMethod.global_game_id = game_id

class Category(OneLineListItem):
    def __init__(
            self,
            category_id = None,
            name = "",
            order_no = None,
            counting_method_id = None,
            **kwargs
            ):
        OneLineListItem.__init__(self,**kwargs)
        self.category_id = category_id
        self.name = name
        self.order_no = order_no
        self.counting_method_id = counting_method_id
        self.text = name