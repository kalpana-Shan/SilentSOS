from fastapi import APIRouter
from pydantic import BaseModel
from database import get_connection

router = APIRouter()

class ContactCreate(BaseModel):
    name: str
    relation: str
    phone: str

@router.post("/contacts")
def add_contact(contact: ContactCreate):
    """Add a trusted contact"""
    conn = get_connection()
    conn.execute(
        "INSERT INTO trusted_contacts (name, relation, phone) VALUES (?, ?, ?)",
        (contact.name, contact.relation, contact.phone)
    )
    conn.commit()
    conn.close()
    return {"message": "Contact added successfully", "contact": contact.dict()}

@router.get("/contacts")
def get_contacts():
    """Get all trusted contacts"""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM trusted_contacts").fetchall()
    conn.close()
    return [dict(row) for row in rows]

@router.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):
    """Delete a trusted contact"""
    conn = get_connection()
    conn.execute("DELETE FROM trusted_contacts WHERE id = ?", (contact_id,))
    conn.commit()
    conn.close()
    return {"message": "Contact deleted"}