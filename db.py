import sqlite3
import inspect

class DBOperations:
    def __init__(self):
        self.conn = sqlite3.connect('bgsc.db')
        self.cursor = self.conn.cursor()
        
    def create_all_objects(self):
        print(inspect.currentframe().f_code.co_name)
        self.create_player_table()
        self.create_game_table()
        self.create_counting_method_table()
        self.create_game_color_table()
        self.create_category_table()
        self.create_setting_table()
        
    ################
    ##### common #####
    ################        
                      
    def drop_all_objects(self):
        print(inspect.currentframe().f_code.co_name)
        self.cursor.execute("DROP TABLE IF EXISTS player")
        self.cursor.execute("DROP TABLE IF EXISTS game")
        self.cursor.execute("DROP TABLE IF EXISTS counting_method")
        self.cursor.execute("DROP TABLE IF EXISTS round")
        self.cursor.execute("DROP TABLE IF EXISTS game_color")
        self.cursor.execute("DROP TABLE IF EXISTS category")
        self.cursor.execute("DROP TABLE IF EXISTS option")
        self.cursor.execute("DROP TABLE IF EXISTS setting")
                                            
    ################
    ##### player #####
    ################
            
    def create_player_table(self):
        print(inspect.currentframe().f_code.co_name)
        self.cursor.execute( "CREATE TABLE IF NOT EXISTS player "
                                            "( id INTEGER PRIMARY KEY"
                                            ", name VARCHAR(50) NOT NULL"
                                            ", avatar VARCHAR(255)"
                                            ", color_r INTEGER"
                                            ", color_g INTEGER"
                                            ", color_b INTEGER"
                                            ", color_t INTEGER"
                                            ", is_deleted BOOLEAN NOT NULL CHECK (is_deleted IN (0, 1))"
                                            ")"
                                            )
        self.conn.commit()
        
    def insert_player(self, name, avatar, color_list):
        print(inspect.currentframe().f_code.co_name)
        color_r = color_list[0] * 255
        color_g = color_list[1] * 255
        color_b = color_list[2] * 255
        color_t = color_list[3]
        self.cursor.execute( "INSERT INTO player "
                                            "(name, avatar, color_r, color_g, color_b, color_t, is_deleted)"
                                            "VALUES "
                                            f"('{name}', '{avatar}', {color_r}, {color_g}, {color_b}, {color_t}, 0)"
                                            )
        self.conn.commit()
        seq = self.cursor.execute(
                                            'SELECT seq '
                                            'FROM sqlite_sequence '
                                            'WHERE name="player" '
                                            ).fetchall()
        self.conn.commit()
        return seq
        
    def update_player(self, id, name, avatar, color_list):
        print(inspect.currentframe().f_code.co_name)
        color_r = color_list[0] * 255
        color_g = color_list[1] * 255
        color_b = color_list[2] * 255
        color_t = color_list[3]
        self.cursor.execute( "UPDATE player "
                                            "SET "
                                            f"name = '{name}'"
                                            f", avatar = '{avatar}'"
                                            f", color_r = {color_r}"
                                            f", color_g = {color_g}"
                                            f", color_b = {color_b}"
                                            f", color_t = {color_t} "
                                            "WHERE "
                                            f"id = {id}"
                                            )
        self.conn.commit()
        
    def delete_player_soft(self, id):
        print(inspect.currentframe().f_code.co_name)
        self.cursor.execute( "UPDATE player "
                                            "SET "
                                            f"is_deleted = 1 "
                                            "WHERE "
                                            f"id = {id}"
                                            )
        self.conn.commit()
        
    def get_player(self, id, name, order_col, order_dir):
        print(inspect.currentframe().f_code.co_name)
        players = self.cursor.execute(
                                            "SELECT "
                                            "id, name, avatar, color_r, color_g, color_b, color_t, is_deleted "
                                            "FROM "
                                            "player "
                                            "WHERE "
                                            f"(id = {id} OR {id} = -1) AND "
                                            f"(name LIKE '%{name}%' OR '{name}' = '-1') AND "
                                            "is_deleted = 0 "
                                            f"ORDER BY {order_col} {order_dir}"
                                            ).fetchall()
        self.conn.commit()
        return players

    ################
    ##### game #####
    ################

    ##### game #####
    def create_game_table(self):
        print(inspect.currentframe().f_code.co_name)
        self.cursor.execute( "CREATE TABLE IF NOT EXISTS game "
                                            "( id INTEGER PRIMARY KEY "
                                            ", name VARCHAR(50) NOT NULL"
                                            ", favorite_icon VARCHAR(50) NOT NULL"
                                            ", image_name VARCHAR(55) NULL"
                                            ", is_deleted BOOLEAN NOT NULL CHECK (is_deleted IN (0, 1))"
                                            ")"
                                            )
        self.conn.commit()
    
    def insert_game(self, name, favorite_icon, image_name = None):
        print(inspect.currentframe().f_code.co_name)
        if image_name == None:
            image_name = name + ".jpg"
        self.cursor.execute( "INSERT INTO game "
                                            "(name, favorite_icon, image_name, is_deleted)"
                                            "VALUES "
                                            f"('{name}', '{favorite_icon}', '{image_name}', 0)"
                                            )
        self.conn.commit()
        seq = self.cursor.execute(
                                            'SELECT seq '
                                            'FROM sqlite_sequence '
                                            'WHERE name="game" '
                                            ).fetchall()
        self.conn.commit()
        return seq
        
    def upsert_game(self, game_id, name, favorite_icon, image_name = None):
        print(inspect.currentframe().f_code.co_name)
        if game_id == -1:
            game_id_final = self.cursor.execute(
                                                "SELECT IFNULL(max(id),0) + 1 "
                                                "FROM game "
                                                ).fetchall()
            self.conn.commit()
            game_id_final = game_id_final[0][0]
        else:
            game_id_final = game_id
        self.cursor.execute( "INSERT INTO game "
                                            "(id, name, favorite_icon, image_name, is_deleted)"
                                            "VALUES "
                                            f"({game_id_final}, '{name}', '{favorite_icon}', '{image_name}', 0)"
                                            "ON CONFLICT (id) "
                                            "DO UPDATE SET "
                                            f"  name = '{name}' "
                                            f", favorite_icon = '{favorite_icon}' "
                                            #f", image_name = '{image_name}' "
                                            )
        self.conn.commit()
        return game_id_final
        
    def delete_game_soft(self, game_id):
        print(inspect.currentframe().f_code.co_name)
        self.cursor.execute(
                                            "UPDATE game "
                                            "SET is_deleted = 1 "
                                            f"WHERE id = {game_id} "
                                            )
        self.conn.commit()
        
    def get_game(self, game_id, name, favorite_icon, order_col, order_dir):
        print(inspect.currentframe().f_code.co_name)
        games = self.cursor.execute(
                                            "SELECT "
                                            "id, name, favorite_icon, image_name, is_deleted "
                                            "FROM "
                                            "game "
                                            "WHERE "
                                            f"(id = {game_id} OR {game_id} = -1) AND "
                                            f"(name LIKE '%{name}%' OR '{name}' = '-1') AND "
                                            f"(favorite_icon = '{favorite_icon}' OR '{favorite_icon}' = '-1') AND "
                                            "is_deleted = 0 "
                                            f"ORDER BY {order_col} {order_dir}"
                                            ).fetchall()
        self.conn.commit()
        return games

    ##### counting_method #####
    def create_counting_method_table(self):
        print(inspect.currentframe().f_code.co_name)
        self.cursor.execute( "CREATE TABLE IF NOT EXISTS counting_method "
                                            "( id INTEGER PRIMARY KEY"
                                            ", name VARCHAR(50) NOT NULL"
                                            ", game_id INTEGER"
                                            ", default_icon BOOLEAN NOT NULL"
                                            ", rivalisation_or_cooperation VARCHAR(50) NOT NULL CHECK (rivalisation_or_cooperation IN ('rivalisation', 'cooperation')) "
                                            ", highest_or_lowest VARCHAR(50) NOT NULL CHECK (highest_or_lowest IN ('highest', 'lowest')) "
                                            ", up_or_down VARCHAR(50) NOT NULL CHECK (up_or_down IN ('up', 'down')) "
                                            ", end_or_rounds VARCHAR(50) NOT NULL CHECK (end_or_rounds IN ('end', 'rounds')) "
                                            ", defined_or_undefined VARCHAR(50) NOT NULL CHECK (defined_or_undefined IN ('defined', 'undefined')) "
                                            ", game_end_condition VARCHAR(50) NOT NULL CHECK (game_end_condition IN ('Manual', 'Rounds', 'Points', 'Rounds or Points', 'Time')) "
                                            ", points_on_start INTEGER NOT NULL"
                                            ", score_ending_the_game INTEGER NULL"
                                            ", number_of_rounds VARCHAR(50) NULL"
                                            ", round_name VARCHAR(50) NOT NULL"
                                            ", notes VARCHAR(1000) NULL"
                                            ", is_deleted BOOLEAN NOT NULL CHECK (is_deleted IN (0, 1))"
                                            ", FOREIGN KEY (game_id) REFERENCES game(id)"
                                            ")"
                                            )
        self.conn.commit()
        
    def upsert_counting_method(self, counting_method_id, name, game_id, default_icon, rivalisation_or_cooperation, highest_or_lowest, up_or_down, end_or_rounds, defined_or_undefined, game_end_condition, points_on_start, score_ending_the_game, number_of_rounds, round_name, notes):
        print(inspect.currentframe().f_code.co_name)
        if counting_method_id == -1:
            counting_method_id_final = self.cursor.execute(
                                                "SELECT IFNULL(max(id),0) + 1 "
                                                "FROM counting_method "
                                                ).fetchall()
            self.conn.commit()
            counting_method_id_final = counting_method_id_final[0][0]
        else:
            counting_method_id_final = counting_method_id
        if default_icon == "checkbox-marked-circle-outline":
            self.cursor.execute( "UPDATE counting_method "
                                                "SET default_icon = 'checkbox-blank-circle-outline' "
                                                f"WHERE game_id = {game_id} "
                                              )
            self.conn.commit()
        self.cursor.execute( "INSERT INTO counting_method "
                                            "(id, name, game_id, default_icon, rivalisation_or_cooperation, highest_or_lowest, up_or_down, end_or_rounds, defined_or_undefined, game_end_condition, points_on_start, score_ending_the_game, number_of_rounds, round_name, notes, is_deleted) "
                                            "VALUES "
                                            f"({counting_method_id_final}, '{name}', '{game_id}', '{default_icon}', '{rivalisation_or_cooperation}', '{highest_or_lowest}', '{up_or_down}', '{end_or_rounds}', '{defined_or_undefined}', '{game_end_condition}', '{points_on_start}', '{score_ending_the_game}', '{number_of_rounds}', '{round_name}', '{notes}', 0) "
                                            "ON CONFLICT (id) "
                                            "DO UPDATE SET "
                                            f"  name = '{name}' "
                                            f", game_id = '{game_id}' "
                                            f", default_icon = '{default_icon}' "
                                            f", rivalisation_or_cooperation = '{rivalisation_or_cooperation}' "
                                            f", highest_or_lowest = '{highest_or_lowest}' "
                                            f", up_or_down = '{up_or_down}' "
                                            f", end_or_rounds = '{end_or_rounds}' "
                                            f", defined_or_undefined = '{defined_or_undefined}' "
                                            f", game_end_condition = '{game_end_condition}' "
                                            f", points_on_start = '{points_on_start}' "
                                            f", score_ending_the_game = '{score_ending_the_game}' "
                                            f", number_of_rounds = '{number_of_rounds}' "
                                            f", round_name = '{round_name}' "
                                            f", notes = '{notes}' "
                                            )
        self.conn.commit()
        return counting_method_id_final
        
    def delete_counting_method_soft(self, counting_method_id):
        print(inspect.currentframe().f_code.co_name)
        self.cursor.execute(
                                            "UPDATE category "
                                            "SET is_deleted = 1 "
                                            f"WHERE counting_method_id = {counting_method_id} "
                                            )
        self.conn.commit()
        self.cursor.execute(
                                            "UPDATE game_color "
                                            "SET is_deleted = 1 "
                                            f"WHERE counting_method_id = {counting_method_id} "
                                            )
        self.conn.commit()
        self.cursor.execute(
                                            "UPDATE counting_method "
                                            "SET is_deleted = 1 "
                                            f"WHERE id = {counting_method_id} "
                                            )
        self.conn.commit()
        
    def get_counting_method(self, counting_method_id, name, game_id, default_only, order_col, order_dir):
        print(inspect.currentframe().f_code.co_name)
        if default_only == 1:
            # Find the default row but in theory there may by none or multiple default_icon = 1
            most_likely_default_id = self.cursor.execute(
                                            "SELECT id "
                                            "FROM counting_method "
                                            f"WHERE game_id = {game_id} AND "
                                            "is_deleted = 0 "
                                            "ORDER BY CASE default_icon WHEN 'checkbox-marked-circle-outline' THEN 1 ELSE 0 END DESC, id DESC "
                                            "LIMIT 1 "
                                            ).fetchall()
            self.conn.commit()
            counting_method_id = most_likely_default_id[0][0]
        counting_methods = self.cursor.execute(
                                            "SELECT "
                                            "id, name, game_id, default_icon, rivalisation_or_cooperation, highest_or_lowest, up_or_down, end_or_rounds, defined_or_undefined, game_end_condition, points_on_start, score_ending_the_game, number_of_rounds, round_name, notes, is_deleted "
                                            "FROM "
                                            "counting_method "
                                            "WHERE "
                                            f"(id = {counting_method_id} OR {counting_method_id} = -1) AND "
                                            f"(name LIKE '%{name}%' OR '{name}' = '-1') AND "
                                            f"(game_id = {game_id} OR {game_id} = -1) AND "
                                            "is_deleted = 0 "
                                            f"ORDER BY {order_col} {order_dir}"
                                            ).fetchall()
        self.conn.commit()
        return counting_methods
    
    def get_counting_method_number(self, game_id):
        print(inspect.currentframe().f_code.co_name)
        counting_methods_number = self.cursor.execute(
                                            "SELECT "
                                            "COUNT(*) "
                                            "FROM "
                                            "counting_method "
                                            "WHERE "
                                            f"(game_id = {game_id} OR {game_id} = -1) AND "
                                            "is_deleted = 0 "
                                            ).fetchall()
        self.conn.commit()
        return int(counting_methods_number[0][0])
        
    ##### category #####
    def create_category_table(self):
        print(inspect.currentframe().f_code.co_name)
        self.cursor.execute( "CREATE TABLE IF NOT EXISTS category"
                                            "( id INTEGER PRIMARY KEY"
                                            ", name VARCHAR(50) NOT NULL"
                                            ", order_no INTEGER"
                                            ", counting_method_id INTEGER"
                                            ", is_deleted BOOLEAN NOT NULL CHECK (is_deleted IN (0, 1))"
                                            ", FOREIGN KEY (counting_method_id) REFERENCES counting_method(id)"
                                            ")"
                                            )
        self.conn.commit()
    
    def upsert_category(self, category_id, name, counting_method_id, order_no):
        print(inspect.currentframe().f_code.co_name)
        if category_id == -1:
            category_id_final = self.cursor.execute(
                                                "SELECT IFNULL(max(id),0) + 1 "
                                                "FROM category "
                                                ).fetchall()
            self.conn.commit()
            category_id_final = category_id_final[0][0]
        else:
            category_id_final = category_id
        self.cursor.execute( "INSERT INTO category "
                                            "(id, name, counting_method_id, order_no, is_deleted)"
                                            "VALUES "
                                            f"('{category_id_final}', '{name}', '{counting_method_id}', '{order_no}', 0)"
                                            "ON CONFLICT (id) "
                                            "DO UPDATE SET "
                                            f"  name = '{name}' "
                                            f", counting_method_id = '{counting_method_id}' "
                                            f", order_no = '{order_no}' "
                                            )
        self.conn.commit()
        return category_id_final
        
    def get_category(self, category_id, counting_method_id, is_deleted, order_col, order_dir):
        print(inspect.currentframe().f_code.co_name)
        categories = self.cursor.execute(
                                            "SELECT "
                                            "id, name, order_no, counting_method_id, is_deleted "
                                            "FROM "
                                            "category "
                                            "WHERE "
                                            f"(id = {category_id} OR {category_id} = -1) AND "
                                            f"(counting_method_id = {counting_method_id} OR {counting_method_id} = -1) AND "
                                            f"(is_deleted = {is_deleted} OR {is_deleted} = -1)"
                                            f"ORDER BY {order_col} {order_dir}"
                                            ).fetchall()
        self.conn.commit()
        return categories

    def delete_category(self, category_id):
        print(inspect.currentframe().f_code.co_name)
        self.cursor.execute(
                                            "UPDATE "
                                            "category "
                                            "SET "
                                            "is_deleted = 1 "
                                            f"WHERE id = {category_id} "
                                            # TODO: hard delete if category was not used yet in historical games
                                            )
        self.conn.commit()
        
    #add new, delete removed, category list has all caregory classes for given counting_method_id
    def merge_category_list(self, counting_method_id, category_list):
        print(inspect.currentframe().f_code.co_name)
        category_ids_db = []
        for cat in self.get_category(-1, counting_method_id, -1, "id", "ASC"):
            category_ids_db.append(cat[0])
        category_ids_app = []
        for cat in category_list:
            category_ids_app.append(cat.category_id)
        print(">category_ids_db")
        print(category_ids_db)
        print(">category_list")
        print(" ".join(str(x.name)+"_"+str(x.counting_method_id) for x in category_list))
        for cat in category_list:
            self.upsert_category(cat.category_id, cat.name, counting_method_id, cat.order_no)
        for cat_id in category_ids_db:
            if cat_id not in category_ids_app and cat_id >= 1:
                self.delete_category(cat_id)
        
    ##### game_color #####
    def create_game_color_table(self):
        print(inspect.currentframe().f_code.co_name)
        self.cursor.execute( "CREATE TABLE IF NOT EXISTS game_color "
                                            "( id INTEGER PRIMARY KEY"
                                            ", color_name VARCHAR(50) NOT NULL"
                                            ", counting_method_id INTEGER"
                                            ", is_deleted BOOLEAN NOT NULL CHECK (is_deleted IN (0, 1))"
                                            ", FOREIGN KEY (counting_method_id) REFERENCES counting_method(id)"
                                            ")"
                                            )
        self.conn.commit()
    
    def insert_game_color(self, color_id, color_name, counting_method_id):
        print(inspect.currentframe().f_code.co_name)
        if color_id == -1:
            self.cursor.execute( "INSERT INTO game_color "
                                                "(color_name, counting_method_id, is_deleted)"
                                                "VALUES "
                                                f"('{color_name}', '{counting_method_id}', 0)"
                                                )
            self.conn.commit()
            seq = self.cursor.execute(
                                                'SELECT seq '
                                                'FROM sqlite_sequence '
                                                'WHERE name="game_color" '
                                                ).fetchall()
            self.conn.commit()
            return seq
        
    def get_game_color(self, game_color_id, counting_method_id, order_col, order_dir):
        print(inspect.currentframe().f_code.co_name)
        colors = self.cursor.execute(
                                            "SELECT "
                                            "id, color_name, counting_method_id, is_deleted "
                                            "FROM "
                                            "game_color "
                                            "WHERE "
                                            f"(id = {game_color_id} OR {game_color_id} = -1) AND "
                                            f"(counting_method_id = '{counting_method_id}' OR '{counting_method_id}' = -1) AND "
                                            "is_deleted = 0 "
                                            f"ORDER BY {order_col} {order_dir}"
                                            ).fetchall()
        self.conn.commit()
        return colors

    def merge_game_colors(self, counting_method_id, colors_list):
        print(inspect.currentframe().f_code.co_name)
        self.cursor.execute(
                                            "DELETE FROM "
                                            "game_color "
                                            "WHERE "
                                            f"counting_method_id = '{counting_method_id}' "
                                            )
        self.conn.commit()
        for color in colors_list:
            self.insert_game_color(-1, color, counting_method_id)
        
    ################
    ##### setting #####
    ################

    def create_setting_table(self):
        print(inspect.currentframe().f_code.co_name)
        self.cursor.execute( "CREATE TABLE IF NOT EXISTS setting "
                                            "( id INTEGER PRIMARY KEY"
                                            ", name VARCHAR(50) NOT NULL"
                                            ", value VARCHAR(50) NOT NULL"
                                            "); "
                                            )
        self.cursor.execute( 
                                            "INSERT INTO setting "
                                            "(name, value)"
                                            "VALUES "
                                            " ('darkmode', 'Dark')"
                                            ",('default_counting_method', 'Points at the end of the game')"
                                            )
        self.conn.commit()        
        
        
    def update_setting(self, name, value):
        print(inspect.currentframe().f_code.co_name)
        self.cursor.execute( "UPDATE setting "
                                            "SET "
                                            f"value = '{value}' "
                                            "WHERE "
                                            f"name = '{name}' "
                                            )
        self.conn.commit()

    def get_setting(self, name):
        print(inspect.currentframe().f_code.co_name)
        settings = self.cursor.execute(
                                            "SELECT "
                                            "value "
                                            "FROM "
                                            "setting "
                                            "WHERE "
                                            f"(name = '{name}' or '{name}' = '-1') "
                                            ).fetchall()
        self.conn.commit()
        return settings[0][0]
