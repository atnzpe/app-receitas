# CÓDIGO ALTERADO E COMENTADO
import flet as ft
import logging

from src.database.database import init_database
from src.utils.logging_setup import setup_logging
from src.utils.theme import AppThemes

from src.views.login_view import LoginView
from src.views.register_view import RegisterView
from src.views.dashboard_view import DashboardView


def main(page: ft.Page):
    """
    Função principal de entrada do aplicativo Flet.
    """

    setup_logging(page)
    logger = logging.getLogger(__name__)
    logger.info("Aplicação iniciada. Configurando o logging...")

    init_database()

    logger.debug("Configurando temas da página.")
    page.title = "Guia Mestre de Receitas"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.theme = AppThemes.light_theme
    page.dark_theme = AppThemes.dark_theme

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    logger.debug("Configurando o roteador de views (ft.Router)...")

    def route_change(e: ft.RouteChangeEvent):
        """
        Função chamada toda vez que a rota (URL) muda.
        """
        logger.info(f"Navegando para a rota: {e.route}")
        page.views.clear()

        if page.route == "/login":
            page.views.append(LoginView(page))
        elif page.route == "/register":
            page.views.append(RegisterView(page))
        elif page.route == "/":
            if page.session.get("logged_in_user") is None:
                logger.warning(
                    "Acesso negado à rota '/'. Usuário não logado. Redirecionando para /login.")
                page.go("/login")
            else:
                logger.debug("Usuário logado. Exibindo DashboardView.")
                page.views.append(DashboardView(page))

        page.update()

    def view_pop(e: ft.ViewPopEvent):
        """
        (CORRIGIDO) Função chamada quando o usuário clica no botão "voltar".
        Agora verifica se a pilha de views não está vazia antes de agir.
        """
        logger.debug("View 'pop' detectada (botão 'voltar').")
        page.views.pop()

        # (CORRIGIDO) Se a pilha de views não estiver vazia, navega para a view anterior.
        if len(page.views) > 0:
            top_view = page.views[-1]
            logger.debug(
                f"Pilha de views não está vazia. Navegando de volta para: {top_view.route}")
            page.go(top_view.route)
        else:
            # Se a pilha estiver vazia (ex: estava na tela de login), não faz nada.
            # O comportamento padrão do Flet (fechar o app no desktop) será acionado se for o caso.
            logger.warning(
                "Pilha de views está vazia após 'pop'. Nenhuma ação de navegação a ser tomada.")

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    logger.info("Configuração inicial completa. Navegando para /login.")
    page.go("/login")


if __name__ == "__main__":
    ft.app(target=main)
