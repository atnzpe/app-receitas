# CÓDIGO ATUALIZADO (PYDANTIC V2)
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class User(BaseModel):
    """
    Modelo de Usuário Blindado (Pydantic V2).
    """
    # Configuração moderna V2: remove espaços de strings automaticamente
    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True
    )

    id: Optional[int] = None
    # 'min_length' continua válido no Field
    full_name: str = Field(..., min_length=2)
    email: str = Field(...)
