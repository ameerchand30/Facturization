from fastapi import APIRouter, Depends, HTTPException, Request
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
# to read all products
@product_router.get("/")
async def read_products(request: Request,db: Session = Depends(get_db), name="read_products"):
    products = db.query(ProductModel).all()
    return templates.TemplateResponse("pages/product.html", {"request": request, "products": products, "current_page": "view_products"})
# to add new product Form
@product_router.get("/addProduct", name="add_product_form")
async def addProduct(request: Request):
    return templates.TemplateResponse("pages/addProduct.html", {"request": request, "current_page": "add_product"})
# to edit a existing product form
@product_router.get("/edit/{product_id}", name="edit_product")
async def edit_product(product_id: int, request: Request, db: Session = Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return templates.TemplateResponse("pages/addProduct.html", {"request": request, "product": product})

# to receive new post request to store a new product
@product_router.post("/", response_model=dict, name="create_product")
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    try:
        product_dict = product.model_dump()
        db_product = ProductModel(**product_dict)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return {"success": True, "message": "Product created successfully"}
    except Exception as e:
        print(e)
        return {"success": False, "message": str(e)}

# to update a product
@product_router.post("/update/{product_id}", response_model=dict, name="update_product")
async def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    try:
        # Unpack the product data into a dictionary
        product_data = product.model_dump()
        db.query(ProductModel).filter(ProductModel.id == product_id).update(product_data)
        db.commit()
        return {"success": True, "message": "Product updated successfully"}
    except Exception as e:
        print(e)
        return {"success": False, "message": str(e)}
# to delete a product 
@product_router.delete("/delete/{product_id}", response_model=dict, name="delete_product") 
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    try:
        db.query(ProductModel).filter(ProductModel.id == product_id).delete()
        db.commit()
        return {"success": True, "message": "Product Deleted successfully"}
    except Exception as e:
        print(e)
        return {"success": False, "message": str(e)}




