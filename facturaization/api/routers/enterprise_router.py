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
    enterprises = crud_enterprise.get_enterprises(db, skip=skip, limit=limit)
    return templates.TemplateResponse("pages/enterprise.html", {"request": request, "enterprises": enterprises, "current_page": "view_enterprise"})

@enterprise_router.get("/add", response_class=HTMLResponse, name="add_enterprise_form")
async def add_enterprise_form(request: Request, db: Session = Depends(get_db)):
    customers = db.query(Clients).all()
    print('customers',customers)
    customer_data = {customer.name: {"email": customer.email,"notes": customer.notes} for customer in customers}
    print('server side customer_data',customer_data)
    return templates.TemplateResponse("pages/addEnterprise.html", {"request": request,"customer_data": customer_data, "customers": customers, "current_page": "add_enterprise"})

@enterprise_router.get("/{enterprise_id}", response_model=schemaEnterprise)
def read_enterprise(enterprise_id: int, db: Session = Depends(get_db)):
    db_enterprise = crud_enterprise.get_enterprise(db, enterprise_id=enterprise_id)
    if db_enterprise is None:
        raise HTTPException(status_code=404, detail="Enterprise not found")
    return db_enterprise
# create enterprise to the database
@enterprise_router.post("/", response_model=schemaEnterprise)
def create_enterprise(enterprise: EnterpriseCreate, db: Session = Depends(get_db)):
    return crud_enterprise.create_enterprise(db=db, enterprise=enterprise)

@enterprise_router.put("/{enterprise_id}", response_model=schemaEnterprise)
def update_enterprise(enterprise_id: int, enterprise: EnterpriseUpdate, db: Session = Depends(get_db)):
    db_enterprise = crud_enterprise.get_enterprise(db, enterprise_id=enterprise_id)
    if db_enterprise is None:
        raise HTTPException(status_code=404, detail="Enterprise not found")
    return crud_enterprise.update_enterprise(db=db, enterprise_id=enterprise_id, enterprise=enterprise)

@enterprise_router.delete("/{enterprise_id}", response_model=schemaEnterprise)
def delete_enterprise(enterprise_id: int, db: Session = Depends(get_db)):
    db_enterprise = crud_enterprise.get_enterprise(db, enterprise_id=enterprise_id)
    if db_enterprise is None:
        raise HTTPException(status_code=404, detail="Enterprise not found")
    return crud_enterprise.delete_enterprise(db=db, enterprise_id=enterprise_id)



