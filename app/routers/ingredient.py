from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Ingrediente, Usuario
from app.schemas.ingredient import IngredientCreate, IngredientUpdate, IngredientResponse
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/ingredients", tags=["Inventario de Ingredientes"])

@router.post("/", response_model=IngredientResponse, status_code=status.HTTP_201_CREATED)
def create_ingredient(
    ingredient_data: IngredientCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    new_ingredient = Ingrediente(
        user_id=current_user.id,
        nombre=ingredient_data.nombre.strip(),
        cantidad=ingredient_data.cantidad,
        unidad=ingredient_data.unidad.strip()
    )
    db.add(new_ingredient)
    db.commit()
    db.refresh(new_ingredient)
    return new_ingredient

@router.get("/", response_model=List[IngredientResponse])
def list_ingredients(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return db.query(Ingrediente).filter(Ingrediente.user_id == current_user.id).all()

@router.put("/{ingredient_id}", response_model=IngredientResponse)
def update_ingredient(
    ingredient_id: int,
    ingredient_data: IngredientUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    ingredient = db.query(Ingrediente).filter(
        Ingrediente.id == ingredient_id,
        Ingrediente.user_id == current_user.id
    ).first()

    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingrediente no encontrado en tu inventario"
        )

    update_fields = ingredient_data.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        if isinstance(value, str):
            value = value.strip()
        setattr(ingredient, field, value)

    db.commit()
    db.refresh(ingredient)
    return ingredient

@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingredient(
    ingredient_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    ingredient = db.query(Ingrediente).filter(
        Ingrediente.id == ingredient_id,
        Ingrediente.user_id == current_user.id
    ).first()

    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingrediente no encontrado en tu inventario"
        )

    db.delete(ingredient)
    db.commit()
    return None