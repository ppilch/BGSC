import inspect
from db import *

class InitialLoad:
     
    def initial_load(self):
        print(inspect.currentframe().f_code.co_name)
        
        dbo = DBOperations()
       
        dbo.drop_all_objects()
        dbo.create_all_objects()
        
        ##### get default_counting_method #####
        default_counting_method = dbo.get_setting("default_counting_method")
        
        ################
        ##### players #####
        
        dbo.insert_player("Paweł", "alpha-p-circle", [121/255, 85/255, 72/255, 1])
        dbo.insert_player("Kornelia", "alpha-k-circle", [244/255, 67/255, 54/255, 1])
        dbo.insert_player("Natan", "alpha-n-circle", [63/255, 81/255, 181/255, 1])
        dbo.insert_player("Estera","alpha-e-circle", [233/255, 30/255, 99/255, 1])
        dbo.insert_player("Tobiasz","alpha-t-circle", [205/255, 220/255, 57/255, 1])
        
        ################
        ##### games #####
        
        ##### agricola #####
        #game
        game_id_agricola = dbo.upsert_game(-1, "Agricola", "star", "Agricola.jpg")
        #counting_method
        #counting_method_id_agricola_points = dbo.upsert_counting_method(default_counting_method, game_id_agricola, "checkbox-marked-circle-outline", "rivalisation", "highest", "up", "end", "defined", "Manual", 0, None, 1, "Game end", "This is standard counting method for each game which you can""t delete")
        counting_method_id_agricola_points = dbo.upsert_counting_method(-1, default_counting_method, game_id_agricola, "checkbox-marked-circle-outline", "cooperation", "lowest", "down", "rounds", "undefined", "Manual", 0, "", 1, "Game end", "This is standard counting method for each game which you can''t delete")
        counting_method_id_agricola_categories = dbo.upsert_counting_method(-1, "Points and categories at the game end", game_id_agricola, "checkbox-blank-circle-outline", "rivalisation", "highest", "up", "end", "defined", "Manual", 0, "", 1, "Game end", "")
        #game_color
        dbo.insert_game_color(-1,"pink", counting_method_id_agricola_points)
        dbo.insert_game_color(-1,"blue", counting_method_id_agricola_points)
        dbo.insert_game_color(-1,"green", counting_method_id_agricola_points)
        dbo.insert_game_color(-1,"amber", counting_method_id_agricola_points)
        dbo.insert_game_color(-1,"pink", counting_method_id_agricola_categories)
        dbo.insert_game_color(-1,"blue", counting_method_id_agricola_categories)
        dbo.insert_game_color(-1,"green", counting_method_id_agricola_categories)
        dbo.insert_game_color(-1,"amber", counting_method_id_agricola_categories)
        #category
        dbo.upsert_category(-1,"Points", counting_method_id_agricola_points, 1)
        dbo.upsert_category(-1,"Field Tiles", counting_method_id_agricola_categories, 1)
        dbo.upsert_category(-1,"Pastures", counting_method_id_agricola_categories, 2)
        dbo.upsert_category(-1,"Grain", counting_method_id_agricola_categories, 3)
        dbo.upsert_category(-1,"Vegetables", counting_method_id_agricola_categories, 4)
        dbo.upsert_category(-1,"Sheep", counting_method_id_agricola_categories, 5)
        dbo.upsert_category(-1,"Wild Boars", counting_method_id_agricola_categories, 6)
        dbo.upsert_category(-1,"Cows", counting_method_id_agricola_categories, 7)
        dbo.upsert_category(-1,"Unused Farmyard Spaces", counting_method_id_agricola_categories, 8)
        dbo.upsert_category(-1,"Fenced Stables", counting_method_id_agricola_categories, 9)
        dbo.upsert_category(-1,"Clay Rooms", counting_method_id_agricola_categories, 10)
        dbo.upsert_category(-1,"Stone Rooms", counting_method_id_agricola_categories, 11)
        dbo.upsert_category(-1,"People", counting_method_id_agricola_categories, 12)
        dbo.upsert_category(-1,"Points for Cards", counting_method_id_agricola_categories, 13)
        dbo.upsert_category(-1,"Bonus Points", counting_method_id_agricola_categories, 14)
        
        ##### carcassonne #####
        #game
        game_id_carcassonne = dbo.upsert_game(-1, "Carcassonne", "star-outline", "Carcassonne.jpg")
        #counting_method
        #counting_method_id_carcassonne_points = dbo.upsert_counting_method(default_counting_method, game_id_carcassonne, "checkbox-marked-circle-outline", "rivalisation", "highest", "up", "rounds", "undefined", "Manual", 0, None, None, "Round", "")
        counting_method_id_carcassonne_points = dbo.upsert_counting_method(-1, default_counting_method, game_id_carcassonne, "checkbox-marked-circle-outline", "rivalisation", "highest", "up", "end", "defined", "Manual", 0, "", "", "Round", "")
        #game_color
        dbo.insert_game_color(-1,"black", counting_method_id_carcassonne_points)
        dbo.insert_game_color(-1,"red", counting_method_id_carcassonne_points)
        dbo.insert_game_color(-1,"blue", counting_method_id_carcassonne_points)
        dbo.insert_game_color(-1,"green", counting_method_id_carcassonne_points)
        dbo.insert_game_color(-1,"yellow", counting_method_id_carcassonne_points)
        dbo.insert_game_color(-1,"white", counting_method_id_carcassonne_points)
        #category
        dbo.upsert_category(-1,"Points", counting_method_id_carcassonne_points, 1)
        
        ##### sen #####
        #game
        game_id_sen = dbo.upsert_game(-1, "Sen", "star-outline", "Sen.jpg")
        #counting_method
        counting_method_id_sen_points = dbo.upsert_counting_method(-1, default_counting_method, game_id_sen, "checkbox-marked-circle-outline", "rivalisation", "lowest", "up", "rounds", "undefined", "Points", 0, 100, "", "Round", "")
        #category
        dbo.upsert_category(-1,"Points", counting_method_id_sen_points, 1)
