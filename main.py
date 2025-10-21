# CÓDIGO COMPLETO E COMENTADO
import logging  # Importa a biblioteca de logging
import flet as ft


# Importa nossas funções e classes customizadas
from src.database.database import init_database
from src.utils.logging_setup import setup_logging
from src.utils.theme import AppThemes

# Importa as "fábricas" de View (telas)
from src.views.login_view import LoginView
from src.views.register_view import RegisterView
from src.views.dashboard_view import DashboardView


def main(page: ft.Page):
    """
    Função principal de entrada do aplicativo Flet.
    Configura a página, inicializa o roteador e o banco de dados.
    """

    # --- 1. CONFIGURAÇÃO DE LOGGING (Debug) ---
    # Configura o logger antes de qualquer outra coisa.
    # Passamos a 'page' para que ele saiba se estamos no Desktop ou Web.
    setup_logging(page)
    logger = logging.getLogger(__name__)
    logger.info("Aplicação iniciada. Configurando o logging...")

    # --- 2. INICIALIZAÇÃO DO BANCO DE DADOS ---
    logger.debug("Inicializando o banco de dados...")
    init_database()

    # --- 3. CONFIGURAÇÕES DA PÁGINA (UX/UI) ---
    logger.debug("Configurando temas da página.")
    page.title = "Guia Mestre de Receitas"
    page.theme_mode = ft.ThemeMode.SYSTEM  # Respeita o tema do sistema

    # Aplica os temas completos que definimos em src/utils/theme.py
    page.theme = AppThemes.light_theme
    page.dark_theme = AppThemes.dark_theme

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- 4. CONFIGURAÇÃO DO ROTEADOR (Navegação) ---
    logger.debug("Configurando o roteador de views (ft.Router)...")

    def route_change(e: ft.RouteChangeEvent):
        """
        Função chamada toda vez que a rota (URL) muda.
        Responsável por exibir a View correta.
        """
        logger.info(f"Navegando para a rota: {e.route}")
        page.views.clear()  # Limpa a view anterior

        # Rota de Login
        if page.route == "/login":
            page.views.append(LoginView(page))

        # Rota de Registro
        elif page.route == "/register":
            page.views.append(RegisterView(page))

        # Rota Principal (Dashboard)
        elif page.route == "/":
            # --- GUARDA DE ROTA (Segurança) ---
            # Verifica se o usuário está logado (na sessão da página)
            if page.session.get("logged_in_user") is None:
                logger.warning(
                    "Acesso negado à rota '/'. Usuário não logado. Redirecionando para /login.")
                page.go("/login")  # Força o redirecionamento
            else:
                logger.debug("Usuário logado. Exibindo DashboardView.")
                page.views.append(DashboardView(page))

        page.update()

    def view_pop(e: ft.ViewPopEvent):
        """
        Função chamada quando o usuário clica no botão "voltar" (ex: no Android).
        """
        logger.debug("View 'pop' detectada (botão 'voltar').")
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # Assinatura dos eventos de roteamento
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    logger.info("Configuração inicial completa. Navegando para /login.")
    page.go("/login")  # Inicia o app na tela de login


if __name__ == "__main__":
    # Executa o aplicativo Flet
    ft.app(target=main)
