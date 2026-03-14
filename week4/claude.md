# Panduan QA & Pengembangan Week 4

## Perintah Kerja (Windows Failsafe)
Gunakan perintah ini karena `make` tidak tersedia:
- **Run App:** `python -m uvicorn backend.app.main:app --reload --port 8000`
- **Testing:** `pytest`
- **Formatting:** `black .` dan `ruff check --fix .`
- **Linting:** `ruff check .`

## Aturan Penjaminan Kualitas (QA Gates)
- **Test-First:** Selalu buat unit test di `backend/tests/` sebelum menambah fitur baru.
- **Strict Linting:** Jangan biarkan ada peringatan dari `ruff` atau `black`.
- **Database:** Jika mengubah skema, pastikan `data/seed.sql` diperbarui agar sinkron.