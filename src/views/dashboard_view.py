# ARQUIVO: src/views/dashboard_view.py
import flet as ft
from src.viewmodels.dashboard_viewmodel import DashboardViewModel
from src.views.components.dashboard_card import DashboardCard
from src.views.components.app_footer import AppFooter
from src.utils.theme import CARD_COLORS


def DashboardView(page: ft.Page) -> ft.View:
    vm = DashboardViewModel(page)

    # Dados dos Cards
    cards_data = [
        {
            "icon": ft.Icons.RESTAURANT_MENU,
            "title": "Minhas Receitas",
            "desc": "Crie e organize suas receitas. Veja suas criações e favoritos.",
            "color": CARD_COLORS["Receitas"]["fg_light"],
            "action": vm.navigate_to_my_recipes
        },
        {
            "icon": ft.Icons.EDIT_NOTE_OUTLINED,
            "title": "Categorias",
            "desc": "Gerencie categorias e pesquise receitas por categorias.",
            "color": CARD_COLORS["Cadastros"]["fg_light"],
            "action": vm.navigate_to_cadastros
        },
        {
            "icon": ft.Icons.SEARCH_OUTLINED,
            "title": "Discovery",
            "desc": "Encontre receitas nativas, suas ou de outros. Pesquise por dispensa.",
            "color": CARD_COLORS["Discovery"]["fg_light"],
            # [ALTERAÇÃO AQUI] De show_feature... para navigate_to_discovery
            "action": vm.navigate_to_discovery
        },
        {
            "icon": ft.Icons.SHOPPING_CART_OUTLINED,
            "title": "Mercado & Lista",
            "desc": "Apps parceiros, Mercados e Lista de Compras para fornecedores.",
            "color": CARD_COLORS["Mercado"]["fg_light"],
            "action": vm.show_feature_in_development_dialog
        }
    ]

    # Constrói a lista responsiva
    responsive_controls = []
    for card in cards_data:
        responsive_controls.append(
            ft.Column(
                controls=[
                    DashboardCard(
                        icon=card["icon"],
                        title=card["title"],
                        description=card["desc"],
                        color=card["color"],
                        on_click=card["action"]
                    )
                ],
                col={"xs": 12, "md": 6, "lg": 6}
            )
        )

    # Layout Principal
    content = ft.Column(
        controls=[
            ft.Container(height=10),
            ft.Text(
                f"Olá, {vm.user.full_name if vm.user else 'Visitante'}!",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.PRIMARY
            ),
            ft.Text("O que vamos cozinhar hoje?",
                    size=16, color=ft.Colors.OUTLINE),
            ft.Divider(height=30, color=ft.Colors.TRANSPARENT),

            ft.ResponsiveRow(
                controls=responsive_controls,
                run_spacing=20,
                spacing=20
            )
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    return ft.View(
        route="/",
        controls=[
            # [CORREÇÃO] Removido o argumento 'minimum' que causava crash
            ft.SafeArea(
                content=content,
                expand=True
            ),
            AppFooter(page)
        ],
        bgcolor=page.theme.color_scheme.surface
    )
