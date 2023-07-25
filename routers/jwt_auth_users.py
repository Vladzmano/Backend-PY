## OAUTH2 JWT ##

from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "c48a7375ab8aa13601e7657a5597b0ae6bae17929efd7feeb03a43b6242ccba7937ffced09dc4cf30ec43efa342019c1b7a248a08ffe256ce46bb78c1f88e810"

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str

users_db = {
    "VladM": {
        "username": "VladM",
        "name": "Vlad mano",
        "email": "test@test.com",
        "disabled": False,
        "password" : "$2a$12$r6U4mv3iz9NaJBV667a30OxHNKK7Wiqm29tjU9.BBokyc2sUVI8Eu"
        },

    "VLZM":{
        "username": "VLZM",
        "name": "mano",
        "email": "test@test.com",
        "disabled": True,
        "password" : "$2a$12$b5nLuMUkVhLZDJXEQomnaezMTr/vL8db6Q74B.LsNWnz37IbfVdbC"
        }
    }

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):

    exeption = HTTPException(
            status_code =status.HTTP_401_UNAUTHORIZED, 
            detail= "Credenciales de autenticacion invalidas", 
            headers= {"WWW-Authenticate" : "Bearer"})

    try:
        username =jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exeption # check exeption above
        
    except JWTError:
        raise exeption # check exeption above
    
    return search_user(username)

async def current_user(user: User =Depends(auth_user)): # criterio de dependencia, siempre tipar el token
    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user 

## parte expuesta de la API

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code =400, detail= "El usuario no es correcto")
    
    # comparacion de password
    user = search_user_db(form.username)


    if not crypt.verify(form.password, user.password):
         raise HTTPException(
            status_code =400, detail= "La contrasena no es correcta")

    access_token = {"sub": user.username, 
                    "exp" : datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer" }


@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user