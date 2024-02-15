from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, OneLineListItem
from kivymd.uix.boxlayout import  MDBoxLayout
from kivy.core.window import Window
from kivymd.uix.snackbar import Snackbar
import inspect

class ItemSelect(OneLineAvatarIconListItem):
    divider = None
    
class ListDialog(MDBoxLayout):
    pass
    
class Messages():
    
    def show_simple_information(self, msg_title, msg_text):
        print(inspect.currentframe().f_code.co_name)
        dialog = MDDialog(
            title = msg_title,
            text = msg_text,
            buttons = [MDFlatButton(text="OK", on_release = lambda x: dialog.dismiss())]
            )
        dialog.open()

    def show_error(self, error_text):
        print(inspect.currentframe().f_code.co_name)
        dialog = MDDialog(
            title = "Error",
            text = error_text,
            buttons = [MDFlatButton(text="OK", on_release = lambda x: dialog.dismiss())]
            )
        dialog.open()
    
    def show_snackbar_OK(self, message, duration = 1):
        player_sbar = Snackbar(
            text=message,
            snackbar_x="10dp",
            snackbar_y="10dp",
            duration = duration,
            )
        player_sbar.size_hint_x = (Window.width - (player_sbar.snackbar_x * 2)) / Window.width
        player_sbar.buttons = [
            MDFlatButton(
                text="OK",
                on_release=player_sbar.dismiss,
                theme_text_color = "Custom",
                text_color = "white",
            )
        ]
        player_sbar.open()
        