# ARQUIVO: main.py
import flet as ft
import traceback
from src.database.database import init_database
from src.database.seeder import seed_native_recipes
from src.core.logger import get_logger
from src.utils.theme import AppThemes

from src.views.login_view import LoginView
from src.views.register_view import RegisterView
from src.views.dashboard_view import DashboardView
from src.views.category_view import CategoryView
from src.views.recipe_create_view import RecipeCreateView
from src.views.recipe_list_view import RecipeListView
from src.views.recipe_detail_view import RecipeDetailView
from src.views.discovery_view import DiscoveryView

logger = get_logger("main")


def main(page: ft.Page):
    def global_error_handler(e):
        error_msg = f"{type(e).__name__}: {str(e)}"
        logger.critical(f"UNHANDLED UI EXCEPTION: {error_msg}", exc_info=True)
        error_dialog = ft.AlertDialog(
            title=ft.Text("Erro Crítico", color=ft.Colors.RED),
            content=ft.Text(
                f"Ocorreu um erro inesperado.\nVerifique os logs.\n\n{error_msg}"),
            actions=[ft.TextButton(
                "Recarregar", on_click=lambda _: page.window_reload())]
        )
        page.overlay.append(error_dialog)
        error_dialog.open = True
        page.update()

    try:
        logger.info("=== INICIANDO APLICAÇÃO (MILITARY GRADE) ===")
        init_database()
        seed_native_recipes()

        page.title = "Guia Mestre de Receitas"
        page.theme_mode = ft.ThemeMode.SYSTEM

        # --- CORREÇÃO SPRINT 5: ScrollBarTheme ---
        theme = AppThemes.light_theme
        theme.scrollbar_theme = ft.ScrollbarTheme(
            thumb_visibility=True,
            thickness=8,
            radius=10,
            main_axis_margin=5,
            thumb_color=ft.Colors.ORANGE_600,
        )
        page.theme = theme
        page.dark_theme = AppThemes.dark_theme
        page.scroll = ft.ScrollMode.ADAPTIVE

        page.data = {"logged_in_user": None}

        def route_change(e: ft.RouteChangeEvent):
            logger.info(f"Navegação: {e.route}")
            page.views.clear()
            user = page.data.get("logged_in_user")
            is_authenticated = user is not None

            try:
                if page.route == "/login":
                    page.views.append(LoginView(page))
                elif page.route == "/register":
                    page.views.append(RegisterView(page))
                elif not is_authenticated:
                    logger.warning(
                        f"Acesso não autorizado a {page.route}. Redirecionando.")
                    page.go("/login")
                elif page.route == "/":
                    page.views.append(DashboardView(page))
                elif page.route == "/categories":
                    page.views.append(CategoryView(page))
                elif page.route == "/my_recipes":
                    page.views.append(RecipeListView(page))
                elif page.route == "/create_recipe":
                    page.views.append(RecipeCreateView(page))
                elif page.route == "/discovery":
                    page.views.append(DiscoveryView(page))
                elif page.route == "/recipe_detail":
                    page.views.append(RecipeDetailView(page))
                page.update()
            except Exception as ex:
                global_error_handler(ex)

        page.on_route_change = route_change
        page.on_view_pop = lambda _: (
            page.views.pop(), page.go(page.views[-1].route))
        page.go("/login")

    except Exception as e:
        logger.critical("Falha Fatal no Main Loop", exc_info=True)


if __name__ == "__main__":
    ft.app(target=main)
