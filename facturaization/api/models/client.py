from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum,DateTime,Date,func
from sqlalchemy.orm import relationship

class Clients(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    nationality = Column(String, nullable=True)
    idNumber = Column(String, nullable=True)
    gender = Column(Enum("M", "F", "O",name="gender_enum"), nullable=True)
    Billing_Street = Column(String)
    City = Column(String)
    State_Province = Column(String)
    Postal_Code = Column(String)
    Country = Column(String)
    email = Column(String)
    phone = Column(String)
    notes = Column(String)
    created_at = Column(DateTime, default=func.now())
    enterprises = relationship("Enterprise", back_populates="client")
    invoices = relationship("Invoice", back_populates="client")
