import mysql.connector
from settings import *

def parse_entries(entries):
    ret = []
    for e in entries:
        ret.append({
            "id": e[0],
            "amount": e[1],
            "description": e[2],
            "category": e[3],
            "type" : e[4]
            })
    return ret

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

    def insert_entry(self, amount, cat_id, type_id, description = ""):
        try:
            query = "INSERT INTO entries (amount, category_id, type_id, description) VALUES (%s, %s, %s, %s) "
            data = (amount, cat_id, type_id, description)
            self.cur.execute(query, data)
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
    
    def del_entry(self, id):
        try:
            query = "DELETE FROM entries WHERE id = %s"
            data = (id, )
            self.cur.execute(query, data)
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        
    def get_entries(self):
        try:
            query = "SELECT entries.id, entries.amount, entries.description, categorias.cat_name, types.type_name FROM entries JOIN categorias JOIN types WHERE entries.category_id = categorias.id AND entries.type_id = types.id"
            self.cur.execute(query)
            results = self.cur.fetchall()
            return parse_entries(results)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
    
    def get_entry(self, id):
        try:
            query = "SELECT entries.id, entries.amount, entries.description, categorias.cat_name, types.type_name FROM entries JOIN categorias JOIN types WHERE entries.category_id = categorias.id AND entries.type_id = types.id AND entries.id = %s"
            data = (id, )
            self.cur.execute(query, data)
            result = self.cur.fetchall()
            return parse_entries(result)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False