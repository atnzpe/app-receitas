# ARQUIVO: src/views/recipe_list_view.py
import flet as ft
from src.viewmodels.recipe_list_viewmodel import RecipeListViewModel
from src.utils.theme import AppDimensions


def RecipeListView(page: ft.Page) -> ft.View:
    vm = RecipeListViewModel(page)
    vm.load_recipes()

    # --- Lista de Itens ---
    def build_list():
        if not vm.recipes:
            return ft.Column(
                [
                    ft.Icon(ft.Icons.NO_MEALS, size=64,
                            color=ft.Colors.GREY_400),
                    ft.Text("Nenhuma receita encontrada.",
                            color=ft.Colors.GREY_500)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )

        list_controls = []
        for recipe in vm.recipes:
            # Lógica simples de exibição
            is_fav = recipe.get('is_favorite', 0)

            list_controls.append(
                ft.Card(
                    content=ft.ListTile(
                        leading=ft.Icon(ft.Icons.RESTAURANT_MENU,
                                        color=ft.Colors.ORANGE),
                        title=ft.Text(recipe['title'],
                                      weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(
                            f"{recipe['preparation_time'] or '?'} min • {recipe['servings'] or 'N/A'}"),
                        trailing=ft.Icon(
                            ft.Icons.STAR if is_fav else ft.Icons.STAR_BORDER,
                            color=ft.Colors.AMBER if is_fav else ft.Colors.GREY
                        ),
                        on_click=lambda e, id=recipe['id']: vm.navigate_to_details(
                            id)
                    ),
                    elevation=1,
                    margin=ft.margin.symmetric(vertical=5)
                )
            )

        return ft.ListView(
            controls=list_controls,
            expand=True,
            padding=10,
            spacing=5
        )

    # --- Botão Flutuante (FAB) ---
    fab = ft.FloatingActionButton(
        # O ícone principal ainda pode ser definido ou removido se estiver no content
        icon=ft.Icons.ADD,
        content=ft.Row(
            [
                ft.Icon(ft.Icons.ADD),
                ft.Text("Nova Receita", weight=ft.FontWeight.BOLD)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        ),
        bgcolor=page.theme.color_scheme.primary,
        width=170,  # Largura fixa necessária para acomodar o texto estendido
        on_click=vm.navigate_to_create
    )

    return ft.View(
        route="/my_recipes",
        controls=[
            ft.SafeArea(
                content=build_list(),
                expand=True
            )
        ],
        appbar=ft.AppBar(
            leading=ft.IconButton(ft.Icons.ARROW_BACK,
                                  on_click=lambda _: page.go("/")),
            title=ft.Text("Minhas Receitas"),
            bgcolor=page.theme.color_scheme.surface
        ),
        floating_action_button=fab,
        bgcolor=page.theme.color_scheme.surface
    )
