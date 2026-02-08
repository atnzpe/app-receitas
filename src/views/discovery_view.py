# ARQUIVO: src/views/discovery_view.py
import flet as ft
from src.viewmodels.discovery_viewmodel import DiscoveryViewModel
from src.core.logger import get_logger

logger = get_logger("src.views.discovery")


def DiscoveryView(page: ft.Page) -> ft.View:
    try:
        vm = DiscoveryViewModel(page)
    except Exception as e:
        logger.critical(f"Falha VM: {e}")
        raise e

    # --- Funções Lógicas ---
    def execute_search(e=None):
        vm.search(
            term=tf_search.value,
            max_time=str(int(slider_time.value)),
            servings=tf_servings.value,
            category_val=dd_category.value
        )
        update_results_ui()

    def clear_filters(e=None):
        tf_search.value = ""
        dd_category.value = "0"
        slider_time.value = 0
        time_label.value = "Tempo: Qualquer"
        tf_servings.value = ""

        # Atualiza a UI
        tf_search.update()
        dd_category.update()
        slider_time.update()
        time_label.update()
        tf_servings.update()

        execute_search()

    # --- Elementos de Filtro (UX Modernizada) ---

    # 1. Busca Textual
    tf_search = ft.TextField(
        label="Buscar Receita",
        hint_text="Ex: Bolo...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=12,
        expand=True,
        height=50,
        bgcolor=ft.Colors.WHITE,
        text_size=14,
        on_submit=lambda e: execute_search()
    )

    # 2. Categoria (Dropdown)
    # [BLINDAGEM] on_change removido do construtor
    dd_category = ft.Dropdown(
        label="Categoria",
        options=vm.categories_options,
        value=str(vm.active_category_id),
        width=180,
        height=50,
        bgcolor=ft.Colors.WHITE,
        border_radius=12,
        content_padding=10,
        text_size=14
    )
    # [BLINDAGEM] Evento atribuído pós-inicialização
    dd_category.on_change = lambda e: execute_search()

    # 3. Slider de Tempo
    time_label = ft.Text("Tempo: Qualquer", size=12, color=ft.Colors.GREY_700)

    def on_slider_change(e):
        val = int(e.control.value)
        time_label.value = f"Tempo: < {val} min" if val > 0 else "Tempo: Qualquer"
        time_label.update()

    slider_time = ft.Slider(
        min=0, max=120, divisions=12, value=0,
        label="{value} min",
        width=150,
        active_color=ft.Colors.ORANGE_600,
        on_change=on_slider_change,
        on_change_end=lambda e: execute_search()
    )

    # 4. Porções
    tf_servings = ft.TextField(
        label="Porções",
        width=80, height=50,
        bgcolor=ft.Colors.WHITE,
        border_radius=12,
        text_size=12,
        keyboard_type=ft.KeyboardType.NUMBER,
        on_submit=lambda e: execute_search()
    )

    results_count_text = ft.Text(
        "", size=12, color=ft.Colors.GREY_600, italic=True)

    # --- Grid de Resultados ---
    results_grid = ft.GridView(
        expand=True,
        runs_count=5,
        max_extent=220,
        child_aspect_ratio=0.75,
        spacing=15,
        run_spacing=15,
        padding=15,
    )

    def update_results_ui():
        results_grid.controls.clear()
        count = len(vm.recipes)
        results_count_text.value = f"{count} receitas encontradas"

        if not vm.recipes:
            # EMPTY STATE
            results_grid.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.SEARCH_OFF, size=60,
                                color=ft.Colors.GREY_300),
                        ft.Text("Nenhuma receita encontrada.",
                                color=ft.Colors.GREY_500, size=16),
                        ft.Container(height=10),
                        ft.OutlinedButton(
                            "Limpar Filtros",
                            icon=ft.Icons.REFRESH,
                            on_click=clear_filters,
                            style=ft.ButtonStyle(color=ft.Colors.ORANGE_700)
                        )
                    ], alignment="center", horizontal_alignment="center"),
                    # [CORREÇÃO] Substituído ft.alignment.center por ft.Alignment(0, 0)
                    alignment=ft.Alignment(0, 0),
                    expand=True,
                    padding=ft.padding.only(top=50)
                )
            )
        else:
            for r in vm.recipes:
                rid = r['id']
                img = r.get('image_path')

                # Card de Receita
                card = ft.Container(
                    content=ft.Column([
                        # Imagem
                        ft.Container(
                            content=ft.Image(src=img, fit="cover", expand=True) if img and len(img) > 5
                            else ft.Icon(ft.Icons.RESTAURANT, size=40, color=ft.Colors.ORANGE_200),
                            bgcolor=ft.Colors.ORANGE_50,
                            expand=3,
                            border_radius=ft.border_radius.only(
                                top_left=12, top_right=12),
                            # [CORREÇÃO] Substituído ft.alignment.center por ft.Alignment(0, 0)
                            alignment=ft.Alignment(0, 0)
                        ),
                        # Texto
                        ft.Container(
                            content=ft.Column([
                                ft.Text(r.get('title'), weight="bold",
                                        size=14, max_lines=2, overflow="ellipsis"),
                                ft.Row([
                                    ft.Row([
                                        ft.Icon(ft.Icons.TIMER_OUTLINED,
                                                size=14, color="grey"),
                                        ft.Text(
                                            f"{r.get('preparation_time', '?')} min", size=12, color="grey")
                                    ], spacing=2),
                                    ft.IconButton(
                                        icon=ft.Icons.STAR if r.get(
                                            'is_favorite') else ft.Icons.STAR_BORDER,
                                        icon_color="amber" if r.get(
                                            'is_favorite') else "grey",
                                        icon_size=22,
                                        tooltip="Favoritar",
                                        on_click=lambda e, x=rid: [
                                            vm.toggle_favorite(x), update_results_ui()]
                                    )
                                ], alignment="spaceBetween", vertical_alignment="center")
                            ], spacing=5),
                            padding=10,
                            expand=2,
                            bgcolor="white",
                            border_radius=ft.border_radius.only(
                                bottom_left=12, bottom_right=12)
                        )
                    ], spacing=0),
                    border_radius=12,
                    shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.with_opacity(
                        0.1, "black"), offset=ft.Offset(0, 4)),
                    on_click=lambda e, x=rid: vm.navigate_to_details(x),
                    ink=True
                )
                results_grid.controls.append(card)

        page.update()

    # Botão de Filtro
    btn_reset = ft.IconButton(
        ft.Icons.FILTER_ALT_OFF,
        tooltip="Limpar Filtros",
        on_click=clear_filters,
        icon_color=ft.Colors.GREY_600
    )

    # Render Inicial
    update_results_ui()

    return ft.View(
        route="/discovery",
        bgcolor=ft.Colors.GREY_50,
        appbar=ft.AppBar(
            title=ft.Text("Discovery", weight="bold"),
            center_title=True,
            bgcolor="white",
            elevation=0,
            leading=ft.IconButton(ft.Icons.ARROW_BACK,
                                  on_click=lambda _: page.go("/"))
        ),
        controls=[
            ft.SafeArea(
                expand=True,
                content=ft.Column(
                    expand=True,
                    spacing=0,
                    controls=[
                        # Painel de Filtros
                        ft.Container(
                            padding=ft.padding.symmetric(
                                horizontal=15, vertical=10),
                            bgcolor="white",
                            border_radius=ft.border_radius.only(
                                bottom_left=25, bottom_right=25),
                            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(
                                0.08, "black"), offset=ft.Offset(0, 5)),
                            content=ft.Column([
                                ft.Row([tf_search, dd_category], spacing=10),
                                ft.Row([
                                    ft.Container(
                                        content=ft.Column(
                                            [time_label, slider_time], spacing=0),
                                        padding=ft.padding.only(top=5)
                                    ),
                                    tf_servings,
                                    ft.Container(width=10),
                                    btn_reset
                                ], alignment="spaceBetween", vertical_alignment="center"),
                                ft.Row([results_count_text],
                                       alignment=ft.MainAxisAlignment.END)
                            ], spacing=10)
                        ),
                        # Grid
                        ft.Column([results_grid], expand=True)
                    ]
                )
            )
        ]
    )
