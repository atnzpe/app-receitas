import flet as ft
import logging
from src.models.user_model import User
from typing import Optional

logger = logging.getLogger(__name__)


class DashboardViewModel:
    def __init__(self, page: ft.Page):
        self.page = page
        self.user: User = self.page.data.get(
            "logged_in_user") if self.page.data else None

        if not self.user:
            logger.warning("Usuário não encontrado na sessão.")

        self.theme_icon_button: Optional[ft.IconButton] = None

    def on_logout(self, e):
        logger.info("Logout solicitado.")
        if self.page.data:
            self.page.data["logged_in_user"] = None
        self.page.go("/login")

    def toggle_theme(self, e):
        try:
            current = self.page.theme_mode
            self.page.theme_mode = ft.ThemeMode.LIGHT if current == ft.ThemeMode.DARK else ft.ThemeMode.DARK
            self.page.update()
        except Exception as ex:
            logger.error(f"Erro tema: {ex}")

    def get_theme_icon(self) -> str:
        return ft.Icons.LIGHT_MODE_OUTLINED if self.page.theme_mode == ft.ThemeMode.DARK else ft.Icons.DARK_MODE_OUTLINED

    def show_feature_in_development_dialog(self, e):
        # Placeholder
        pass

    def navigate_to_cadastros(self, e):
        self.page.go("/categories")

    def navigate_to_my_recipes(self, e):
        # MUDANÇA: Agora vai para a lista, não direto para criar
        self.page.go("/my_recipes")
