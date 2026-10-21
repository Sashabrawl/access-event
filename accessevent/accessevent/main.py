from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    if request.method == "POST":
        note_text = request.form.get("note")
        if note_text:
            c.execute("INSERT INTO notes (text) VALUES (?)", (note_text,))
            conn.commit()
        return redirect("/")

    c.execute("SELECT * FROM notes")
    notes = c.fetchall()
    conn.close()

    html = '''
    <h1>Мои заметки</h1>
    <form method="POST">
        <input type="text" name="note" placeholder="Напишите заметку" required>
        <button type="submit">Добавить</button>
    </form>
    <ul>
    '''
    for note in notes:
        html += f"<li>{note[1]}</li>"
    html += "</ul>"
    
    return html

if __name__ == "__main__":
    app.run(debug=True, port=5003)
