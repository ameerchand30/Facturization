from fastapi import APIRouter, Depends, HTTPException, Request, Form, Response
from fastapi.responses import RedirectResponse, HTMLResponse, StreamingResponse
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
from weasyprint import HTML,CSS
from pathlib import Path
from bs4 import BeautifulSoup

templates = Jinja2Templates(directory="templates")

report_router = APIRouter(
    prefix="/report",
    tags=["Reposts"],
    responses={404: {"description": "page Not found"}},
)

@report_router.get("/invoiceNumber/{invoice_id}", response_class=HTMLResponse, name="getReportForm")
async def create_report_form(invoice_id: int  ,request: Request, db: Session = Depends(get_db)):
    invoice_data = get_invoice_details(db, invoice_id)
    return templates.TemplateResponse("pages/generateReport.html", {
        "request": request,
        **invoice_data
    })

# to genraet PDF
@report_router.get("/pdf/{invoice_id}")
async def generate_pdf(
    invoice_id: int, 
    request: Request, 
    db: Session = Depends(get_db)
):
    try:
        invoice_data = get_invoice_details(db, invoice_id)
        html_content = templates.TemplateResponse(
            "pages/pdf.html",
            {
                "request": request,
                **invoice_data,
                "pdf_mode": True
            }
        ).body.decode()
        # Get CSS file path
        css_file = Path("static/css/pdf.css")
        # Generate PDF
        html = HTML(string=html_content, base_url=str(request.base_url))
        css = CSS(filename=css_file)
        pdf = html.write_pdf(stylesheets=[css])
        
        return Response(
            content=pdf,
            media_type="application/pdf",
            headers={"Content-Disposition": f"inline; filename=invoice_{invoice_id}.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_invoice_details(db: Session, invoice_id: int):
    """Get invoice and calculate totals"""
    invoice = crud_report.get_invoice_with_details(db=db, invoice_id=invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    total_ht = sum(item.unit_price * item.quantity for item in invoice.invoice_items)
    tva = total_ht * 0.20
    total_ttc = total_ht + tva
    
    return {
        "invoice": invoice,
        "total_ht": total_ht,
        "tva": tva,
        "total_ttc": total_ttc
    }

