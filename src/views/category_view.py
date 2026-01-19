# ARQUIVO: src/views/category_view.py
# CÓDIGO CORRIGIDO
import flet as ft
from src.viewmodels.category_viewmodel import CategoryViewModel
from src.utils.theme import AppDimensions


def CategoryView(page: ft.Page) -> ft.View:
    vm = CategoryViewModel(page)

    # --- Input Modal ---
    name_field = ft.TextField(
        label="Nome da Categoria",
        hint_text="Ex: Low Carb",
        capitalization=ft.TextCapitalization.SENTENCES,
        on_submit=vm.save_category,
        border_radius=AppDimensions.BORDER_RADIUS,
        prefix_icon=ft.Icons.LABEL_OUTLINE
    )

    vm.name_field = name_field

    # Dialog definido, mas NÃO anexado ao page.dialog aqui.
    # O ViewModel cuidará de colocá-lo no overlay.
    dialog = ft.AlertDialog(
        title=ft.Text("Nova Categoria"),
        content=ft.Container(content=name_field, height=70),
        actions=[
            ft.TextButton("Cancelar", on_click=vm.close_dialog),
            ft.ElevatedButton("Salvar", on_click=vm.save_category),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    vm.dialog = dialog
    # REMOVIDO: page.dialog = dialog

    # --- Lista ---
    list_view = ft.ListView(
        expand=True,
        spacing=5,
        padding=10
    )
    vm.list_view = list_view

    # --- AppBar ---
    app_bar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            on_click=lambda _: page.go("/"),
            tooltip="Voltar ao Dashboard"
        ),
        title=ft.Text("Gerenciar Categorias", weight=ft.FontWeight.BOLD),
        center_title=False,
        bgcolor=page.theme.color_scheme.surface,
        elevation=0
    )

    # --- FAB ---
    fab = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        content=ft.Text("Nova", weight=ft.FontWeight.BOLD),
        on_click=vm.open_dialog,
        bgcolor=page.theme.color_scheme.primary,
    )

    # Init
    vm.initialize()

    return ft.View(
        route="/categories",
        appbar=app_bar,
        floating_action_button=fab,
        controls=[
            ft.SafeArea(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=list_view,
                            expand=True,
                            width=800,
                            alignment=ft.Alignment(0, -1),
                        )
                    ],
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                expand=True
            )
        ],
        bgcolor=page.theme.color_scheme.surface,
        padding=0
    )
