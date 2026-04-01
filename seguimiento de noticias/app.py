import os
from flask import Flask, render_template, request, redirect, url_for
from supabase import create_client, Client

app = Flask(__name__)

# --- CONFIGURACIÓN DE TU PROYECTO (YA LISTO) ---
SUPABASE_URL = "https://pxdhodxhbfhyldbgcggv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB4ZGhvZHhoYmZoeWxkYmdjZ2d2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzUwNTE5MjQsImV4cCI6MjA5MDYyNzkyNH0.lLVdzE202u_Rao2A7sIJUFB6i6WbHi9-Fc5AahWDPq8"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    # Usamos el nombre de tu tabla: "titulo"
    try:
        # Intentamos traer los datos de la tabla que creaste
        response = supabase.table("titulo").select("*").order("id", desc=True).execute()
        noticias = response.data
    except Exception as e:
        print(f"Error al leer de Supabase: {e}")
        noticias = []
    
    return render_template('index.html', noticias=noticias)

@app.route('/agregar', methods=['POST'])
def agregar():
    titulo_form = request.form.get('titulo') 
    sentimiento = request.form.get('sentimiento')
    foto = request.files.get('foto')
    foto_url = ""

    # 1. Subir foto al Storage si seleccionaste una
    if foto:
        try:
            # Nombre único para que no se repitan fotos de tus reportes
            file_name = f"reporte_{os.urandom(3).hex()}.jpg"
            # Subimos al bucket: imagenes_reportes
            supabase.storage.from_("imagenes_reportes").upload(file_name, foto.read())
            # Obtenemos el link para que se vea en internet
            foto_url = supabase.storage.from_("imagenes_reportes").get_public_url(file_name)
        except Exception as e:
            print(f"Error con la foto: {e}")

    # 2. Guardar en la tabla "titulo"
    try:
        supabase.table("titulo").insert({
            "titulo": titulo_form, 
            "sentimiento": sentimiento, 
            "foto_url": foto_url
        }).execute()
    except Exception as e:
        print(f"Error al guardar noticia: {e}")

    return redirect(url_for('index'))

if __name__ == '__main__':
    # Configuración para que Render no falle (Puerto dinámico)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)