l<DrawerClickableItem@MDNavigationDrawerItem>
#    focus_color: "#e7e4c0"
#    text_color: "#4a4939"
#    icon_color: "#4a4939"
#    ripple_color: "#c5bdd2"
#    selected_color: "#0c6c4d"


<DrawerLabelItem@MDNavigationDrawerItem>
#    text_color: "#4a4939"
#    icon_color: "#4a4939"
    focus_behavior: False
#    selected_color: "#4a4939"
    _no_ripple_effect: True
    
MDScreen:
    name: "XXX"
    MDNavigationLayout:

        MDScreenManager:
        	id: scr_mngr

            ##### Main screens #####
            #New Game
            MDScreen:
                name: "newgame"
                MDTopAppBar:
                    title: "New Game"
                    elevation: 4
                    pos_hint: {"top": 1}
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("toggle")]]
                BoxLayout:

            #Players
            MDScreen:
                name: "players"
                BoxLayout:
                    id: playersBox
                    orientation: "vertical"
                    pos_hint: {"top": 1}
                    MDTopAppBar:
                        title: "Players"
                        elevation: 4
                        pos_hint: {"top": 1}
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("toggle")]]
                
                    ScrollView:
                        do_scroll_x: False
                        pos_hint: {"top": 1}
                        MDList:
                            id: mdlPlayers
                            pos_hint: {"top": 1}
                            
                MDFloatingActionButton:
                    icon: 'plus-thick'
                    elevation_normal: 12
                    pos_hint: {'center_x': 0.85, 'center_y':0.05}
                    on_release: app.p.show_player_dialog(action="Add")
                
            #Games
            MDScreen:
                name: "games"
                MDTopAppBar:
                    title: "Games"
                    elevation: 4
                    pos_hint: {"top": 1}
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("toggle")]]
                BoxLayout:               

            #Games History
            MDScreen:
                name: "gameshistory"
                MDTopAppBar:
                    title: "Games History"
                    elevation: 4
                    pos_hint: {"top": 1}
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("toggle")]]
                BoxLayout:

            #About
            MDScreen:
                name: "about"
                MDTopAppBar:
                    title: "About"
                    elevation: 4
                    pos_hint: {"top": 1}
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("toggle")]]
                BoxLayout:

            #Options
            MDScreen:
                name: "options"
                MDTopAppBar:
                    title: "Options"
                    elevation: 4
                    pos_hint: {"top": 1}
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("toggle")]]
                BoxLayout:
                                             
        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)
                
            MDNavigationDrawerMenu:

                DrawerClickableItem:
                    icon: "plus"
                    text: "New Game"
                    on_release: app.root.ids.scr_mngr.current = 'newgame'
                    on_release: nav_drawer.set_state("close")
                    
                DrawerClickableItem:
                    icon: "account-multiple"
                    text: "Players"
                    on_release: app.root.ids.scr_mngr.current = 'players'
                    on_release: nav_drawer.set_state("close")
           
                DrawerClickableItem:
                    icon: "chess-pawn"
                    text: "Games"
                    on_release: app.root.ids.scr_mngr.current = 'games'
                    on_release: nav_drawer.set_state("close")

                DrawerClickableItem:
                    icon: "history"
                    text: "Games History"
                    on_release: app.root.ids.scr_mngr.current = 'gameshistory'
                    on_release: nav_drawer.set_state("close")

                DrawerClickableItem:
                    icon: "information"
                    text: "About"
                    on_release: app.root.ids.scr_mngr.current = 'about'
                    on_release: nav_drawer.set_state("close")

                DrawerClickableItem:
                    icon: "cog"
                    text: "Options"
                    on_release: app.root.ids.scr_mngr.current = 'options'
                    on_release: nav_drawer.set_state("close")