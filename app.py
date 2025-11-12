from flask import Flask, render_template, request, redirect, url_for
import sqlite3, os

app = Flask(__name__)

# --- Database setup ---
DB = "database.db"
if not os.path.exists(DB):
    conn = sqlite3.connect(DB)
    conn.execute('CREATE TABLE reminders (id INTEGER PRIMARY KEY, name TEXT, dosage TEXT, time TEXT)')
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT * FROM reminders")
    reminders = cur.fetchall()
    conn.close()
    return render_template("index.html", reminders=reminders)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    dosage = request.form['dosage']
    time = request.form['time']
    conn = sqlite3.connect(DB)
    conn.execute("INSERT INTO reminders (name, dosage, time) VALUES (?, ?, ?)", (name, dosage, time))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)