# ARQUIVO: src/views/recipe_list_view.py
# OBJETIVO: Listagem com botão de Editar.
import flet as ft
from src.viewmodels.recipe_list_viewmodel import RecipeListViewModel
from src.utils.theme import AppDimensions


def RecipeListView(page: ft.Page) -> ft.View:
    vm = RecipeListViewModel(page)
    vm.load_recipes()

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
            is_fav = bool(recipe.get('is_favorite', 0))
            is_mine = recipe['user_id'] == vm.user.id

            # Botões de Ação
            fav_icon = ft.IconButton(
                icon=ft.Icons.STAR if is_fav else ft.Icons.STAR_BORDER,
                icon_color=ft.Colors.AMBER if is_fav else ft.Colors.GREY,
                tooltip="Favoritar",
                on_click=lambda e, id=recipe['id']: vm.toggle_favorite(id)
            )

            delete_icon = ft.IconButton(
                icon=ft.Icons.DELETE_OUTLINE,
                icon_color=ft.Colors.RED_400,
                tooltip="Excluir",
                visible=is_mine,
                on_click=lambda e, id=recipe['id']: vm.delete_recipe(id)
            )

            # [NOVO] Botão de Editar
            edit_icon = ft.IconButton(
                icon=ft.Icons.EDIT_OUTLINED,
                icon_color=ft.Colors.BLUE,
                tooltip="Editar",
                visible=is_mine,
                on_click=lambda e, id=recipe['id']: vm.navigate_to_edit(id)
            )

            list_controls.append(
                ft.Card(
                    content=ft.ListTile(
                        leading=ft.Icon(ft.Icons.RESTAURANT_MENU,
                                        color=ft.Colors.ORANGE),
                        title=ft.Text(recipe['title'],
                                      weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(
                            f"{recipe['preparation_time'] or '?'} min • {recipe['servings'] or 'N/A'}"),
                        # Adicionado edit_icon na Row
                        trailing=ft.Row(
                            controls=[edit_icon, fav_icon, delete_icon],
                            alignment=ft.MainAxisAlignment.END,
                            width=140
                        )
                    ),
                    elevation=1,
                    margin=ft.margin.symmetric(vertical=5)
                )
            )

        return ft.ListView(controls=list_controls, expand=True, padding=10, spacing=5)

    fab = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        content=ft.Row(
            [ft.Icon(ft.Icons.ADD), ft.Text(
                "Nova Receita", weight=ft.FontWeight.BOLD)],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5
        ),
        width=170,
        on_click=vm.navigate_to_create,
        bgcolor=page.theme.color_scheme.primary
    )

    return ft.View(
        route="/my_recipes",
        controls=[ft.SafeArea(content=build_list(), expand=True)],
        appbar=ft.AppBar(
            leading=ft.IconButton(ft.Icons.ARROW_BACK,
                                  on_click=lambda _: page.go("/")),
            title=ft.Text("Minhas Receitas"),
            bgcolor=page.theme.color_scheme.surface
        ),
        floating_action_button=fab,
        bgcolor=page.theme.color_scheme.surface
    )
