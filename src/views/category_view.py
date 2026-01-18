# ARQUIVO: src/views/category_view.py
# CÓDIGO COMPLETO E BLINDADO

import flet as ft
from src.viewmodels.category_viewmodel import CategoryViewModel
from src.utils.theme import AppDimensions


def CategoryView(page: ft.Page) -> ft.View:
    """
    Tela de CRUD de Categorias.
    Apresenta uma lista rolável e um botão flutuante para adicionar novos itens.
    """

    # Instancia o Cérebro da Tela
    vm = CategoryViewModel(page)

    # --- Elementos do Modal (Formulário) ---
    name_field = ft.TextField(
        label="Nome da Categoria",
        hint_text="Ex: Massas Artesanais",
        on_submit=vm.save_category,  # UX: Salvar ao dar Enter
        text_capitalization=ft.TextCapitalization.SENTENCES,
        prefix_icon=ft.Icons.LABEL
    )

    dialog = ft.AlertDialog(
        content=ft.Container(content=name_field, width=300),
        actions=[
            ft.TextButton("Cancelar", on_click=vm.close_dialog),
            ft.ElevatedButton(
                "Salvar", on_click=vm.save_category, icon=ft.Icons.SAVE),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        shape=ft.RoundedRectangleBorder(radius=10)
    )

    # Injeção de Dependência (Conecta View -> ViewModel)
    vm.name_field = name_field
    vm.dialog = dialog
    page.dialog = dialog  # Necessário para o overlay funcionar

    # --- Lista de Dados ---
    list_view = ft.ListView(
        expand=True,
        spacing=5,
        padding=10,
        auto_scroll=False
    )
    vm.list_view = list_view

    # --- Botão Flutuante (FAB) ---
    fab = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        text="Nova Categoria",
        on_click=lambda _: vm.open_dialog(None),
        bgcolor=page.theme.color_scheme.primary,  # Cor do tema
    )

    # --- Cabeçalho (Navigation) ---
    app_bar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            tooltip="Voltar ao Dashboard",
            on_click=lambda _: page.go("/")  # Navegação segura via Rota
        ),
        title=ft.Text("Gerenciar Categorias"),
        center_title=False,
        bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.BLACK)
    )

    # Carrega os dados (Seed + User Data)
    vm.initialize()

    return ft.View(
        route="/categories",
        appbar=app_bar,
        floating_action_button=fab,
        controls=[
            ft.SafeArea(
                content=ft.Column(
                    controls=[
                        # Aqui poderíamos adicionar uma barra de busca no futuro
                        ft.Container(list_view, expand=True)
                    ],
                    expand=True
                ),
                expand=True
            )
        ],
        bgcolor=page.theme.color_scheme.background
    )
