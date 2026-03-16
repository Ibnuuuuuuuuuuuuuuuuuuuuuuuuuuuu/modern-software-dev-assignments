from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# --- CATEGORY SCHEMAS ---
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int
    class Config:
        from_attributes = True

# --- NOTE SCHEMAS ---
class NoteBase(BaseModel):
    title: str
    content: str
    category_id: Optional[int] = None

class NoteCreate(NoteBase):
    pass

class NotePatch(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[int] = None

class NoteRead(NoteBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    category: Optional[CategoryRead] = None # Menampilkan detail kategori jika ada

    class Config:
        from_attributes = True

# --- ACTION ITEM SCHEMAS (INI YANG HILANG) ---
class ActionItemBase(BaseModel):
    content: str
    due_date: Optional[str] = None
    status: Optional[str] = "pending"
    priority: Optional[str] = "normal"
    note_id: Optional[int] = None

class ActionItemCreate(ActionItemBase):
    pass

class ActionItemPatch(BaseModel):
    content: Optional[str] = None
    due_date: Optional[str] = None
    status: Optional[str] = None

class ActionItemRead(ActionItemBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True