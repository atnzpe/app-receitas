# CÓDIGO COMPLETO E COMENTADO
"""
ViewModel para o DashboardView.
Gerencia o estado da UI e os eventos de clique.
"""
import flet as ft
from src.models.user_model import User
from typing import Optional

class DashboardViewModel:
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.user: User = self.page.session.get("logged_in_user")
        
        # Referência ao ícone de tema para atualização
        self.theme_icon_button: Optional[ft.IconButton] = None

    def on_logout(self, e):
        """Limpa a sessão e retorna ao login."""
        self.page.session.clear()
        self.page.go("/login")

    def toggle_theme(self, e):
        """
        Troca o tema da página (light/dark), conforme requisito
        e vídeo de referência.
        """
        self.page.theme_mode = (
            ft.ThemeMode.LIGHT 
            if self.page.theme_mode == ft.ThemeMode.DARK 
            else ft.ThemeMode.DARK
        )
        
        # Atualiza o ícone do botão
        if self.theme_icon_button:
            self.theme_icon_button.icon = self.get_theme_icon()
        
        self.page.update()

    def get_theme_icon(self) -> str:
        """
        Retorna o ícone correto com base no tema atual.
       
        """
        if self.page.theme_mode == ft.ThemeMode.SYSTEM:
             # Se for system, decide pelo tema atual da página
             # (Assumindo que o padrão do sistema possa ser escuro)
             return (
                 ft.icons.LIGHT_MODE_OUTLINED 
                 if self.page.dark_theme 
                 else ft.icons.DARK_MODE_OUTLINED
             )
        
        return (
            ft.icons.LIGHT_MODE_OUTLINED # Ícone de Sol (está no modo escuro)
            if self.page.theme_mode == ft.ThemeMode.DARK 
            else ft.icons.DARK_MODE_OUTLINED # Ícone de Lua (está no modo claro)
        )

    def close_dialog(self, dialog: ft.AlertDialog, e):
        """Fecha o AlertDialog (overlay)."""
        dialog.open = False
        self.page.update()

    def show_feature_in_development_dialog(self, e):
        """
        Exibe um AlertDialog (overlay) para funcionalidades
        ainda não implementadas.
        """
        # (e.control.data vem do DashboardCard)
        card_title = e.control.data if hasattr(e, 'control') else "Funcionalidade"
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"🚀 Em Breve: {card_title}"),
            content=ft.Text(
                "Esta funcionalidade está em desenvolvimento e será implementada em breve, "
                "seguindo nossa arquitetura MVVM."
            ),
            actions=[
                ft.TextButton("Entendido!", on_click=lambda evt: self.close_dialog(dialog, evt))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        # Abre o diálogo no overlay
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
        
    def navigate_to_cadastros(self, e):
        """Ação específica para o card 'Cadastros'."""
        # TODO: Implementar a rota /cadastros na Sprint 3
        print("Navegando para /cadastros (Ainda não implementado)")
        self.show_feature_in_development_dialog(e)