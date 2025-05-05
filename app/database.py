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

def parse_enum(list, enum_type):
    ret = []
    enums = {
        "cat": "cat_name",
        "type": "type_name"
    }
    for e in list:
        ret.append({
            "id": e[0],
            enums[enum_type]: e[1]
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
    
    def get_categorias(self):
        try:
            query = "SELECT id, cat_name FROM categorias"
            self.cur.execute(query)
            results = self.cur.fetchall()
            return parse_enum(results, "cat")

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
    
    def get_types(self):
        try:
            query = "SELECT id, type_name FROM types"
            self.cur.execute(query)
            results = self.cur.fetchall()
            return parse_enum(results, "type")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
    
    def insert_type(self, name):
        try:
            query = "INSERT INTO types (type_name) VALUES (%s)"
            data = (name, )
            self.cur.execute(query, data)
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
    
    def insert_cat(self, name):
        try:
            query = "INSERT INTO categorias (cat_name) VALUES (%s)"
            data = (name, )
            self.cur.execute(query, data)
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False