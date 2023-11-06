import sqlite3

class DBOperations:
    def __init__(self):
        self.conn = sqlite3.connect('bgsc.db')
        self.cursor = self.conn.cursor()
        self.create_player_table()
        
    def create_player_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Player(id integer PRIMARY KEY AUTOINCREMENT, name varchar(50) NOT NULL, icon varchar(50), is_deleted BOOLEAN NOT NULL CHECK (completed IN (0, 1)))")
        self.con.commit()
        
        