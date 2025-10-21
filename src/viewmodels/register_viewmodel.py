# CÓDIGO COMPLETO E COMENTADO
"""
ViewModel para a RegisterView.
Contém a lógica de registro de novos usuários.
"""

import logging
from typing import Optional
import flet as ft

from src.database import auth_queries  # Camada de dados

logger = logging.getLogger(__name__)


class RegisterViewModel:

    def __init__(self, page: ft.Page):
        self.page = page
        logger.debug("RegisterViewModel inicializado.")

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
        """Usa o page.overlay (via SnackBar) para feedback."""
        logger.debug(
            f"Exibindo SnackBar (Overlay). Erro={is_error}. Msg='{message}'")
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=self.page.theme.color_scheme.error if is_error else ft.Colors.GREEN_600,
            duration=3000
        )
        self.page.snack_bar.open = True
        self.page.update()

    def on_register_click(self, e):
        """Lógica de registro."""
        logger.debug("Evento on_register_click disparado.")
        try:
            if not self._validate_inputs():
                logger.warning("Validação de registro falhou.")
                return

            name = self.name_field.value.strip()
            email = self.email_field.value.strip()
            password = self.password_field.value

            # Chama a camada de Queries
            logger.debug(f"Chamando auth_queries para registrar: {email}")
            user = auth_queries.register_user(name, email, password)

            if user:
                # Log de sucesso já é feito em auth_queries
                self._show_overlay_feedback(
                    "Registro realizado com sucesso! Redirecionando...",
                    is_error=False
                )
                self.page.go("/login")  # Redireciona para o login
            else:
                # Log de falha (email duplicado) já é feito em auth_queries
                self._show_overlay_feedback("Este email já está em uso.")

        except Exception as ex:
            logger.error(
                f"Erro inesperado em on_register_click: {ex}", exc_info=True)
            self._show_overlay_feedback(
                "Ocorreu um erro inesperado ao registrar.")

    def on_navigate_to_login(self, e):
        """Navega de volta para a tela de login."""
        logger.debug(
            "Evento on_navigate_to_login disparado. Navegando para /login.")
        self.page.go("/login")

    def _validate_inputs(self) -> bool:
        """Validação inline dos campos de registro."""
        name_valid = self.name_field.value and len(
            self.name_field.value.strip()) > 2
        email_valid = self.email_field.value and "@" in self.email_field.value
        pass_valid = self.password_field.value and len(
            self.password_field.value) >= 6

        self.name_field.error_text = None if name_valid else "Nome deve ter > 2 caracteres."
        self.email_field.error_text = None if email_valid else "Email inválido."
        self.password_field.error_text = None if pass_valid else "Senha deve ter >= 6 caracteres."

        self.page.update()
        return name_valid and email_valid and pass_valid
