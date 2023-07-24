from fastapi import FastAPI
from routers import products

app = FastAPI() # instance


# Routers

app.include_router(products.router)

@app.get("/") # the protocol used on this interaction is the standard 'https' - 'http'. get = call or pull from server
async def root(): # this function will act whenever it cantm and dont depent of a constant server sync.
    return "Hola FastAPI!"

# Url local : http://102.0.0.1:8000

@app.get("/url")
async def url():
    return "{ url : https:// mywebsite.com/python }"


# Url local : http://127.0.0.1:8000/url

# start uvicorn server by using: uvicorn main:app --reload


# Documentacion en Swagger http://127.0.0.1:8000/docs
# Documentacion en  Redocly http://127.0.0.1:8000/redocs