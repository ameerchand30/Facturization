from sqlalchemy.orm import Session
from api.models.enterprise import Enterprise
from api.schemas.enterprise import EnterpriseCreate, EnterpriseUpdate

def get_enterprise(db: Session, enterprise_id: int):
    return db.query(Enterprise).filter(Enterprise.id == enterprise_id).first()

def get_enterprises(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Enterprise).offset(skip).limit(limit).all()

def create_enterprise(db: Session, enterprise: EnterpriseCreate):
    db_enterprise = enterprise
    db.add(db_enterprise)
    db.commit()
    db.refresh(db_enterprise)
    return db_enterprise

def update_enterprise(db: Session, enterprise_id: int, enterprise: EnterpriseUpdate):
    db_enterprise = db.query(Enterprise).filter(Enterprise.id == enterprise_id).first()
    if db_enterprise:
        for key, value in enterprise.dict().items():
            setattr(db_enterprise, key, value)
        db.commit()
        db.refresh(db_enterprise)
    return db_enterprise

def delete_enterprise(db: Session, enterprise_id: int):
    db_enterprise = db.query(Enterprise).filter(Enterprise.id == enterprise_id).first()
    if db_enterprise:
        db.delete(db_enterprise)
        db.commit()
    return db_enterprise