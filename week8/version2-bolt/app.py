from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Inisialisasi database SQLite sederhana
def init_db():
    conn = sqlite3.connect('dev.db')
    conn.execute('CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, title TEXT, content TEXT)')
    conn.close()

@app.route('/notes', methods=['GET', 'POST'])
def handle_notes():
    conn = sqlite3.connect('dev.db')
    conn.row_factory = sqlite3.Row
    if request.method == 'POST':
        data = request.json
        cur = conn.cursor()
        cur.execute('INSERT INTO notes (title, content) VALUES (?, ?)', (data['title'], data['content']))
        conn.commit()
        return jsonify({"message": "Note created successfully"}), 201
    
    notes = conn.execute('SELECT * FROM notes').fetchall()
    return jsonify([dict(ix) for ix in notes])

if __name__ == '__main__':
    init_db()
    print("Server running on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)