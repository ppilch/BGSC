from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.list import OneLineAvatarIconListItem

class MDColors(MDGridLayout):
    def __init__(
            self,
            colors_dict = None,
            **kwargs
            ):
        super().__init__(**kwargs)
        #self.red = [244/255,67/255,54/255,1]
#        self.pink = [233/255,30/255,99/255,1]
#        self.purple = [156/255,39/255,176/255,1]
#        self.deepPurple = [103/255,58/255,183/255,1]
#        self.indigo = [63/255,81/255,181/255,1]
#        self.blue = [33/255,150/255,243/255,1]
#        self.lightBlue = [3/255,169/255,244/255,1]
#        self.cyan = [0/255,188/255,212/255,1]
#        self.teal = [0/255,150/255,136/255,1]
#        self.green = [76/255,175/255,80/255,1]
#        self.lightGreen = [139/255,195/255,74/255,1]
#        self.lime = [205/255,220/255,57/255,1]
#        self.yellow = [255/255,253/255,59/255,1]
#        self.amber = [255/255,193/255,7/255,1]
#        self.orange = [255/255,152/255,0/255,1]
#        self.deepOrange = [255/255,87/255,34/255,1]
#        self.brown = [121/255,85/255,72/255,1]
#        self.grey = [178/255,178/255,178/255,1]
#        self.white = [230/255,230/255,230/255,1]
#        self.black = [51/255,51/255,51/255,1]
    colors_dict = {
            "red":[244/255,67/255,54/255,1],
            "pink":[233/255,30/255,99/255,1],
            "purple":[156/255,39/255,176/255,1],
            "deepPurple":[103/255,58/255,183/255,1],
            "indigo":[63/255,81/255,181/255,1],
            "blue":[33/255,150/255,243/255,1],
            "lightBlue":[3/255,169/255,244/255,1],
            "cyan":[0/255,188/255,212/255,1],
            "teal":[0/255,150/255,136/255,1],
            "green":[76/255,175/255,80/255,1],
            "lightGreen":[139/255,195/255,74/255,1],
            "lime":[205/255,220/255,57/255,1],
            "yellow":[255/255,253/255,59/255,1],
            "amber":[255/255,193/255,7/255,1],
            "orange":[255/255,152/255,0/255,1],
            "deepOrange":[255/255,87/255,34/255,1],
            "brown":[121/255,85/255,72/255,1],
            "grey":[178/255,178/255,178/255,1 ],
            "white":[230/255,230/255,230/255,1],
            "black":[51/255,51/255,51/255,1]
        }
        
            #red,
#            pink,
#            purple,
#            deepPurple,
#            indigo,
#            blue,
#            lightBlue,
#            cyan,
#            teal,
#            green,
#            lightGreen,
#            lime,
#            yellow,
#            amber,
#            orange,
#            deepOrange,
#            brown,
#            grey,
#            white,
#            black,