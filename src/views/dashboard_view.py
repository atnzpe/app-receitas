# ARQUIVO: src/views/dashboard_view.py
import flet as ft
from src.viewmodels.dashboard_viewmodel import DashboardViewModel
from src.views.components.dashboard_card import DashboardCard
from src.views.components.app_footer import AppFooter
from src.utils.theme import CARD_COLORS, AppFonts


def DashboardView(page: ft.Page) -> ft.View:
    vm = DashboardViewModel(page)
    user_name = vm.user.full_name if vm.user else "Visitante"

    # Definição dos Cards
    # [CORREÇÃO] Chave alterada de "desc" para "description" para evitar KeyError
    cards = [
        {
            "icon": ft.Icons.RESTAURANT_MENU,
            "title": "Minhas Receitas",
            "description": "Gerencie suas criações.",  # Corrigido aqui
            "color": CARD_COLORS["Receitas"]["fg_light"],
            "action": vm.navigate_to_my_recipes
        },
        {
            "icon": ft.Icons.EDIT_NOTE,
            "title": "Categorias",
            "description": "Organize seu livro.",  # Corrigido aqui
            "color": CARD_COLORS["Cadastros"]["fg_light"],
            "action": vm.navigate_to_cadastros
        },
        {
            "icon": ft.Icons.SEARCH,
            "title": "Discovery",
            "description": "Busca inteligente.",  # Corrigido aqui
            "color": CARD_COLORS["Discovery"]["fg_light"],
            "action": vm.navigate_to_discovery
        },
        {
            "icon": ft.Icons.SHOPPING_CART,
            "title": "Mercado",
            "description": "Em breve.",  # Corrigido aqui
            "color": CARD_COLORS["Mercado"]["fg_light"],
            "action": vm.show_feature_in_development_dialog
        }
    ]

    responsive_cards = [
        ft.Column([
            DashboardCard(
                icon=c["icon"],
                title=c["title"],
                description=c["description"],  # Agora a chave existe!
                color=c["color"],
                on_click=c["action"]
            )
        ], col={"xs": 12, "md": 6}) for c in cards
    ]

    content = ft.Column([
        ft.Container(height=20),
        ft.Text(f"Olá, {user_name}!", size=AppFonts.TITLE_LARGE,
                weight="bold", color=ft.Colors.PRIMARY),
        ft.Text("O que vamos cozinhar hoje?",
                size=AppFonts.BODY_MEDIUM, color="grey"),
        ft.Divider(height=30, color="transparent"),
        ft.ResponsiveRow(responsive_cards, run_spacing=20, spacing=20)
    ], scroll=ft.ScrollMode.AUTO, expand=True)

    return ft.View(
        route="/",
        controls=[
            ft.SafeArea(content=content, expand=True),
            AppFooter(page)
        ],
        bgcolor=page.theme.color_scheme.surface
    )
