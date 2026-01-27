# ARQUIVO: src/views/recipe_detail_view.py
import flet as ft
from src.core.logger import get_logger
from src.database.recipe_queries import RecipeQueries

logger = get_logger("src.views.recipe_detail")


def RecipeDetailView(page: ft.Page) -> ft.View:
    recipe_id = page.data.get("detail_recipe_id")
    user = page.data.get("logged_in_user")

    db = RecipeQueries()
    recipe = db.get_recipe_details(recipe_id) if recipe_id else None

    # Função de retorno seguro
    def go_back(e):
        page.go("/my_recipes")

    if not recipe:
        return ft.View(
            route="/recipe_detail",
            appbar=ft.AppBar(title=ft.Text("Erro"), bgcolor=ft.Colors.RED),
            controls=[ft.Text("Receita não encontrada.")]
        )

    # Verifica propriedade para mostrar botão Editar
    is_owner = recipe['user_id'] == user.id if user else False

    # --- UI Components ---

    # 1. Cabeçalho (Título e Metadados)
    header = ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.RESTAURANT, size=60, color=ft.Colors.ORANGE_400),
            ft.Text(recipe['title'], size=24, weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER),
            ft.Row([
                ft.Icon(ft.Icons.TIMER, size=16),
                ft.Text(f"{recipe['preparation_time'] or '?'} min"),
                ft.Container(width=10),
                ft.Icon(ft.Icons.PEOPLE, size=16),
                ft.Text(f"{recipe['servings'] or 'N/A'}")
            ], alignment=ft.MainAxisAlignment.CENTER)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=20,
        bgcolor=ft.Colors.SURFACE_VARIANT,
        border_radius=10
    )

    # 2. Lista de Ingredientes
    ingredients_controls = []
    if recipe.get('ingredients'):
        for ing in recipe['ingredients']:
            ingredients_controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CIRCLE, size=8,
                                color=ft.Colors.GREEN),
                        ft.Text(
                            f"{ing['quantity'] or ''} {ing['unit'] or ''} {ing['name']}".strip(), size=16)
                    ]),
                    padding=5
                )
            )
    else:
        ingredients_controls.append(ft.Text("Sem ingredientes cadastrados."))

    # 3. Modo de Preparo
    instructions_text = ft.Text(
        recipe['instructions'],
        size=16,
        selectable=True,  # Permite copiar texto
        text_align=ft.TextAlign.JUSTIFY
    )

    # 4. Ações (Rodapé)
    actions_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=20)

    if is_owner:
        def on_edit(e):
            page.data["editing_recipe_id"] = recipe['id']
            page.go("/create_recipe")

        actions_row.controls.append(
            ft.ElevatedButton("Editar", icon=ft.Icons.EDIT, on_click=on_edit)
        )

    # Compartilhar/Imprimir (Placeholders visuais)
    actions_row.controls.append(
        ft.IconButton(icon=ft.Icons.SHARE, tooltip="Compartilhar (Em breve)")
    )

    return ft.View(
        route="/recipe_detail",
        appbar=ft.AppBar(
            leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=go_back),
            title=ft.Text("Detalhes"),
            center_title=True,
            bgcolor=page.theme.color_scheme.surface
        ),
        controls=[
            ft.SafeArea(
                content=ft.Column([
                    header,
                    ft.Divider(height=20),
                    ft.Text("Ingredientes", size=18,
                            weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY),
                    ft.Column(ingredients_controls),
                    ft.Divider(height=20),
                    ft.Text("Modo de Preparo", size=18,
                            weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY),
                    ft.Container(content=instructions_text, padding=10, border=ft.Border.all(
                        1, ft.Colors.OUTLINE_VARIANT), border_radius=8),
                    ft.Container(height=20),
                    actions_row
                ], scroll=ft.ScrollMode.AUTO, expand=True, spacing=10),
                expand=True,
                minimum=10  # Padding seguro
            )
        ],
        bgcolor=page.theme.color_scheme.surface
    )
