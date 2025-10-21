# CÓDIGO COMPLETO E COMENTADO
import flet as ft
from src.viewmodels.dashboard_viewmodel import DashboardViewModel
from src.views.components.dashboard_card import DashboardCard
from src.views.components.app_footer import AppFooter
from src.utils.theme import CARD_COLORS,AppDimensions,AppThemes,AppFonts # Importa as cores

def DashboardView(page: ft.Page) -> ft.View:
    """
    Retorna a ft.View para a rota de Dashboard ('/').
    Esta é a tela principal após o login.
    """
    
    # 1. Instanciar o ViewModel
    vm = DashboardViewModel(page)
    
    # --- 2. Definição dos Controles ---

    # Botão de Tema (referência é passada ao VM)
    vm.theme_icon_button = ft.IconButton(
        icon=vm.get_theme_icon(),
        tooltip="Mudar tema",
        on_click=vm.toggle_theme # 3. Bindar evento
    )

    # AppBar (Cabeçalho)
    app_bar = ft.AppBar(
        leading=ft.Icon(ft.Icons.RESTAURANT_MENU, color=ft.Colors.DEEP_ORANGE_500),
        title=ft.Text("App de Receitas", weight=ft.FontWeight.BOLD),
        center_title=False,
        bgcolor=ft.Colors.with_opacity(0.02, ft.Colors.BLACK),
        actions=[
            vm.theme_icon_button,
            ft.IconButton(
                icon=ft.Icons.LOGOUT_OUTLINED,
                tooltip="Sair (Logout)",
                on_click=vm.on_logout # 3. Bindar evento
            )
        ]
    )

    # Grid de Cards Responsivo (Mobile-First)
    dashboard_grid = ft.GridView(
        controls=[
            DashboardCard(
                icon_name=ft.Icons.BOOK_OUTLINED,
                title="Minhas Receitas",
                subtitle="Organize e visualize suas receitas.",
                color_scheme=CARD_COLORS["Receitas"],
                on_card_click=vm.show_feature_in_development_dialog
            ),
            DashboardCard(
                icon_name=ft.Icons.EDIT_NOTE_OUTLINED,
                title="Cadastros",
                subtitle="Gerencie ingredientes e categorias.",
                color_scheme=CARD_COLORS["Cadastros"],
                on_card_click=vm.navigate_to_cadastros # Evento específico
            ),
            DashboardCard(
                icon_name=ft.Icons.SEARCH_OUTLINED,
                title="Discovery",
                subtitle="Encontre receitas com o que tem em casa.",
                color_scheme=CARD_COLORS["Discovery"],
                on_card_click=vm.show_feature_in_development_dialog
            ),
            DashboardCard(
                icon_name=ft.Icons.SHOPPING_CART_OUTLINED,
                title="Mercado",
                subtitle="Acesse apps parceiros para compras.",
                color_scheme=CARD_COLORS["Mercado"],
                on_card_click=vm.show_feature_in_development_dialog
            ),
            DashboardCard(
                icon_name=ft.Icons.LIST_ALT_OUTLINED,
                title="Lista de Compras",
                subtitle="Crie e compartilhe sua lista.",
                color_scheme=CARD_COLORS["Lista"],
                on_card_click=vm.show_feature_in_development_dialog
            ),
        ],
        expand=True,
        max_extent=350, # Responsividade: máximo de 350px por card
        child_aspect_ratio=1.8,
        spacing=15,
        run_spacing=15
    )
    
    # Conteúdo principal (Grid + Rodapé)
    main_content = ft.Column(
        controls=[
            ft.Container(
                content=dashboard_grid,
                padding=AppDimensions.PAGE_PADDING,
                expand=True
            ),
            AppFooter()
        ],
        expand=True,
        spacing=0
    )

    # 5. Retornar a ft.View
    return ft.View(
        route="/",
        appbar=app_bar,
        controls=[
            ft.SafeArea(
                content=main_content,
                expand=True
            )
        ],
        padding=0,
        # (CORRIGIDO) Apenas bgcolor é necessário. O Flet usa page.dark_theme
        # para aplicar a cor correta do background no modo escuro.
        bgcolor=page.theme.color_scheme.background,
        # (REMOVIDO) bgcolor_dark=page.dark_theme.color_scheme.background
    )