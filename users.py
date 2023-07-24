### Users ###

## Get de Usuarios ##

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/users1")
async def users1():
    return "Hola FastAPI users"


# Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url:str
    age: int

users_list = [User(id = 1, name= "Vlad", surname= "Mano", url= "https://mywebsite.com", age= 34),
              User(id = 2, name= "jhon", surname= "Smith", url= "https://mywebsite1.com", age= 34),
              User(id = 3, name= "Amal", surname= "Ashanty", url= "https://mywebsite2.com", age= 34)] #basemodel parmite crear una entidad, permite tratarlo de difernetes formas.

@app.get("/usersjson")
async def usersjson():
    return [{ "name": "vlad", "surname": "Mano", "url": "https:// mywebsite.com"},
            { "name": "Jhon", "surname": "Smith", "url": "https:// mywebsite1.com" },
            { "name": "Amal", "surname": "Ashanty", "url": "https:// mywebsite2.com" }]


@app.get("/users")
async def users():
    return users_list



# Path

@app.get("/user/{id}")
async def user(id: int):
    return search_users(id)

# Query

@app.get("/userquery/") # can be changes to /user/
async def user(id: int):
    return search_users(id)

def search_users(id: int):
    users = filter(lambda user: user.id == id, users_list)

    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}