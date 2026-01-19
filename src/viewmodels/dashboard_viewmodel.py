# CÓDIGO ATUALIZADO
import flet as ft
import logging
from src.models.user_model import User
from typing import Optional

logger = logging.getLogger(__name__)


class DashboardViewModel:
    def __init__(self, page: ft.Page):
        self.page = page
        # Recupera de page.data
        self.user: User = self.page.data.get("logged_in_user")

        # Fallback de segurança se o usuário for None (não deveria acontecer)
        if not self.user:
            logger.warning("Usuário não encontrado na sessão (page.data).")

        logger.debug(
            f"Dashboard VM init: {self.user.email if self.user else 'None'}")
        self.theme_icon_button: Optional[ft.IconButton] = None

    def on_logout(self, e):
        logger.info("Logout solicitado.")
        self.page.data["logged_in_user"] = None  # Limpa sessão
        self.page.go("/login")

    def toggle_theme(self, e):
        try:
            current = self.page.theme_mode
            self.page.theme_mode = ft.ThemeMode.LIGHT if current == ft.ThemeMode.DARK else ft.ThemeMode.DARK
            if self.theme_icon_button:
                self.theme_icon_button.icon = self.get_theme_icon()
            self.page.update()
        except Exception as ex:
            logger.error(f"Erro tema: {ex}")

    def get_theme_icon(self) -> str:
        if self.page.theme_mode == ft.ThemeMode.SYSTEM:
            return ft.Icons.LIGHT_MODE_OUTLINED if self.page.platform_brightness == ft.Brightness.DARK else ft.Icons.DARK_MODE_OUTLINED
        return ft.Icons.LIGHT_MODE_OUTLINED if self.page.theme_mode == ft.ThemeMode.DARK else ft.Icons.DARK_MODE_OUTLINED

    def close_dialog(self, dialog, e):
        dialog.open = False
        self.page.update()

    def show_feature_in_development_dialog(self, e):
        card_title = e.control.data if hasattr(
            e, 'control') else "Funcionalidade"
        dialog = ft.AlertDialog(
            title=ft.Text(f"🚀 Em Breve: {card_title}"),
            content=ft.Text("Funcionalidade em desenvolvimento."),
            actions=[ft.TextButton(
                "Ok", on_click=lambda evt: self.close_dialog(dialog, evt))],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def navigate_to_cadastros(self, e):
        self.page.go("/categories")
