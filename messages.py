from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, OneLineListItem
from kivymd.uix.boxlayout import  MDBoxLayout
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
        