 
from fastapi import APIRouter, Request

product_router = APIRouter(
    prefix="/product",
    tags=["Product"]
) 

@product_router.get("/product")
async def product(request: Request):
    return templates.TemplateResponse("pages/product.html", {"request": request})
@product_router.get("/addProduct")
async def addProduct(request: Request):
    return templates.TemplateResponse("pages/addProduct.html", {"request": request})