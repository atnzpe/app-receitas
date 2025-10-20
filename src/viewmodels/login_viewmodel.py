# CÓDIGO COMPLETO E COMENTADO
"""
ViewModel para a LoginView.
Contém o estado (email, senha) e a lógica de autenticação.
"""
import flet as ft
from src.database import auth_queries
from typing import Optional

class LoginViewModel:
    
    def __init__(self, page: ft.Page):
        """
        O ViewModel precisa da 'page' para poder realizar a navegação (roteamento)
        e para acessar o 'overlay'.
        """
        self.page = page
        
        # Referências aos controles da View (para ler valores)
        self.email_field: Optional[ft.TextField] = None
        self.password_field: Optional[ft.TextField] = None

    def set_controls(self, email_field: ft.TextField, password_field: ft.TextField):
        """Recebe as referências dos controles da View."""
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

    def on_login_click(self, e):
        """Lógica executada quando o botão 'Entrar' é clicado."""
        if not self._validate_inputs():
            # A validação _validate_inputs() já atualiza a UI com error_text inline
            return

        email = self.email_field.value.strip()
        password = self.password_field.value
        
        # Chama a camada de Queries
        user = auth_queries.get_user_by_email_and_password(email, password)
        
        if user:
            print(f"Login bem-sucedido: {user.full_name}")
            # Limpa sessão (caso seja um re-login)
            self.page.session.clear()
            # Armazena o usuário na sessão da página (compartilhamento de estado)
            self.page.session.set("logged_in_user", user)
            
            # Navega para o Dashboard (rota principal '/')
            self.page.go("/")
        else:
            # Usa o OVERLAY (SnackBar) para feedback de erro
            self._show_overlay_feedback("Email ou senha inválidos.")
        
    def on_navigate_to_register(self, e):
        """Navega para a tela de registro."""
        self.page.go("/register")

    def _validate_inputs(self) -> bool:
        """
        Validação simples dos campos.
        O error_text inline (do TextField) é a melhor prática para
        feedback de validação, não de ação.
        """
        email_valid = self.email_field.value is not None and "@" in self.email_field.value
        pass_valid = self.password_field.value is not None and len(self.password_field.value) > 0
        
        self.email_field.error_text = None if email_valid else "Email inválido."
        self.password_field.error_text = None if pass_valid else "Senha não pode estar vazia."
        
        self.page.update() # Atualiza os error_text
        return email_valid and pass_valid