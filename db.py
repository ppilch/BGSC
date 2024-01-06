import sqlite3
import inspect

class DBOperations:
    def __init__(self):
        self.conn = sqlite3.connect('bgsc.db')
        self.cursor = self.conn.cursor()
        self.drop_all_objects()
        self.create_player_table()
        self.create_setting_table()
        self.create_game_table()
        self.create_counting_method_table()
        self.create_round_table()
        self.create_category_table()
        self.fake_data()
        
 
    ################
    ##### common #####
    ################        
                      
    def drop_all_objects(self):
        print(inspect.currentframe().f_code.co_name)
        self.cursor.execute("DROP TABLE IF EXISTS player")
        self.cursor.execute("DROP TABLE IF EXISTS game")
        self.cursor.execute("DROP TABLE IF EXISTS counting_method")
        self.cursor.execute("DROP TABLE IF EXISTS round")
        self.cursor.execute("DROP TABLE IF EXISTS category")
        self.cursor.execute("DROP TABLE IF EXISTS option")
                                            
    ################
    ##### player #####
    ################
            
    def create_player_table(self):
        print(inspect.currentframe().f_code.co_name)
        self.cursor.execute( "CREATE TABLE IF NOT EXISTS player "
                                            "( id INTEGER PRIMARY KEY AUTOINCREMENT"
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
                                            "is_deleted = 0 AND "
                                            f"(name LIKE '%{name}%' OR '{name}' = '-1') "
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
                                            "( id INTEGER PRIMARY KEY AUTOINCREMENT"
                                            ", name VARCHAR(50) NOT NULL"
                                            ", is_favorite BOOLEAN NOT NULL CHECK (is_favorite IN (0, 1))"
                                            ", is_deleted BOOLEAN NOT NULL CHECK (is_deleted IN (0, 1))"
                                            ")"
                                            )
        self.conn.commit()
    
    def insert_game(self, name, is_favorite):
        print(inspect.currentframe().f_code.co_name)
        self.cursor.execute( "INSERT INTO game "
                                            "(name, is_favorite, is_deleted)"
                                            "VALUES "
                                            f"('{name}', '{is_favorite}', 0)"
                                            )
        self.conn.commit()
        seq = self.cursor.execute(
                                            'SELECT seq '
                                            'FROM sqlite_sequence '
                                            'WHERE name="game" '
                                            ).fetchall()
        self.conn.commit()
        return seq
        
    ##### counting_method #####
    def create_counting_method_table(self):
        print(inspect.currentframe().f_code.co_name)
        self.cursor.execute( "CREATE TABLE IF NOT EXISTS counting_method "
                                            "( id INTEGER PRIMARY KEY AUTOINCREMENT"
                                            ", name VARCHAR(50) NOT NULL"
                                            ", game_id INTEGER"
                                            ", rivalisation_or_cooperation VARCHAR(50) NOT NULL"
                                            ", highest_or_lowest VARCHAR(50) NOT NULL"
                                            ", up_or_down VARCHAR(50) NOT NULL"
                                            ", end_or_rounds VARCHAR(50) NOT NULL"
                                            ", defined_or_undefined VARCHAR(50) NOT NULL"
                                            ", game_end_condition VARCHAR(50) NOT NULL"
                                            ", points_on_start INTEGER NOT NULL"
                                            ", score_ending_the_game INTEGER NULL"
                                            ", number_of_rounds VARCHAR(50) NOT NULL"
                                            ", round_name VARCHAR(50) NOT NULL"
                                            ", is_deleted BOOLEAN NOT NULL CHECK (is_deleted IN (0, 1))"
                                            ", FOREIGN KEY (game_id) REFERENCES game(id)"
                                            ")"
                                            )
        self.conn.commit()
        
    def insert_counting_method(self, name, game_id, rivalisation_or_cooperation, highest_or_lowest, up_or_down, end_or_rounds, defined_or_undefined, game_end_condition, points_on_start, score_ending_the_game, number_of_rounds, round_name):
        print(inspect.currentframe().f_code.co_name)
        self.cursor.execute( "INSERT INTO counting_method "
                                            "(name, game_id, rivalisation_or_cooperation, highest_or_lowest, up_or_down, end_or_rounds, defined_or_undefined, game_end_condition, points_on_start, score_ending_the_game, number_of_rounds, round_name, is_deleted)"
                                            "VALUES "
                                            f"('{name}', '{game_id}', '{rivalisation_or_cooperation}', '{highest_or_lowest}', '{up_or_down}', '{end_or_rounds}', '{defined_or_undefined}', '{game_end_condition}', '{points_on_start}', '{score_ending_the_game}', '{number_of_rounds}', '{round_name}', 0)"
                                            )
        self.conn.commit()
        seq = self.cursor.execute(
                                            'SELECT seq '
                                            'FROM sqlite_sequence '
                                            'WHERE name="game" '
                                            ).fetchall()
        self.conn.commit()
        return seq
        
    ##### round #####
    def create_round_table(self):
        print(inspect.currentframe().f_code.co_name)
        self.cursor.execute( "CREATE TABLE IF NOT EXISTS round "
                                            "( id INTEGER PRIMARY KEY AUTOINCREMENT"
                                            ", name VARCHAR(50) NOT NULL"
                                            ", order_no INTEGER"
                                            ", counting_method_id INTEGER"
                                            ", is_deleted BOOLEAN NOT NULL CHECK (is_deleted IN (0, 1))"
                                            ", FOREIGN KEY (counting_method_id) REFERENCES counting_method(id)"
                                            ")"
                                            )
        self.conn.commit()
        
    ##### category #####
    def create_category_table(self):
        print(inspect.currentframe().f_code.co_name)
        self.cursor.execute( "CREATE TABLE IF NOT EXISTS category "
                                            "( id INTEGER PRIMARY KEY AUTOINCREMENT"
                                            ", name VARCHAR(50) NOT NULL"
                                            ", order_no INTEGER"
                                            ", counting_method_id INTEGER"
                                            ", is_deleted BOOLEAN NOT NULL CHECK (is_deleted IN (0, 1))"
                                            ", FOREIGN KEY (counting_method_id) REFERENCES counting_method(id)"
                                            ")"
                                            )
        self.conn.commit()
        
    ################
    ##### setting #####
    ################

    def create_setting_table(self):
        print(inspect.currentframe().f_code.co_name)
        self.cursor.execute( "CREATE TABLE IF NOT EXISTS setting "
                                            "( id INTEGER PRIMARY KEY AUTOINCREMENT"
                                            ", name VARCHAR(50) NOT NULL"
                                            ", value VARCHAR(50) NOT NULL"
                                            "); "
                                            )
        self.cursor.execute( 
                                            "INSERT INTO setting "
                                            "(name, value)"
                                            "VALUES "
                                            " ('darkmode', 'Light')"
                                            ",('default counting mode', 'Points at the game end')"
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
        return settings
        
    def fake_data(self):
        print(inspect.currentframe().f_code.co_name)
        #players
        self.insert_player("Paweł", "alpha-p-circle", [121/255, 85/255, 72/255, 1])
        self.insert_player("Kornelia", "alpha-k-circle", [244/255, 67/255, 54/255, 1])
        self.insert_player("Natan", "alpha-n-circle", [63/255, 81/255, 181/255, 1])
        self.insert_player("Estera","alpha-e-circle", [233/255, 30/255, 99/255, 1])
        self.insert_player("Tobiasz","alpha-t-circle", [205/255, 220/255, 57/255, 1])
        #games
        game_id_agricola = self.insert_game("Agricola", 1)
        game_id_kosci = self.insert_game("Kości", 0)
        game_id_sen = self.insert_game("Sen", 0)
        #counting_method
        #self.insert_counting_method()
        
        