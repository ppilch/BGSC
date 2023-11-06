from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.image import Image

from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.app import App, MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.icon_definitions import md_icons

def assign_icon(txtName):
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
    
    players_mdlist = None
    player_dialog = None
    delete_player_confirmation_dialog = None
    selected_player = ObjectProperty()
    selected_player_left_icon = ObjectProperty()
    selected_player_color = [0,0,0,1]
    action = "Add"
    
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
        "black":["checkbox-blank-circle",[0/255,0/255,0/255,1]]
    }

    def set_players_mdlist(self):
        app = MDApp.get_running_app()  # get a refrence to the running App
        self.players_mdlist = app.root.ids.mdlPlayers
        
    def show_player_dialog(self, action):
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
                    MDFlatButton(text='OK', on_release=lambda x:self.save_player(x,self.player_edit_content_cls, action))]
                )
            if action == "Edit":    #when empty then is always in error/red which I want to show only after not providing a name
                self.player_edit_content_cls.ids.tfPlayerName.required = True
                self.player_edit_content_cls.ids.tfPlayerName.helper_text_mode = "on_error"
        self.player_dialog.open()

    def close_player_dialog(self, *args):
        self.player_dialog.dismiss()
        self.player_dialog = None
        self.selected_player_color = [0,0,0,1]
        
    def save_player(self, instance_btn, content_cls, action):
        self.set_players_mdlist()
        if len(self.player_edit_content_cls.ids.tfPlayerName.text) == 0 or None: 
            self.player_edit_content_cls.ids.tfPlayerName.required = True
            self.player_edit_content_cls.ids.tfPlayerName.error = True
            self.player_edit_content_cls.ids.tfPlayerName.helper_text_mode = "on_error"
            return
        if action == "Add":
            player_name = self.player_edit_content_cls.ids.tfPlayerName.text
            player_widget = PlayerWithAvatar(text=player_name)
            player_left_avatar_widget = IconLeftWidget(
                id = "left_widget",
                icon = assign_icon(player_name),
                theme_icon_color = "Custom",
                icon_color = self.selected_player_color,
                )
            player_right_icon_widget = IconRightWidget(
                icon="pencil",
                on_release = lambda x: self.change_line_item(line_item = player_widget, left_avatar = player_left_avatar_widget),
                text = self.player_edit_content_cls.ids.tfPlayerName.text
            )
            player_widget.add_widget(player_left_avatar_widget)
            player_widget.add_widget(player_right_icon_widget)
            #app.root.ids.mdlPlayers.add_widget(player_widget)
            self.players_mdlist.add_widget(player_widget)
        elif action == "Edit":
            self.selected_player.text = self.player_edit_content_cls.ids.tfPlayerName.text
            self.selected_player_left_icon.icon = assign_icon(self.player_edit_content_cls.ids.tfPlayerName.text)
            self.selected_player_left_icon.icon_color = self.selected_player_color
        self.close_player_dialog()
    
    def reset_color_selection(self):
        for color in self.colors_dict:
            self.player_edit_content_cls.ids[color].icon = self.colors_dict[color][0]

    def change_line_item(self, line_item, left_avatar):
        # Here 'entry' is the widget that has been passed.
        # Store this entry to access it from anywhere in this class.
        self.selected_player = line_item
        self.selected_player_left_icon = left_avatar
        self.selected_player_left_icon_color = self.selected_player_left_icon.icon_color
        self.show_player_dialog(action="Edit")
        self.player_edit_content_cls.ids.tfPlayerName.text = self.selected_player.text
        selected_icon_color_name = list(self.colors_dict.keys())[list(self.colors_dict.values()).index(["checkbox-blank-circle",self.selected_player_left_icon_color])]
        self.player_edit_content_cls.ids[selected_icon_color_name].icon = "checkbox-marked-circle"
 
    def close_delete_player_confirmation_dialog(self, *args, action):
        self.set_players_mdlist()
        self.delete_player_confirmation_dialog.dismiss()
        self.delete_player_confirmation_dialog = None
        if action == "YES":
            self.close_player_dialog()
            self.players_mdlist.remove_widget(self.selected_player)
            
    def show_delete_player_confirmation_dialog(self):
        if not self.delete_player_confirmation_dialog:
            self.delete_player_confirmation_dialog = MDDialog(
                text="Delete player?",
                buttons=[
                    MDFlatButton(text="CANCEL", on_release = lambda x: self.close_delete_player_confirmation_dialog(action = "CANCEL")),
                    MDFlatButton(text="YES", on_release = lambda x: self.close_delete_player_confirmation_dialog(action = "YES"))
                ]
            )
        self.delete_player_confirmation_dialog.open()
            
    def delete_player(self):
        if self.action == "Add":
            self.player_edit_content_cls.ids.tfPlayerName.text = ""
        if self.action == "Edit":
            self.show_delete_player_confirmation_dialog()
            