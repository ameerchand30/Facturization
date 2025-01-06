from sqlalchemy.orm import Session
from api.models.invoice import Invoice, InvoiceItem
from api.schemas.invoice import InvoiceCreate, InvoiceUpdate, InvoiceItemCreate

def get_invoice(db: Session, invoice_id: int):
    return db.query(Invoice).filter(Invoice.id == invoice_id).first()

def get_invoices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Invoice).offset(skip).limit(limit).all()

def create_invoice(db: Session, invoice: InvoiceCreate):
    db_invoice = Invoice(
        client_id=invoice.client_id,
        enterprise_id=invoice.enterprise_id,
        creation_date=invoice.creation_date,
        due_date=invoice.due_date,
        partial_amount=invoice.partial_amount,
        total_amount=invoice.total_amount,
        special_invoice_no=invoice.special_invoice_no,
        description=invoice.description,
        tax=invoice.tax,
        payment_method=invoice.payment_method
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)

    for item in invoice.invoice_items:
        db_invoice_item = InvoiceItem(
            invoice_id=db_invoice.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            # total_price=item.quantity * item.unit_price
        )
        db.add(db_invoice_item)
    
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def update_invoice(db: Session, invoice_id: int, invoice: InvoiceUpdate):
    db_invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not db_invoice:
        return None

    db_invoice.client_id = invoice.client_id
    db_invoice.enterprise_id = invoice.enterprise_id
    db_invoice.creation_date = invoice.creation_date
    db_invoice.due_date = invoice.due_date
    db_invoice.partial_amount = invoice.partial_amount
    db_invoice.total_amount = invoice.total_amount
    db_invoice.special_invoice_no = invoice.special_invoice_no
    db_invoice.description = invoice.description
    db_invoice.tax = invoice.tax
    db_invoice.payment_method = invoice.payment_method

    db.query(InvoiceItem).filter(InvoiceItem.invoice_id == invoice_id).delete()
    for item in invoice.invoice_items:
        db_invoice_item = InvoiceItem(
            invoice_id=db_invoice.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            total_price=item.quantity * item.unit_price
        )
        db.add(db_invoice_item)

    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def delete_invoice(db: Session, invoice_id: int):
    db_invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if db_invoice:
        db.delete(db_invoice)
        db.commit()
    return db_invoice