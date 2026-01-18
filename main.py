import flet as ft
import traceback
from src.database.database import init_database
from src.core.logger import get_logger
from src.core.exceptions import AppError
from src.utils.theme import AppThemes

# Importações de Views
from src.views.login_view import LoginView
from src.views.register_view import RegisterView
from src.views.dashboard_view import DashboardView

logger = get_logger("main")


def main(page: ft.Page):
    # --- GLOBAL ERROR BOUNDARY (Blindagem UI) ---
    def global_error_handler(e):
        """
        Captura erros não tratados na interface para não fechar o app na cara do usuário.
        """
        error_details = f"{type(e).__name__}: {str(e)}"
        logger.critical(
            f"UNHANDLED UI EXCEPTION: {error_details}", exc_info=True)

        page.dialog = ft.AlertDialog(
            title=ft.Text("Erro Inesperado 🛑", color=ft.Colors.RED),
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Ocorreu um erro crítico. Por favor, contate o suporte."),
                    ft.Text(error_details, font_family="monospace",
                            color=ft.Colors.RED_900, size=12)
                ], tight=True),
                padding=10,
                bgcolor=ft.Colors.RED_50,
                border_radius=5
            ),
            actions=[ft.TextButton(
                "Fechar", on_click=lambda _: page.window_close())],
        )
        page.dialog.open = True
        page.update()

    # Se o Flet suportar, registre o handler (ou use try/except global)
    # page.on_error = global_error_handler

    try:
        logger.info("=== INICIANDO APLICAÇÃO (MILITARY GRADE) ===")

        # 1. Setup Crítico
        init_database()

        # 2. Configuração Visual
        page.title = "Guia Mestre de Receitas"
        page.theme_mode = ft.ThemeMode.SYSTEM
        page.theme = AppThemes.light_theme
        page.dark_theme = AppThemes.dark_theme
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # 3. Sistema de Roteamento
        def route_change(e: ft.RouteChangeEvent):
            logger.info(f"Navegação: {e.route}")
            page.views.clear()

            try:
                if page.route == "/login":
                    page.views.append(LoginView(page))
                elif page.route == "/register":
                    page.views.append(RegisterView(page))
                elif page.route == "/":
                    if page.session.get("logged_in_user") is None:
                        logger.warning(
                            "Acesso não autorizado ao Dashboard. Redirecionando.")
                        page.go("/login")
                    else:
                        page.views.append(DashboardView(page))
                page.update()
            except Exception as view_error:
                # Captura erros na construção da View
                global_error_handler(view_error)

        def view_pop(e: ft.ViewPopEvent):
            page.views.pop()
            if page.views:
                page.go(page.views[-1].route)

        page.on_route_change = route_change
        page.on_view_pop = view_pop

        # 4. Boot
        page.go("/login")

    except AppError as e:
        logger.critical(f"Falha de Inicialização Controlada: {e}")
    except Exception as e:
        logger.critical("Falha Catastrófica no Main Loop", exc_info=True)
        traceback.print_exc()


if __name__ == "__main__":
    ft.app(target=main)
