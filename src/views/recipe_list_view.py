# ARQUIVO: src/views/recipe_list_view.py
import flet as ft
from src.viewmodels.recipe_list_viewmodel import RecipeListViewModel


def RecipeListView(page: ft.Page) -> ft.View:
    vm = RecipeListViewModel(page)

    # Configura o modo para "my" (Minhas Receitas) explicitamente
    vm.current_mode = "my"
    vm.load_recipes()

    def build_list():
        if not vm.recipes:
            return ft.Column(
                [
                    ft.Icon(ft.Icons.NO_MEALS, size=64,
                            color=ft.Colors.GREY_400),
                    ft.Text("Você ainda não tem receitas.",
                            color=ft.Colors.GREY_500),
                    ft.Text("Crie uma nova ou favorite alguma!",
                            color=ft.Colors.GREY_400, size=12)
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
                visible=is_mine,  # Só dono deleta
                on_click=lambda e, id=recipe['id']: vm.delete_recipe(id)
            )

            edit_icon = ft.IconButton(
                icon=ft.Icons.EDIT_OUTLINED,
                icon_color=ft.Colors.BLUE,
                visible=is_mine,  # Só dono edita
                on_click=lambda e, id=recipe['id']: vm.navigate_to_edit(id)
            )

            # Card Clicável -> Leva aos Detalhes (Modo Leitura)
            card_content = ft.ListTile(
                leading=ft.Icon(ft.Icons.RESTAURANT_MENU,
                                color=ft.Colors.ORANGE),
                title=ft.Text(recipe['title'], weight=ft.FontWeight.BOLD),
                subtitle=ft.Text(
                    f"{recipe['preparation_time'] or '?'} min • {recipe['servings'] or 'N/A'}"),
                trailing=ft.Row(
                    controls=[edit_icon, fav_icon, delete_icon],
                    alignment=ft.MainAxisAlignment.END,
                    width=140
                ),
                # AÇÃO DE CLIQUE: Navega para leitura completa
                on_click=lambda e, id=recipe['id']: vm.navigate_to_details(id)
            )

            list_controls.append(
                ft.Card(
                    content=card_content,
                    elevation=2,
                    margin=ft.margin.symmetric(vertical=5)
                )
            )

        return ft.ListView(controls=list_controls, expand=True, padding=10, spacing=5)

    fab = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        content=ft.Row([ft.Icon(ft.Icons.ADD), ft.Text("Nova")],
                       alignment="center", spacing=5),
        width=120,
        on_click=vm.navigate_to_create,
        bgcolor=page.theme.color_scheme.primary
    )

    return ft.View(
        route="/my_recipes",
        controls=[
            ft.SafeArea(
                content=ft.Column([
                    # Removemos as Abas. Agora é só a lista direta.
                    build_list()
                ], expand=True)
            )
        ],
        appbar=ft.AppBar(
            leading=ft.IconButton(ft.Icons.ARROW_BACK,
                                  on_click=lambda _: page.go("/")),
            title=ft.Text("Minhas Receitas"),
            center_title=True,
            bgcolor=page.theme.color_scheme.surface,
            elevation=0
        ),
        floating_action_button=fab,
        bgcolor=page.theme.color_scheme.surface
    )
