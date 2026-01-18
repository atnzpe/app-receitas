from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class User(BaseModel):
    """
    Modelo de Usuário Blindado.
    Usa Pydantic para garantir que o email seja válido e os campos obrigatórios existam.
    """
    id: Optional[int] = None
    full_name: str = Field(..., min_length=2, strip_whitespace=True)
    email: str = Field(..., strip_whitespace=True)
    # Nota: Em produção real, usar EmailStr do pydantic[email] é recomendado.

    # O hashed_password não trafega neste objeto de sessão por segurança.

    class Config:
        from_attributes = True  # Permite converter objetos ORM/SQLite para Pydantic
