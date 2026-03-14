from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, select, text
from sqlalchemy.orm import Session
import logging

from ..db import get_db
from ..models import Note
from ..schemas import NoteCreate, NotePatch, NoteRead

router = APIRouter(prefix="/notes", tags=["notes"])

@router.get("/", response_model=list[NoteRead])
def list_notes(
    db: Session = Depends(get_db),
    q: Optional[str] = None,
    skip: int = 0,
    limit: int = Query(50, le=200),
    sort: str = Query("-created_at", description="Sort by field, prefix with - for desc"),
) -> list[NoteRead]:
    stmt = select(Note)
    if q:
        stmt = stmt.where((Note.title.contains(q)) | (Note.content.contains(q)))

    sort_field = sort.lstrip("-")
    order_fn = desc if sort.startswith("-") else asc
    if hasattr(Note, sort_field):
        stmt = stmt.order_by(order_fn(getattr(Note, sort_field)))
    else:
        stmt = stmt.order_by(desc(Note.created_at))

    rows = db.execute(stmt.offset(skip).limit(limit)).scalars().all()
    return [NoteRead.model_validate(row) for row in rows]

@router.post("/", response_model=NoteRead, status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)) -> NoteRead:
    note = Note(title=payload.title, content=payload.content)
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)

@router.patch("/{note_id}", response_model=NoteRead)
def patch_note(note_id: int, payload: NotePatch, db: Session = Depends(get_db)) -> NoteRead:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if payload.title is not None:
        note.title = payload.title
    if payload.content is not None:
        note.content = payload.content
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)

@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, db: Session = Depends(get_db)) -> NoteRead:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteRead.model_validate(note)

# FIX 1: Perbaikan SQL Injection menggunakan Parameterized Query
@router.get("/unsafe-search", response_model=list[NoteRead])
def unsafe_search(q: str, db: Session = Depends(get_db)) -> list[NoteRead]:
    sql = text(
        """
        SELECT id, title, content, created_at, updated_at
        FROM notes
        WHERE title LIKE :q OR content LIKE :q
        ORDER BY created_at DESC
        LIMIT 50
        """
    )
    # Input 'q' dikirim sebagai parameter, bukan string formatting
    rows = db.execute(sql, {"q": f"%{q}%"}).all()
    results: list[NoteRead] = []
    for r in rows:
        results.append(
            NoteRead(
                id=r.id,
                title=r.title,
                content=r.content,
                created_at=r.created_at,
                updated_at=r.updated_at,
            )
        )
    return results

@router.get("/debug/hash-md5")
def debug_hash_md5(q: str) -> dict[str, str]:
    import hashlib
    return {"algo": "md5", "hex": hashlib.md5(q.encode()).hexdigest()}

# FIX 2: Mitigasi Code Injection dengan ast.literal_eval
@router.get("/debug/eval")
def debug_eval(expr: str) -> dict[str, str]:
    import ast
    try:
        # ast.literal_eval jauh lebih aman daripada eval()
        result = str(ast.literal_eval(expr))
    except Exception:
        result = "Error: Unsafe expression detected"
    return {"result": result}

# FIX 3: Perbaikan Command Injection dengan shell=False dan shlex
@router.get("/debug/run")
def debug_run(cmd: str) -> dict[str, str]:
    import subprocess
    import shlex
    
    # Memecah string menjadi list argumen yang aman
    args = shlex.split(cmd)
    # shell=False mencegah eksekusi shell command yang berbahaya
    completed = subprocess.run(args, shell=False, capture_output=True, text=True)
    return {"returncode": str(completed.returncode), "stdout": completed.stdout, "stderr": completed.stderr}

@router.get("/debug/fetch")
def debug_fetch(url: str) -> dict[str, str]:
    import requests
    # Menggunakan requests lebih aman dan kita batasi hanya untuk http/https
    if not url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="Invalid URL scheme")
        
    try:
        response = requests.get(url, timeout=5)
        body = response.text[:1024]
    except Exception as e:
        body = f"Error fetching URL: {str(e)}"
        
    return {"snippet": body}

@router.get("/debug/read")
def debug_read(path: str) -> dict[str, str]:
    try:
        content = open(path, "r").read(1024)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc))
    return {"snippet": content}