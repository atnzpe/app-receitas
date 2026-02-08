# ARQUIVO: src/viewmodels/dashboard_viewmodel.py
import flet as ft
from src.core.logger import get_logger

logger = get_logger("src.viewmodels.dashboard")


class DashboardViewModel:
    def __init__(self, page: ft.Page):
        self.page = page
        self.user = self.page.data.get("logged_in_user")

    def navigate_to_my_recipes(self, e):
        logger.info("Navegando para: Minhas Receitas")
        # Tente page.go se push_route falhar visualmente,
        # mas vamos manter o padrão do projeto primeiro.
        self.page.go("/my_recipes")

    def navigate_to_cadastros(self, e):
        logger.info("Navegando para: Categorias")
        self.page.go("/categories")

    def navigate_to_discovery(self, e):
        logger.info("Navegando para: Discovery")
        self.page.go("/discovery")

    def show_feature_in_development_dialog(self, e):
        logger.info("Abrindo modal: Em Desenvolvimento")
        dlg = ft.AlertDialog(
            title=ft.Text("Em Desenvolvimento"),
            content=ft.Text("Funcionalidade em breve!"),
            actions=[
                ft.TextButton("OK", on_click=lambda _: self._close_dialog(dlg))
            ],
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def _close_dialog(self, dlg):
        dlg.open = False
        self.page.update()
