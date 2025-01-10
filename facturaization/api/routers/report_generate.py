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
from api.routers.crud import crud_report
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

report_router = APIRouter(
    prefix="/report",
    tags=["Reposts"],
    responses={404: {"description": "page Not found"}},
)
@report_router.get("/invoiceNumber/{invoice_id}", response_class=HTMLResponse, name="getReportForm")
async def create_report_form(invoice_id: int  ,request: Request, db: Session = Depends(get_db)):
    invoice = crud_report.get_invoice_with_details(db=db, invoice_id=invoice_id)
   # Calculate totals
    total_ht = sum(item.unit_price * item.quantity for item in invoice.invoice_items)
    tva = total_ht * 0.20  # 20% TVA
    total_ttc = total_ht + tva
    return templates.TemplateResponse("pages/generateReport.html",
    {"request": request, "invoice": invoice,
    "total_ht": total_ht,
    "tva": tva,
    "total_ttc": total_ttc,
    "current_page": "read_invoice"})
