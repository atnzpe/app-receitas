# CÓDIGO COMPLETO E COMENTADO
import flet as ft
from typing import Callable

"""
Componente de UI reutilizável (View) para os cards do Dashboard.
Baseado nas imagens fornecidas (light/dark).
"""

class DashboardCard(ft.UserControl):
    
    def __init__(
        self,
        icon_name: str,
        title: str,
        subtitle: str,
        color_scheme: dict,
        on_card_click: Callable
    ):
        """
        Inicializa o card.
        
        :param icon_name: O nome do ícone (ex: ft.icons.BOOK_OUTLINED)
        :param title: O título principal do card.
        :param subtitle: O texto descritivo.
        :param color_scheme: Um dict com {'bg_light', 'fg_light', 'bg_dark', 'fg_dark'}
        :param on_card_click: A função a ser chamada quando o card for clicado.
        """
        super().__init__()
        self.icon_name = icon_name
        self.title = title
        self.subtitle = subtitle
        self.color_scheme = color_scheme
        self.on_card_click = on_card_click
        
    def build(self):
        """Constrói a UI do card."""
        
        # Container do Ícone (Círculo colorido)
        icon_container = ft.Container(
            content=ft.Icon(
                name=self.icon_name, 
                size=32
            ),
            width=64,
            height=64,
            border_radius=32,
            alignment=ft.alignment.center,
            
            # Definição de cores adaptativas (light/dark)
            color=self.color_scheme['fg_light'],
            bgcolor=self.color_scheme['bg_light'],
            color_dark=self.color_scheme['fg_dark'],
            bgcolor_dark=self.color_scheme['bg_dark'],
        )
        
        # Textos
        title_text = ft.Text(self.title, size=20, weight=ft.FontWeight.SEMI_BOLD)
        subtitle_text = ft.Text(
            self.subtitle, 
            size=14, 
            theme_style=ft.TextThemeStyle.BODY_MEDIUM # Cor adaptativa
        )

        # O Card em si
        return ft.Container(
            content=ft.Column(
                controls=[
                    icon_container,
                    ft.Container(height=10), # Espaçador
                    title_text,
                    subtitle_text,
                ],
                spacing=5,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            ),
            padding=20,
            border_radius=12,
            on_hover=self.on_hover,
            on_click=self.on_card_click,
            data=self.title, # Armazena o título para o callback (usado no AlertDialog)
            
            # Styling do card (claro)
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_200),
            
            # Styling (escuro) - simula o dark:bg-gray-800/50
            bgcolor_dark=ft.Colors.with_opacity(0.5, ft.Colors.GREY_800),
            border_dark=ft.border.all(1, ft.Colors.with_opacity(0.5, ft.Colors.GREY_700)),
        )

    def on_hover(self, e: ft.HoverEvent):
        """Efeito de hover para dar feedback visual."""
        e.control.scale = ft.transform.Scale(1.03) if e.data == "true" else ft.transform.Scale(1.0)
        e.control.shadow = (
            ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 5),
            )
            if e.data == "true"
            else None
        )
        e.control.update()