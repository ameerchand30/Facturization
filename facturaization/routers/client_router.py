from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


client_router = APIRouter(
    tags=["Client"]
)   

@client_router.get("/client")
async def client(request: Request):
    return templates.TemplateResponse("pages/client.html", {"request": request})
@client_router.get("/addClient")
async def addClient(request: Request):
    return templates.TemplateResponse("pages/addClient.html", {"request": request})