# ARQUIVO: src/viewmodels/login_viewmodel.py
# OBJETIVO: Gerenciar lógica de login com feedback visual BLINDADO (Overlay Modal).
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

        # Referência para o diálogo ativo (Evita problemas de GC)
        self.current_dialog: Optional[ft.AlertDialog] = None

    def set_controls(self, email_field, password_field):
        self.email_field = email_field
        self.password_field = password_field

    def _close_dialog(self, e):
        """Fecha o diálogo ativo e atualiza a UI."""
        if self.current_dialog:
            self.current_dialog.open = False
            self.page.update()

    def _show_feedback_modal(self, title: str, message: str, is_error: bool = True):
        """
        Exibe modal usando estratégia de Overlay (Compatibilidade Máxima).
        """
        icon = ft.Icons.ERROR_OUTLINE if is_error else ft.Icons.CHECK_CIRCLE_OUTLINE
        color = ft.Colors.RED if is_error else ft.Colors.GREEN

        # Criação do Diálogo
        dlg = ft.AlertDialog(
            title=ft.Row([
                ft.Icon(icon, color=color, size=30),
                ft.Text(title)
            ]),
            content=ft.Text(message, size=16),
            actions=[
                ft.TextButton("OK", on_click=self._close_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.current_dialog = dlg

        # Injeção no Overlay (Blindagem)
        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.update()

        logger.info(f"Modal de feedback exibido: {title} - {message}")

    def on_login_click(self, e):
        try:
            email = self.email_field.value.strip()
            password = self.password_field.value

            if not email or not password:
                self._show_feedback_modal(
                    "Atenção", "Preencha todos os campos.", is_error=True)
                return

            logger.info(f"Tentando login: {email}")
            user = auth_queries.get_user_by_email_and_password(email, password)

            if user:
                # Login Sucesso
                if self.page.data is None:
                    self.page.data = {}
                self.page.data["logged_in_user"] = user

                logger.info(f"Sessão iniciada: {user.email}")
                self.page.go("/")
            else:
                # Login Falha (Credenciais)
                # O log de warning já ocorre dentro de auth_queries, aqui exibimos o modal
                self._show_feedback_modal(
                    "Erro de Login", "Credenciais inválidas ou usuário não encontrado.", is_error=True)

        except Exception as ex:
            logger.error(f"Erro no login: {ex}", exc_info=True)
            self._show_feedback_modal(
                "Erro Crítico", f"Falha interna: {str(ex)}", is_error=True)

    def on_navigate_to_register(self, e):
        self.page.go("/register")
