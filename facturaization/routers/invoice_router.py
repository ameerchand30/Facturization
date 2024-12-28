from fastapi import APIRouter, Request

invoice_router = APIRouter(
    prefix="/invoice",
    tags=["Invoice"]
) 
@invoice_router.get("/invoice")
async def addInvoices(request: Request):
    return templates.TemplateResponse("pages/invoices.html", {"request": request})
@invoice_router.get("/createInvoice")
async def addInvoices(request: Request):
    return templates.TemplateResponse("pages/createInvoice.html", {"request": request})