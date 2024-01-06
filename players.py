####################################################################
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

def assign_icon(txtName):
    print(inspect.currentframe().f_code.co_name)
    firstLetter = txtName[0].lower()
    if ord(firstLetter) >= 97 and ord(firstLetter) <= 122:
        return f"alpha-{firstLetter}-circle"
    elif ord(firstLetter) >= 48 and ord(firstLetter) <= 57:
        return f"numeric-{firstLetter}-circle"
    else:
        return "cat"
                
class PlayerEdit(BoxLayout):
    pass

class PlayerWithAvatar(OneLineAvatarIconListItem):
    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        # state a pk which we shall use link the list items with the database primary keys
        self.pk = pk
        
class PlayersManagement(MDScreen):
    #def __init__(self):
        #dbo = DBOperations()
    
    player_edit_content_cls = None
    players_mdlist = None
    player_dialog = None
    delete_player_confirmation_dialog = None
    running_app = None
    selected_player = ObjectProperty()
    selected_player_left_icon = ObjectProperty()
    selected_player_color = [51,51,51,1]
    selected_player_id = 0
    selected_player_name = "Player X"
    selected_player_avatar = "alpha-x-circle"
    action = "Add"
    players_already_loaded_from_db = False
    player_filter_name = ""
    player_order_column = "Id"
    player_order_direction = "ASC"
    
    colors_dict = {
        "red":["checkbox-blank-circle",[244/255,67/255,54/255,1]],
        "pink":["checkbox-blank-circle",[233/255,30/255,99/255,1]],
        "purple":["checkbox-blank-circle",[156/255,39/255,176/255,1]],
        "deepPurple":["checkbox-blank-circle",[103/255,58/255,183/255,1]],
        "indigo":["checkbox-blank-circle",[63/255,81/255,181/255,1]],
        "blue":["checkbox-blank-circle",[33/255,150/255,243/255,1]],
        "lightBlue":["checkbox-blank-circle",[3/255,169/255,244/255,1]],
        "cyan":["checkbox-blank-circle",[0/255,188/255,212/255,1]],
        "teal":["checkbox-blank-circle",[0/255,150/255,136/255,1]],
        "green":["checkbox-blank-circle",[76/255,175/255,80/255,1]],
        "lightGreen":["checkbox-blank-circle",[139/255,195/255,74/255,1]],
        "lime":["checkbox-blank-circle",[205/255,220/255,57/255,1]],
        "yellow":["checkbox-blank-circle",[255/255,253/255,59/255,1]],
        "amber":["checkbox-blank-circle",[255/255,193/255,7/255,1]],
        "orange":["checkbox-blank-circle",[255/255,152/255,0/255,1]],
        "deepOrange":["checkbox-blank-circle",[255/255,87/255,34/255,1]],
        "brown":["checkbox-blank-circle",[121/255,85/255,72/255,1]],
        "grey":["checkbox-blank-circle",[178/255,178/255,178/255,1 ]],
        "white":["checkbox-blank-circle",[230/255,230/255,230/255,1]],
        "black":["checkbox-blank-circle",[51/255,51/255,51/255,1]]
    }

    def players_load_screen(self):
        print(inspect.currentframe().f_code.co_name)
        self.running_app = MDApp.get_running_app()
        self.players_mdlist = self.running_app.root.ids.mdlPlayers
        self.reload_players_list()
        #Workaround from stackoverflow (size not working in .kv)
        self.running_app.root.ids.mdsc_player_order_column.ids.segment_panel.width = (Window.width - dp(60))/2
        self.running_app.root.ids.mdsc_player_order_direction.ids.segment_panel.width = (Window.width - dp(60))/2
                
    def show_player_dialog(self, action):
        print(inspect.currentframe().f_code.co_name)
        if not self.player_dialog:
            self.action = action
            self.player_edit_content_cls = PlayerEdit()
            self.player_dialog = MDDialog(
                title = f"{action} player:",
                type = "custom",
                pos_hint = {"center_x": .5, "center_y": .6},
                content_cls = self.player_edit_content_cls,
                buttons=[
                    MDFlatButton(text='CANCEL', on_release=self.close_player_dialog),
                    MDFlatButton(text='OK', on_release=lambda x:self.save_player(self.player_edit_content_cls, action))]
                )
            if action == "Edit":    #when empty then is always in error/red which I want to show only after not providing a name
                self.player_edit_content_cls.ids.tfPlayerName.required = True
                self.player_edit_content_cls.ids.tfPlayerName.helper_text_mode = "on_error"
        self.player_dialog.open()

    def close_player_dialog(self, *args):
        print(inspect.currentframe().f_code.co_name)
        self.player_dialog.dismiss()
        self.player_dialog = None
        self.selected_player_color = [51,51,51,1]
        
    def save_player(self, content_cls, action):
        method = inspect.currentframe().f_code.co_name
        print(method)
        #self.set_players_mdlist()
        if action == "Add" and (len(self.player_edit_content_cls.ids.tfPlayerName.text) == 0 or len(self.player_edit_content_cls.ids.tfPlayerName.text) > 50):
            print(method + "-Add-0")
            self.player_edit_content_cls.ids.tfPlayerName.required = True
            self.player_edit_content_cls.ids.tfPlayerName.error = True
            self.player_edit_content_cls.ids.tfPlayerName.helper_text_mode = "on_error"
            return
        if action == "Add":
            print(method + "-Add-assign")
            player_name = self.player_edit_content_cls.ids.tfPlayerName.text
            player_color = self.selected_player_color
            player_avatar = assign_icon(player_name)
        if action == "Load":
            print(method + "-Load-assign")
            player_id = self.selected_player_id
            player_name = self.selected_player_name
            player_color = self.selected_player_color
            player_avatar = self.selected_player_avatar
        if action == "Edit":
            print(method + "-Edit-assign")
            player_id = self.selected_player_id
            player_name = self.player_edit_content_cls.ids.tfPlayerName.text
            player_color = self.selected_player_color
            player_avatar = assign_icon(player_name)
        if action == "Load":
            print(method + "-Load-action")
            player_widget = PlayerWithAvatar(text=player_name, pk = player_id)
            player_left_avatar_widget = IconLeftWidget(
                id = "left_widget",
                icon = player_avatar,
                theme_icon_color = "Custom",
                icon_color = player_color,
                )
            player_right_icon_widget = IconRightWidget(
                icon="pencil",
                on_release = lambda x: self.change_line_item(line_item = player_widget, left_avatar = player_left_avatar_widget),
                #text = self.player_edit_content_cls.ids.tfPlayerName.text
            )
            player_widget.add_widget(player_left_avatar_widget)
            player_widget.add_widget(player_right_icon_widget)
            self.players_mdlist.add_widget(player_widget)
        if action == "Add":
            print(method + "-Add-action")
            player_id = dbo.insert_player(player_name, player_avatar, player_color)
            print("inserted player id")
            print(player_id)
            #new_player = dbo.get_player(player_id[0][0], "-1", "")
            #self.load_player(new_player)
            self.reload_players_list()
        if action == "Edit":
            print(method + "-Edit-action")
            self.selected_player.text = player_name
            self.selected_player_left_icon.icon_color = player_color
            self.selected_player_left_icon.icon = player_avatar
            dbo.update_player(player_id,player_name, player_avatar, player_color)
        if action == "Add" or action == "Edit":
            print(method + "-CloseDialog")
            self.close_player_dialog()
            self.show_saved_player_snackbar("saved")

    def get_id(self,  butt_instance):
        print(inspect.currentframe().f_code.co_name)
        the_id = None
        for butt_id, button in self.player_edit_content_cls.ids.items():
            if button == butt_instance:
                the_id = butt_id
                break
        return the_id
            
    def reset_color_selection(self, button):
        print(inspect.currentframe().f_code.co_name)
        selected_color_id = self.get_id(butt_instance = button)
        #self.player_edit_content_cls = PlayerEdit()
        #print(self.player_edit_content_cls)
        for color in self.colors_dict:
            self.player_edit_content_cls.ids[color].icon = self.colors_dict[color][0]
        self.player_edit_content_cls.ids[selected_color_id].icon = "checkbox-marked-circle"
        self.selected_player_color = button.icon_color

    def change_line_item(self, line_item, left_avatar):
        print(inspect.currentframe().f_code.co_name)
        # Here 'entry' is the widget that has been passed.
        # Store this entry to access it from anywhere in this class.
        self.selected_player = line_item
        self.selected_player_left_icon = left_avatar
        self.selected_player_left_icon_color = left_avatar.icon_color
        self.selected_player_color = left_avatar.icon_color
        self.show_player_dialog(action="Edit")
        self.player_edit_content_cls.ids.tfPlayerName.text = self.selected_player.text
        selected_icon_color_name = list(self.colors_dict.keys())[list(self.colors_dict.values()).index(["checkbox-blank-circle",self.selected_player_left_icon_color])]
        self.player_edit_content_cls.ids[selected_icon_color_name].icon = "checkbox-marked-circle"
        self.selected_player_id = self.selected_player.pk
 
    def close_delete_player_confirmation_dialog(self, *args, action):
        print(inspect.currentframe().f_code.co_name)
        #self.set_players_mdlist()
        self.delete_player_confirmation_dialog.dismiss()
        self.delete_player_confirmation_dialog = None
        if action == "YES":
            self.close_player_dialog()
            dbo.delete_player_soft(id= self.selected_player.pk)
            self.players_mdlist.remove_widget(self.selected_player)
            self.show_saved_player_snackbar("deleted")
            
            
    def show_delete_player_confirmation_dialog(self):
        print(inspect.currentframe().f_code.co_name)
        if not self.delete_player_confirmation_dialog:
            self.delete_player_confirmation_dialog = MDDialog(
                title="Delete player?",
                text="This player still will be visible in history if played any games.",
                buttons=[
                    MDFlatButton(text="CANCEL", on_release = lambda x: self.close_delete_player_confirmation_dialog(action = "CANCEL")),
                    MDFlatButton(text="YES", on_release = lambda x: self.close_delete_player_confirmation_dialog(action = "YES"))
                ]
            )
        self.delete_player_confirmation_dialog.open()
            
    def delete_player(self):
        print(inspect.currentframe().f_code.co_name)
        if self.action == "Add":
            self.player_edit_content_cls.ids.tfPlayerName.text = ""
        if self.action == "Edit":
            self.show_delete_player_confirmation_dialog()
      
    def load_player(self, players_from_db):
        print(inspect.currentframe().f_code.co_name)
        if players_from_db != []:
            for player in players_from_db:
                self.selected_player_id = player[0]
                self.selected_player_name = player[1]
                self.selected_player_avatar = player[2]
                self.selected_player_color = []
                self.selected_player_color.append(player[3]/255)
                self.selected_player_color.append(player[4]/255)
                self.selected_player_color.append(player[5]/255)
                self.selected_player_color.append(player[6])
                self.save_player(None, action = "Load")
                
    def open_players_backdrop(self, the_backdrop):
        print(inspect.currentframe().f_code.co_name)
        the_backdrop.open(-Window.height / 4)
        the_backdrop.left_action_items = [["menu",lambda x: self.running_app.root.ids.nav_drawer.set_state("toggle")]]
        
    def clear_players_list(self):
        print(inspect.currentframe().f_code.co_name)
        self.players_mdlist.clear_widgets()
        
    def filter_players(self, name):
        print(inspect.currentframe().f_code.co_name)
        if name == "":
            self.player_filter_name = -1
            self.running_app.root.ids.bkdp_players.header_text = f"Filters: None"
        else:
            self.player_filter_name = name
            self.running_app.root.ids.bkdp_players.header_text = f"Filters: {name}"
        self.reload_players_list()
        
    def change_player_order_column(self, segmented_control, segmented_item):
        print(inspect.currentframe().f_code.co_name)
        if segmented_item.text != "Name":
            self.player_order_column = "id"
        else:
            self.player_order_column = "Name"
        self.reload_players_list()
        
    def change_player_order_direction(self, segmented_control, segmented_item):
        print(inspect.currentframe().f_code.co_name)
        if segmented_item.text == "A-Z":
            self.player_order_direction = "ASC"
        else:
            self.player_order_direction = "DESC"
        self.reload_players_list()
        
    def reload_players_list(self):
        self.clear_players_list()
        db_players = dbo.get_player(-1, self.player_filter_name, self.player_order_column, self.player_order_direction)
        self.load_player(db_players)
        
    def show_saved_player_snackbar(self, action):
        Snackbar(
            text=f"Player {action}",
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=(Window.width - (dp(10) * 2)) / Window.width / 2,
            #pos_hint = {'center_x': .5}
        ).open()