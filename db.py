import sqlite3
import inspect

class DBOperations:
    def __init__(self):
        self.conn = sqlite3.connect('bgsc.db')
        self.cursor = self.conn.cursor()
        #self.drop_all_objects()
        self.create_player_table()
        self.create_setting_table()
 
    ################
    ##### common #####
    ################        
                      
    def drop_all_objects(self):
        print(inspect.currentframe().f_code.co_name)
        self.cursor.execute("DROP TABLE IF EXISTS player")
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
        #print(sqlite3.version)
        #print(sqlite3.sqlite_version)
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
                                            "('darkmode', 'Light')"
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
                        
                
        
#dbo = DBOperations()
#dbo.insert_player("Pawel", "alpha-p-circle", [0, 0, 0, 1])
