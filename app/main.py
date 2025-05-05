from functools import wraps
from fastapi import FastAPI, Header, HTTPException, Response, Request, Body
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse, PlainTextResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import WebApplicationClient
from pydantic import BaseModel
from settings import *
from dotenv import load_dotenv
import random
import os
import string
import traceback
import requests
import database


app = FastAPI()
templates =  Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Entry(BaseModel):
    desc: str
    amount: float
    cat: int
    type: int

load_dotenv()

_db = database.Database()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
client = WebApplicationClient(CLIENT_ID)
scope = ["openid", "profile", "email"]
oauth = OAuth2Session(client=client, redirect_uri=CALLBACK_URL, scope=scope)


def generate_state():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

def auth_required(func):
    @wraps(func)
    def wrapper(*args, request: Request, **kwargs):
        token = request.cookies.get("auth_token")
        if not token or not _db.validate_token(token):
            raise HTTPException(status_code=401, detail="Unauthorized")
        return func(*args, request=request, **kwargs)
    return wrapper


@app.get("/")
def read_root(request: Request):
    if request.cookies.get("auth_token") is None:
        return templates.TemplateResponse("index-loggedout.html", {"request": request})
    else:
        return RedirectResponse(url="/api/index")

@app.get("/api/login")
def login():
    state = generate_state()
    auth_url, state_generated = oauth.authorization_url(AUTH_BASE_URL, state=state)
    response = RedirectResponse(url=auth_url)
    response.set_cookie(key="oauth_state", value=state, httponly=True)
    return response

@app.get("/api/callback")
def callback(request: Request, code: str, state: str):
    try:
        stored_state = request.cookies.get("oauth_state")
        if state != stored_state:
            raise HTTPException(status_code=400, detail="CSRF error: state does not match.")
        
        client = WebApplicationClient(CLIENT_ID)
        oauth = OAuth2Session(client=client, redirect_uri=CALLBACK_URL, state=state)

        token = oauth.fetch_token(
            TOKEN_URL, 
            client_secret=CLIENT_SECRET, 
            authorization_response=str(request.url)
        )

        access_token = token.get("access_token")
        if not access_token:
            raise HTTPException(status_code=400, detail="No access token in response.")

        userinfo_response = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
        if not userinfo_response.ok:
            raise HTTPException(status_code=400, detail="Failed to fetch user info.")

        user_info = userinfo_response.json()
        email = user_info.get("email")
        name = user_info.get("name")

        if not _db.save_token(email=email, name=name, token=access_token):
            raise HTTPException(status_code=500, detail="Failed to save user.")

        response = RedirectResponse(url="/")
        response.set_cookie(key="auth_token", value=access_token, httponly=True)
        response.delete_cookie("oauth_state")
        return response
    except Exception as e:
        tb = traceback.format_exc()
        return PlainTextResponse(f"Erro no callback: \n{tb}")

@app.get("/index")
@auth_required
def index(request: Request):
    token = request.cookies.get("auth_token")
    return templates.TemplateResponse("index.html", {"request": request, "user": _db.get_username(token)})

@app.get("/entries")
@auth_required
def entries(request: Request):
    token = request.cookies.get("auth_token")
    return templates.TemplateResponse("entries.html", {"request": request, "entradas": _db.get_entries(token), "categorias": _db.get_categorias(), "types": _db.get_types()})

@app.post("/api/entry")
@auth_required
def add_entry(request: Request, entry: Entry):
    amount = entry.amount
    cat = entry.cat
    desc = entry.desc
    type = entry.type
    ret = _db.insert_entry(amount=amount, cat_id=cat, description=desc, type_id=type, token=request.cookies.get("auth_token"))
    return "Ok" if ret else "Error"

@app.delete("/api/entry/{id}")
@auth_required
def del_entry(request: Request, id: int):
    ret = _db.del_entry(id)
    return "Ok" if ret else "Error"

@app.put("/api/entry/{id}")
@auth_required
def edit_entry(request: Request, id: int, entry: Entry):
    ret = _db.edit_entry(id, entry)
    return "Ok" if ret else "Error" 

@app.get("/api/entry")
@auth_required
def get_all_entries(request: Request):
    return _db.get_entries(request.cookies.get("auth_token"))

@app.get("/api/entry/{id}")
@auth_required
def get_entry(request: Request, id: int):
    return _db.get_entry(id, request.cookies.get("auth_token"))

@app.get("/api/type")
@auth_required
def get_type(request: Request):
    return _db.get_types()

@app.get("/api/type/{id}")
@auth_required
def get_type(request: Request, id: int):
    return _db.get_type(id)

@app.post("/api/type")
@auth_required
def insert_type(request: Request, name: str):
    return _db.insert_type(name)

@app.delete("/api/type/{id}")
@auth_required
def del_type(request: Request, id: int):
    return _db.del_type(id)

@app.get("/api/cat")
@auth_required
def get_cat(request: Request):
    return _db.get_categorias()

@app.get("/api/cat/{id}")
@auth_required
def get_cat(request: Request, id: int):
    return _db.get_categoria(id)

@app.post("/api/cat")
@auth_required
def insert_cat(request: Request, name: str):
    return _db.insert_cat(name)

@app.delete("/api/cat/{id}")
@auth_required
def del_cat(request: Request, id: int):
    return _db.del_cat(id)