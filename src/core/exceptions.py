"""
Define a hierarquia de exceções da aplicação.
Isso elimina a ambiguidade de erros genéricos e permite que a UI reaja adequadamente.
"""

class AppError(Exception):
    """Classe base para todas as exceções lógicas do App."""
    def __init__(self, message: str, original_error: Exception = None):
        super().__init__(message)
        self.original_error = original_error

class DatabaseError(AppError):
    """Falha crítica relacionada ao banco de dados (conexão, integridade, queries)."""
    pass

class ValidationError(AppError):
    """Falha na validação de dados (Modelos Pydantic ou Regras de Negócio)."""
    pass

class AuthenticationError(AppError):
    """Falhas de login, sessão expirada ou credenciais inválidas."""
    pass