### Users ###

## Get de Usuarios ##

from fastapi import FastAPI, HTTPException
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
              User(id = 2, name= "jhon", surname= "Smith", url= "https://mywebsite1.com", age= 18),
              User(id = 3, name= "Amal", surname= "Ashanty", url= "https://mywebsite2.com", age= 20),
              User(id = 4, name= "Kuman", surname= "Shikakr", url= "https://mywebsite3.com", age= 43)] 

#basemodel permite crear una entidad, permite tratarlo de difernetes formas.

@app.get("/usersjson")
async def usersjson():
    return [{ "name": "vlad", "surname": "Mano", "url": "https:// mywebsite.com"},
            { "name": "Jhon", "surname": "Smith", "url": "https:// mywebsite1.com" },
            { "name": "Amal", "surname": "Ashanty", "url": "https:// mywebsite2.com" }]


@app.get("/users")
async def users():
    return users_list



# Path : paramatros que son fijos, esto es obligatorio. ayuda a mantenr la coherencia de la API

@app.get("/user/{id}")
async def user(id: int):
    return search_users(id)

# Query : parametros pra elaizar la peticion
# Esto incluye una comprobacion

## GET ##

@app.get("/user/") # can be changes to /user/
async def user(id: int):
    return search_users(id)

def search_users(id: int):
    users = filter(lambda user: user.id == id, users_list)

    try: # comprobacion aqui
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}
    


## paginacion, es una capacidad variable dinamico
# "? se utiliza para el primera parametro del query string luego se utiliza & para concatenar mas datos/IDs"


## POST ##

@app.post("/user/",response_model= User, status_code=201) # operacion para incertar nuevos datos, ademas se puede fdefinir
async def user(user: User):
    if type(search_users(user.id)) == User:
        raise HTTPException(status_code=204, detail= "El usuario ya existe") #$$ con raise retorna el error correcto por la consola
     
    users_list.append(user)
    return user

# tiene que bastar con el codigo de error para informar el usuario de APi que esta pasando.    

## PUT ##

@app.put("/user/")
async def user(user : User):

    found = False

    for index, saved_user in enumerate(users_list): # creamos un indice para saber cul usuario actualizar
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error" : "No se ha actualizado el user"}

    else:
        return user
    

## DELETE ##


@app.delete("/user/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list): # creamos un indice para saber cual usuario actualizar.
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
        return{"error":"se ha eliminado el user"}
        

def search_users(id: int):
    users = filter(lambda user: user.id == id, users_list)

    try: # comprobacion aqui
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"} 
    
"""
## Aprender a utilizar los codigos de status HTTP ##

for more reference use the link below:
https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

es muy importante documentar los codigos de status de nuestras API para las personas que la consumen.

Eg:

100 cannoy have a body
200 all ok
201 after creating something new
204 not content to return to the client
300 Redirection
301 permanent redirection
307 temp redirection
304 not modifier
400 an error
404 not found
500 internal server error

"""