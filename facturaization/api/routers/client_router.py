from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from api.models.client import Clients
from api.schemas.client import Client, ClientCreate, ClientUpdate
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

client_router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
    responses={404: {"description": "Not found"}},
)

@client_router.get("/add", response_class=HTMLResponse)
async def add_client_form(request: Request):
    return templates.TemplateResponse("pages/addClient.html", {"request": request})

@client_router.post("/", response_class=RedirectResponse)
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
    return RedirectResponse(url="/clients/add", status_code=303)

@client_router.get("/", response_model=List[Client])
def read_clients(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    clients = db.query(Clients).offset(skip).limit(limit).all()
    return clients

@client_router.get("/{client_id}", response_model=Client)
def read_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Clients).filter(Clients.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@client_router.put("/{client_id}", response_model=Client)
def update_client(client_id: int, client: ClientUpdate, db: Session = Depends(get_db)):
    db_client = db.query(Clients).filter(Clients.id == client_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    for key, value in client.dict().items():
        setattr(db_client, key, value)
    db.commit()
    db.refresh(db_client)
    return db_client

@client_router.delete("/{client_id}", response_model=Client)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    db_client = db.query(Clients).filter(Clients.id == client_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(db_client)
    db.commit()
    return db_client