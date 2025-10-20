# CÓDIGO COMPLETO E COMENTADO
from dataclasses import dataclass, field
from typing import List, Optional

"""
Definição dos 'Models' da aplicação.

No padrão MVVM, o Model representa os dados e a lógica de negócio.
Eles são "POPOs" (Plain Old Python Objects).
Usaremos dataclasses para uma definição clara, limpa e tipada.
Estes models são o "contrato" de dados entre o Banco de Dados e os ViewModels.
"""

@dataclass
class Ingredient:
    """Modelo para um ingrediente."""
    id: Optional[int]
    name: str
    quantity: str  # Ex: "200g", "1 xícara", "a gosto"
    recipe_id: int # Chave estrangeira para a Receita

@dataclass
class Category:
    """Modelo para uma categoria de receita."""
    id: Optional[int]
    name: str

@dataclass
class Recipe:
    """Modelo principal para uma receita."""
    id: Optional[int]
    title: str
    instructions: str
    category_id: Optional[int]
    prep_time_minutes: Optional[int]
    source_url: Optional[str]
    image_path: Optional[str] # Caminho local para a imagem (offline-first)
    
    # Estes campos são preenchidos separadamente pelo ViewModel
    ingredients: List[Ingredient] = field(default_factory=list)
    category_name: Optional[str] = None