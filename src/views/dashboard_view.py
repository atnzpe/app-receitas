# CÓDIGO ALTERADO E COMENTADO
import flet as ft
from src.viewmodels.dashboard_viewmodel import DashboardViewModel
from src.views.components.dashboard_card import DashboardCard
from src.views.components.app_footer import AppFooter

# (Definição de CARD_Colors permanece a mesma)
CARD_Colors = {
    "Receitas": {
        "bg_light": ft.Colors.RED_100, "fg_light": ft.Colors.RED_600,
        "bg_dark": ft.Colors.with_opacity(0.4, ft.Colors.RED_900), "fg_dark": ft.Colors.RED_300
    },
    "Cadastros": {
        "bg_light": ft.Colors.BLUE_100, "fg_light": ft.Colors.BLUE_600,
        "bg_dark": ft.Colors.with_opacity(0.4, ft.Colors.BLUE_900), "fg_dark": ft.Colors.BLUE_300
    },
    "Discovery": {
        "bg_light": ft.Colors.YELLOW_100, "fg_light": ft.Colors.YELLOW_700,
        "bg_dark": ft.Colors.with_opacity(0.4, ft.Colors.YELLOW_900), "fg_dark": ft.Colors.YELLOW_300
    },
    "Mercado": {
        "bg_light": ft.Colors.GREEN_100, "fg_light": ft.Colors.GREEN_600,
        "bg_dark": ft.Colors.with_opacity(0.4, ft.Colors.GREEN_900), "fg_dark": ft.Colors.GREEN_300
    },
    "Lista": {
        "bg_light": ft.Colors.PURPLE_100, "fg_light": ft.Colors.PURPLE_600,
        "bg_dark": ft.Colors.with_opacity(0.4, ft.Colors.PURPLE_900), "fg_dark": ft.Colors.PURPLE_300
    },
}


def DashboardView(page: ft.Page) -> ft.View:
    """
    Retorna a ft.View para a rota de Dashboard ('/').
    (REFATORADO) Adicionado SafeArea.
    """
    
    vm = DashboardViewModel(page)
    
    vm.theme_icon_button = ft.IconButton(
        icon=vm.get_theme_icon(),
        tooltip="Mudar tema",
        on_click=vm.toggle_theme
    )

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
                on_click=vm.on_logout
            )
        ]
    )

    dashboard_grid = ft.GridView(
        controls=[
            DashboardCard(
                icon_name=ft.Icons.BOOK_OUTLINED,
                title="Minhas Receitas",
                subtitle="Organize e visualize suas receitas.",
                color_scheme=CARD_Colors["Receitas"],
                on_card_click=vm.show_feature_in_development_dialog
            ),
            DashboardCard(
                icon_name=ft.Icons.EDIT_NOTE_OUTLINED,
                title="Cadastros",
                subtitle="Gerencie ingredientes e categorias.",
                color_scheme=CARD_Colors["Cadastros"],
                on_card_click=vm.navigate_to_cadastros
            ),
            DashboardCard(
                icon_name=ft.Icons.SEARCH_OUTLINED,
                title="Discovery",
                subtitle="Encontre receitas com o que tem em casa.",
                color_scheme=CARD_Colors["Discovery"],
                on_card_click=vm.show_feature_in_development_dialog
            ),
            DashboardCard(
                icon_name=ft.Icons.SHOPPING_CART_OUTLINED,
                title="Mercado",
                subtitle="Acesse apps parceiros para compras.",
                color_scheme=CARD_Colors["Mercado"],
                on_card_click=vm.show_feature_in_development_dialog
            ),
            DashboardCard(
                icon_name=ft.Icons.LIST_ALT_OUTLINED,
                title="Lista de Compras",
                subtitle="Crie e compartilhe sua lista.",
                color_scheme=CARD_Colors["Lista"],
                on_card_click=vm.show_feature_in_development_dialog
            ),
        ],
        expand=True,
        max_extent=350,
        child_aspect_ratio=1.8,
        spacing=15,
        run_spacing=15
    )
    
    # (NOVO) Conteúdo principal da tela
    main_content = ft.Column(
        controls=[
            ft.Container(
                content=dashboard_grid,
                padding=20,
                expand=True
            ),
            AppFooter()
        ],
        expand=True,
        spacing=0
    )

    return ft.View(
        route="/",
        appbar=app_bar,
        controls=[
            # (NOVO) Adicionado SafeArea conforme diretriz Mobile-First
            # Note que o appbar fica FORA do SafeArea.
            ft.SafeArea(
                content=main_content,
                expand=True
            )
        ],
        padding=0,
        bgcolor=ft.Colors.GREY_50,
        bgcolor_dark=ft.Colors.GREY_900
    )