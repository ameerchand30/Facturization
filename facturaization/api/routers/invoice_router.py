from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from typing import List,Optional
from datetime import date
from database import get_db
from api.models.client import Clients
from api.models.enterprise import Enterprise
from api.models.product import ProductModel
from api.models.invoice import Invoice, InvoiceItem
from api.schemas.invoice import InvoiceCreate, InvoiceUpdate, InvoiceItemCreate,Invoice as InvoiceSchema
from api.routers.crud import crud_invoice
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

invoice_router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"],
    responses={404: {"description": "Not found"}},
)
# to show enterprise and customer data while creating inovice
@invoice_router.get("/create", response_class=HTMLResponse, name="create_invoice_form")
async def create_invoice_form(request: Request, db: Session = Depends(get_db)):
    customers = db.query(Clients).all()
    products = db.query(ProductModel).all()
    enterprise_data = [{"id": enterprise.id, "name": enterprise.name} for enterprise in db.query(Enterprise).all()]
    customer_data = {customer.name: {"id": customer.id,"email":customer.email } for customer in customers}
    product_data = {product.name: {"id": product.id, "unit_price": product.price,"description":product.description} for product in products}
    return templates.TemplateResponse("pages/createInvoice.html", {"request": request, "customer_data": customer_data, "product_data": product_data, "enterprise_data": enterprise_data, "current_page": "create_invoices"})

# to show invoices
@invoice_router.get("/read", response_class=HTMLResponse, name="read_invoices")
def read_invoices(request: Request, db: Session = Depends(get_db)):
    invoices = crud_invoice.get_invoices(db)
    return templates.TemplateResponse("pages/invoices.html", {"request": request, "invoices": invoices, "current_page": "read_invoices"})

# to edit the invocies form
@invoice_router.get("/edit/{invoice_id}", response_class=HTMLResponse, name="edit_invoice_form")
async def edit_invoice_form(invoice_id: int, request: Request, db: Session = Depends(get_db)):
    invoice = crud_invoice.get_invoice(db=db, invoice_id=invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    customers = db.query(Clients).all()
    products = db.query(ProductModel).all()
    enterprise_data = [{"id": enterprise.id, "name": enterprise.name} for enterprise in db.query(Enterprise).all()] # Note method
    customer_data = {customer.name: {"id": customer.id,"email":customer.email } for customer in customers} # Another method 
    product_data = {product.name: {"id": product.id, "unit_price": product.price,"description":product.description} for product in products}
    
    return templates.TemplateResponse(
        "pages/createInvoice.html",
        {
            "request": request,
            "invoice": invoice,
            "customer_data": customer_data,
            "product_data": product_data,
            "enterprise_data": enterprise_data,
            "current_page": "create_invoices",
            "mode": "edit",
            "rowCounter": len(invoice.invoice_items)  # Add rowCounter
        }
    )
 
# to create new invoice
@invoice_router.post("/", response_model=dict, name="create_invoice")
def create_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    try:
        crud_invoice.create_invoice(db=db, db_invoice=invoice)
        return {"success": True, "message": "Client created successfully"}
    except Exception as e:
        print(e)
        db.rollback()
        return {"success": False, "message": str(e)}
# to update invoice
@invoice_router.post("/update/{invoice_id}", response_model=dict, name="update_invoice")
async def update_invoice(invoice_id: int, invoice_data: InvoiceUpdate, db: Session = Depends(get_db)):
    try:
        crud_invoice.update_invoice(db=db, invoice_id=invoice_id, invoice=invoice_data)
        return {"success": True, "message": "Enterprise created successfully"}
    except Exception as e:
        print(e)
        db.rollback()
        return {"success": False, "message": str(e)}

# to delete invoice
@invoice_router.delete("/delete/{invoice_id}", response_model=dict, name="delete_invoice")
async def delete_invoice(invoice_id: int,db: Session = Depends(get_db)):
    try:
        crud_invoice.delete_invoice(db=db ,invoice_id=invoice_id)
        return {"success": True, "message": "Client Delted successfully"}
    except Exception as e:
        print(e)
        return {"success": False, "message": str(e)}
