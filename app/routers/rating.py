from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Calificacion, Receta, Usuario
from app.schemas.rating import RatingCreate, RatingResponse
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/recipes/{recipe_id}/ratings", tags=["Calificaciones de Recetas"])

@router.post("/", response_model=RatingResponse, status_code=status.HTTP_201_CREATED)
def create_or_update_rating(
    recipe_id: int,
    rating_data: RatingCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    recipe = db.query(Receta).filter(Receta.id == recipe_id).first()
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La receta especificada no existe"
        )

    existing_rating = db.query(Calificacion).filter(
        Calificacion.receta_id == recipe_id,
        Calificacion.user_id == current_user.id
    ).first()

    if existing_rating:
        existing_rating.puntuacion = rating_data.puntuacion
        existing_rating.comentario = rating_data.comentario.strip() if rating_data.comentario else None
        db.commit()
        db.refresh(existing_rating)
        return existing_rating

    new_rating = Calificacion(
        user_id=current_user.id,
        receta_id=recipe_id,
        puntuacion=rating_data.puntuacion,
        comentario=rating_data.comentario.strip() if rating_data.comentario else None
    )
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating

@router.get("/", response_model=List[RatingResponse])
def list_recipe_ratings(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    recipe = db.query(Receta).filter(Receta.id == recipe_id).first()
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La receta especificada no existe"
        )

    return db.query(Calificacion).filter(Calificacion.receta_id == recipe_id).all()