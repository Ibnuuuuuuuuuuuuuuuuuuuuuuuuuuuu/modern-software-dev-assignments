from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .db import Base

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    # Relationship ke Note
    notes = relationship("Note", back_populates="category")

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # ForeignKey ke Category
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    category = relationship("Category", back_populates="notes")

# INI YANG HILANG: Tambahkan kembali model ActionItem
class ActionItem(Base):
    __tablename__ = "action_items"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    due_date = Column(String, nullable=True)
    status = Column(String, default="pending") # pending, completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    priority = Column(String, default="normal")
    
    # Opsional: Jika action item mau dihubungkan ke note tertentu
    note_id = Column(Integer, ForeignKey("notes.id"), nullable=True)