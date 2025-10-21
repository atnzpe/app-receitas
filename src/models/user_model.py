# CÓDIGO COMPLETO E COMENTADO
from dataclasses import dataclass
from typing import Optional

"""
Definição do Model 'User'.
"""

@dataclass
class User:
    """
    Modelo para um usuário.
    Representa um usuário autenticado na aplicação.
    """
    id: int
    full_name: str
    email: str
    # O hashed_password NUNCA deve ser armazenado neste objeto
    # após a autenticação, por motivos de segurança.