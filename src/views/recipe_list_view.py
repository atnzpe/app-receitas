# ARQUIVO: src/views/recipe_list_view.py
import flet as ft
from src.viewmodels.recipe_list_viewmodel import RecipeListViewModel


def RecipeListView(page: ft.Page) -> ft.View:
    vm = RecipeListViewModel(page)

    # [SCROLL FIX] GridView usado como lista (runs_count=1) mas com performance de grid
    recipes_list = ft.GridView(
        expand=True,
        runs_count=1,            # 1 Coluna = Lista
        # Largura máxima (responsivo em telas gigantes)
        max_extent=600,
        child_aspect_ratio=4.0,  # Card bem horizontal
        spacing=10,
        padding=20,
    )

    def render_recipes():
        recipes_list.controls.clear()

        if not vm.recipes:
            recipes_list.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.NO_MEALS, size=64,
                                color=ft.Colors.GREY_400),
                        ft.Text("Nenhuma receita encontrada.",
                                color=ft.Colors.GREY_500)
                    ], horizontal_alignment="center"),
                    alignment=ft.Alignment(0, 0), padding=40
                )
            )
        else:
            for r in vm.recipes:
                is_owner = (vm.user and r['user_id'] == vm.user.id)
                img_url = r.get('image_path')
                is_fav = bool(r.get('is_favorite', 0))

                # Miniatura
                if img_url and len(img_url) > 5:
                    leading_content = ft.Image(
                        src=img_url, width=60, height=60, fit="cover", border_radius=8)
                else:
                    leading_content = ft.Container(
                        content=ft.Icon(ft.Icons.RESTAURANT_MENU,
                                        color=ft.Colors.ORANGE_600),
                        bgcolor=ft.Colors.ORANGE_50, width=60, height=60, border_radius=8, alignment=ft.Alignment(0, 0)
                    )

                # Ações: Editar (Dono) ou Favoritar (Visitante)
                if is_owner:
                    trailing = ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(content=ft.Text(
                                "Editar"), icon=ft.Icons.EDIT, on_click=lambda e, rid=r['id']: vm.navigate_to_edit(rid)),
                            ft.PopupMenuItem(content=ft.Text(
                                "Excluir"), icon=ft.Icons.DELETE, on_click=lambda e, rid=r['id']: vm.delete_recipe(rid)),
                        ]
                    )
                else:
                    trailing = ft.IconButton(
                        icon=ft.Icons.STAR if is_fav else ft.Icons.STAR_BORDER,
                        icon_color=ft.Colors.AMBER if is_fav else ft.Colors.GREY_400,
                        tooltip="Favoritar",
                        on_click=lambda e, rid=r['id']: [
                            vm.toggle_favorite(rid), render_recipes()]
                    )

                recipes_list.controls.append(
                    ft.Card(
                        elevation=1,
                        content=ft.Container(
                            padding=10,
                            bgcolor=ft.Colors.WHITE,
                            border_radius=10,
                            content=ft.ListTile(
                                leading=leading_content,
                                title=ft.Text(
                                    r['title'], weight=ft.FontWeight.W_600),
                                subtitle=ft.Text(
                                    f"{r.get('preparation_time', '?')} min"),
                                trailing=trailing,
                                on_click=lambda e, rid=r['id']: vm.navigate_to_details(
                                    rid)
                            )
                        )
                    )
                )
        page.update()

    original_load = vm.load_recipes
    vm.load_recipes = lambda: (original_load(), render_recipes())
    vm.load_recipes()

    return ft.View(
        route="/my_recipes",
        bgcolor=ft.Colors.GREY_100,
        floating_action_button=ft.FloatingActionButton(
            content=ft.Row([ft.Icon(ft.Icons.ADD), ft.Text(
                "Nova")], alignment="center", spacing=5),
            bgcolor=ft.Colors.ORANGE_600,
            width=120,
            on_click=vm.navigate_to_create
        ),
        appbar=ft.AppBar(
            title=ft.Text("Minhas Receitas"),
            center_title=True,
            bgcolor=ft.Colors.WHITE,
            leading=ft.IconButton(ft.Icons.ARROW_BACK,
                                  on_click=lambda _: page.go("/"))
        ),
        controls=[
            ft.SafeArea(
                content=ft.Column([
                    ft.Container(content=recipes_list, expand=True)
                ], expand=True)
            )
        ]
    )
