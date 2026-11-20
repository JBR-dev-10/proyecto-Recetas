from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Ingrediente, Receta, Usuario
from app.schemas.recipe import RecipeGenerateRequest, RecipeResponse
from app.services.auth_service import get_current_user
from app.services.llm_service import generate_recipe_from_ingredients

router = APIRouter(prefix="/recipes", tags=["Recetas con IA"])

@router.post("/generate", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
def generate_recipe(
    request_data: RecipeGenerateRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    ingredient_names = []

    if request_data.usar_inventario:
        user_ingredients = db.query(Ingrediente).filter(Ingrediente.user_id == current_user.id).all()
        ingredient_names.extend([f"{item.cantidad} {item.unidad} de {item.nombre}" for item in user_ingredients])

    if request_data.ingredientes_extra:
        ingredient_names.extend([ing.strip() for ing in request_data.ingredientes_extra if ing.strip()])

    if not ingredient_names:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes tener ingredientes en tu inventario o enviar ingredientes_extra para generar una receta."
        )

    try:
        recipe_data = generate_recipe_from_ingredients(
            ingredients=ingredient_names,
            preferences=request_data.preferencias
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc)
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error al comunicarse con el servicio de IA: {str(exc)}"
        )

    new_recipe = Receta(
        user_id=current_user.id,
        nombre_plato=recipe_data["nombre_plato"],
        ingredientes_json=recipe_data["ingredientes_json"],
        pasos_json=recipe_data["pasos_json"],
        tiempo_estimado=recipe_data["tiempo_estimado"],
        dificultad=recipe_data["dificultad"]
    )
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe

@router.get("/", response_model=List[RecipeResponse])
def list_recipes(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return db.query(Receta).filter(Receta.user_id == current_user.id).all()

@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    recipe = db.query(Receta).filter(
        Receta.id == recipe_id,
        Receta.user_id == current_user.id
    ).first()
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receta no encontrada"
        )
    return recipe