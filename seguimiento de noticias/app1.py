from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Función para conectar a la base de datos
def conectar_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Crear la tabla si no existe
with conectar_db() as con:
    con.execute('CREATE TABLE IF NOT EXISTS noticias (id INTEGER PRIMARY KEY, titulo TEXT, sentimiento TEXT)')

@app.route('/')
def index():
    con = conectar_db()
    noticias = con.execute('SELECT * FROM noticias').fetchall()
    return render_template('index.html', noticias=noticias)

@app.route('/agregar', methods=['POST'])
def agregar():
    titulo = request.form['titulo']
    sentimiento = request.form['sentimiento']
    with conectar_db() as con:
        con.execute('INSERT INTO noticias (titulo, sentimiento) VALUES (?, ?)', (titulo, sentimiento))
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)