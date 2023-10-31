<PlayerEdit>
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "280dp"
    
    BoxLayout:
        size_hint: (1,0.1)
        orientation: "horizontal"

        MDTextField:
            id: tfPlayerName
            hint_text: "Name"
            pos_hint: {"center_x": 1, "center_y": .9}
            
        MDIconButton:
            icon: "delete"
            pos_hint: {"center_x": 1, "center_y": .9}
            on_release: app.p.delete_player()
            
            
    GridLayout:
        cols: 4
        rows: 5
        #Red
        MDIconButton:
            id: red
            icon: "checkbox-blank-circle"
            theme_icon_color: "Custom"
            icon_color: 244/255,67/255,54/255,1
            size_hint: (0.25, 0.2)
            on_release:
                app.p.reset_color_selection();
                red.icon = "checkbox-marked-circle";
                app.p.selected_player_color = self.icon_color
        #Pink
        MDIconButton:
            id: pink
            icon: "checkbox-blank-circle"
            theme_icon_color: "Custom"
            icon_color: 233/255,30/255,99/255,1
            size_hint: (0.25, 0.2)
            on_release:
                app.p.reset_color_selection();
                pink.icon = "checkbox-marked-circle";
                app.p.selected_player_color = self.icon_color
        #Pink
        
        #Purple
        MDIconButton:
            id: purple
            icon: "checkbox-blank-circle"
            theme_icon_color: "Custom"
            icon_color: 156/255,39/255,176/255,1
            size_hint: (0.25, 0.2)
            on_release:
                app.p.reset_color_selection();
                purple.icon = "checkbox-marked-circle";
                app.p.selected_player_color = self.icon_color
        #DeepPurple
        MDIconButton:
            id: deepPurple
            icon: "checkbox-blank-circle"
            theme_icon_color: "Custom"
            icon_color: 103/255,58/255,183/255,1
            size_hint: (0.25, 0.2)
            on_release:
                app.p.reset_color_selection();
                deepPurple.icon = "checkbox-marked-circle";
                app.p.selected_player_color = self.icon_color
        #Indigo
        MDIconButton:
            id: indigo
            icon: "checkbox-blank-circle"
            theme_icon_color: "Custom"
            icon_color: 63/255,81/255,181/255,1
            size_hint: (0.25, 0.2)
            on_release:
                app.p.reset_color_selection();
                indigo.icon = "checkbox-marked-circle";
                app.p.selected_player_color = self.icon_color
        #Blue
        MDIconButton:
            id: blue
            icon: "checkbox-blank-circle"
            theme_icon_color: "Custom"
            icon_color: 33/255,150/255,243/255,1
            size_hint: (0.25, 0.2)
            on_release:
                app.p.reset_color_selection();
                blue.icon = "checkbox-marked-circle";
                app.p.selected_player_color = self.icon_color
        #LightBlue
        MDIconButton:
            id: lightBlue
            icon: "checkbox-blank-circle"
            theme_icon_color: "Custom"
            icon_color: 3/255,169/255,244/255,1
            size_hint: (0.25, 0.2)
            on_release:
                app.p.reset_color_selection();
                lightBlue.icon = "checkbox-marked-circle";
                app.p.selected_player_color = self.icon_color
        #Cyan
        MDIconButton:
            id: cyan
            icon: "checkbox-blank-circle"
            theme_icon_color: "Custom"
            icon_color: 0/255,188/255,212/255,1
            size_hint: (0.25, 0.2)
            on_release:
                app.p.reset_color_selection();
                cyan.icon = "checkbox-marked-circle";
                app.p.selected_player_color = self.icon_color
        #Teal
        MDIconButton:
            id: teal
            icon: "checkbox-blank-circle"
            theme_icon_color: "Custom"
            icon_color: 0/255,150/255,136/255,1
            size_hint: (0.25, 0.2)
            on_release:
                app.p.reset_color_selection();
                teal.icon = "checkbox-marked-circle";
                app.p.selected_player_color = self.icon_color
        #Green
        MDIconButton:
            id: green
            icon: "checkbox-blank-circle"
            theme_icon_color: "Custom"
            icon_color: 76/255,175/255,80/255,1
            size_hint: (0.25, 0.2)
            on_release:
                app.p.reset_color_selection();
                green.icon = "checkbox-marked-circle";
                app.p.selected_player_color = self.icon_color
        #LightGreen
        MDIconButton:
            id: lightGreen
            icon: "checkbox-blank-circle"
            theme_icon_color: "Custom"
            icon_color: 139/255,195/255,74/255,1
            size_hint: (0.25, 0.2)
            on_release:
                app.p.reset_color_selection();
                lightGreen.icon = "checkbox-marked-circle";
                app.p.selected_player_color = self.icon_color
        #Lime
        MDIconButton:
            id: lime
            icon: "checkbox-blank-circle"
            theme_icon_color: "Custom"
            icon_color: 205/255,220/255,57/255,1
            size_hint: (0.25, 0.2)
            on_release:
                app.p.reset_color_selection();
                lime.icon = "checkbox-marked-circle";
                app.p.selected_player_color = self.icon_color
        #Yellow
        MDIconButton:
            id: yellow
            icon: "checkbox-blank-circle"
            theme_icon_color: "Custom"
            icon_color: 255/255,253/255,59/255,1
            size_hint: (0.25, 0.2)
            on_release:
                app.p.reset_color_selection();
                yellow.icon = "checkbox-marked-circle";
                app.p.selected_player_color = self.icon_color
        #Amber
        MDIconButton:
            id: amber
            icon: "circle"
            theme_icon_color: "Custom"
            icon_color: 255/255,193/255,7/255,1
            size_hint: (0.25, 0.2)
            on_release:
                app.p.reset_color_selection();
                amber.icon = "checkbox-marked-circle";
                app.p.selected_player_color = self.icon_color
        #Orange
        MDIconButton:
            id: orange
            icon: "circle"
            theme_icon_color: "Custom"
            icon_color: 255/255,152/255,0/255,1
            size_hint: (0.25, 0.2)
            on_release:
                app.p.reset_color_selection();
                orange.icon = "checkbox-marked-circle";
                app.p.selected_player_color = self.icon_color
        #DeepOrange
        MDIconButton:
            id: deepOrange
            icon: "circle"
            theme_icon_color: "Custom"
            icon_color: 255/255,87/255,34/255,1
            size_hint: (0.25, 0.2)
            on_release:
                app.p.reset_color_selection();
                deepOrange.icon = "checkbox-marked-circle";
                app.p.selected_player_color = self.icon_color
        #Brown
        MDIconButton:
            id: brown
            icon: "circle"
            theme_icon_color: "Custom"
            icon_color: 121/255,85/255,72/255,1
            size_hint: (0.25, 0.2)
            on_release:
                app.p.reset_color_selection();
                brown.icon = "checkbox-marked-circle";
                app.p.selected_player_color = self.icon_color
        #Grey
        MDIconButton:
            id: grey
            icon: "circle"
            theme_icon_color: "Custom"
            icon_color: 178/255,178/255,178/255,1 
            size_hint: (0.25, 0.2)
            on_release:
                app.p.reset_color_selection();
                grey.icon = "checkbox-marked-circle";
                app.p.selected_player_color = self.icon_color
        #White
        MDIconButton:
            id: white
            icon: "circle"
            theme_icon_color: "Custom"
            icon_color: 230/255,230/255,230/255,1
            size_hint: (0.25, 0.2)
            on_release:
                app.p.reset_color_selection();
                white.icon = "checkbox-marked-circle";
                app.p.selected_player_color = self.icon_color
        #Black
        MDIconButton:
            id: black
            icon: "circle"
            theme_icon_color: "Custom"
            icon_color: 0/255,0/255,0/255,1
            size_hint: (0.25, 0.2)
            on_release:
                app.p.reset_color_selection();
                black.icon = "checkbox-marked-circle";
                app.p.selected_player_color = self.icon_color
