from fastapi import FastAPI, Request,APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
# from routers.auth_router import auth
from api.routers.client_router import client_router
# from routers.product_router import product_router
# from routers.enterprise_router import enterprise_router
# from routers.invoice_router import invoice_router

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Include routers
# app.include_router(auth)
app.include_router(client_router)
# app.include_router(product_router)
# app.include_router(enterprise_router)
# app.include_router(invoice_router)

# auth
"""
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("login/login.html", {"request": request})

@app.get("/register")
async def register(request: Request):
    return templates.TemplateResponse("login/register.html", {"request": request})

@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login/login.html", {"request": request})
#clinets
@app.get("/client")
async def client(request: Request):
    return templates.TemplateResponse("pages/client.html", {"request": request})
@app.get("/addClient")
async def addClient(request: Request):
    return templates.TemplateResponse("pages/addClient.html", {"request": request})
#products
@app.get("/product")
async def product(request: Request):
    return templates.TemplateResponse("pages/product.html", {"request": request})
@app.get("/addProduct")
async def addProduct(request: Request):
    return templates.TemplateResponse("pages/addProduct.html", {"request": request})

#invoice
@app.get("/invoice")
async def addInvoices(request: Request):
    return templates.TemplateResponse("pages/invoices.html", {"request": request})
@app.get("/createInvoice")
async def addInvoices(request: Request):
    return templates.TemplateResponse("pages/createInvoice.html", {"request": request})

#enterprise
@app.get("/addEnterprise")
async def addEnterprise(request: Request):
    return templates.TemplateResponse("pages/addEnterprise.html", {"request": request})

@app.get("/enterprise")
async def addEnterprise(request: Request):
    return templates.TemplateResponse("pages/enterprise.html", {"request": request})

#facture
@app.get("/facture")
async def addEnterprise(request: Request):
    return templates.TemplateResponse("pages/generateReport.html", {"request": request})

@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse("pages/dashboard.html", {"request": request})
@app.post('/dashboard')
async def dashboard(request: Request):
    context = {
        'company_name': 'Lal Autos',
        'user_name': 'Ameer Chand',
        'page_title': 'Dashboard',
        'current_currency': 'EUR',
        'nav_items': [
            {'name': 'Dashboard', 'icon': 'home', 'active': True, 'can_add': False},
            {'name': 'Clients', 'icon': 'users', 'can_add': True},
            # Add other nav items...
        ],
        'transactions': [
            {'name': 'Invoices', 'amount': '0,00', 'status': 'primary'},
            {'name': 'Payments', 'amount': '0,00', 'status': 'success'},
            {'name': 'Expenses', 'amount': '0,00', 'status': 'dark'},
            {'name': 'Outstanding', 'amount': '0,00', 'status': 'danger'}
        ],
        'outstanding_invoices': 0,
        'chart_data': {
            'labels': ['01/Dec/2024', '15/Dec/2024', '31/Dec/2024'],
            'datasets': [{
                'label': 'Overview',
                'data': [0, 0, 0],
                'borderColor': '#0d6efd',
                'tension': 0.1
            }]
        }
    }
    
    return templates.TemplateResponse("pages/dashboard.html",{"request": request, **context} )
"""
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
