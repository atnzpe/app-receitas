# CÓDIGO COMPLETO E COMENTADO
import flet as ft
from typing import Callable

"""
Componente de UI reutilizável (View) para os cards do Dashboard.
(CORRIGIDO) Herda de ft.Container para compatibilidade com a nova API do Flet,
resolvendo o AttributeError: 'flet' has no attribute 'UserControl'.
"""

class DashboardCard(ft.Container): # Herda de ft.Container
    
    def __init__(
        self,
        icon_name: str,
        title: str,
        subtitle: str,
        color_scheme: dict,
        on_card_click: Callable
    ):
        # A lógica do método build() foi movida para o __init__().
        
        # 1. Cria o Círculo do Ícone
        icon_container = ft.Container(
            content=ft.Icon(
                name=icon_name, 
                size=32
            ),
            width=64,
            height=64,
            border_radius=32,
            alignment=ft.alignment.center,
            color=color_scheme['fg_light'],
            bgcolor=color_scheme['bg_light'],
            color_dark=color_scheme['fg_dark'],
            bgcolor_dark=color_scheme['bg_dark'],
        )
        
        # 2. Cria os Textos
        title_text = ft.Text(title, size=AppFonts.BODY_LARGE, weight=ft.FontWeight.SEMI_BOLD)
        subtitle_text = ft.Text(
            subtitle, 
            size=AppFonts.BODY_SMALL, 
            theme_style=ft.TextThemeStyle.BODY_MEDIUM 
        )

        # 3. Chama o construtor da classe pai (ft.Container)
        # Passando todas as propriedades do card principal.
        super().__init__(
            content=ft.Column(
                controls=[
                    icon_container,
                    ft.Container(height=10),
                    title_text,
                    subtitle_text,
                ],
                spacing=5,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            ),
            padding=AppDimensions.PAGE_PADDING,
            border_radius=AppDimensions.BORDER_RADIUS,
            on_hover=self.on_hover,
            on_click=on_card_click, # Binda o clique
            data=title, # Armazena o título para o modal
            bgcolor=ft.colors.WHITE,
            border=ft.border.all(1, ft.colors.GREY_200),
            bgcolor_dark=ft.colors.with_opacity(0.5, ft.colors.GREY_800),
            border_dark=ft.border.all(1, ft.colors.with_opacity(0.5, ft.colors.GREY_700)),
        )

    def on_hover(self, e: ft.HoverEvent):
        """Efeito de hover para dar feedback visual."""
        # 'self' é o próprio ft.Container
        self.scale = ft.transform.Scale(1.03) if e.data == "true" else ft.transform.Scale(1.0)
        self.shadow = (
            ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.colors.with_opacity(0.1, ft.colors.BLACK),
                offset=ft.Offset(0, 5),
            )
            if e.data == "true"
            else None
        )
        self.update()