import flet as ft
from src.viewmodels.login_viewmodel import LoginViewModel
from src.views.components.app_footer import AppFooter
from src.utils.theme import AppDimensions, AppFonts


def LoginView(page: ft.Page) -> ft.View:
    vm = LoginViewModel(page)

    email_field = ft.TextField(label="Email", keyboard_type=ft.KeyboardType.EMAIL,
                               prefix_icon=ft.Icons.EMAIL_OUTLINED, border_radius=AppDimensions.BORDER_RADIUS)
    password_field = ft.TextField(label="Senha", password=True, can_reveal_password=True,
                                  prefix_icon=ft.Icons.LOCK_OUTLINED, border_radius=AppDimensions.BORDER_RADIUS)

    login_button = ft.ElevatedButton(
        content=ft.Text("Entrar", weight=ft.FontWeight.BOLD),
        icon=ft.Icons.LOGIN,
        on_click=vm.on_login_click,
        width=float('inf'),
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(
            radius=AppDimensions.BORDER_RADIUS), padding=15)
    )
    register_button = ft.TextButton(content=ft.Text(
        "Não tem uma conta? Registre-se aqui."), on_click=vm.on_navigate_to_register, width=float('inf'))

    vm.set_controls(email_field, password_field)

    login_form_card = ft.Container(
        content=ft.Column([
            ft.Text("App de Receitas", size=AppFonts.TITLE_LARGE,
                    weight=ft.FontWeight.BOLD),
            ft.Text("Faça login para continuar",
                    size=AppFonts.BODY_MEDIUM, color=ft.Colors.GREY_700),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            email_field, password_field, login_button, register_button
        ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        width=AppDimensions.FIELD_MAX_WIDTH, padding=AppDimensions.PAGE_PADDING, border_radius=AppDimensions.BORDER_RADIUS,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color=ft.Colors.with_opacity(
            0.1, ft.Colors.BLACK), offset=ft.Offset(0, 5)),
        bgcolor=ft.Colors.SURFACE,
    )

    return ft.View(
        route="/login",
        controls=[ft.SafeArea(content=ft.Column([
            ft.Container(content=ft.Row([login_form_card], alignment=ft.MainAxisAlignment.CENTER), alignment=ft.Alignment(
                0, 0), expand=True, padding=ft.padding.symmetric(horizontal=AppDimensions.PAGE_PADDING)),
            AppFooter()
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, expand=True), expand=True)],
        padding=0,
        bgcolor=page.theme.color_scheme.surface,  # CORRIGIDO
    )
