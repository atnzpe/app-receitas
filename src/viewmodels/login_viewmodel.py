# CÓDIGO ATUALIZADO
import flet as ft
from typing import Optional
from src.core.logger import get_logger
from src.database import auth_queries

logger = get_logger("src.viewmodels.login")


class LoginViewModel:
    def __init__(self, page: ft.Page):
        self.page = page
        self.email_field: Optional[ft.TextField] = None
        self.password_field: Optional[ft.TextField] = None

    def set_controls(self, email_field, password_field):
        self.email_field = email_field
        self.password_field = password_field

    def _show_overlay(self, msg: str, is_error: bool = True):
        color = self.page.theme.color_scheme.error if is_error else ft.Colors.GREEN_600
        self.page.snack_bar = ft.SnackBar(content=ft.Text(msg), bgcolor=color)
        self.page.snack_bar.open = True
        self.page.update()

    def on_login_click(self, e):
        try:
            email = self.email_field.value.strip()
            password = self.password_field.value

            if not email or not password:
                self._show_overlay("Preencha todos os campos.")
                return

            logger.info(f"Tentando login: {email}")
            user = auth_queries.get_user_by_email_and_password(email, password)

            if user:
                # CORREÇÃO: Usando page.data para persistência em memória
                if self.page.data is None:
                    self.page.data = {}
                self.page.data["logged_in_user"] = user

                logger.info(f"Sessão iniciada: {user.email}")
                self.page.go("/")
            else:
                self._show_overlay("Credenciais inválidas.")

        except Exception as ex:
            logger.error(f"Erro no login: {ex}", exc_info=True)
            self._show_overlay("Erro interno.")

    def on_navigate_to_register(self, e):
        self.page.go("/register")
