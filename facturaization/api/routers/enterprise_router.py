 
from fastapi import APIRouter, Request

enterprise_router = APIRouter(
    prefix="/enterprise",
    tags=["Enterprise"]
) 

@enterprise_router.get("/addEnterprise")
async def addEnterprise(request: Request):
    return templates.TemplateResponse("pages/addEnterprise.html", {"request": request})

@enterprise_router.get("/enterprise")
async def addEnterprise(request: Request):
    return templates.TemplateResponse("pages/enterprise.html", {"request": request})