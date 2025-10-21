# CÓDIGO ALTERADO E COMENTADO
import flet as ft
from src.viewmodels.register_viewmodel import RegisterViewModel
from src.views.components.app_footer import AppFooter

def RegisterView(page: ft.Page) -> ft.View:
    """
    Retorna a ft.View para a rota de Registro.
    (REFATORADO) Adicionado SafeArea e melhorias de responsividade mobile.
    """
    
    vm = RegisterViewModel(page)
    
    name_field = ft.TextField(
        label="Nome Completo",
        prefix_icon=ft.Icons.PERSON_OUTLINE
    )
    
    email_field = ft.TextField(
        label="Email",
        keyboard_type=ft.KeyboardType.EMAIL,
        prefix_icon=ft.Icons.EMAIL_OUTLINED
    )
    
    password_field = ft.TextField(
        label="Senha (mín. 6 caracteres)",
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.Icons.LOCK_OUTLINED
    )
    
    register_button = ft.ElevatedButton(
        text="Registrar",
        icon=ft.Icons.PERSON_ADD,
        on_click=vm.on_register_click,
        width=float('inf')
    )
    
    login_button = ft.TextButton(
        text="Já tem uma conta? Faça login.",
        on_click=vm.on_navigate_to_login,
        width=float('inf')
    )
    
    vm.set_controls(name_field, email_field, password_field)
    
    register_form_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Criar Nova Conta", size=28, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                name_field,
                email_field,
                password_field,
                register_button,
                login_button
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=350,
        ),
        # (ALTERADO) Definimos max_width para responsividade mobile
        max_width=400,
        padding=20,
        border_radius=10,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            offset=ft.Offset(0, 5),
        ),
        bgcolor=ft.Colors.WHITE,
        bgcolor_dark=ft.Colors.with_opacity(0.03, ft.Colors.WHITE10),
    )

    # (NOVO) Conteúdo principal da tela
    main_content = ft.Column(
        controls=[
            ft.Container(
                content=ft.Row(
                    [register_form_card], # Row para centralizar o card
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                alignment=ft.alignment.center,
                expand=True
            ),
            AppFooter()
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        expand=True
    )

    return ft.View(
        route="/register",
        controls=[
            # (NOVO) Adicionado SafeArea conforme diretriz Mobile-First
            ft.SafeArea(
                content=main_content,
                expand=True
            )
        ],
        padding=0,
        bgcolor=ft.Colors.GREY_50,
        bgcolor_dark=ft.Colors.GREY_900
    )