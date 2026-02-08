# ARQUIVO: src/views/components/dashboard_card.py
import flet as ft
import logging
from src.utils.theme import AppDimensions, AppFonts

logger = logging.getLogger("src.components.card")


def DashboardCard(icon: str, title: str, description: str, color: str, on_click):
    """
    Componente de Card Responsivo harmonizado com o Design System.
    """
    def internal_click(e):
        if on_click:
            on_click(e)
        else:
            logger.warning(f"Card {title} sem ação definida.")

    return ft.Card(
        elevation=AppDimensions.CARD_ELEVATION,  # Usa constante do tema
        # surface_tint_color removido para compatibilidade máxima
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Icon(icon, size=48, color=color),
                        alignment=ft.Alignment(0, 0),
                        padding=ft.padding.only(
                            bottom=AppDimensions.SMALL_SPACING)
                    ),
                    ft.Text(
                        value=title,
                        size=AppFonts.BODY_LARGE,  # Fonte padronizada
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.ON_SURFACE
                    ),
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        value=description,
                        size=AppFonts.BODY_SMALL,  # Fonte padronizada
                        color=ft.Colors.ON_SURFACE_VARIANT,
                        text_align=ft.TextAlign.CENTER,
                        max_lines=2,
                        overflow=ft.TextOverflow.ELLIPSIS,
                        no_wrap=False
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=AppDimensions.SMALL_SPACING,
                tight=True
            ),
            padding=AppDimensions.PAGE_PADDING,
            border_radius=AppDimensions.BORDER_RADIUS,
            on_click=internal_click,
            ink=True,
            # [CORREÇÃO CRÍTICA] Uso correto da classe Animation
            animate=ft.Animation(duration=200, curve="easeOut"),
        )
    )
