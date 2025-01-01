from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from api.models.product import ProductModel
from api.schemas.product import Product, ProductCreate, ProductUpdate
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

product_router = APIRouter(
    prefix="/products",
    tags=["Product"]
) 

@product_router.get("/")
async def read_products(request: Request,db: Session = Depends(get_db), name="read_products"):
    products = db.query(ProductModel).all()
    return templates.TemplateResponse("pages/product.html", {"request": request, "products": products})

@product_router.get("/addProduct", name="add_product_form")
async def addProduct(request: Request):
    return templates.TemplateResponse("pages/addProduct.html", {"request": request})

@product_router.get("/edit/{product_id}", name="edit_product")
async def edit_product(product_id: int, request: Request, db: Session = Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return templates.TemplateResponse("pages/addProduct.html", {"request": request, "product": product})

@product_router.post("/", response_class=RedirectResponse, name="create_product")
async def create_product(
    name: str = Form(...),
    ref_number: str = Form(None),
    price: float = Form(None),
    notes: str = Form(None),
    db: Session = Depends(get_db)
):
    product_data = {
        "name": name,
        "ref_number": ref_number,
        "price": price,
        "description": notes,
    }
    db_product = ProductModel(**product_data)
    print(product_data)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return RedirectResponse(url="/products/", status_code=303)
    return product_data

@product_router.post("/update/{product_id}", response_class=RedirectResponse, name="update_product")
async def update_product(
    product_id: int,
    name: str = Form(...),
    ref_number: str = Form(None),
    price: float = Form(None),
    notes: str = Form(None),
    db: Session = Depends(get_db)
):
    product_data = {
        "name": name,
        "ref_number": ref_number,
        "price": price,
        "description": notes,
    }
    db.query(ProductModel).filter(ProductModel.id == product_id).update(product_data)
    db.commit()
    return RedirectResponse(url="/products", status_code=303)

@product_router.get("/delete/{product_id}", response_class=RedirectResponse, name="delete_product") 
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    db.query(ProductModel).filter(ProductModel.id == product_id).delete()
    db.commit()
    return RedirectResponse(url="/products", status_code=303)



