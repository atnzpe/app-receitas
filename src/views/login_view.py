# CÓDIGO COMPLETO E COMENTADO
"""
A View de Login.
Responsável apenas pela UI (controles Flet).
"""
import flet as ft
from src.viewmodels.login_viewmodel import LoginViewModel

def LoginView(page: ft.Page) -> ft.View:
    """
    Retorna a ft.View para a rota de Login.
    Usamos uma função em vez de uma classe para Views de Rota.
    """
    
    # 1. Instanciar o ViewModel
    vm = LoginViewModel(page)
    
    # 2. Criar os Controles
    title = ft.Text("App de Receitas", size=32, weight=ft.FontWeight.BOLD)
    subtitle = ft.Text("Faça login para continuar", size=18, color=ft.Colors.GREY_700)
    
    email_field = ft.TextField(
        label="Email",
        keyboard_type=ft.KeyboardType.EMAIL,
        prefix_icon=ft.Icons.EMAIL_OUTLINED
    )
    
    password_field = ft.TextField(
        label="Senha",
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.Icons.LOCK_OUTLINED
    )
    
    login_button = ft.ElevatedButton(
        text="Entrar",
        icon=ft.Icons.LOGIN,
        on_click=vm.on_login_click, # 3. Bindar evento ao ViewModel
        width=float('inf')
    )
    
    register_button = ft.TextButton(
        text="Não tem uma conta? Registre-se aqui.",
        on_click=vm.on_navigate_to_register, # 3. Bindar evento ao ViewModel
        width=float('inf')
    )
    
    # 4. Passar referências de controle para o ViewModel
    vm.set_controls(email_field, password_field)

    # 5. Retornar a ft.View
    return ft.View(
        route="/login",
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        title,
                        subtitle,
                        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                        email_field,
                        password_field,
                        login_button,
                        register_button
                    ],
                    spacing=15,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                width=400,
                padding=20,
                border_radius=10,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                    offset=ft.Offset(0, 5),
                ),
                # Adaptação ao tema
                bgcolor=ft.Colors.WHITE,
                bgcolor_dark=ft.Colors.with_opacity(0.03, ft.Colors.WHITE10),
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        # Fundo da página de login
        bgcolor=ft.Colors.GREY_50,
        bgcolor_dark=ft.Colors.GREY_900
    )