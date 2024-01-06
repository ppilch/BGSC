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

#KivyMD modules
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, OneLineListItem, IconLeftWidget, IconRightWidget, OneLineIconListItem
from kivymd.app import App, MDApp
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
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
from kivymd.uix.segmentedcontrol import MDSegmentedControlItem

#My modules
from db import *
from messages import Messages
from datatable_operations import DataTableOperations
from game import Game, CountingMethod, Round, Category

dbo = DBOperations()
msg = Messages()

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
 

class EditGameManagement(MDScreen):

    dto = DataTableOperations()

    running_app = None
    menu = None
    dialog = None
    tbl_rounds = None
    tbl_categories = None
    category_edit_dialog = None
    category_edit_content_cls = None
    game = None
    counting_method = None
    
    def editgame_load_screen(self):
        print(inspect.currentframe().f_code.co_name)
        self.running_app = MDApp.get_running_app()
        #Workaround from stackoverflow (size not working in .kv)
        self.running_app.root.ids.seg_scoring_type_rivcoop.ids.segment_panel.width = (Window.width - dp(24))
        self.running_app.root.ids.seg_scoring_type_highlow.ids.segment_panel.width = (Window.width - dp(24))
        self.running_app.root.ids.seg_scoring_type_updown.ids.segment_panel.width = (Window.width - dp(24))
        self.running_app.root.ids.seg_scoring_type_endround.ids.segment_panel.width = (Window.width - dp(24))
        self.running_app.root.ids.seg_scoring_type_defrounds.ids.segment_panel.width = (Window.width - dp(24))
        #self.running_app.root.ids.seg_scoring_type_highlow.current_active_segment = 
        self.fill_rounds_tab()
        self.fill_categories_tab()
        self.load_datafrom_db()
        self.generate_rounds()
        self.editgame_post_load_screen()
        
    def editgame_post_load_screen(self):
        print(inspect.currentframe().f_code.co_name)
        Clock.schedule_once(partial(self.set_segmented_control,"rivcoop","right"),0)
        Clock.schedule_once(partial(self.set_segmented_control,"highlow","right"),0)
        Clock.schedule_once(partial(self.set_segmented_control,"updown","right"),0)
        Clock.schedule_once(partial(self.set_segmented_control,"endround","right"),0)
        Clock.schedule_once(partial(self.set_segmented_control,"defrounds","right"),0)
        
    def load_datafrom_db(self):
        print(inspect.currentframe().f_code.co_name)
        self.game = Game(
            game_id = None,
            name = None,
            favorite = None,
        )
        
        self.counting_method = CountingMethod(
            counting_method_id = None,
            name = None,
            game_id = self.game.game_id,
            scoring_type_rivcoop = "Rivalisation",
            scoring_type_highlow = "Highest",
            scoring_type_updown = "Up",
            scoring_type_endround = "End",
            scoring_type_defrounds = "Defined",
            game_end_condition = None,
            points_on_start = "0",
            score_ending_the_game = None,
            number_of_rounds = "1",
            round_name = "Game end",
        )
        self.running_app.root.ids.txt_points_on_start.text = "0" #self.game.points_on_start
        self.running_app.root.ids.txt_number_of_rounds.text = "1" #self.game.number_of_rounds
        self.running_app.root.ids.txt_round_name.text = "Game end" #self.game.round_name
        self.running_app.root.ids.txt_counting_method.text = "At game end" #
    
    def fill_rounds_tab(self):
        print(inspect.currentframe().f_code.co_name)
        self.tbl_rounds = MDDataTable(
            #ids = "tbl_rounds",
            rows_num=1000,
            #check = True,
            sorted_on = "Number",
            sorted_order ="ASC",
            column_data = [
                ("Number", dp(25)),
                ("Round name", dp(40))
            ],
        )
        self.running_app.root.ids.tab_rounds.add_widget(self.tbl_rounds)
        
        btn_refresh_table = TooltipMDIconButton (
            #id: ico_table_rounds_refresh
            icon = "table-refresh",
            tooltip_text = "(Re-)Generate rounds in the table below",
            pos_hint = {"top": 1, "right":1},
            on_release = lambda x: self.generate_rounds()
        )
        self.running_app.root.ids.tab_rounds.add_widget(btn_refresh_table)
        
    def fill_categories_tab(self):
        self.tbl_categories = MDDataTable(
            rows_num=1000,
            check = True,
            sorted_on = "Number",
            sorted_order ="ASC",
            column_data = [
                ("Number", dp(25)),
                ("Category name", dp(40))
            ],
        )
        self.running_app.root.ids.tab_categories.add_widget(self.tbl_categories)
        
        btn_refresh_table = TooltipMDIconButton (
            #id: ico_table_rounds_refresh
            icon = "table-edit",
            tooltip_text = "Edit categories in the table below",
            pos_hint = {"top": 1, "right":1},
            on_release = lambda x: self.open_dialog_category_edit()
        )
        self.running_app.root.ids.tab_categories.add_widget(btn_refresh_table)
        
    def dont_save_game(self):
        print(inspect.currentframe().f_code.co_name)
        self.running_app.root.ids.scr_mngr.transition.direction = "right"
        self.running_app.root.ids.scr_mngr.current = 'games'
        
    def delete_game(self):
        print(inspect.currentframe().f_code.co_name)
        if self.running_app.root.ids.txt_counting_method.text == "At game end":
            msg.show_simple_information("Information", "Can't delete 'At game end' counting method because this is default one for each game.")
        else:
            #TextInput
            self.running_app.root.ids.txt_points_on_start.text = ""
            self.running_app.root.ids.txt_game_name.text = ""
            self.running_app.root.ids.txt_number_of_rounds.text = ""
            self.running_app.root.ids.txt_round_name.text = ""
            #Icon
            self.running_app.root.ids.ico_favorite_game.icon = "star-outline"
            self.running_app.root.ids.ico_counting_method.icon = "expand-all"
            #Tables
            self.dto.delete_rows(self.tbl_rounds)
            self.dto.delete_rows(self.tbl_categories)
                
    def change_favorites(self):
        print(inspect.currentframe().f_code.co_name)
        current_icon = self.running_app.root.ids.ico_favorite_game.icon
        if current_icon == "star":
            self.running_app.root.ids.ico_favorite_game.icon = "star-outline"
            self.running_app.root.ids.ico_favorite_game.tooltip_text = "Add to favorites"
        else:
            self.running_app.root.ids.ico_favorite_game.icon = "star"
            self.running_app.root.ids.ico_favorite_game.tooltip_text = "Remove from favorites"
        
    def validate_number_of_rounds(self):
        print(inspect.currentframe().f_code.co_name)
        if self.running_app.root.ids.txt_number_of_rounds.text in {"","-"}:
            self.running_app.root.ids.txt_number_of_rounds.error = True
        elif int(self.running_app.root.ids.txt_number_of_rounds.text) <1:
            self.running_app.root.ids.txt_number_of_rounds.error = True
        
    def validate_all_fields(self, validation_bitmask):
        print(inspect.currentframe().f_code.co_name)
        '''
        pow(2, 0) -   1 - Game name
        pow(2, 1) -   2 - Points on start
        pow(2, 2) -   4 - Number of rounds
        pow(2, 3) -   8 - Round Name
        pow(2, 4) - 16 - Counting method
        '''
        dialog_title = ""
        dialog_message = ""
        if (1 & validation_bitmask == 1) and self.running_app.root.ids.txt_game_name.text == "":
            dialog_title = "Invalid value in field 'Game name'"
            dialog_message = "Please provide a text for field 'Game name'."
        elif (2 & validation_bitmask == 2) and self.running_app.root.ids.txt_points_on_start.text in {"","-"}:
            dialog_title = "Invalid value in field 'Points on start'."
            dialog_message = "Please provide integer value for field 'Points on start'."
        elif (4 & validation_bitmask == 4) and self.running_app.root.ids.txt_number_of_rounds.text in {"","-"}:
            dialog_title = "Invalid value in field 'Number of rounds'"
            dialog_message = "Please provide integer value (minimum 1) for field 'Number of rounds'."
        elif (4 & validation_bitmask == 4) and int(self.running_app.root.ids.txt_number_of_rounds.text) < 1:
            dialog_title = "Invalid value in field 'Number of rounds'"
            dialog_message = "Please provide integer value (minimum 1) for field 'Number of rounds'."
        elif (8 & validation_bitmask == 8) and self.running_app.root.ids.txt_round_name.text == "":
            dialog_title = "Invalid value in field 'Round name'"
            dialog_message = "Please provide a text for field 'Round name'."
        elif (8 & validation_bitmask == 16) and self.running_app.root.ids.txt_counting_method.text == "":
            dialog_title = "Invalid value in field 'Counting method'"
            dialog_message = "Please provide a text for field 'Counting method'."
        if dialog_message != "":
            msg.show_simple_information(dialog_title, dialog_message)
            return "failure"
        else:
            return "success"
        
    def generate_rounds(self):
        print(inspect.currentframe().f_code.co_name)
        validation_bitmask = pow(2, 2) + pow(2, 3)
        validation_result = self.validate_all_fields(validation_bitmask)
        if validation_result == "failure":
            return
        self.dto.delete_rows(self.tbl_rounds)
        for round_number in range(int(self.running_app.root.ids.txt_number_of_rounds.text)):
            round_name = self.running_app.root.ids.txt_round_name.text
            if self.running_app.root.ids.txt_number_of_rounds.text != "1":
                round_name = round_name + " " + str(round_number + 1)
            self.dto.add_row_to_table(self.tbl_rounds, round_number + 1, round_name)
  
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
            }
            ]
        self.menu = MDDropdownMenu(
            caller = self.running_app.root.ids.drp_end_game_condition,
            items = menu_list,
            width_mult = 4
        )
        self.menu.open()
        
    def drp_item_selected_game_end_condition(self, item_text):
        print(inspect.currentframe().f_code.co_name)
        self.running_app.root.ids.drp_end_game_condition.text = item_text
        self.menu.dismiss()
      
    def show_counting_method_dialog(self):
        print(inspect.currentframe().f_code.co_name)
        if not self.dialog:
            counting_method_list = ["At game end", "Another method"]
            dialog_list = ListDialog()
            for item in counting_method_list:
                list_item = ItemConfirm(text=item)
                dialog_list.ids.md_list.add_widget(list_item)
            self.dialog = MDDialog(
                title = "Select counting method",
                type = "custom",
                content_cls = dialog_list,
                )
        self.dialog.open()

    def select_counting_method(self, item_control):
        print(inspect.currentframe().f_code.co_name)
        self.running_app.root.ids.txt_counting_method.text = item_control.text
        self.dialog.dismiss()
        
    ##############################
    ########## Edit category ##########
    def open_dialog_category_edit(self):
        print(inspect.currentframe().f_code.co_name)
        self.category_edit_content_cls = CategoryEdit()
        self.category_edit_dialog = MDDialog(
            title = "Edit categories:",
            type = "custom",
            content_cls = self.category_edit_content_cls,
            buttons=[
                MDFlatButton(text='CANCEL', on_release = lambda x: self.category_edit_dialog.dismiss()),
                #MDFlatButton(text='OK', on_release=lambda x:self.save_categories(self.player_edit_content_cls))
                ]
            )
        self.category_edit_dialog.open()

    def open_drp_category_edit(self):
        print(inspect.currentframe().f_code.co_name)
        drp_menu = None
        menu_list = [
            {
                "viewclass":"OneLineListItem",
                "text": "Points",
                "on_release" : lambda x = "Points" : self.drp_item_selected_category_edit(drp_menu, x)
            }
        ]
        drp_menu = MDDropdownMenu(
            caller = self.category_edit_content_cls.ids.drp_category_edit,
            items = menu_list,
            width_mult = 4
        )
        drp_menu.open()
       
    def open_drp_category_actions(self):
        print(inspect.currentframe().f_code.co_name)
        menu_list = [
            {
                "viewclass": "IconListItem",
                "icon":'plus',
                "text": "Add",
                #"on_release": lambda x=i: self.set_item(x)
            },
            {
                "viewclass": "IconListItem",
                "icon":'delete',
                #"on_release": lambda x=i: self.set_item(x)
            }
        ]
        drp_menu = MDDropdownMenu(
            caller = self.category_edit_content_cls.ids.ico_select_action,
            items = menu_list,
            width_mult = 2.5
        )
        drp_menu.open()
       
    def drp_item_selected_category_edit(self, drp_menu, item_text):
        print(inspect.currentframe().f_code.co_name)
        self.category_edit_content_cls.ids.txt_category_name.text = item_text
        drp_menu.dismiss()
    ########## Edit category ##########
    ##############################
    
    ###################################
    ########## Segmented controls ##########
    def scoring_type_rivcoop_change(self, seg_ctrl, seg_ctrl_item):
        print(inspect.currentframe().f_code.co_name)
        self.game.scoring_type_rivcoop = seg_ctrl_item.text
        
    def scoring_type_highlow_change(self, seg_ctrl, seg_ctrl_item):
        print(inspect.currentframe().f_code.co_name)
        self.game.scoring_type_highlow = seg_ctrl_item.text
        
    def scoring_type_updown_change(self, seg_ctrl, seg_ctrl_item):
        print(inspect.currentframe().f_code.co_name)
        self.game.scoring_type_updown = seg_ctrl_item.text
        
    def scoring_type_endround_change(self, seg_ctrl, seg_ctrl_item):
        print(inspect.currentframe().f_code.co_name)
        self.game.scoring_type_endround = seg_ctrl_item.text
        
    def scoring_type_defrounds_change(self, seg_ctrl, seg_ctrl_item):
        print(inspect.currentframe().f_code.co_name)
        self.game.scoring_type_defrounds = seg_ctrl_item.text
        
    def set_segmented_control(self, seg_ctrl, seg_ctrl_item, *args):
        print(inspect.currentframe().f_code.co_name)
        if seg_ctrl == "rivcoop":
            multiplier = 0
        if seg_ctrl == "highlow":
            multiplier = 1
        elif seg_ctrl == "updown":
            multiplier = 2
        elif seg_ctrl == "endround":
            multiplier = 3
        elif seg_ctrl == "defrounds":
            multiplier = 4
            
        if seg_ctrl_item == "left":
            x = 0.25*Window.width
        elif seg_ctrl_item == "right":
            x = 0.75*Window.width
            
        y = Window.height - \
            self.running_app.root.ids.tpb_editgame.height - \
            self.running_app.root.ids.txt_game_name.height - \
            self.running_app.root.ids.txt_counting_method.height - \
            dp(12) - dp(8) * 2 - \
            multiplier * (self.running_app.root.ids.seg_scoring_type_highlow.height + dp(8))
        
        touch = MouseMotionEvent(None, 0, (x,y))  # args are device, id, spos
        touch.button = 'left'
        touch.pos = (x,y)
        touch.x = touch.px = touch.ox = x
        touch.y = touch.py = touch.oy = y
        Window.dispatch('on_touch_down', touch)
    ########## Segmented controls ##########
    ###################################
   
    def sync_class_from_widget(self):
        print(inspect.currentframe().f_code.co_name)
        self.game.name = self.game.get_name(self.running_app.root.ids.txt_game_name.text),
        self.game.favorite = self.game.get_favorite(self.running_app.root.ids.ico_favorite_game.icon),
        self.counting_method.name = self.game.get_counting_method(self.running_app.root.ids.txt_counting_method.text),
        # I dont see a way to sync segmented controls other than only when it changes
        self.counting_method.game_end_condition = self.game.get_game_end_condition(self.running_app.root.ids.drp_end_game_condition.text),
        self.counting_method.points_on_start = self.game.get_points_on_start(self.running_app.root.ids.txt_points_on_start.text),
        self.counting_method.score_ending_the_game = self.game.get_score_ending_the_game(self.running_app.root.ids.txt_score_ending_the_game.text),
        self.counting_method.number_of_rounds = self.game.get_number_of_rounds(self.running_app.root.ids.txt_number_of_rounds.text),
        self.counting_method.round_name = self.game.get_round_name(self.running_app.root.ids.txt_round_name.text),
 