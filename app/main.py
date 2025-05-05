from typing import Union
from fastapi import FastAPI
import database
app = FastAPI()

_db = database.Database()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/entry")
def add_entry(amount: float, cat: int, type: int, desc: str):
    ret = _db.insert_entry(amount=amount, cat_id=cat, description=desc, type_id=type)
    return "Ok" if ret else "Error"

@app.delete("/entry/{id}")
def del_entry(id: int):
    ret = _db.del_entry(id)
    return "Ok" if ret else "Error"

@app.get("/entry")
def get_all_entries():
    return _db.get_entries()

@app.get("/entry/{id}")
def get_entry(id: int):
    return _db.get_entry(id)

@app.get("/type")
def get_type():
    return _db.get_types()

@app.get("/type/{id}")
def get_type(id: int):
    return _db.get_type(id)

@app.post("/type")
def insert_type(name: str):
    return _db.insert_type(name)

@app.delete("/type/{id}")
def del_type(id: int):
    return _db.del_type(id)

@app.get("/cat")
def get_cat():
    return _db.get_categorias()

@app.get("/cat/{id}")
def get_cat(id: int):
    return _db.get_categoria(id)

@app.post("/cat")
def insert_cat(name: str):
    return _db.insert_cat(name)

@app.delete("/cat/{id}")
def del_cat(id: int):
    return _db.del_cat(id)