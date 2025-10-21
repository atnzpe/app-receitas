# CÓDIGO COMPLETO E COMENTADO
import flet as ft

def AppFooter() -> ft.Container:
    """
    Retorna um componente de rodapé reutilizável para todas as telas,
    conforme requisito da Sprint 2 ("Criado por...").
    Garante consistência e atende à diretriz Mobile-First (SafeArea o protege).
    """
    
    # URL do LinkedIn do Arquiteto
    LINKEDIN_URL = "https://www.linkedin.com/in/atnzpe/" 
    
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.CODE_ROUNDED, size=16),
                ft.Text("Criado por "),
                ft.TextButton(
                    text="atnzpe", # Seu símbolo/nome
                    url=LINKEDIN_URL,
                    # Lança a URL no navegador
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