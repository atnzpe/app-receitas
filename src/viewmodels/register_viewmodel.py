# ARQUIVO: src/viewmodels/register_viewmodel.py
import logging
import time  # [CORREÇÃO] Necessário para o delay tático
from typing import Optional
import flet as ft
from src.database import auth_queries

logger = logging.getLogger(__name__)


class RegisterViewModel:
    def __init__(self, page: ft.Page):
        self.page = page
        logger.debug("RegisterViewModel init.")
        self.name_field: Optional[ft.TextField] = None
        self.email_field: Optional[ft.TextField] = None
        self.password_field: Optional[ft.TextField] = None

    def set_controls(self, name, email, password):
        logger.debug("Controles vinculados.")
        self.name_field = name
        self.email_field = email
        self.password_field = password

    def _show_overlay_feedback(self, msg: str, is_error: bool = True):
        logger.debug(f"SnackBar: {msg}")
        color = ft.Colors.RED if is_error else ft.Colors.GREEN

        # Cria e exibe a SnackBar
        snack = ft.SnackBar(
            content=ft.Text(msg, color=ft.Colors.WHITE, weight="bold"),
            bgcolor=color,
            duration=3000  # 3 segundos
        )
        self.page.snack_bar = snack
        self.page.snack_bar.open = True
        self.page.update()

    def on_register_click(self, e):
        logger.debug("Click Registrar.")

        # Feedback visual imediato (Desabilita botão ou mostra loading se houvesse)
        self.page.update()

        try:
            if not self._validate_inputs():
                logger.warning("Inputs inválidos.")
                self._show_overlay_feedback("Verifique os campos em vermelho.")
                return

            name = self.name_field.value.strip()
            email = self.email_field.value.strip()
            password = self.password_field.value

            logger.debug(f"Chamando auth_queries para: {email}")
            user = auth_queries.register_user(name, email, password)

            if user:
                logger.info(f"Sucesso: {user.email}")
                # 1. Mostra mensagem de sucesso
                self._show_overlay_feedback(
                    "Conta criada com sucesso! Redirecionando...", is_error=False)

                # 2. [CORREÇÃO] Delay tático para o usuário ler a mensagem
                self.page.update()
                time.sleep(1.5)

                # 3. Navega para o login
                self.page.go("/login")
            else:
                logger.warning("Falha: Email duplicado.")
                # Tratamento de erro específico para duplicidade
                if self.email_field:
                    self.email_field.error_text = "Este e-mail já está em uso."
                    self.email_field.update()
                self._show_overlay_feedback(
                    "Não foi possível criar a conta.", is_error=True)

        except Exception as ex:
            logger.error(f"Erro View Register: {ex}", exc_info=True)
            self._show_overlay_feedback(f"Erro interno: {str(ex)}")

    def on_navigate_to_login(self, e):
        logger.debug("Nav Login.")
        self.page.go("/login")

    def _validate_inputs(self) -> bool:
        logger.debug("Validando inputs...")
        n_val = self.name_field.value.strip() if self.name_field.value else ""
        e_val = self.email_field.value.strip() if self.email_field.value else ""
        p_val = self.password_field.value if self.password_field.value else ""

        n_ok = len(n_val) > 2
        e_ok = "@" in e_val and "." in e_val  # Validação simples de email
        p_ok = len(p_val) >= 6

        self.name_field.error_text = None if n_ok else "Nome deve ter no mínimo 3 letras."
        self.email_field.error_text = None if e_ok else "Digite um e-mail válido."
        self.password_field.error_text = None if p_ok else "Senha deve ter no mínimo 6 caracteres."

        self.name_field.update()
        self.email_field.update()
        self.password_field.update()

        return n_ok and e_ok and p_ok
