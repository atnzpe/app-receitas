# ARQUIVO: src/models/recipe_model.py
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional


class Ingredient(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)
    id: Optional[int] = None
    name: str = Field(..., min_length=2)
    quantity: str = Field(default="a gosto")
    recipe_id: int


class Category(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    id: Optional[int] = None
    name: str = Field(..., min_length=2)
    user_id: Optional[int] = None  # Se None, é Nativa
    is_favorite: bool = False      # Novo campo para controle de UI

    @property
    def is_native(self) -> bool:
        return self.user_id is None


class Recipe(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)
    id: Optional[int] = None
    title: str = Field(..., min_length=3)
    instructions: str = ""
    category_id: Optional[int] = None
    prep_time_minutes: Optional[int] = Field(None, ge=0)
    source_url: Optional[str] = None
    image_path: Optional[str] = None
    ingredients: List[Ingredient] = []
    category_name: Optional[str] = None
