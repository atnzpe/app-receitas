# CÓDIGO COMPLETO E COMENTADO
"""
ViewModel para a LoginView.
Contém o estado (email, senha) e a lógica de autenticação.
"""
import logging
from typing import Optional
import flet as ft # Importado apenas para tipagem e page actions

from src.database import auth_queries # Camada de dados

logger = logging.getLogger(__name__)

class LoginViewModel:
    
    def __init__(self, page: ft.Page):
        """
        O ViewModel precisa da 'page' para:
        1. Navegação (page.go)
        2. Overlays (page.snack_bar)
        3. Sessão (page.session)
        """
        self.page = page
        logger.debug("LoginViewModel inicializado.")
        
        # Referências aos controles da View (para ler valores)
        self.email_field: Optional[ft.TextField] = None
        self.password_field: Optional[ft.TextField] = None

    def set_controls(self, email_field: ft.TextField, password_field: ft.TextField):
        """Recebe as referências dos controles da View."""
        self.email_field = email_field
        self.password_field = password_field

    def _show_overlay_feedback(self, message: str, is_error: bool = True):
        """Usa o page.overlay (via SnackBar) para feedback."""
        logger.debug(f"Exibindo SnackBar (Overlay). Erro={is_error}. Msg='{message}'")
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=self.page.theme.color_scheme.error if is_error else ft.Colors.GREEN_600,
            duration=3000
        )
        self.page.snack_bar.open = True
        self.page.update()

    def on_login_click(self, e):
        """Lógica executada quando o botão 'Entrar' é clicado."""
        logger.debug("Evento on_login_click disparado.")
        try:
            if not self._validate_inputs():
                logger.warning("Validação de login falhou.")
                return

            email = self.email_field.value.strip()
            password = self.password_field.value
            
            # Chama a camada de Queries
            logger.debug(f"Chamando auth_queries para autenticar: {email}")
            user = auth_queries.get_user_by_email_and_password(email, password)
            
            if user:
                logger.info(f"Login bem-sucedido para usuário ID: {user.id}")
                self.page.session.clear()
                self.page.session.set("logged_in_user", user)
                self.page.go("/") # Navega para o Dashboard
            else:
                # Log de falha já é feito em auth_queries
                self._show_overlay_feedback("Email ou senha inválidos.")
        
        except Exception as ex:
            logger.error(f"Erro inesperado em on_login_click: {ex}", exc_info=True)
            self._show_overlay_feedback("Ocorreu um erro inesperado.")

    def on_navigate_to_register(self, e):
        """Navega para a tela de registro."""
        logger.debug("Evento on_navigate_to_register disparado. Navegando para /register.")
        self.page.go("/register")

    def _validate_inputs(self) -> bool:
        """Validação inline dos campos (não usa overlay)."""
        email_valid = self.email_field.value and "@" in self.email_field.value
        pass_valid = bool(self.password_field.value) # (bool(None) is False, bool("") is False)
        
        self.email_field.error_text = None if email_valid else "Email inválido."
        self.password_field.error_text = None if pass_valid else "Senha não pode estar vazia."
        
        self.page.update()
        return email_valid and pass_valid