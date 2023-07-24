from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI() # instance

oauth2 = OAuth2PasswordBearer(tokenUrl="login") # sistema de seguridad buid-in FastaPI

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
        "password" : "12345"
        },

    "VLZM":{
        "username": "VLZM",
        "name": "mano",
        "email": "test@test.com",
        "disabled": True,
        "password" : "654321"
        }
    }

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    

    
async def current_user(token: str =Depends(oauth2)): # criterio de dependencia, siempre tipar el token
    user = search_user(token)
    if not users_db:
        raise HTTPException(
            status_code =status.HTTP_401_UNAUTHORIZED, 
            detail= "Credenciales de autenticacion invalidas", 
            headers= {"WWW-Authenticate" : "Bearer"})
    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code =400, detail= "El usuario no es correcto")
    
    user = search_user_db(form.username)
    if not form.password == user.password:
         raise HTTPException(
            status_code =400, detail= "La contrasena no es correcta")
    

    return {"access_token": user.username, "token_type": "bearer" }

@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user