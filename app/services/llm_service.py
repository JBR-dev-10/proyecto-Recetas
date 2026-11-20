import os
import json
from typing import List, Optional, Dict, Any
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

SYSTEM_PROMPT = """Eres un chef experto y nutricionista. Tu única función es generar recetas de cocina estructuradas a partir de los ingredientes disponibles del usuario.
Debes responder ÚNICAMENTE con un objeto JSON válido (sin markdown, sin bloques ```json y sin texto adicional antes o después) que cumpla exactamente con esta estructura:
{
  "nombre_plato": "Nombre claro y apetitoso del plato",
  "ingredientes": [
    {"nombre": "ingrediente", "cantidad": "cantidad y unidad"}
  ],
  "pasos": [
    "Paso 1 detallado",
    "Paso 2 detallado"
  ],
  "tiempo_estimado": "Ej. 25 minutos",
  "dificultad": "Fácil | Media | Difícil"
}
Prioriza los ingredientes proporcionados y respeta las preferencias del usuario si se indican."""

def generate_recipe_from_ingredients(
    ingredients: List[str],
    preferences: Optional[str] = None
) -> Dict[str, Any]:
    if not GROQ_API_KEY or GROQ_API_KEY == "pendiente_fase_5":
        raise ValueError("La variable GROQ_API_KEY no está configurada con una clave válida.")

    client = Groq(api_key=GROQ_API_KEY)

    user_content = f"Ingredientes disponibles: {', '.join(ingredients) if ingredients else 'básicos de despensa'}."
    if preferences:
        user_content += f"\nPreferencias: {preferences}."

    completion = client.chat.completions.create(
        model=GROQ_MODEL,
        temperature=0.4,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content}
        ]
    )

    raw_content = completion.choices[0].message.content
    data = json.loads(raw_content)

    return {
        "nombre_plato": str(data.get("nombre_plato", "Receta generada")),
        "ingredientes_json": data.get("ingredientes", []),
        "pasos_json": data.get("pasos", []),
        "tiempo_estimado": str(data.get("tiempo_estimado", "30 minutos")),
        "dificultad": str(data.get("dificultad", "Media"))
    }