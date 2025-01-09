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

@invoice_router.get("/create", response_class=HTMLResponse, name="create_invoice_form")
async def create_invoice_form(request: Request, db: Session = Depends(get_db)):
    customers = db.query(Clients).all()
    products = db.query(ProductModel).all()
    enterprise_data = [{"id": enterprise.id, "name": enterprise.name} for enterprise in db.query(Enterprise).all()]
    customer_data = {customer.name: {"id": customer.id,"email":customer.email } for customer in customers}
    product_data = {product.name: {"id": product.id, "unit_price": product.price,"description":product.description} for product in products}
    return templates.TemplateResponse("pages/createInvoice.html", {"request": request, "customer_data": customer_data, "product_data": product_data, "enterprise_data": enterprise_data, "current_page": "create_invoices"})

@invoice_router.get("/edit/{invoice_id}", response_class=HTMLResponse, name="edit_invoice_form")
async def edit_invoice_form(invoice_id: int, request: Request, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    customers = db.query(Clients).all()
    products = db.query(ProductModel).all()
    customer_data = {customer.name: {"id": customer.id, "enterprises": [{"id": enterprise.id, "name": enterprise.name} for enterprise in customer.enterprises]} for customer in customers}
    product_data = {product.name: {"id": product.id, "unit_price": product.unit_price} for product in products}
    return templates.TemplateResponse("pages/createInvoice.html", {"request": request, "invoice": invoice, "customer_data": customer_data, "product_data": product_data})
@invoice_router.post("/edit/{invoice_id}", response_class=RedirectResponse, name="update_invoice")
def update_invoice(
    invoice_id: int,
    customerId: int = Form(...),
    enterpriseId: int = Form(...),
    invoiceItems: List[InvoiceItemCreate] = Form(...),
    db: Session = Depends(get_db)
):
    invoice_data = InvoiceUpdate(
        client_id=customerId,
        enterprise_id=enterpriseId,
        invoice_items=invoiceItems
    )
    crud_invoice.update_invoice(db=db, invoice_id=invoice_id, invoice=invoice_data)
    return RedirectResponse(url="/invoices", status_code=303)
# to create new invoice
@invoice_router.post("/", response_class=RedirectResponse, name="create_invoice")
def create_invoice(
    customerId: int = Form(...),
    enterpriseId: int = Form(...),
    creationDate: date = Form(...),
    paidDate: Optional[str] = Form(None),
    specialNo: Optional[str] = Form(None),
    Notes: Optional[str] = Form(None),
    productId: List[str] = Form(...),
    productUnitPri: Optional[List[str]] = Form(None),
    productQty: Optional[List[str]] = Form(None),
    db: Session = Depends(get_db)
):
    print('product_id',productId)
    print('customer_id',customerId)
   
    invoice_items = [
        InvoiceItem(
            product_id=productId,
            quantity=productQty,
            unit_price=productUnitPri,
        )
        for productId, productQty, productUnitPri in zip(productId, productQty, productUnitPri)
    ]
    invoice = Invoice(
        client_id=customerId,
        enterprise_id=enterpriseId,
        creation_date = creationDate,
        invoice_items=invoice_items
    )
    print(invoice)
    crud_invoice.create_invoice(db=db, invoice=invoice)
    return RedirectResponse(url="/invoices/create", status_code=303)


@invoice_router.get("/read", response_class=HTMLResponse, name="read_invoices")
def read_invoices(request: Request, db: Session = Depends(get_db)):
    invoices = crud_invoice.get_invoices(db)
    return templates.TemplateResponse("pages/invoices.html", {"request": request, "invoices": invoices, "current_page": "read_invoices"})