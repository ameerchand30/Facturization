from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum,DateTime,Date,func
from sqlalchemy.orm import relationship
# Assuming you have a Base class defined
# Define the

class Clients(Base):
    __tablename__ = "Clients"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    nationality = Column(String, nullable=True)
    idNumber = Column(String, nullable=True)
    gender = Column(Enum("M", "F", "O",name="gender_enum"), nullable=True)
    Billing_Street = Column(String, nullable=True)
    City = Column(String, nullable=True)
    Postal_Code = Column(String, nullable=True)
    Country = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    