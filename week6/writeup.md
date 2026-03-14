# Week 6 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **TODO** \
SUNet ID: **TODO** \
Citations: **TODO**

This assignment took me about **TODO** hours to do. 


## Brief findings overview 
> TODO

Fix #1
a. File and line(s)

backend/app/routers/notes.py (Baris 71-79)

b. Rule/category Semgrep flagged

python.sqlalchemy.security.audit.avoid-sqlalchemy-text

c. Brief risk description

Penggunaan f-string dalam query SQL manual memungkinkan penyerang melakukan SQL Injection, di mana mereka bisa memanipulasi perintah database untuk melihat, mengubah, atau menghapus data sensitif.

d. Your change (short code diff or explanation, AI coding tool usage)

Mengubah query string menjadi parameterized query dengan placeholder :q dan mengirimkan variabel sebagai kamus (dictionary) pada fungsi db.execute().

e. Why this mitigates the issue

Mitigasi ini memastikan bahwa input dari pengguna dianggap sebagai data (string) murni oleh mesin database, bukan sebagai bagian dari perintah yang bisa dieksekusi.

Fix #2
a. File and line(s)

backend/app/routers/notes.py (Baris 104)

b. Rule/category Semgrep flagged

python.lang.security.audit.eval-detected

c. Brief risk description

Fungsi eval() mengeksekusi string apa pun sebagai kode Python. Hal ini sangat berbahaya karena dapat menyebabkan Remote Code Execution (RCE) jika input dikontrol oleh pihak luar.

d. Your change (short code diff or explanation, AI coding tool usage)

Mengganti fungsi eval() dengan ast.literal_eval() untuk membatasi evaluasi hanya pada struktur data statis Python (seperti list atau dict), bukan kode yang dapat dieksekusi.

e. Why this mitigates the issue

ast.literal_eval tidak mendukung operasi fungsi atau pemanggilan sistem, sehingga menutup celah eksekusi kode berbahaya secara paksa.

Fix #3
a. File and line(s)

backend/app/routers/notes.py (Baris 112)

b. Rule/category Semgrep flagged

python.lang.security.audit.subprocess-shell-true

c. Brief risk description

Penggunaan subprocess.run dengan shell=True memungkinkan penyerang menyisipkan perintah terminal tambahan (Command Injection) melalui karakter seperti & atau ;.

d. Your change (short code diff or explanation, AI coding tool usage)

Menggunakan shlex.split(cmd) untuk memecah perintah menjadi daftar argumen dan mengatur parameter shell=False.

e. Why this mitigates the issue

Dengan shell=False, sistem hanya akan menjalankan program utama yang ditentukan tanpa melalui perantara shell (seperti bash/cmd), sehingga perintah tambahan yang disisipkan penyerang tidak akan dieksekusi.

Fix #4
a. File and line(s)

backend/app/main.py (Baris 24)

b. Rule/category Semgrep flagged

python.fastapi.security.wildcard-cors.wildcard-cors

c. Brief risk description

Penggunaan wildcard (*) pada CORS memungkinkan domain asing mana pun untuk berinteraksi dengan API, yang bisa disalahgunakan dalam serangan Cross-Site Request Forgery.

d. Your change

Membatasi allow_origins hanya untuk http://localhost:8000 dan http://127.0.0.1:8000.

e. Why this mitigates the issue

Memastikan hanya aplikasi frontend resmi saja yang diizinkan untuk melakukan permintaan data ke server backend.

Fix #5
a. File and line(s)

backend/app/routers/notes.py (Baris 122)

b. Rule/category Semgrep flagged

python.lang.security.audit.dynamic-urllib-use-detected

c. Brief risk description

urllib.request.urlopen mendukung skema file://, sehingga penyerang bisa mengirimkan URL yang memaksa server membaca file sistem internal (Server-Side Request Forgery).

d. Your change

Mengganti urllib dengan library requests dan menambahkan validasi skema URL (http:// atau https://).

e. Why this mitigates the issue

Membatasi akses server hanya ke protokol web luar dan mencegah akses ilegal ke sistem file lokal.