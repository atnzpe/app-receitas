# ARQUIVO: src/views/discovery_view.py
import flet as ft
from src.viewmodels.discovery_viewmodel import DiscoveryViewModel
from src.utils.theme import AppDimensions
from src.core.logger import get_logger

logger = get_logger("src.views.discovery")


def DiscoveryView(page: ft.Page) -> ft.View:
    try:
        vm = DiscoveryViewModel(page)
    except Exception as e:
        logger.critical(f"Falha VM: {e}")
        raise e

    # --- Elementos de UI ---
    results_count_text = ft.Text(
        "", size=14, color=ft.Colors.GREY_600, italic=True)

    tf_search = ft.TextField(
        label="Buscar",
        hint_text="Nome...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=12,
        expand=True,
        height=50,
        bgcolor=ft.Colors.WHITE
    )

    # [FIX] Suffix Icon Compatível
    tf_max_time = ft.TextField(
        label="Max Min",
        width=100, height=50,
        keyboard_type=ft.KeyboardType.NUMBER,
        bgcolor=ft.Colors.WHITE,
        border_radius=12
    )

    tf_servings = ft.TextField(
        label="Porções",
        width=100, height=50,
        bgcolor=ft.Colors.WHITE,
        border_radius=12
    )

    # Grid de Resultados (Configurado para Scroll)
    results_grid = ft.GridView(
        # [CRÍTICO] Permite ocupar altura e ativar scroll
        expand=True,
        runs_count=5,            # Tenta 5 colunas
        max_extent=220,          # Largura máxima do card
        child_aspect_ratio=0.75,  # Formato retrato
        spacing=10,
        run_spacing=10,
        padding=10,

    )

    def update_results_ui():
        try:
            results_grid.controls.clear()
            count = len(vm.recipes)
            results_count_text.value = f"{count} receitas" if count > 0 else ""

            if not vm.recipes:
                results_grid.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.SEARCH_OFF, size=50,
                                    color=ft.Colors.GREY_300),
                            ft.Text("Nada encontrado.",
                                    color=ft.Colors.GREY_500)
                        ], alignment="center"),
                        alignment=ft.Alignment(0, 0),
                        expand=True
                    )
                )
            else:
                for r in vm.recipes:
                    rid = r['id']
                    title = r.get('title', 'Sem Título')
                    img = r.get('image_path')

                    # Imagem do Card
                    if img and len(img) > 5:
                        img_widget = ft.Image(
                            src=img,
                            fit="cover",  # Use a string "cover" em vez de ft.ImageFit.COVER
                            expand=True,                            border_radius=ft.border_radius.only(
                                top_left=12, top_right=12)
                        )
                    else:
                        img_widget = ft.Container(
                            content=ft.Icon(ft.Icons.RESTAURANT,
                                            size=40, color=ft.Colors.ORANGE_200),
                            bgcolor=ft.Colors.ORANGE_50, alignment=ft.Alignment(0, 0), expand=True,
                            border_radius=ft.border_radius.only(
                                top_left=12, top_right=12)
                        )

                    # Card
                    card = ft.Container(
                        content=ft.Column([
                            ft.Container(content=img_widget, expand=3),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text(title, weight="bold", size=14,
                                            max_lines=2, overflow="ellipsis"),
                                    ft.Row([
                                        ft.Text(
                                            f"{r.get('preparation_time', '?')} min", size=12, color="grey"),
                                        ft.IconButton(
                                            icon=ft.Icons.STAR if r.get(
                                                'is_favorite') else ft.Icons.STAR_BORDER,
                                            icon_color="amber" if r.get(
                                                'is_favorite') else "grey",
                                            icon_size=20,
                                            on_click=lambda e, x=rid: [
                                                vm.toggle_favorite(x), update_results_ui()]
                                        )
                                    ], alignment="spaceBetween")
                                ]),
                                padding=10, expand=2
                            )
                        ], spacing=0),
                        bgcolor="white", border_radius=12,
                        shadow=ft.BoxShadow(
                            blur_radius=5, color=ft.Colors.with_opacity(0.1, "black")),
                        on_click=lambda e, x=rid: vm.navigate_to_details(x)
                    )
                    results_grid.controls.append(card)

            page.update()
        except Exception as e:
            logger.error(f"Erro UI: {e}")

    def execute_search(e=None):
        vm.search(tf_search.value, tf_max_time.value, tf_servings.value)
        update_results_ui()

    # Vínculos
    tf_search.on_submit = execute_search
    tf_max_time.on_submit = execute_search
    tf_servings.on_submit = execute_search
    btn_filter = ft.IconButton(
        ft.Icons.FILTER_LIST, on_click=execute_search, bgcolor=ft.Colors.ORANGE_100)

    # Render inicial
    update_results_ui()

    return ft.View(
        route="/discovery",
        bgcolor=ft.Colors.GREY_100,
        appbar=ft.AppBar(
            title=ft.Text("Discovery"),
            center_title=True,
            bgcolor="white",
            leading=ft.IconButton(
                ft.Icons.ARROW_BACK,
                on_click=lambda _: page.go("/")
            )
        ),
        controls=[
            ft.SafeArea(
                expand=True,
                content=ft.Column(
                    expand=True,
                    controls=[
                        # Bloco de Filtros (Fixo no topo)
                        ft.Container(
                            padding=15,
                            bgcolor="white",
                            border_radius=ft.border_radius.only(
                                bottom_left=20, bottom_right=20
                            ),
                            content=ft.Column([
                                ft.Row([tf_search, btn_filter], spacing=10),
                                ft.Row([tf_max_time, tf_servings], spacing=10),
                                results_count_text,
                                ft.Divider(),
                            ])
                        ),
                        # Área da Grid (Expansível com Scroll)
                        # O scroll deve ser aplicado na Coluna que contém a Grid ou na própria Grid
                        ft.Column(
                            controls=[results_grid],
                            scroll=ft.ScrollMode.AUTO,
                            expand=True,

                        )
                    ]
                )
            )
        ]
    )
