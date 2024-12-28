from fastapi import APIRouter, Request

auth = APIRouter()

@auth.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("login/login.html", {"request": request})

@auth.get("/register")
async def register(request: Request):
    return templates.TemplateResponse("login/register.html", {"request": request})

@auth.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login/login.html", {"request": request})
