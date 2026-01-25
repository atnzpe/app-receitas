# CÓDIGO ATUALIZADO (FLET 0.80+)
import flet as ft
from src.utils.theme import AppDimensions


def AppFooter() -> ft.Container:
    LINKEDIN_URL = "https://www.linkedin.com/in/gleysonatanazio/"

    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(
                    ft.Icons.CODE_ROUNDED,
                    size=AppDimensions.FOOTER_ICON_SIZE,
                    color=ft.Colors.ON_SURFACE_VARIANT
                ),
                ft.Text("Criado por "),
                ft.TextButton(
                    content=ft.Text("Gleyson Atanazio"),  # Correção Botão
                    url=LINKEDIN_URL,
                    on_click=lambda e: e.page.launch_url(LINKEDIN_URL),
                    style=ft.ButtonStyle(
                        padding=0,
                        overlay_color=ft.Colors.TRANSPARENT
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=AppDimensions.SMALL_SPACING
        ),
        height=AppDimensions.FOOTER_HEIGHT,
        # CORREÇÃO AQUI:
        alignment=ft.Alignment(0, 0),
        bgcolor=ft.Colors.SURFACE
    )
