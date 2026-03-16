from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# 1. Impor database dan model duluan agar Base terdefinisi
from .db import apply_seed_if_needed, engine
from .models import Base 

# 2. Baru impor router (karena router bergantung pada models)
from .routers import categories as categories_router
from .routers import action_items as action_items_router
from .routers import notes as notes_router

app = FastAPI(title="Modern Software Dev Starter (Week 7)", version="0.1.0")

# Ensure data dir exists
Path("data").mkdir(parents=True, exist_ok=True)

# Mount static frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Compatibility with FastAPI lifespan events
@app.on_event("startup")
def startup_event() -> None:
    # Ini akan membuat tabel 'categories' dan 'notes' secara otomatis
    Base.metadata.create_all(bind=engine)
    apply_seed_if_needed()

@app.get("/")
async def root() -> FileResponse:
    return FileResponse("frontend/index.html")

# Registrasi Routers
app.include_router(categories_router.router)
app.include_router(notes_router.router)
app.include_router(action_items_router.router)