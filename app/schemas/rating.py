from pydantic import BaseModel, Field
from typing import Optional

class RatingCreate(BaseModel):
    puntuacion: int = Field(..., ge=1, le=5, example=5)
    comentario: Optional[str] = Field(default=None, max_length=500, example="Quedó excelente y muy rápido de preparar")

class RatingResponse(BaseModel):
    id: int
    user_id: int
    receta_id: int
    puntuacion: int
    comentario: Optional[str] = None

    class Config:
        from_attributes = True