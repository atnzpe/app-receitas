# CÓDIGO COMPLETO E COMENTADO
from dataclasses import dataclass
from typing import Optional

"""
Definição do Model 'User'.
Separado do recipe_model para melhor organização das responsabilidades.
"""

@dataclass
class User:
    """Modelo para um usuário."""
    id: int
    full_name: str
    email: str
    # O hashed_password NUNCA deve ser armazenado no objeto
    # após a autenticação por motivos de segurança.
    # O objeto User representa um usuário logado.