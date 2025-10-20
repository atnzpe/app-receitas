# CÓDIGO COMPLETO E COMENTADO
import flet as ft
from src.views.main_view import MainView
from src.database.database import init_database

def main(page: ft.Page):
    """
    Função principal de entrada do aplicativo Flet.
    Configura a página e inicializa a View principal.
    """
    
    # --- 1. INICIALIZAÇÃO DO BANCO DE DADOS ---
    # Garante que o DB e as tabelas existam antes de carregar a UI
    # (Requisito Offline-First)
    init_database()
    
    # --- 2. CONFIGURAÇÕES DA PÁGINA (UX/UI) ---
    page.title = "Guia Mestre de Receitas"
    page.theme_mode = ft.ThemeMode.SYSTEM  # Respeita o tema do sistema (Claro/Escuro)
    
    # Aplicar a cor semente (seed_color) conforme (C) Contexto
    # Usarei um tom de verde ou laranja para culinária. Vamos de 'deepOrange'.
    page.theme = ft.Theme(color_scheme_seed="deepOrange")
    page.dark_theme = ft.Theme(color_scheme_seed="deepOrange")
    
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- 3. INICIALIZAÇÃO DA VIEW PRINCIPAL ---
    # Instancia a View principal.
    # A MainView (MVVM) será responsável por instanciar seu próprio ViewModel.
    main_view = MainView()
    
    # Adiciona a visualização principal à página
    page.add(main_view)
    
    # Define a rolagem da página, se necessário
    page.scroll = ft.ScrollMode.ADAPTIVE
    
    # Atualiza a página para renderizar os controles
    page.update()

if __name__ == "__main__":
    # Executa o aplicativo Flet
    # view=ft.AppView.FLET_APP_WEB para testar no browser
    # view=ft.AppView.FLET_APP para desktop
    ft.app(target=main)