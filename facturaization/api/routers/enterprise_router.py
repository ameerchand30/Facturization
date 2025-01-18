from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from api.routers.crud import crud_enterprise  # Correct import statement

from api.schemas.enterprise import Enterprise as schemaEnterprise, EnterpriseCreate, EnterpriseUpdate
from api.models.client import Clients
from api.schemas.client import Client
from api.models.enterprise import Enterprise
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

enterprise_router = APIRouter(
    prefix="/enterprises",
    tags=["Enterprises"],
    responses={404: {"description": "Not found"}},
)

# show the enterprise page
@enterprise_router.get("/", response_class=HTMLResponse, name="read_enterprises")
def read_enterprises(request: Request ,skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    enterprises = db.query(Enterprise, Clients).join(Clients, Enterprise.client_id == Clients.id).offset(skip).limit(limit).all()
    return templates.TemplateResponse("pages/enterprise.html", {"request": request, "enterprises": enterprises, "current_page": "view_enterprise"})
# show the enterprise Form page with the customer data
@enterprise_router.get("/add", response_class=HTMLResponse, name="add_enterprise_form")
async def add_enterprise_form(request: Request, db: Session = Depends(get_db)):
    customers = db.query(Clients).all()
    customer_data = {customer.name: {"customer_id": customer.id,"email": customer.email,"notes": customer.notes} for customer in customers}
    return templates.TemplateResponse("pages/addEnterprise.html", {"request": request,"customer_data": customer_data, "customers": customers, "current_page": "add_enterprise"})

# create enterprise to the database
@enterprise_router.post("/", response_model=dict, name="create_enterprise")
def create_enterprise( enterprise : EnterpriseCreate, db: Session = Depends(get_db)):
    # print(enterprise.__dict__)
    try:
        enterprise_dict = enterprise.model_dump()
        db_enterprise = Enterprise(**enterprise_dict)
        crud_enterprise.create_enterprise(db=db, enterprise=db_enterprise)
        return {"success": True, "message": "Enterprise created successfully"}
    except Exception as e:
        print(e)
        return {"success": False, "message": str(e)}

# link the edit enterprise page
@enterprise_router.get("/edit/{enterprise_id}", response_class=HTMLResponse, name="edit_enterprise_form")
def edit_enterprise_form(enterprise_id: int, request: Request, db: Session = Depends(get_db)):
    enterprise = crud_enterprise.get_enterprise(db, enterprise_id=enterprise_id)
    if enterprise is None:
        raise HTTPException(status_code=404, detail="Enterprise not found")
    customers = db.query(Clients).all()
    customer_data = {customer.name: {"customer_id": customer.id,"email": customer.email,"notes": customer.notes} for customer in customers}
    return templates.TemplateResponse("pages/addEnterprise.html", {"request": request, "enterprise": enterprise, "customer_data": customer_data, "customers": customers, "current_page": "edit_enterprise"})

# update enterprise to the database
@enterprise_router.post("/update/{enterprise_id}", response_model=dict, name="update_enterprise")
def update_enterprise(enterprise_id: int, enterprise : EnterpriseUpdate ,db: Session = Depends(get_db)):
    try:
        enterprise_dict = enterprise.model_dump()
        db_enterprise = Enterprise(**enterprise_dict)
        crud_enterprise.update_enterprise(db,enterprise_id,enterprise_dict)
        return {"success": True, "message": "Enterprise has been updated"}
        
    except Exception as e:
        print(e)
        return {"success": False, "message": str(e)}
# to delete the enterprise 
@enterprise_router.delete("/delete/{enterprise_id}", response_model = dict, name="delete_enterprise")
def delete_enterprise(enterprise_id: int, request: Request ,db: Session = Depends(get_db)):
    try:
        crud_enterprise.delete_enterprise(db,enterprise_id)
        return {"success": True, "message": "Product Deleted successfully"}
    except Exception as e:
        print(e)
        return {"success": False, "message": str(e)}




