from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional


class Ingredient(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=2)
    quantity: str = Field(default="a gosto")
    recipe_id: int

    class Config:
        from_attributes = True


class Category(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=2)

    class Config:
        from_attributes = True


class Recipe(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., min_length=3, description="Título da receita")
    instructions: str = ""
    category_id: Optional[int] = None
    prep_time_minutes: Optional[int] = Field(
        None, ge=0)  # Deve ser maior ou igual a 0
    source_url: Optional[str] = None
    image_path: Optional[str] = None

    # Campos calculados ou aninhados
    ingredients: List[Ingredient] = []
    category_name: Optional[str] = None

    class Config:
        from_attributes = True
