from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum,DateTime,Date,func,Float
from sqlalchemy.orm import relationship

class ProductModel(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    ref_number = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    invoice_items = relationship("InvoiceItem", back_populates="product")
    
