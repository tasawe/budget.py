import mysql.connector
from settings import *

class Database():
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = "localhost",
            user = MYSQL_USER,
            passwd = MYSQL_PWD,
            database = MYSQL_DB
        )
        self.cur = self.conn.cursor()
    
    def close(self):
        self.conn.close()

    def insert_entry(self, amount, cat_id, description = ""):
        try:
            query = "INSERT INTO entries (amount, category_id, description) VALUES (%s, %s, %s) "
            data = (amount, cat_id, description)
            self.cur.execute(query, data)
            self.conn.commit()
            print("Ok")
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False