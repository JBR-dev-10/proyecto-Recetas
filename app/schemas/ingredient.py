from pydantic import BaseModel, Field
from typing import Optional

class IngredientBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, example="Arroz")
    cantidad: float = Field(..., gt=0, example=2.0)
    unidad: str = Field(..., min_length=1, max_length=50, example="tazas")

class IngredientCreate(IngredientBase):
    pass

class IngredientUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    cantidad: Optional[float] = Field(None, gt=0)
    unidad: Optional[str] = Field(None, min_length=1, max_length=50)

class IngredientResponse(IngredientBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True