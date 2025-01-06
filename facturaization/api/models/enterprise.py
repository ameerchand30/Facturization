from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from .client import Clients  # Import the Clients model

class Enterprise(Base):
    __tablename__ = "enterprises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    state = Column(String)
    postalCode = Column(String)
    city = Column(String)
    siretNo = Column(String)
    notes = Column(String)
    client_id = Column(Integer, ForeignKey('clients.id'))

    client = relationship("Clients", back_populates="enterprises")
    invoices = relationship("Invoice", back_populates="enterprises")