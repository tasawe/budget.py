from typing import Union
from fastapi import FastAPI
import database
app = FastAPI()

_db = database.Database()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/add_entry")
def add_entry(amount: float, cat: int, desc: str):
    ret = _db.insert_entry(amount=amount, cat_id=cat, description=desc)
    return "Ok" if ret else "Error"