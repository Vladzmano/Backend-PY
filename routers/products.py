from fastapi import APIRouter

router = APIRouter(prefix= "/products",
                tags=["Products"], #esto sirve para agrupar las API por categori apropia
                responses= {404:{"mensaje" : "No encontrado"}})

product_list =  ["producto 1", "producto 2", 
                 "producto 3", "producto 4", 
                 "producto 5"]

@router.get("/")
async def products():
    return product_list


@router.get("/{id}")
async def products(id: int):
    return product_list[id]