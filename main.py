import flet as ft
import traceback
from src.database.database import init_database
from src.core.logger import get_logger
from src.utils.theme import AppThemes
from src.views.login_view import LoginView
from src.views.register_view import RegisterView
from src.views.dashboard_view import DashboardView
from src.views.category_view import CategoryView

logger = get_logger("main")


def main(page: ft.Page):
    def global_error_handler(e):
        logger.critical(f"UNHANDLED UI EXCEPTION: {e}", exc_info=True)
        page.dialog = ft.AlertDialog(title=ft.Text("Erro"), content=ft.Text("Erro crítico."), actions=[
                                     ft.TextButton("Fechar", on_click=lambda _: page.window_close())])
        page.dialog.open = True
        page.update()

    try:
        logger.info("=== INICIANDO APLICAÇÃO ===")
        init_database()
        page.title = "Guia Mestre de Receitas"
        page.theme_mode = ft.ThemeMode.SYSTEM
        page.theme = AppThemes.light_theme
        page.dark_theme = AppThemes.dark_theme
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.scroll = ft.ScrollMode.ADAPTIVE

        # Sessão Global em Memória
        page.data = {"logged_in_user": None}

        def route_change(e: ft.RouteChangeEvent):
            logger.info(f"Navegação: {e.route}")
            page.views.clear()
            try:
                user = page.data.get("logged_in_user")
                if page.route == "/login":
                    page.views.append(LoginView(page))
                elif page.route == "/register":
                    page.views.append(RegisterView(page))
                elif page.route == "/":
                    if not user:
                        page.go("/login")
                    else:
                        page.views.append(DashboardView(page))
                elif page.route == "/categories":
                    if not user:
                        page.go("/login")
                    else:
                        page.views.append(CategoryView(page))
                page.update()
            except Exception as ex:
                global_error_handler(ex)

        page.on_route_change = route_change
        page.on_view_pop = lambda e: (page.views.pop(), page.go(
            page.views[-1].route)) if page.views else None
        page.go("/login")

    except Exception as e:
        logger.critical("Falha Main", exc_info=True)


if __name__ == "__main__":
    ft.app(target=main)
