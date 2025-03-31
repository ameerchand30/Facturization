from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from api.models.client import Clients
from api.schemas.client import Client,ClientCreate,ClientUpdate
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

client_router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
    responses={404: {"description": "Not found"}},
)
# to show all clinets form
@client_router.get("/", response_class=HTMLResponse , name="read_clients")
async def read_clients(request: Request, db: Session = Depends(get_db)):
    clients = db.query(Clients).all()
    return templates.TemplateResponse("pages/clients.html", {"request": request, "clients": clients, "current_page": "view_clients"})
# to add Client form
@client_router.get("/add", response_class=HTMLResponse, name="add_client_form")
async def add_client_form(request: Request):
    return templates.TemplateResponse("pages/addClient.html", {"request": request, "client": None, "current_page": "add_client"})
# when a Enterpenieur Click on Edit 
@client_router.get("/edit/{client_id}", response_class=HTMLResponse, name="edit_client_form")
async def edit_client_form(client_id: int, request: Request, db: Session = Depends(get_db)):
    client = db.query(Clients).filter(Clients.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return templates.TemplateResponse("pages/addClient.html", {"request": request, "client": client, "current_page": "edit_client"})
# this is to add new Client 
@client_router.post("/", response_model=dict, name="create_client")
async def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    try:
        client_data = client.model_dump()
        db_client = Clients(**client_data)
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        return {"success": True, "message": "Client created successfully"}
    except Exception as e:
        print(e)
        return {"success": False, "message": str(e)}
# to update client
@client_router.post("/update/{client_id}", response_model=dict, name="update_client")
async def update_client(
    client_id: int,
    clinet: ClientUpdate,
    db: Session = Depends(get_db)
):
    try:
        client_data = clinet.model_dump()
        db.query(Clients).filter(Clients.id == client_id).update(client_data)
        db.commit()
        return {"success": True, "message": "Client updated successfully"}
    except Exception as e:
        print(e)
        return {"success": False, "message": str(e)}
@client_router.delete("/delete/{client_id}",response_model=dict, name="delete_client")
async def delete_client(client_id: int, db: Session = Depends(get_db)):
    try:
        db.query(Clients).filter(Clients.id == client_id).delete()
        db.commit()
        return {"success": True, "message": "Client Deleted successfully"}
    except Exception as e:
        print(e)
        return {"success": False, "message": str(e)}