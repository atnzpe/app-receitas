# ARQUIVO: src/views/recipe_detail_view.py
import flet as ft
import traceback
from src.core.logger import get_logger
from src.database.recipe_queries import RecipeQueries

# Inicialização do Logger Tático
logger = get_logger("src.views.recipe_detail")


def RecipeDetailView(page: ft.Page) -> ft.View:
    logger.info(">>> Iniciando construção da RecipeDetailView")

    recipe_id = page.data.get("detail_recipe_id")
    user = page.data.get("logged_in_user")

    try:
        if not recipe_id:
            logger.warning("Tentativa de acesso sem ID de receita.")
            raise ValueError("ID da receita não fornecido.")

        logger.info(f"Buscando detalhes da receita ID: {recipe_id}")
        db = RecipeQueries()
        recipe = db.get_recipe_details(recipe_id)

        if not recipe:
            logger.error(f"Receita ID {recipe_id} não encontrada no banco.")
            return _build_error_view(page, "Receita não encontrada.")

    except Exception as e:
        logger.critical(f"Erro fatal ao buscar dados: {e}")
        return _build_error_view(page, f"Erro ao carregar dados: {str(e)}")

    # Lógica de Permissão
    is_owner = False
    if user and recipe.get('user_id') == user.id:
        is_owner = True

    # --- Construção da UI Segura ---
    try:
        def go_back(e):
            logger.info("Navegando de volta para Discovery/Lista.")
            page.go("/discovery")

        # Cabeçalho com Ícone e Título
        header = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.RESTAURANT_MENU, size=64,
                        color=ft.Colors.ORANGE_400),
                ft.Text(
                    recipe['title'],
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Row([
                    ft.Icon(ft.Icons.TIMER, size=16, color=ft.Colors.GREY_600),
                    ft.Text(f"{recipe.get('preparation_time') or '?'} min"),
                    ft.Container(width=10),
                    ft.Icon(ft.Icons.PEOPLE, size=16,
                            color=ft.Colors.GREY_600),
                    ft.Text(f"{recipe.get('servings') or 'N/A'} porções")
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            bgcolor=ft.Colors.GREY_200,
            border_radius=12
        )

        # Lista de Ingredientes
        ingredients_controls = []
        if recipe.get('ingredients'):
            for ing in recipe['ingredients']:
                ingredients_controls.append(
                    ft.Row([
                        ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE,
                                size=16, color=ft.Colors.GREEN),
                        ft.Text(
                            f"{ing['name']} - {ing['quantity'] or ''} {ing['unit'] or ''}", size=16)
                    ])
                )
        else:
            ingredients_controls.append(
                ft.Text("Sem ingredientes cadastrados.", italic=True, color=ft.Colors.GREY))

        ingredients_list = ft.Column(controls=ingredients_controls, spacing=5)

        # Modo de Preparo
        instructions_text = ft.Text(
            recipe.get('instructions', 'Sem instruções.'),
            size=16,
            selectable=True
        )

        # Ações (Editar - Apenas Dono)
        actions_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=20)

        if is_owner:
            def on_edit(e):
                logger.info(f"Navegando para edição da receita {recipe['id']}")
                page.data["editing_recipe_id"] = recipe['id']
                page.go("/create_recipe")

            actions_row.controls.append(
                ft.ElevatedButton(
                    content=ft.Row(
                        [ft.Icon(ft.Icons.EDIT), ft.Text("Editar Receita")], spacing=5),
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE),
                    on_click=on_edit
                )
            )

        # Retorno da View Principal
        return ft.View(
            route="/recipe_detail",
            appbar=ft.AppBar(
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=go_back),
                title=ft.Text("Detalhes da Receita"),
                bgcolor=ft.Colors.GREY_100
                # [CORREÇÃO] Removed surface_tint_color
            ),
            controls=[
                ft.SafeArea(
                    content=ft.Column([
                        header,
                        ft.Divider(),
                        ft.Text(
                            "Ingredientes", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_800),
                        ingredients_list,
                        ft.Divider(),
                        ft.Text("Modo de Preparo", size=20,
                                weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_800),
                        ft.Container(
                            content=instructions_text,
                            padding=15,
                            bgcolor=ft.Colors.GREY_50,
                            border_radius=8,
                            # [CORREÇÃO] ft.Border.all (Maiúsculo)
                            border=ft.Border.all(1, ft.Colors.GREY_300)
                        ),
                        ft.Container(height=20),
                        actions_row
                    ], scroll=ft.ScrollMode.AUTO, expand=True, spacing=10),
                    expand=True
                    # [CORREÇÃO] Removed minimum=10
                )
            ],
            bgcolor=ft.Colors.WHITE
        )

    except Exception as e:
        logger.critical(
            f"Erro ao renderizar UI de detalhes: {traceback.format_exc()}")
        return _build_error_view(page, f"Erro visual: {e}")


def _build_error_view(page, message):
    """Renderiza uma tela de erro segura para não fechar o app."""
    return ft.View(
        route="/recipe_detail",
        appbar=ft.AppBar(
            leading=ft.IconButton(ft.Icons.ARROW_BACK,
                                  on_click=lambda _: page.go("/discovery")),
            title=ft.Text("Erro"),
            bgcolor=ft.Colors.RED_100
        ),
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ERROR_OUTLINE,
                            size=64, color=ft.Colors.RED),
                    ft.Text(message, size=18, color=ft.Colors.RED_900,
                            text_align=ft.TextAlign.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.Alignment(0, 0),
                expand=True
            )
        ],
        bgcolor=ft.Colors.WHITE
    )
