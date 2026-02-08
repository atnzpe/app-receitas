# ARQUIVO: src/views/login_view.py
import flet as ft
from src.viewmodels.login_viewmodel import LoginViewModel
from src.views.components.app_footer import AppFooter
from src.utils.theme import AppDimensions, AppFonts


def LoginView(page: ft.Page) -> ft.View:
    vm = LoginViewModel(page)

    email_field = ft.TextField(label="Email", keyboard_type="email",
                               prefix_icon=ft.Icons.EMAIL, border_radius=10, on_submit=vm.on_login_click)
    pass_field = ft.TextField(label="Senha", password=True, can_reveal_password=True,
                              prefix_icon=ft.Icons.LOCK, border_radius=10, on_submit=vm.on_login_click)

    btn_log = ft.ElevatedButton("Entrar", icon=ft.Icons.LOGIN, on_click=vm.on_login_click, width=float(
        'inf'), style=ft.ButtonStyle(padding=15))
    btn_reg = ft.TextButton(
        "Criar conta", on_click=vm.on_navigate_to_register, width=float('inf'))

    vm.set_controls(email_field, pass_field)

    form = ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.LOCK_PERSON, size=64,
                    color=page.theme.color_scheme.primary),
            ft.Text("Acesso Restrito", size=24, weight="bold"),
            ft.Divider(height=10, color="transparent"),
            email_field, pass_field,
            btn_log, btn_reg
        ], spacing=15, horizontal_alignment="center"),
        width=400, padding=30, border_radius=15, bgcolor=ft.Colors.SURFACE,
        shadow=ft.BoxShadow(
            blur_radius=15, color=ft.Colors.with_opacity(0.1, "black"))
    )

    return ft.View(
        route="/login",
        controls=[
            ft.SafeArea(
                content=ft.Column([
                    ft.Container(
                        content=form, alignment=ft.Alignment(0, 0), expand=True,
                        # [CORREÇÃO] Padding atualizado
                        padding=ft.padding.symmetric(horizontal=20)
                    ),
                    AppFooter()
                ], expand=True)
            )
        ],
        padding=0, bgcolor=page.theme.color_scheme.surface
    )
