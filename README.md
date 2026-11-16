# Generador de Recetas con Inventario e IA

Aplicación web funcional desarrollada con **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **JWT** y **Groq API (`llama-3.3-70b-versatile`)** que permite a los usuarios registrar su inventario de ingredientes disponibles y generar recetas estructuradas mediante inteligencia artificial, gestionarlas en su historial personal, calificarlas de 1 a 5 estrellas y eliminarlas.

---

## Arquitectura y Stack Tecnológico

* **Backend:** Python 3.13 + FastAPI (API REST documentada con Swagger/OpenAPI)
* **Base de Datos:** PostgreSQL + SQLAlchemy ORM
* **Autenticación y Seguridad:** JWT (JSON Web Tokens) + Hashing de contraseñas con Bcrypt
* **Inteligencia Artificial:** Groq API (`llama-3.3-70b-versatile`) encapsulado en `app/llm_service.py` con salida estricta en JSON
* **Frontend:** HTML + Jinja2 + CSS minimalista con Favicon integrado
* **Pruebas Automatizadas:** Pytest
* **Contenedores y Despliegue:** Docker + Docker Compose + Nginx + SSL (Let's Encrypt) en VPS

---

## Estructura del Proyecto

```text
proyecto-recetas/
├── app/
│   ├── models/          # Modelos relacionales SQLAlchemy (usuarios, ingredientes, recetas, calificaciones)
│   ├── routers/         # Endpoints de la API REST (auth, ingredients, recipes)
│   ├── schemas/         # Esquemas de validación de datos con Pydantic
│   ├── services/        # Lógica de negocio y autenticación JWT
│   ├── static/          # Archivos estáticos (CSS y favicon.ico)
│   ├── templates/       # Plantillas HTML con Jinja2
│   ├── tests/           # Pruebas unitarias y de integración con pytest
│   ├── database.py      # Configuración de conexión y sesión con PostgreSQL
│   ├── llm_service.py   # Servicio encapsulado de conexión y parseo JSON con Groq LLM
│   └── main.py          # Punto de entrada de la aplicación FastAPI
├── Dockerfile           # Imagen de producción para el backend FastAPI
├── docker-compose.yml   # Orquestación de servicios separados (web + db)
├── pytest.ini           # Configuración del entorno de pruebas
├── requirements.txt     # Dependencias del proyecto Python
├── .env.example         # Plantilla de variables de entorno requeridas
└── README.md            # Documentación completa del proyecto
```

---

## Variables de Entorno

Antes de ejecutar la aplicación, crea un archivo `.env` en la raíz del proyecto basado en `.env.example`:

```env
DATABASE_URL=postgresql://postgres:postgres_password@db:5432/recetas_db
JWT_SECRET_KEY=cambiar_esta_llave_secreta_por_una_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
GROQ_API_KEY=tu_api_key_de_groq_aqui
```

---

## Guía de Instalación y Ejecución Local (Desarrollo)

### 1. Clonar el repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd proyecto-recetas
```

### 2. Crear y activar el entorno virtual
```bash
python -m venv venv
```
* **En Windows (PowerShell):**
  ```powershell
  venv\Scripts\Activate.ps1
  ```
* **En Linux / macOS:**
  ```bash
  source venv/bin/activate
  ```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno locales
Copia `.env.example` a `.env` y asegúrate de apuntar `DATABASE_URL` a tu instancia local de PostgreSQL (por ejemplo `localhost:5432`) e incluir tu `GROQ_API_KEY` válida:
```bash
cp .env.example .env
```

### 5. Ejecutar el servidor de desarrollo
```bash
uvicorn app.main:app --reload
```
* **Interfaz Web:** `http://127.0.0.1:8000`
* **Documentación Interactiva (Swagger UI):** `http://127.0.0.1:8000/docs`

---

## Ejecución con Docker y Docker Compose (Producción)

Para levantar tanto la aplicación FastAPI como la base de datos PostgreSQL en contenedores separados:

1. Asegúrate de tener configurado tu archivo `.env` en la raíz del proyecto.
2. Construye e inicia los contenedores en segundo plano:
   ```bash
   docker-compose up --build -d
   ```
3. Verifica que ambos servicios (`web` y `db`) estén corriendo correctamente:
   ```bash
   docker-compose ps
   ```

---

## Ejecución de Pruebas Automatizadas (Pytest)

Para validar los esquemas, la generación de prompts, el parseo JSON del LLM y los endpoints de la API:

```bash
pytest -v
```

---
