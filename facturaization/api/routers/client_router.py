from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from api.models.client import Clients
from api.schemas.client import Client, ClientCreate, ClientUpdate

client_router = APIRouter(
    prefix="/api",
    tags=["Clients"],
    responses={404: {"description": "Not found"}},
)
@client_router.post("/clients/", response_model=Client)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    db_client = Clients(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@client_router.get("/clients/", response_model=List[Client])
def read_clients(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    clients = db.query(Clients).offset(skip).limit(limit).all()
    return clients

@client_router.get("/clients/{client_id}", response_model=Client)
def read_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Clients).filter(Clients.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@client_router.put("/clients/{client_id}", response_model=Client)
def update_client(client_id: int, client: ClientUpdate, db: Session = Depends(get_db)):
    db_client = db.query(Clients).filter(Clients.id == client_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    for key, value in client.dict().items():
        setattr(db_client, key, value)
    db.commit()
    db.refresh(db_client)
    return db_client

@client_router.delete("/clients/{client_id}", response_model=Client)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    db_client = db.query(Clients).filter(Clients.id == client_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(db_client)
    db.commit()
    return db_client