from pydantic import BaseModel, Field
from typing import List, Optional, Any

class RecipeGenerateRequest(BaseModel):
    preferencias: Optional[str] = Field(
        default=None,
        max_length=200,
        example="Receta rápida, alta en proteína y sin gluten"
    )
    usar_inventario: bool = Field(
        default=True,
        description="Si es True, toma los ingredientes registrados del usuario"
    )
    ingredientes_extra: Optional[List[str]] = Field(
        default=None,
        example=["ajo", "aceite de oliva"]
    )

class RecipeResponse(BaseModel):
    id: int
    user_id: int
    nombre_plato: str
    ingredientes_json: Any
    pasos_json: Any
    tiempo_estimado: str
    dificultad: str

    class Config:
        from_attributes = True