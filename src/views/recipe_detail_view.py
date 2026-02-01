# ARQUIVO: src/views/recipe_detail_view.py
import flet as ft
import traceback
from src.core.logger import get_logger
from src.database.recipe_queries import RecipeQueries

logger = get_logger("src.views.recipe_detail")


def RecipeDetailView(page: ft.Page) -> ft.View:
    """
    Tela de Detalhes da Receita.
    Exibe todas as informações e permite compartilhamento e edição.
    """
    logger.info(">>> Iniciando construção da RecipeDetailView")

    recipe_id = page.data.get("detail_recipe_id")
    user = page.data.get("logged_in_user")

    # [SMART BACK] Recupera a rota anterior definida na lista
    previous_route = page.data.get("previous_route", "/discovery")

    # --- Busca de Dados ---
    try:
        if not recipe_id:
            raise ValueError("ID não fornecido.")
        db = RecipeQueries()
        recipe = db.get_recipe_details(recipe_id)
        if not recipe:
            raise ValueError("Receita não encontrada.")
    except Exception as e:
        logger.critical(f"Erro ao carregar receita: {e}")
        return _build_error_view(page, str(e), previous_route)

    is_owner = (user and recipe.get('user_id') == user.id)

    # --- Construção da UI ---
    try:
        def go_back(e):
            logger.info(f"Voltando para contexto: {previous_route}")
            page.go(previous_route)

        def share_recipe(e):
            page.snack_bar = ft.SnackBar(ft.Text("Link copiado! (Simulado)"))
            page.snack_bar.open = True
            page.update()

        # 1. Imagem Hero
        img_src = recipe.get('image_path')
        if img_src and len(img_src) > 5:
            image_control = ft.Image(
                src=img_src,
                width=float('inf'),
                height=250,
                # [CORREÇÃO CRÍTICA] Usando string para compatibilidade total
                fit="cover",
                error_content=ft.Container(
                    content=ft.Icon(ft.Icons.BROKEN_IMAGE,
                                    size=50, color=ft.Colors.GREY_400),
                    alignment=ft.Alignment(0, 0),
                    bgcolor=ft.Colors.GREY_200
                )
            )
        else:
            # Fallback elegante
            image_control = ft.Container(
                content=ft.Icon(ft.Icons.RESTAURANT, size=60,
                                color=ft.Colors.ORANGE_300),
                alignment=ft.Alignment(0, 0),
                height=180,
                bgcolor=ft.Colors.ORANGE_50
            )

        header_image_container = ft.Container(
            content=image_control,
            border_radius=12,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            margin=ft.margin.only(bottom=15)
        )

        # 2. Informações Principais
        title_section = ft.Column([
            ft.Text(recipe['title'], size=28, weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER),
            ft.Row([
                ft.Icon(ft.Icons.TIMER_OUTLINED,
                        size=18, color=ft.Colors.GREY),
                ft.Text(f"{recipe.get('preparation_time')} min"),
                ft.Container(width=15),
                ft.Icon(ft.Icons.PEOPLE_OUTLINE,
                        size=18, color=ft.Colors.GREY),
                ft.Text(f"{recipe.get('servings')} porções"),
            ], alignment=ft.MainAxisAlignment.CENTER)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        # 3. Ingredientes
        ing_controls = []
        if recipe.get('ingredients'):
            for ing in recipe['ingredients']:
                ing_controls.append(ft.Row([
                    ft.Icon(ft.Icons.CHECK_CIRCLE, size=16,
                            color=ft.Colors.GREEN),
                    ft.Text(
                        f"{ing['name']} - {ing['quantity'] or ''} {ing['unit'] or ''}")
                ]))
        else:
            ing_controls.append(
                ft.Text("Sem ingredientes.", italic=True, color=ft.Colors.GREY))

        ingredients_list = ft.Column(ing_controls, spacing=5)

        # 4. Instruções
        instructions_text = ft.Text(recipe.get(
            'instructions', ''), size=16, selectable=True)

        # 5. Dicas e Fonte (Refinado conforme DoD da Sprint 5)
        extras = []
        if recipe.get('additional_instructions'):
            extras.append(
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.LIGHTBULB_CIRCLE,
                                    color=ft.Colors.AMBER_700),
                            ft.Text("Dica do Chef",
                                    weight=ft.FontWeight.BOLD, size=16)
                        ]),
                        ft.Text(recipe['additional_instructions'],
                                italic=True, size=14)
                    ], spacing=5),
                    bgcolor=ft.Colors.AMBER_50,
                    padding=15,
                    border_radius=10,
                    border=ft.Border.all(1, ft.Colors.AMBER_200),
                    margin=ft.margin.only(top=10)
                )
            )

        if recipe.get('source'):
            extras.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.LANGUAGE, size=16,
                                color=ft.Colors.BLUE_700),
                        ft.Text(
                            f"Origem: {recipe['source']}", color=ft.Colors.BLUE_700, weight=ft.FontWeight.W_500)
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    padding=ft.padding.only(top=10)
                )
            )
        # 6. Barra de Ações
        actions = [
            ft.IconButton(ft.Icons.SHARE, tooltip="Compartilhar",
                          on_click=share_recipe)
        ]
        if is_owner:
            def on_edit(e):
                logger.info(f"Navegando para edição da receita {recipe['id']}")
                page.data["editing_recipe_id"] = recipe['id']
                page.go("/create_recipe")

            actions.insert(0, ft.IconButton(
                ft.Icons.EDIT, tooltip="Editar", icon_color=ft.Colors.BLUE, on_click=on_edit))

        return ft.View(
            route="/recipe_detail",
            appbar=ft.AppBar(
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=go_back),
                title=ft.Text("Detalhes"),
                actions=actions,
                bgcolor=ft.Colors.WHITE,
                center_title=True
            ),
            controls=[
                ft.SafeArea(
                    content=ft.Container(
                        content=ft.Column([
                            header_image_container,
                            title_section,
                            ft.Divider(),
                            ft.Text(
                                "Ingredientes", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_800),
                            ingredients_list,
                            ft.Divider(),
                            ft.Text(
                                "Modo de Preparo", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_800),
                            ft.Container(
                                content=instructions_text,
                                padding=15,
                                bgcolor=ft.Colors.GREY_50,
                                border_radius=8,
                                border=ft.Border.all(1, ft.Colors.GREY_300)
                            ),
                            ft.Column(extras, spacing=10),
                            ft.Container(height=30)
                        ], scroll=ft.ScrollMode.AUTO),
                        padding=20,
                        expand=True
                    ),
                    expand=True
                )
            ],
            bgcolor=ft.Colors.WHITE
        )

    except Exception as e:
        logger.critical(f"Erro visual fatal: {traceback.format_exc()}")
        return _build_error_view(page, str(e), previous_route)


def _build_error_view(page, message, back_route):
    return ft.View(
        route="/recipe_detail",
        appbar=ft.AppBar(title=ft.Text("Erro"), bgcolor=ft.Colors.RED_100, leading=ft.IconButton(
            ft.Icons.ARROW_BACK, on_click=lambda _: page.go(back_route))),
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ERROR_OUTLINE,
                            size=64, color=ft.Colors.RED),
                    ft.Text(f"Erro: {message}", size=18,
                            color=ft.Colors.RED_900)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.Alignment(0, 0),
                expand=True
            )
        ],
        bgcolor=ft.Colors.WHITE
    )
