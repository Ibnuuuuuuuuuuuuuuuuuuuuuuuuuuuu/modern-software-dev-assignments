# Intent
Menjalankan pemeriksaan kualitas menyeluruh (Formatting, Linting, dan Testing) serta memberikan ringkasan kelayakan kode.

# Steps
1. Jalankan `black .` untuk merapikan format kode.
2. Jalankan `ruff check .` untuk memeriksa standar penulisan.
3. Jalankan `pytest` untuk memastikan semua fitur berfungsi normal.

# Output
Berikan laporan singkat:
- **Format:** OK/Error
- **Linting:** OK/Error
- **Tests:** (Jumlah passed/failed)
Jika ada yang gagal, berikan rekomendasi perbaikan spesifik.