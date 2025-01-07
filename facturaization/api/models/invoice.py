from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Enum as SQLAEnum
from sqlalchemy.orm import relationship
from database import Base
import datetime
from .client import Clients
from .enterprise import Enterprise
from .product import ProductModel
from enum import Enum

class PaymentMethodEnum(str, Enum):
    CASH = "Cash"
    CREDIT_CARD = "Credit Card"
    BANK_TRANSFER = "Bank Transfer"
    PAYPAL = "PayPal"

class Invoice(Base):
    __tablename__ = 'invoices'
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('clients.id', ondelete='CASCADE'))
    enterprise_id = Column(Integer, ForeignKey('enterprises.id'))
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)
    due_date = Column(DateTime, default=None)
    partial_amount = Column(Float)
    total_amount = Column(Float)
    special_invoice_no = Column(String)
    description = Column(String)
    tax = Column(Float)
    payment_method = Column(SQLAEnum(PaymentMethodEnum))
    client = relationship("Clients", back_populates="invoices")
    enterprises = relationship("Enterprise", back_populates="invoices")
    invoice_items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")

class InvoiceItem(Base):
    __tablename__ = 'invoice_items'
    
    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id', ondelete='CASCADE'), index=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer)
    unit_price = Column(Float)
    
    invoice = relationship("Invoice", back_populates="invoice_items")
    product = relationship("ProductModel", back_populates="invoice_items")
    