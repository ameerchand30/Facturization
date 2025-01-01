from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from api.models.client import Clients
from api.schemas.client import Client
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

client_router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
    responses={404: {"description": "Not found"}},
)

@client_router.get("/", response_class=HTMLResponse , name="read_clients")
async def read_clients(request: Request, db: Session = Depends(get_db)):
    clients = db.query(Clients).all()
    return templates.TemplateResponse("pages/clients.html", {"request": request, "clients": clients, "current_page": "view_clients"})

@client_router.get("/add", response_class=HTMLResponse, name="add_client_form")
async def add_client_form(request: Request):
    return templates.TemplateResponse("pages/addClient.html", {"request": request, "client": None, "current_page": "add_client"})

@client_router.get("/edit/{client_id}", response_class=HTMLResponse, name="edit_client_form")
async def edit_client_form(client_id: int, request: Request, db: Session = Depends(get_db)):
    client = db.query(Clients).filter(Clients.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return templates.TemplateResponse("pages/addClient.html", {"request": request, "client": client, "current_page": "edit_client"})

@client_router.post("/", response_class=RedirectResponse, name="create_client")
async def create_client(
    name: str = Form(...),
    nationality: str = Form(None),
    idNumber: str = Form(None),
    gender: str = Form(None),
    Billing_Street: str = Form(None),
    City: str = Form(None),
    Postal_Code: str = Form(None),
    Country: str = Form(None),
    email: str = Form(None),
    phone: str = Form(None),
    notes: str = Form(None),
    db: Session = Depends(get_db)
):
    client_data = {
        "name": name,
        "nationality": nationality,
        "idNumber": idNumber,
        "gender": gender,
        "Billing_Street": Billing_Street,
        "City": City,
        "Postal_Code": Postal_Code,
        "Country": Country,
        "email": email,
        "phone": phone,
        "notes": notes,
    }
    db_client = Clients(**client_data)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return RedirectResponse(url="/clients", status_code=303)

@client_router.post("/edit/{client_id}", response_class=RedirectResponse, name="update_client")
async def update_client(
    client_id: int,
    name: str = Form(...),
    nationality: str = Form(None),
    idNumber: str = Form(None),
    gender: str = Form(None),
    Billing_Street: str = Form(None),
    City: str = Form(None),
    Postal_Code: str = Form(None),
    Country: str = Form(None),
    email: str = Form(None),
    phone: str = Form(None),
    notes: str = Form(None),
    db: Session = Depends(get_db)
):
    client = db.query(Clients).filter(Clients.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    client_data = {
        "name": name,
        "nationality": nationality,
        "idNumber": idNumber,
        "gender": gender,
        "Billing_Street": Billing_Street,
        "City": City,
        "Postal_Code": Postal_Code,
        "Country": Country,
        "email": email,
        "phone": phone,
        "notes": notes,
    }
    for key, value in client_data.items():
        setattr(client, key, value)
    db.commit()
    db.refresh(client)
    return RedirectResponse(url="/clients", status_code=303)