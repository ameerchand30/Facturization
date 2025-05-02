from fastapi import FastAPI, Request,APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

# from routers.invoice_router import invoice_router
from api.routers.auth_router import auth_router
from api.routers.client_router import client_router
from api.routers.product_router import product_router
from api.routers.enterprise_router import enterprise_router
from api.routers.invoice_router import invoice_router
from api.routers.report_generate import report_router
from api.routers.dashboard_routes import dashboard_router
from api.routers.enterprise_profile_router import enterprise_profile_router
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


# Set up CORS middleware (if needed)

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Include routers
# app.include_router(auth)
app.include_router(auth_router)
app.include_router(client_router)
app.include_router(product_router)
app.include_router(enterprise_router)
app.include_router(invoice_router)
app.include_router(report_router)
app.include_router(dashboard_router)
app.include_router(enterprise_profile_router)



@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("pages/User/LandingPage/landing-page.html", {"request": request})

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
