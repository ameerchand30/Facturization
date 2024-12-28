from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


client_router = APIRouter(
    tags=["Client"]
)   

@client_router.get("/")
async def client():
    return {"message": "Client router"}

@client_router.get("/addClient")
async def addClient():
    return {"message": "Add client router"}
 