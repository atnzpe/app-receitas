# ARQUIVO: src/models/recipe.py
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

# --- 1. Sub-model para Ingredientes ---


class IngredientSchema(BaseModel):
    """Schema para validação de ingredientes."""
    name: str = Field(..., min_length=2, description="Nome do ingrediente")
    quantity: Optional[str] = Field(None, description="Quantidade")
    unit: Optional[str] = Field(None, description="Unidade")

    model_config = ConfigDict(from_attributes=True)

# --- 2. Modelo Base ---


class RecipeBase(BaseModel):
    """Campos comuns da receita."""
    category_id: int = Field(..., description="ID da categoria")
    title: str = Field(..., min_length=3, max_length=5000)
    preparation_time: Optional[int] = Field(None, ge=1)
    servings: Optional[str] = Field(None)
    instructions: str = Field(..., min_length=1)

    # [SPRINT 5] Novos Campos
    additional_instructions: Optional[str] = Field(None)
    source: Optional[str] = Field(None)
    image_path: Optional[str] = Field(None, description="URL da imagem")

    model_config = ConfigDict(from_attributes=True)

# --- 3. Model Criação ---


class RecipeCreate(RecipeBase):
    """Usado na entrada de dados (UI -> Backend)."""
    ingredients: List[IngredientSchema] = Field(default_factory=list)

# --- 4. Model Leitura ---


class RecipeRead(RecipeBase):
    """Usado na saída de dados (Backend -> UI)."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    ingredients: List[IngredientSchema] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
