from fastapi import FastAPI, Request,APIRouter, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

# from routers.invoice_router import invoice_router
from facturaization.api.routers.auth_router import auth_router
from facturaization.api.routers.client_router import client_router
from facturaization.api.routers.product_router import product_router
from facturaization.api.routers.enterprise_router import enterprise_router
from facturaization.api.routers.invoice_router import invoice_router
from facturaization.api.routers.report_generate import report_router
from facturaization.api.routers.dashboard_routes import dashboard_router
from facturaization.api.routers.enterprise_profile_router import enterprise_profile_router
from facturaization.api.routers.client_invoices_router import client_invoices_router
# models
""" from facturaization.api.models.client import Clients
from facturaization.api.models.enterprise import Enterprise
from facturaization.api.models.product import ProductModel
from facturaization.api.models.invoice import Invoice, InvoiceItem """

# database
from facturaization.database import Base, engine, get_db, db_manager




# Create the FastAPI app
app = FastAPI()

# Initialize the database manager
@app.on_event("startup")
async def startup_event():
    # This will ensure database exists and all tables are created
    db_manager.initialize()

# Use the get_db dependency in your routes
@app.get("/test-db")
async def test_db(db = Depends(get_db)):
    return {"message": "Database connection successful"}

# Create the database tables   
# Base.metadata.create_all(bind=engine)

# Set up CORS middleware (if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

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
app.include_router(client_invoices_router)


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("pages/User/LandingPage/landing-page.html", {"request": request})

@app.get("/{full_path:path}")  
async def catch_all(request: Request, full_path: str):
    return templates.TemplateResponse("pages/User/LandingPage/landing-page.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
