import flet as ft
from typing import Callable
# (ALTERADO) Importa todas as constantes necessárias de theme.py
from src.utils.theme import AppDimensions, AppFonts

"""
Componente de UI reutilizável (View) para os cards do Dashboard.
(REFATORADO) Usa constantes de AppDimensions e AppFonts e corrige erros
de propriedades inválidas.
"""


class DashboardCard(ft.Card):

    def __init__(
        self,
        icon_name: str,
        title: str,
        subtitle: str,
        color_scheme: dict,
        on_card_click: Callable
    ):

        # 1. Cria o Círculo do Ícone (REFATORADO)
        icon_container = ft.Container(
            content=ft.Icon(
                name=icon_name,
                size=AppDimensions.ICON_SIZE_MEDIUM,  # Usa constante
                # (CORRIGIDO) Cor do ícone definida com sintaxe de dicionário
                color={"light": color_scheme['fg_light'],
                       "dark": color_scheme['fg_dark']},
            ),
            width=AppDimensions.ICON_CONTAINER_SIZE,  # Usa constante
            height=AppDimensions.ICON_CONTAINER_SIZE,  # Usa constante
            border_radius=AppDimensions.ICON_CONTAINER_BORDER_RADIUS,  # Usa constante
            alignment=ft.alignment.center,
            # (CORRIGIDO) Cor de fundo definida com sintaxe de dicionário
            bgcolor={"light": color_scheme['bg_light'],
                     "dark": color_scheme['bg_dark']},
            # (REMOVIDO) Propriedades inválidas color_dark e bgcolor_dark
        )

        # 2. Cria os Textos (REFATORADO)
        title_text = ft.Text(
            title,
            size=AppFonts.BODY_LARGE,  # Usa constante
            # (CORRIGIDO) ft.FontWeight.W_600 é o equivalente a SEMI_BOLD
            weight=ft.FontWeight.W_600
        )
        subtitle_text = ft.Text(
            subtitle,
            size=AppFonts.BODY_SMALL,  # Usa constante
            theme_style=ft.TextThemeStyle.BODY_MEDIUM
        )

        # 3. Chama o construtor da classe pai (ft.Card) (REFATORADO)
        super().__init__(
            content=ft.Container(  # Container interno para padding e eventos
                content=ft.Column(
                    controls=[
                        icon_container,
                        # Usa constante para espaçamento
                        ft.Container(height=AppDimensions.MEDIUM_SPACING),
                        title_text,
                        subtitle_text,
                    ],
                    spacing=AppDimensions.SMALL_SPACING,  # Usa constante
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
                padding=AppDimensions.PAGE_PADDING,  # Usa constante
                on_hover=self.on_hover,  # Mantém on_hover aqui
                on_click=on_card_click,  # Mantém on_click aqui
                data=title,
                border_radius=AppDimensions.BORDER_RADIUS,  # Usa constante
                ink=True,  # Adiciona efeito visual de clique (Ripple)
            ),
            elevation=AppDimensions.CARD_ELEVATION,  # Usa constante
        )

    def on_hover(self, e: ft.HoverEvent):
        """Efeito de hover para dar feedback visual."""
        # A elevação muda ao passar o mouse
        self.elevation = AppDimensions.CARD_ELEVATION * \
            2 if e.data == "true" else AppDimensions.CARD_ELEVATION
        self.update()
