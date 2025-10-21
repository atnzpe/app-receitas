import flet as ft
# (ALTERADO) Importa constantes de theme.py
from src.utils.theme import AppDimensions

def AppFooter() -> ft.Container:
    """
    Retorna um componente de rodapé reutilizável.
    (REFATORADO) Usa constantes de AppDimensions e cores do tema.
    """
    
    LINKEDIN_URL = "https://www.linkedin.com/in/gleysonatanazio/" 
    
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(
                    ft.Icons.CODE_ROUNDED, 
                    size=AppDimensions.FOOTER_ICON_SIZE, # Usa constante
                    # (ALTERADO) Usa cor sutil do tema
                    color=ft.Colors.ON_SURFACE_VARIANT 
                ),
                ft.Text("Criado por "),
                ft.TextButton(
                    text="Gleyson Atanazio",
                    url=LINKEDIN_URL,
                    on_click=lambda e: e.page.launch_url(LINKEDIN_URL), 
                    style=ft.ButtonStyle(
                        padding=0,
                        overlay_color=ft.Colors.TRANSPARENT
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=AppDimensions.SMALL_SPACING # Usa constante
        ),
        height=AppDimensions.FOOTER_HEIGHT, # Usa constante
        alignment=ft.alignment.center,
        # (ALTERADO) Usa cor de superfície variante sutil do tema
        bgcolor=ft.Colors.SURFACE
    )