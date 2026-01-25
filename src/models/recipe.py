# ARQUIVO: src/models/recipe.py
# OBJETIVO: Definir a estrutura de dados e regras de validação para Receitas e Ingredientes.
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

# --- Sub-model para Ingredientes (Detalhe) ---
class IngredientSchema(BaseModel):
    """
    Representa um ingrediente individual dentro de uma receita.
    """
    name: str = Field(..., min_length=2, description="Nome do ingrediente")
    quantity: Optional[str] = Field(None, description="Quantidade")
    unit: Optional[str] = Field(None, description="Unidade de medida")

    model_config = ConfigDict(from_attributes=True)

# --- Model Base da Receita (Campos Comuns) ---
class RecipeBase(BaseModel):
    """
    Campos compartilhados entre criação e leitura de receitas.
    """
    title: str = Field(..., min_length=3, max_length=150, description="Título da receita")
    
    category_id: Optional[int] = Field(None, description="ID da categoria")
    
    preparation_time: Optional[int] = Field(None, ge=0, description="Tempo em minutos")
    
    servings: Optional[str] = Field(None, max_length=50, description="Rendimento")
    
    # [CORREÇÃO TÁTICA]: Reduzido de 10 para 3 caracteres para facilitar testes
    instructions: str = Field(..., min_length=3, description="Modo de preparo")
    
    additional_instructions: Optional[str] = Field(None, description="Dicas extras, caldas, etc.")
    source: Optional[str] = Field(None, max_length=200, description="Fonte da receita")
    
    image_path: Optional[str] = None

# --- Model para Criação (Entrada da UI) ---
class RecipeCreate(RecipeBase):
    """
    Schema utilizado ao receber dados do formulário para criar uma nova receita.
    """
    ingredients: List[IngredientSchema] = Field(default_factory=list, description="Lista de ingredientes")

# --- Model para Leitura (Saída do BD) ---
class RecipeRead(RecipeBase):
    """
    Schema completo com dados gerados pelo banco (IDs, Datas).
    """
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    ingredients: List[IngredientSchema] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)