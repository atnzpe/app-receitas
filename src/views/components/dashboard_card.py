import flet as ft
from typing import Callable
from src.utils.theme import AppDimensions, AppFonts


class DashboardCard(ft.Card):
    def __init__(
        self,
        icon_name: str,
        title: str,
        subtitle: str,
        color_scheme: dict,
        on_card_click: Callable
    ):
        # Extração segura de cores (evita passar dicionário para o controle)
        fg_color = color_scheme.get("fg_light", ft.Colors.BLACK)
        bg_color = color_scheme.get("bg_light", ft.Colors.WHITE)

        icon_container = ft.Container(
            content=ft.Icon(
                icon_name,  # POSICIONAL: Funciona independente se o parâmetro chama 'name' ou 'value'
                size=AppDimensions.ICON_SIZE_MEDIUM,
                color=fg_color,
            ),
            width=AppDimensions.ICON_CONTAINER_SIZE,
            height=AppDimensions.ICON_CONTAINER_SIZE,
            border_radius=AppDimensions.ICON_CONTAINER_BORDER_RADIUS,
            alignment=ft.Alignment(0, 0),
            bgcolor=bg_color,
        )

        super().__init__(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        icon_container,
                        ft.Container(height=AppDimensions.MEDIUM_SPACING),
                        ft.Text(title, size=AppFonts.BODY_LARGE,
                                weight=ft.FontWeight.W_600),
                        ft.Text(subtitle, size=AppFonts.BODY_SMALL,
                                color=ft.Colors.OUTLINE),
                    ],
                    spacing=AppDimensions.SMALL_SPACING,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
                padding=AppDimensions.PAGE_PADDING,
                on_hover=self.on_hover,
                on_click=on_card_click,
                data=title,
                border_radius=AppDimensions.BORDER_RADIUS,
                ink=True,
            ),
            elevation=AppDimensions.CARD_ELEVATION,
        )

    def on_hover(self, e: ft.HoverEvent):
        self.elevation = AppDimensions.CARD_ELEVATION * \
            2 if e.data == "true" else AppDimensions.CARD_ELEVATION
        self.update()
