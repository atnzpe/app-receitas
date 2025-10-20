# CÓDIGO ALTERADO E COMENTADO
import flet as ft
from src.database.database import init_database

# (NOVO) Importa as "fábricas" de View
from src.views.login_view import LoginView
from src.views.register_view import RegisterView
from src.views.dashboard_view import DashboardView

# (REMOVIDO) A MainView estática não é mais necessária
# from src.views.main_view import MainView


def main(page: ft.Page):
    """
    Função principal de entrada do aplicativo Flet.
    Configura a página, inicializa o roteador e o banco de dados.
    """

    # --- 1. INICIALIZAÇÃO DO BANCO DE DADOS ---
    init_database()

    # --- 2. CONFIGURAÇÕES DA PÁGINA (UX/UI) ---
    page.title = "Guia Mestre de Receitas"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.theme = ft.Theme(color_scheme_seed="deepOrange")
    page.dark_theme = ft.Theme(color_scheme_seed="deepOrange")

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- 3. (NOVO) CONFIGURAÇÃO DO ROTEADOR ---

    def route_change(e: ft.RouteChangeEvent):
        """
        Função chamada toda vez que a rota (URL) muda.
        Responsável por exibir a View correta.
        """
        page.views.clear()

        # Rota de Login (Padrão)
        if page.route == "/login":
            page.views.append(LoginView(page))

        # Rota de Registro
        elif page.route == "/register":
            page.views.append(RegisterView(page))

        # Rota de Dashboard (Principal)
        elif page.route == "/":
            # --- GUARDA DE ROTA (Segurança) ---
            # Verifica se o usuário está logado (na sessão da página)
            if page.session.get("logged_in_user") is None:
                # Se não estiver logado, força o redirecionamento para /login
                print("Acesso negado ao Dashboard. Redirecionando para /login.")
                page.go("/login")
            else:
                # Se estiver logado, mostra o Dashboard
                page.views.append(DashboardView(page))

        page.update()

    def view_pop(e: ft.ViewPopEvent):
        """
        Função chamada quando o usuário clica no botão "voltar" (ex: no Android).
        """
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # Assinatura dos eventos de roteamento
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # (REMOVIDO) Não adicionamos mais a view estática
    # main_view = MainView()
    # page.add(main_view)

    # (NOVO) Navegação inicial: Inicia o app na tela de login
    print("Iniciando app. Navegando para /login.")
    page.go("/login")

    # (REMOVIDO) page.update() é chamado pelo page.go()


if __name__ == "__main__":
    ft.app(target=main)
