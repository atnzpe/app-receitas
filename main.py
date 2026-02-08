# ARQUIVO: main.py
import flet as ft
import traceback
from src.database.database import init_database
from src.database.seeder import seed_native_recipes
from src.core.logger import get_logger
from src.utils.theme import AppThemes

# Importação das Views
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
    # Tratamento Global de Erros UI
    def global_error_handler(e):
        error_msg = f"{type(e).__name__}: {str(e)}"
        logger.critical(f"UNHANDLED UI EXCEPTION: {error_msg}", exc_info=True)
        # Tenta mostrar erro na tela mesmo se tudo falhar
        page.add(ft.Text(f"ERRO CRÍTICO:\n{error_msg}", color=ft.Colors.RED))
        page.update()

    try:
        logger.info("=== INICIANDO APLICAÇÃO (MILITARY GRADE) ===")

        # 1. Banco de Dados
        init_database()
        seed_native_recipes()

        # 2. Configurações da Janela
        page.title = "Guia Mestre de Receitas"
        page.theme_mode = ft.ThemeMode.SYSTEM

        # Tema
        theme = AppThemes.light_theme
        theme.scrollbar_theme = ft.ScrollbarTheme(
            thumb_visibility=True,
            thickness=8,
            radius=10,
            thumb_color=ft.Colors.ORANGE_600,
        )
        page.theme = theme
        page.dark_theme = AppThemes.dark_theme

        # [IMPORTANTE] Dados de Sessão
        page.data = {"logged_in_user": None}

        # 3. Sistema de Roteamento
        def route_change(e: ft.RouteChangeEvent):
            logger.info(f"Navegação Solicitada: {e.route}")
            page.views.clear()

            try:
                # Lógica de Roteamento
                user = page.data.get("logged_in_user")
                is_auth = user is not None

                if page.route == "/login":
                    logger.debug("Renderizando LoginView")
                    page.views.append(LoginView(page))

                elif page.route == "/register":
                    logger.debug("Renderizando RegisterView")
                    page.views.append(RegisterView(page))

                # Proteção de Rota
                elif not is_auth:
                    logger.warning(
                        f"Acesso negado a {page.route}. Redirecionando Login.")
                    page.go("/login")
                    return

                elif page.route == "/":
                    logger.debug("Renderizando DashboardView")
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
                logger.info("View renderizada com sucesso.")

            except Exception as ex:
                logger.error(
                    f"Erro ao renderizar rota {page.route}: {ex}", exc_info=True)
                global_error_handler(ex)

        def view_pop(e):
            logger.debug("View Pop (Voltar)")
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)

        page.on_route_change = route_change
        page.on_view_pop = view_pop

        # 4. Boot Inicial
        logger.info("Forçando navegação inicial para /login")
        page.go("/login")

    except Exception as e:
        logger.critical("Falha Fatal no Boot do Main", exc_info=True)


if __name__ == "__main__":
    ft.app(target=main)
