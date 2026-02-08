# ARQUIVO: src/views/register_view.py
import flet as ft
from src.viewmodels.register_viewmodel import RegisterViewModel
from src.views.components.app_footer import AppFooter
from src.utils.theme import AppDimensions, AppFonts


def RegisterView(page: ft.Page) -> ft.View:
    vm = RegisterViewModel(page)

    name_field = ft.TextField(
        label="Nome", prefix_icon=ft.Icons.PERSON, border_radius=10)
    email_field = ft.TextField(
        label="Email", keyboard_type="email", prefix_icon=ft.Icons.EMAIL, border_radius=10)
    pass_field = ft.TextField(label="Senha", password=True,
                              can_reveal_password=True, prefix_icon=ft.Icons.LOCK, border_radius=10)

    btn_reg = ft.ElevatedButton("Registrar", icon=ft.Icons.PERSON_ADD, on_click=vm.on_register_click, width=float(
        'inf'), style=ft.ButtonStyle(padding=15))
    btn_log = ft.TextButton(
        "Já tenho conta", on_click=vm.on_navigate_to_login, width=float('inf'))

    vm.set_controls(name_field, email_field, pass_field)

    form = ft.Container(
        content=ft.Column([
            ft.Text("Nova Conta", size=24, weight="bold"),
            ft.Divider(height=10, color="transparent"),
            name_field, email_field, pass_field,
            btn_reg, btn_log
        ], spacing=15, horizontal_alignment="center"),
        width=400, padding=30, border_radius=15, bgcolor=ft.Colors.SURFACE,
        shadow=ft.BoxShadow(
            blur_radius=15, color=ft.Colors.with_opacity(0.1, "black"))
    )

    return ft.View(
        route="/register",
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
