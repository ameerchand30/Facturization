from fastapi import FastAPI, Request,APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# from routers.invoice_router import invoice_router
from api.routers.client_router import client_router
from api.routers.product_router import product_router
from api.routers.enterprise_router import enterprise_router
from api.routers.invoice_router import invoice_router
from api.routers.report_generate import report_router
# models
from api.models.client import Clients
from api.models.enterprise import Enterprise
from api.models.product import ProductModel
from api.models.invoice import Invoice, InvoiceItem

# database
from database import Base, engine

# Create the database tables   
Base.metadata.create_all(bind=engine)


# Create the FastAPI app
app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Include routers
# app.include_router(auth)
app.include_router(client_router)
app.include_router(product_router)
app.include_router(enterprise_router)
app.include_router(invoice_router)
app.include_router(report_router)


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("pages/User/LandingPage/landing-page.html", {"request": request})
@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("pages/User/login/login.html", {"request": request})
@app.get("/register")
async def register(request: Request):
    return templates.TemplateResponse("pages/User/login/register.html", {"request": request})
@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse("pages/dashboard.html", {"request": request,"current_page": "dashboard"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
# Routes
@app.get("/login")
async def read_root(request: Request):
    return templates.TemplateResponse("login/login.html", {"request": request})

@app.get("/register")
async def register(request: Request):
    return templates.TemplateResponse("login/register.html", {"request": request})

@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login/login.html", {"request": request})
