from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Configuración de la base de datos
DB_PATH = 'database.db'

def conectar_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Crear tabla al iniciar
with conectar_db() as con:
    con.execute('CREATE TABLE IF NOT EXISTS noticias (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT, sentimiento TEXT)')

@app.route('/')
def index():
    con = conectar_db()
    noticias = con.execute('SELECT * FROM noticias ORDER BY id DESC').fetchall()
    return render_template('index.html', noticias=noticias)

@app.route('/agregar', methods=['POST'])
def agregar():
    titulo = request.form.get('titulo')
    sentimiento = request.form.get('sentimiento')
    if titulo:
        with conectar_db() as con:
            con.execute('INSERT INTO noticias (titulo, sentimiento) VALUES (?, ?)', (titulo, sentimiento))
    return redirect('/')

if __name__ == '__main__':
    # Puerto dinámico para que Render no falle
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)