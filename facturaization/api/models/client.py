from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum,DateTime,Date,func
from sqlalchemy.orm import relationship
# Assuming you have a Base class defined
# Define the

class Clients(Base):
    __tablename__ = "Clients"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    passport_no = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(Enum("M", "F", "O",name="gender_enum"), nullable=True)
    created_at = Column(DateTime, default=func.now())
    comment = Column(String, nullable=True)
    email = Column(String, nullable=True)