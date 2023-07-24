from fastapi import FastAPI

app = FastAPI()


@app.get("/products")
async def products():
    return["producto 1", "producto 2", "producto 3", "producto 4", "producto 5"]