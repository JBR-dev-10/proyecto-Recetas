import os
import sys
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import engine
from app.models import models
from app.routers import auth, ingredient, recipes, rating

# Asegura que la carpeta static exista para evitar errores al montar
os.makedirs("app/static", exist_ok=True)

if "pytest" not in sys.modules:
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

templates = Jinja2Templates(directory="app/templates")

app.include_router(auth.router)
app.include_router(ingredient.router)
app.include_router(recipes.router)
app.include_router(rating.router)


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="panel.html")


@app.get("/panel", response_class=HTMLResponse)
def view_panel(request: Request):
    return templates.TemplateResponse(request=request, name="panel.html")


@app.get("/health")
def health_check():
    return {"status": "ok"}