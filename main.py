from fastapi import FastAPI

app = FastAPI() # instance

@app.get("/") # the protocol used on this interaction is the standard 'https' - 'http'. get = call or pull from server
async def root(): # this function will act whenever it cantm and dont depent of a constant server sync.
    return "Hola FastAPI!"

@app.get("/url")
async def url():
    return "{ url : https:// mywebsite.com/python }"


