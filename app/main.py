import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.database import engine
from app.models import models

# Asegura que la carpeta static exista para evitar errores al montar
os.makedirs("app/static", exist_ok=True)

try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Aviso de conexión DB: {e}")

app = FastAPI(
    title="Generador de Recetas con Inventario e IA",
    description="API REST y aplicación web para gestión de inventario y generación de recetas mediante LLM.",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Recetas IA - Inventario Inteligente</title>
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
        <style>
            body { font-family: system-ui, -apple-system, sans-serif; background: #f4f6f9; color: #1e293b; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .card { background: white; padding: 2.5rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); max-width: 520px; text-align: center; }
            h1 { color: #0f172a; margin-bottom: 0.5rem; }
            p { color: #475569; line-height: 1.6; }
            .badge { display: inline-block; background: #dcfce7; color: #166534; padding: 0.3rem 0.8rem; border-radius: 999px; font-size: 0.85rem; font-weight: 600; margin-bottom: 1rem; }
            .btn { display: inline-block; margin-top: 1.2rem; background: #2563eb; color: white; text-decoration: none; padding: 0.75rem 1.5rem; border-radius: 8px; font-weight: 600; }
        </style>
    </head>
    <body>
        <div class="card">
            <span class="badge">● Sistema Activo en Producción (HTTPS)</span>
            <h1>Generador de Recetas con IA</h1>
            <p>Plataforma backend con FastAPI, PostgreSQL y Groq LLM para gestión de inventario personal y generación estructurada de recetas.</p>
            <a href="/docs" class="btn">Explorar API en Swagger UI (/docs)</a>
        </div>
    </body>
    </html>
    """

@app.get("/health")
def health_check():
    return {"status": "ok"}