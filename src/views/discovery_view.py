# ARQUIVO: src/views/discovery_view.py
import flet as ft
import traceback
from src.viewmodels.discovery_viewmodel import DiscoveryViewModel
from src.utils.theme import AppDimensions
from src.core.logger import get_logger

# Inicialização do Logger Tático
logger = get_logger("src.views.discovery")


def DiscoveryView(page: ft.Page) -> ft.View:
    logger.info(">>> Iniciando construção da DiscoveryView")

    try:
        vm = DiscoveryViewModel(page)
    except Exception as e:
        logger.critical(f"Falha fatal ao iniciar ViewModel: {e}")
        raise e

    # --- Elementos de UI ---

    # Campo de busca
    search_field = ft.TextField(
        label="Buscar por Nome",
        hint_text="Ex: Bolo de Cenoura",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=AppDimensions.BORDER_RADIUS,
        on_submit=lambda e: execute_search(),
        expand=True,
        text_size=16,
        bgcolor=ft.Colors.GREY_100,
        color=ft.Colors.ON_SURFACE
    )

    # Container onde os resultados serão renderizados dinamicamente
    results_container = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=10
    )

    def update_results_ui():
        """
        Reconstrói a lista de resultados baseada em vm.recipes.
        Blindagem: Tratamento de exceção para evitar crash na renderização.
        """
        try:
            logger.debug("Iniciando atualização da UI de resultados...")
            results_container.controls.clear()

            count = len(vm.recipes)
            logger.info(f"Dados recebidos do ViewModel. Qtd receitas: {count}")

            if not vm.recipes:
                # Estado Vazio / Sem Resultados
                _render_empty_state()
            else:
                # Renderiza Lista
                _render_recipe_list()

            page.update()
            logger.debug("UI atualizada com sucesso.")

        except Exception as e:
            # Captura erro de UI e evita crash total
            error_trace = traceback.format_exc()
            logger.error(
                f"ERRO CRÍTICO NA RENDERIZAÇÃO: {e}\nTraceback: {error_trace}")

            # Feedback visual de erro para o usuário (Fail-Safe)
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Erro ao exibir resultados: {e}"),
                bgcolor=ft.Colors.ERROR
            )
            page.snack_bar.open = True
            page.update()

    def _render_empty_state():
        logger.debug("Renderizando estado vazio.")
        if not search_field.value:
            icon_bg = ft.Icons.AUTO_AWESOME
            title_bg = "Descubra Novos Sabores"
            desc_bg = "Selecione o modo acima e digite para começar."
        else:
            icon_bg = ft.Icons.SEARCH_OFF
            title_bg = "Nada encontrado"
            desc_bg = f"Não achamos receitas para '{search_field.value}'."

        results_container.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Icon(icon_bg, size=80, color=ft.Colors.GREY_300),
                    ft.Text(title_bg, size=20, weight=ft.FontWeight.BOLD,
                            color=ft.Colors.ON_SURFACE),
                    ft.Text(desc_bg, color=ft.Colors.ON_SURFACE_VARIANT,
                            text_align=ft.TextAlign.CENTER),
                ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10),
                alignment=ft.Alignment(0, 0),
                padding=40
            )
        )

    def _render_recipe_list():
        logger.debug("Iterando sobre receitas para criação de Cards...")
        for recipe in vm.recipes:
            try:
                is_fav = bool(recipe.get('is_favorite', 0))
                recipe_id = recipe.get('id')
                title = recipe.get('title', 'Sem Título')

                # Log detalhado por item (Verbose)
                # logger.debug(f"Processando receita ID: {recipe_id} - {title}")

                subtitle_content = [
                    ft.Text(f"{recipe.get('preparation_time', '?')} min")]

                if vm.search_mode == 'pantry' and 'match_count' in recipe:
                    matches = recipe['match_count']
                    subtitle_content.append(ft.Container(width=5))
                    subtitle_content.append(
                        ft.Container(
                            content=ft.Text(
                                f"{matches} coincidem", size=12, color=ft.Colors.WHITE),
                            bgcolor=ft.Colors.GREEN_600,
                            padding=ft.padding.symmetric(
                                horizontal=8, vertical=2),
                            border_radius=4
                        )
                    )

                card_content = ft.ListTile(
                    leading=ft.Container(
                        content=ft.Icon(ft.Icons.RESTAURANT_MENU,
                                        color=ft.Colors.ORANGE_700),
                        bgcolor=ft.Colors.ORANGE_50,
                        padding=10,
                        border_radius=10
                    ),
                    title=ft.Text(title, weight=ft.FontWeight.BOLD),
                    subtitle=ft.Row(subtitle_content, spacing=0),
                    trailing=ft.IconButton(
                        icon=ft.Icons.STAR if is_fav else ft.Icons.STAR_BORDER,
                        icon_color=ft.Colors.AMBER if is_fav else ft.Colors.GREY_400,
                        tooltip="Favoritar",
                        on_click=lambda e, id=recipe_id: [
                            logger.info(f"Click: Favoritar ID {id}"),
                            vm.toggle_favorite(id),
                            update_results_ui()
                        ]
                    ),
                    on_click=lambda e, id=recipe_id: [
                        logger.info(f"Click: Detalhes ID {id}"),
                        vm.navigate_to_details(id)
                    ]
                )

                # [CORREÇÃO ESTRUTURAL]
                # Card não recebe cor. O Container interno recebe a cor.
                # Isso resolve o erro TypeError: Card.__init__() got unexpected keyword 'color'
                results_container.controls.append(
                    ft.Card(
                        elevation=2,
                        margin=ft.margin.only(bottom=5),
                        content=ft.Container(
                            content=card_content,
                            bgcolor=ft.Colors.WHITE,  # Cor aplicada aqui com segurança
                            border_radius=12,        # Arredondamento visual
                            padding=5
                        )
                    )
                )
            except Exception as item_error:
                logger.error(f"Erro ao renderizar item da lista: {item_error}")
                continue  # Pula item quebrado, não quebra a lista toda

    def execute_search():
        logger.info(f"ACTION: Disparando busca por: '{search_field.value}'")
        vm.search(search_field.value)
        update_results_ui()

    search_button = ft.IconButton(
        icon=ft.Icons.ARROW_FORWARD,
        bgcolor=ft.Colors.PRIMARY,
        icon_color=ft.Colors.ON_PRIMARY,
        on_click=lambda e: execute_search(),
        tooltip="Pesquisar"
    )

    # --- Botões de Modo ---
    btn_mode_name = ft.ElevatedButton(
        content=ft.Row([ft.Icon(ft.Icons.SEARCH),
                       ft.Text("Por Nome")], spacing=5),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            bgcolor=ft.Colors.PRIMARY,
            color=ft.Colors.ON_PRIMARY,
        ),
        on_click=lambda e: set_mode("name")
    )

    btn_mode_pantry = ft.OutlinedButton(
        content=ft.Row([ft.Icon(ft.Icons.KITCHEN),
                       ft.Text("Minha Dispensa")], spacing=5),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            color=ft.Colors.ON_SURFACE_VARIANT,
            side=ft.BorderSide(1, ft.Colors.OUTLINE)
        ),
        on_click=lambda e: set_mode("pantry")
    )

    def set_mode(mode):
        logger.info(f"ACTION: Alternando modo para: {mode}")
        vm.toggle_mode(mode)

        # Atualiza visual dos botões
        if mode == "name":
            btn_mode_name.style.bgcolor = ft.Colors.PRIMARY
            btn_mode_name.style.color = ft.Colors.ON_PRIMARY
            btn_mode_pantry.style.bgcolor = None
            btn_mode_pantry.style.color = ft.Colors.ON_SURFACE_VARIANT
            btn_mode_pantry.style.side = ft.BorderSide(1, ft.Colors.OUTLINE)
            search_field.label = "Nome da Receita"
            search_field.hint_text = "Ex: Lasanha, Pudim..."
            search_field.prefix_icon = ft.Icons.SEARCH
        else:
            btn_mode_name.style.bgcolor = None
            btn_mode_name.style.color = ft.Colors.ON_SURFACE_VARIANT
            btn_mode_pantry.style.bgcolor = ft.Colors.PRIMARY
            btn_mode_pantry.style.color = ft.Colors.ON_PRIMARY
            btn_mode_pantry.style.side = ft.BorderSide(
                0, ft.Colors.TRANSPARENT)
            search_field.label = "O que tem na geladeira?"
            search_field.hint_text = "Ex: ovo, leite, farinha"
            search_field.prefix_icon = ft.Icons.KITCHEN

        search_field.value = ""
        search_field.focus()
        update_results_ui()

    # --- Inicialização ---
    update_results_ui()

    tab_buttons_row = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(content=btn_mode_name, expand=True),
                ft.Container(width=10),
                ft.Container(content=btn_mode_pantry, expand=True),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        bgcolor=ft.Colors.SURFACE,
        alignment=ft.Alignment(0, 0)
    )

    return ft.View(
        route="/discovery",
        controls=[
            ft.SafeArea(
                content=ft.Column([
                    tab_buttons_row,
                    ft.Container(
                        content=ft.Row([search_field, search_button]),
                        padding=ft.padding.symmetric(
                            horizontal=20, vertical=10),
                        bgcolor=page.theme.color_scheme.surface
                    ),
                    ft.Divider(height=1, color=ft.Colors.GREY_300),
                    ft.Container(content=results_container,
                                 expand=True, padding=10)
                ], expand=True)
            )
        ],
        appbar=ft.AppBar(
            leading=ft.IconButton(ft.Icons.ARROW_BACK,
                                  on_click=lambda _: page.go("/")),
            title=ft.Text("Discovery"),
            center_title=True,
            bgcolor=page.theme.color_scheme.surface
        ),
        bgcolor=page.theme.color_scheme.surface
    )
