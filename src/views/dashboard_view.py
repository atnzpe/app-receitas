# CÓDIGO COMPLETO E COMENTADO
"""
A View do Dashboard (Tela Principal pós-login).
POR ENQUANTO, é apenas um placeholder para provar que o roteamento
e a autenticação (Sprint 1) funcionam.
"""
import flet as ft
from src.models.user_model import User # Usaremos para tipagem

def DashboardView(page: ft.Page) -> ft.View:
    """
    Retorna a ft.View para a rota de Dashboard ('/').
    """
    
    # Recupera o usuário da sessão (garantido pelo router)
    user: User = page.session.get("logged_in_user")
    
    welcome_text = ft.Text(
        f"Bem-vindo(a), {user.full_name.split()[0]}!", 
        size=24
    )
    
    placeholder_text = ft.Text(
        "Sprint 1 Concluída! Autenticação e Roteamento funcionam.",
        size=16
    )
    
    def on_logout(e):
        page.session.clear()
        page.go("/login")

    logout_button = ft.ElevatedButton("Logout", icon=ft.Icons.LOGOUT, on_click=on_logout)

    return ft.View(
        route="/",
        controls=[
            ft.Column(
                [
                    welcome_text,
                    placeholder_text,
                    logout_button
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )