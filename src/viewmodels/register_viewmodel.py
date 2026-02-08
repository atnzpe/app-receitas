# ARQUIVO: src/viewmodels/register_viewmodel.py
import logging
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
        color = self.page.theme.color_scheme.error if is_error else ft.Colors.GREEN_600
        self.page.snack_bar = ft.SnackBar(content=ft.Text(msg), bgcolor=color)
        self.page.snack_bar.open = True
        self.page.update()

    def on_register_click(self, e):
        logger.debug("Click Registrar.")
        try:
            if not self._validate_inputs():
                logger.warning("Inputs inválidos.")
                return

            name = self.name_field.value.strip()
            email = self.email_field.value.strip()
            password = self.password_field.value

            logger.debug(f"Chamando auth_queries para: {email}")
            user = auth_queries.register_user(name, email, password)

            if user:
                logger.info(f"Sucesso: {user.email}")
                self._show_overlay_feedback("Conta criada! Redirecionando...", is_error=False)
                self.page.push_route("/login") # [CORREÇÃO] push_route
            else:
                logger.warning("Falha: Email duplicado.")
                if self.email_field:
                    self.email_field.error_text = "E-mail já cadastrado."
                    self.page.update()
                else:
                    self._show_overlay_feedback("E-mail já existe.")

        except Exception as ex:
            logger.error(f"Erro View Register: {ex}", exc_info=True)
            self._show_overlay_feedback("Erro interno.")

    def on_navigate_to_login(self, e):
        logger.debug("Nav Login.")
        self.page.push_route("/login")

    def _validate_inputs(self) -> bool:
        logger.debug("Validando inputs...")
        n_val = self.name_field.value.strip() if self.name_field.value else ""
        e_val = self.email_field.value.strip() if self.email_field.value else ""
        p_val = self.password_field.value if self.password_field.value else ""

        n_ok = len(n_val) > 2
        e_ok = "@" in e_val
        p_ok = len(p_val) >= 6

        self.name_field.error_text = None if n_ok else "Nome curto."
        self.email_field.error_text = None if e_ok else "Email inválido."
        self.password_field.error_text = None if p_ok else "Senha curta (min 6)."
        
        self.page.update()
        logger.debug(f"Status Validação: Nome={n_ok}, Email={e_ok}, Senha={p_ok}")
        return n_ok and e_ok and p_ok