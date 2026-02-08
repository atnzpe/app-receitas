# ARQUIVO: src/views/recipe_list_view.py
import flet as ft
from src.viewmodels.recipe_list_viewmodel import RecipeListViewModel


def RecipeListView(page: ft.Page) -> ft.View:
    vm = RecipeListViewModel(page)

    # [SCROLL FIX] GridView deve ser o controle principal para ter scrollbar nativa
    recipes_list = ft.GridView(
        expand=True,          # Ocupa todo o espaço vertical disponível
        runs_count=1,         # 1 Coluna = Comportamento de Lista
        max_extent=600,       # Largura máxima dos cards
        child_aspect_ratio=4.0,
        spacing=10,
        padding=20,
        # Auto-scroll é nativo do GridView, não precisa configurar 'scroll' aqui
    )

    def render_recipes():
        recipes_list.controls.clear()

        if not vm.recipes:
            # Estado Vazio
            recipes_list.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.NO_MEALS, size=64,
                                color=ft.Colors.GREY_400),
                        ft.Text("Nenhuma receita encontrada.",
                                color=ft.Colors.GREY_500)
                    ], horizontal_alignment="center", spacing=10),
                    alignment=ft.Alignment(0, 0),
                    padding=40
                )
            )
        else:
            # Renderização dos Cards
            for r in vm.recipes:
                is_owner = (vm.user and r['user_id'] == vm.user.id)
                img_url = r.get('image_path')
                is_fav = bool(r.get('is_favorite', 0))

                # Miniatura (Imagem ou Ícone)
                if img_url and len(img_url) > 5:
                    leading_content = ft.Image(
                        src=img_url, width=60, height=60, fit="cover", border_radius=8)
                else:
                    leading_content = ft.Container(
                        content=ft.Icon(ft.Icons.RESTAURANT_MENU,
                                        color=ft.Colors.ORANGE_600),
                        bgcolor=ft.Colors.ORANGE_50, width=60, height=60,
                        border_radius=8, alignment=ft.Alignment(0, 0)
                    )

                # Ações (Menu ou Favorito)
                if is_owner:
                    trailing = ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(
                                content=ft.Text("Editar"), icon=ft.Icons.EDIT,
                                on_click=lambda e, rid=r['id']: vm.navigate_to_edit(
                                    rid)
                            ),
                            ft.PopupMenuItem(
                                content=ft.Text("Excluir"), icon=ft.Icons.DELETE,
                                on_click=lambda e, rid=r['id']: vm.delete_recipe(
                                    rid)
                            ),
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

                # Adiciona o Card ao GridView
                recipes_list.controls.append(
                    ft.Card(
                        elevation=2,  # Leve aumento para destaque
                        content=ft.Container(
                            padding=5,
                            bgcolor=ft.Colors.WHITE,
                            border_radius=10,
                            content=ft.ListTile(
                                leading=leading_content,
                                title=ft.Text(
                                    r['title'], weight=ft.FontWeight.W_600),
                                subtitle=ft.Text(
                                    f"{r.get('preparation_time', '?')} min • {r.get('servings', '?')} porções"),
                                trailing=trailing,
                                on_click=lambda e, rid=r['id']: vm.navigate_to_details(
                                    rid)
                            )
                        )
                    )
                )
        page.update()

    # Hook para recarregar lista
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
                # [CORREÇÃO CRÍTICA]
                # Removemos a ft.Column(scroll=AUTO) e colocamos o recipes_list direto.
                # Como recipes_list é um GridView com expand=True, ele vai gerenciar
                # o scroll e exibir a barra lateral definida no theme.py.
                content=recipes_list,
                expand=True
            )
        ]
    )
