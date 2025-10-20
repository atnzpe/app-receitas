# CÓDIGO COMPLETO E COMENTADO
import flet as ft

def AppFooter() -> ft.Container:
    """
    Retorna um componente de rodapé reutilizável para todas as telas,
    conforme requisito da Sprint 2.
    """
    
    # IMPORTANTE: Substitua pela sua URL do LinkedIn
    LINKEDIN_URL = "https://www.linkedin.com/in/gleysonatanazio/" 
    
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.CODE_ROUNDED, size=16),
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
            spacing=4
        ),
        height=40,
        alignment=ft.alignment.center,
        # Define uma cor de fundo sutil que se adapta ao tema
        bgcolor=ft.Colors.with_opacity(0.03, ft.Colors.ON_SURFACE)
    )