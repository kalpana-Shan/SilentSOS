# routes/contacts.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import get_db

router = APIRouter()

class ContactCreate(BaseModel):
    name: str
    relation: Optional[str] = None
    phone: Optional[str] = None
    email: str

@router.get("/contacts")
def get_contacts():
    conn = get_db()
    contacts = conn.execute("SELECT * FROM trusted_contacts ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(c) for c in contacts]

@router.post("/contacts")
def add_contact(contact: ContactCreate):
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO trusted_contacts (name, relation, phone, email) VALUES (?, ?, ?, ?)",
        (contact.name, contact.relation, contact.phone, contact.email)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"id": new_id, "message": f"Contact '{contact.name}' added successfully"}

@router.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):
    conn = get_db()
    conn.execute("DELETE FROM trusted_contacts WHERE id = ?", (contact_id,))
    conn.commit()
    conn.close()
    return {"message": "Contact deleted successfully"}