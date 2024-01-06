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
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.icon_definitions import md_icons
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.tooltip.tooltip import MDTooltip
from kivymd.uix.menu import MDDropdownMenu
from editgame import *

Window.keyboard_anim_args = {'d':.2, 't': 'in_out_expo'}
Window.softinput_mode = 'below_target'

kv = """
<TooltipMDIconButton@MDIconButton+MDTooltip>

<ItemConfirm>
    id: item_confirm
    on_release: app.eg.select_counting_method(item_confirm)

MDScreen:
    id: scr_edit_game
    name: "testapp"
    
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            id: tpb_editgame
            title: "Edit Game"
            left_action_items: [["arrow-left", lambda x: app.eg.dont_save_game(),"Back"]]
            right_action_items: [["delete", lambda x: app.eg.delete_game(),"Delete"],["content-save", lambda x: app.eg.editgame_load_screen(),"Save"]]
            elevation: 4
            pos_hint: {"top": 1}
    
        MDScrollView:
            id: edit_game_scroll_view
            #height: scr_edit_game.height/2
            #pos_hint: {"y": -tpb_editgame.height/scr_edit_game.height}
                        
            MDList:
                id: mylist
                size_hint_y: None
                height: self.minimum_height
                padding: "12dp", "0dp", "12dp", "0dp"
                spacing: "8dp"
                
                MDGridLayout:
                    cols: 2
                    size_hint_y: None
                    height: self.minimum_height
                            
                    MDTextField:
                        id: txt_game_name
                        hint_text: "Game name"
                        max_text_length: 50
                        font_size: "24dp"
                                        
                    TooltipMDIconButton:
                        id: ico_favorite_game
                        icon: "star-outline"
                        tooltip_text: "Add to favorites"
                        icon_size: "30dp"
                        on_release: app.eg.change_favorites()
                    
                    MDTextField:
                        id: txt_counting_method
                        text: "At game end"
                        hint_text: "Counting method"
                        max_text_length: 50
                        font_size: "24dp"
                        required: True
                                                 
                    TooltipMDIconButton:
                        id: ico_counting_method
                        icon: "expand-all"
                        tooltip_text: "Select counting method"
                        on_release: app.eg.show_counting_method_dialog()

                MDSegmentedControl:
                    id: seg_scoring_type_rivcoop
                    on_active: app.eg.scoring_type_rivcoop_change(*args)
                    MDSegmentedControlItem:
                        id: sci_game_type_rivcoop_riv
                        text: "Rivalisation"
                        font_size: "14dp"
                    MDSegmentedControlItem:
                        id: sci_game_type_rivcoop_coop
                        text: "Cooperation"
                        font_size: "14dp"
                    
                MDSegmentedControl:
                    id: seg_scoring_type_highlow
                    on_active: app.eg.scoring_type_highlow_change(*args)
                    MDSegmentedControlItem:
                        id: sci_game_type_highlow_high
                        text: "Highest score wins"
                        font_size: "14dp"
                    MDSegmentedControlItem:
                        id: sci_game_type_highlow_low
                        text: "Lowest score wins"
                        font_size: "14dp"
                    
                MDSegmentedControl:
                    id: seg_scoring_type_updown
                    on_active: app.eg.scoring_type_updown_change(*args)
                    MDSegmentedControlItem:
                        text: "Scoring up"
                        font_size: "14dp"
                    MDSegmentedControlItem:
                        text: "Scoring down"
                        font_size: "14dp"
                                                     
                MDSegmentedControl:
                    id: seg_scoring_type_endround
                    on_active: app.eg.scoring_type_endround_change(*args)
                    MDSegmentedControlItem:
                        text: "Scoring at the end"
                        font_size: "14dp"
                    MDSegmentedControlItem:
                        text: "Scoring after rounds"
                        font_size: "14dp"
                                            
                MDSegmentedControl:
                    id: seg_scoring_type_defrounds
                    on_active: app.eg.scoring_type_defrounds_change(*args)
                    MDSegmentedControlItem:
                        text: "Defined rounds number"
                        font_size: "14dp"
                    MDSegmentedControlItem:
                        text: "Undefined rounds number"
                        font_size: "14dp"
                        
                MDGridLayout:
                    cols: 2
                    size_hint_y: None
                    height: self.minimum_height
                    spacing: "12dp"
                    padding: "0dp", "0dp", "0dp", "12dp"
                    
                    ### DropDown
                    MDLabel:
                        text: "Game end condition:"
                        size_hint_x: 0.5
                                                    
                    MDDropDownItem:
                        id: drp_end_game_condition
                        text: "Manual"
                        size_hint_x: 0.5
                        on_release: app.eg.open_drp_game_end_conditions()
                    
                    ### TextFields               
                    MDTextField:
                        id: txt_points_on_start
                        text: "1"
                        hint_text: "Points on start"
                        helper_text: "Leave empty if not defined"
                        helper_text_mode: "persistent"
                        input_filter: "int"
                        font_size: "24dp"
                        required: True
                                                
                    MDTextField:
                        id: txt_score_ending_the_game
                        hint_text: "Score ending the game"
                        helper_text: "Leave empty if not defined"
                        helper_text_mode: "persistent"
                        input_filter: "int"
                        font_size: "24dp"
                        #size_hint_x: 0.5
                                        
                    MDTextField:
                        id: txt_number_of_rounds
                        text: "1"
                        hint_text: "Number of rounds"
                        helper_text: "Minimum 1"
                        helper_text_mode: "persistent"
                        input_filter: "int"
                        font_size: "24dp"
                        on_text: app.eg.validate_number_of_rounds()
                                            
                    MDTextField:
                        id: txt_round_name
                        text: "Game end"
                        hint_text: "Round name"
                        helper_text: "Round/Phase/Stage/etc."
                        helper_text_mode: "persistent"
                        font_size: "24dp"
                        required: True
                                        
                    
        MDTabs:
            id: tab_edit_game
            padding: "12dp", "0dp", "12dp", "0dp"
            size_hint_y: 0.35
            Tab:
                id: tab_rounds
                title: "Rounds"
            Tab:
                id: tab_categories
                title: "Categories"
            Tab:
                id: tab_rules
                title: "Rules"
                
    #MDFloatingActionButton:
#        icon: 'plus-thick'
#        elevation_normal: 12
#        pos_hint: {'x': 0.8, 'y':0.67}

"""

class TestApp(MDApp):

    running_app = None
    menu = None
    
    eg = EditGameManagement()
    msg = Messages()
    
    def build(self):
        print(inspect.currentframe().f_code.co_name)
        self.theme_cls.theme_style = "Dark"
        Builder.load_file('./kv/messages.kv')
        Builder.load_file('./kv/category_edit.kv')
        return Builder.load_string(kv)

TestApp().run()
