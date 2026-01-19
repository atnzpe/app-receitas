import flet as ft
from src.viewmodels.dashboard_viewmodel import DashboardViewModel
from src.views.components.dashboard_card import DashboardCard
from src.views.components.app_footer import AppFooter
from src.utils.theme import CARD_COLORS, AppDimensions


def DashboardView(page: ft.Page) -> ft.View:
    vm = DashboardViewModel(page)

    vm.theme_icon_button = ft.IconButton(
        icon=vm.get_theme_icon(),
        tooltip="Mudar tema",
        on_click=vm.toggle_theme
    )

    app_bar = ft.AppBar(
        leading=ft.Icon(ft.Icons.RESTAURANT_MENU,
                        color=ft.Colors.DEEP_ORANGE_500),
        title=ft.Text("App de Receitas", weight=ft.FontWeight.BOLD),
        center_title=False,
        bgcolor=ft.Colors.with_opacity(0.02, ft.Colors.BLACK),
        actions=[
            vm.theme_icon_button,
            ft.IconButton(icon=ft.Icons.LOGOUT_OUTLINED,
                          tooltip="Sair", on_click=vm.on_logout)
        ]
    )

    dashboard_grid = ft.GridView(
        controls=[
            DashboardCard(ft.Icons.BOOK_OUTLINED, "Minhas Receitas", "Organize suas receitas.",
                          CARD_COLORS["Receitas"], vm.show_feature_in_development_dialog),
            DashboardCard(ft.Icons.EDIT_NOTE_OUTLINED, "Cadastros", "Gerencie categorias.",
                          CARD_COLORS["Cadastros"], vm.navigate_to_cadastros),
            DashboardCard(ft.Icons.SEARCH_OUTLINED, "Discovery", "Encontre receitas.",
                          CARD_COLORS["Discovery"], vm.show_feature_in_development_dialog),
            DashboardCard(ft.Icons.SHOPPING_CART_OUTLINED, "Mercado", "Apps parceiros.",
                          CARD_COLORS["Mercado"], vm.show_feature_in_development_dialog),
            DashboardCard(ft.Icons.LIST_ALT_OUTLINED, "Lista de Compras", "Sua lista.",
                          CARD_COLORS["Lista"], vm.show_feature_in_development_dialog),
        ],
        expand=True,
        max_extent=350,
        child_aspect_ratio=1.8,
        spacing=15,
        run_spacing=15
    )

    return ft.View(
        route="/",
        appbar=app_bar,
        controls=[
            ft.SafeArea(
                content=ft.Column([
                    ft.Container(content=dashboard_grid,
                                 padding=AppDimensions.PAGE_PADDING, expand=True),
                    AppFooter()
                ], expand=True, spacing=0),
                expand=True
            )
        ],
        padding=0,
        bgcolor=page.theme.color_scheme.surface,  # Uso correto do tema
    )
