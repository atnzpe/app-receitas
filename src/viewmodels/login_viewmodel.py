# ARQUIVO: src/viewmodels/login_viewmodel.py
import logging
from typing import Optional
import flet as ft
from src.database import auth_queries

logger = logging.getLogger("src.viewmodels.login")


class LoginViewModel:
    def __init__(self, page: ft.Page):
        self.page = page
        logger.debug("LoginViewModel inicializado.")
        self.email_field: Optional[ft.TextField] = None
        self.password_field: Optional[ft.TextField] = None

    def set_controls(self, email, password):
        """Vincula campos da view ao viewmodel."""
        self.email_field = email
        self.password_field = password

    def _show_snackbar(self, msg, is_error=True):
        """Exibe feedback visual."""
        try:
            color = ft.Colors.RED if is_error else ft.Colors.GREEN
            # Cria um novo SnackBar a cada vez para evitar erros de referência
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(msg), bgcolor=color)
            self.page.snack_bar.open = True
            self.page.update()
        except Exception as e:
            logger.error(f"Erro ao mostrar SnackBar: {e}")

    def on_login_click(self, e):
        """Processa o clique no botão de login."""
        logger.debug("Botão Login clicado.")
        try:
            # 1. Limpa erros visuais anteriores
            if self.email_field:
                self.email_field.error_text = None
            if self.password_field:
                self.password_field.error_text = None
            self.page.update()

            # 2. Obtém valores
            email = self.email_field.value.strip() if self.email_field else ""
            password = self.password_field.value if self.password_field else ""

            # 3. Validação básica
            if not email or not password:
                logger.warning("Campos vazios no login.")
                if not email and self.email_field:
                    self.email_field.error_text = "Obrigatório."
                if not password and self.password_field:
                    self.password_field.error_text = "Obrigatório."
                self.page.update()
                return

            # 4. Autenticação no Banco
            logger.debug(f"Consultando banco para: {email}")
            user = auth_queries.get_user_by_email_and_password(email, password)

            # 5. Decisão
            if user:
                logger.info(f"Login AUTORIZADO para: {user.email}")

                # Salva na sessão
                self.page.data["logged_in_user"] = user

                # Feedback
                self._show_snackbar("Bem-vindo!", is_error=False)

                # NAVEGAÇÃO CRÍTICA
                logger.info(">>> NAVEGANDO PARA DASHBOARD (/) <<<")
                self.page.go("/")

            else:
                logger.warning(f"Login NEGADO para: {email}")
                if self.password_field:
                    self.password_field.error_text = "Credenciais inválidas."
                self.page.update()

        except Exception as ex:
            logger.critical(f"Erro no fluxo de login: {ex}", exc_info=True)
            self._show_snackbar("Erro interno no sistema.")

    def on_navigate_to_register(self, e):
        logger.debug("Navegando para Registro.")
        self.page.go("/register")
