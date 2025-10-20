# CÓDIGO COMPLETO E COMENTADO
"""
ViewModel para a RegisterView.
"""
import flet as ft
from src.database import auth_queries
from typing import Optional

class RegisterViewModel:
    
    def __init__(self, page: ft.Page):
        self.page = page
        
        # Referências da View
        self.name_field: Optional[ft.TextField] = None
        self.email_field: Optional[ft.TextField] = None
        self.password_field: Optional[ft.TextField] = None

    def set_controls(self, name_field, email_field, password_field):
        """Recebe as referências dos controles da View."""
        self.name_field = name_field
        self.email_field = email_field
        self.password_field = password_field

    def _show_overlay_feedback(self, message: str, is_error: bool = True):
        """
        Usa o page.overlay (via SnackBar) para feedback,
        conforme diretriz da Sprint 1.
        """
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=ft.Colors.RED_600 if is_error else ft.Colors.GREEN_600,
            duration=3000
        )
        self.page.snack_bar.open = True
        self.page.update()

    def on_register_click(self, e):
        """Lógica de registro."""
        if not self._validate_inputs():
            return

        name = self.name_field.value.strip()
        email = self.email_field.value.strip()
        password = self.password_field.value
        
        # Chama a camada de Queries
        user = auth_queries.register_user(name, email, password)
        
        if user:
            print(f"Registro bem-sucedido: {user.full_name}")
            self._show_overlay_feedback(
                "Registro realizado com sucesso! Redirecionando...",
                is_error=False
            )
            # Redireciona para o login
            self.page.go("/login")

        else:
            self._show_overlay_feedback("Este email já está em uso.")
        
    def on_navigate_to_login(self, e):
        """Navega de volta para a tela de login."""
        self.page.go("/login")

    def _validate_inputs(self) -> bool:
        """Validação dos campos de registro (usa error_text inline)."""
        name_valid = self.name_field.value is not None and len(self.name_field.value.strip()) > 2
        email_valid = self.email_field.value is not None and "@" in self.email_field.value
        pass_valid = self.password_field.value is not None and len(self.password_field.value) >= 6
        
        self.name_field.error_text = None if name_valid else "Nome deve ter > 2 caracteres."
        self.email_field.error_text = None if email_valid else "Email inválido."
        self.password_field.error_text = None if pass_valid else "Senha deve ter >= 6 caracteres."
        
        self.page.update()
        return name_valid and email_valid and pass_valid