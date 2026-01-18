# CÓDIGO COMPLETO E COMENTADO
"""
ViewModel para o DashboardView.
Gerencia o estado da UI e os eventos de clique do Dashboard.
"""
import flet as ft
import logging
from src.models.user_model import User
from typing import Optional

logger = logging.getLogger(__name__)


class DashboardViewModel:

    def __init__(self, page: ft.Page):
        self.page = page
        # Recupera o usuário logado da sessão
        self.user: User = self.page.session.get("logged_in_user")
        logger.debug(
            f"DashboardViewModel inicializado para o usuário: {self.user.email}")

        # Referência ao ícone de tema para atualização
        self.theme_icon_button: Optional[ft.IconButton] = None

    def on_logout(self, e):
        """Limpa a sessão e retorna ao login."""
        logger.info(
            f"Logout solicitado pelo usuário: {self.user.email}. Redirecionando para /login.")
        self.page.session.clear()
        self.page.go("/login")

    def toggle_theme(self, e):
        """
        Troca o tema da página (light/dark).

        """
        try:
            current_mode = self.page.theme_mode
            self.page.theme_mode = (
                ft.ThemeMode.LIGHT
                if current_mode == ft.ThemeMode.DARK
                else ft.ThemeMode.DARK
            )

            if self.theme_icon_button:
                self.theme_icon_button.icon = self.get_theme_icon()

            logger.debug(f"Tema alterado para: {self.page.theme_mode}")
            self.page.update()
        except Exception as ex:
            logger.error(f"Erro ao trocar o tema: {ex}", exc_info=True)

    def get_theme_icon(self) -> str:
        """
        Retorna o ícone correto com base no tema atual.

        """
        if self.page.theme_mode == ft.ThemeMode.SYSTEM:
            current_theme = self.page.platform_brightness
            return (
                ft.Icons.LIGHT_MODE_OUTLINED
                if current_theme == ft.Brightness.DARK
                else ft.Icons.DARK_MODE_OUTLINED
            )

        return (
            ft.Icons.LIGHT_MODE_OUTLINED  # Ícone de Sol (está no modo escuro)
            if self.page.theme_mode == ft.ThemeMode.DARK
            # Ícone de Lua (está no modo claro)
            else ft.Icons.DARK_MODE_OUTLINED
        )

    def close_dialog(self, dialog: ft.AlertDialog, e):
        """Fecha o AlertDialog (overlay)."""
        logger.debug("Fechando AlertDialog.")
        dialog.open = False
        self.page.update()

    def show_feature_in_development_dialog(self, e):
        """
        Exibe um AlertDialog (overlay) para funcionalidades
        ainda não implementadas.
        """
        card_title = e.control.data if hasattr(
            e, 'control') else "Funcionalidade"
        logger.debug(f"Exibindo modal 'Em Desenvolvimento' para: {card_title}")

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"🚀 Em Breve: {card_title}"),
            content=ft.Text(
                "Esta funcionalidade está em desenvolvimento e será implementada em breve, "
                "seguindo nossa arquitetura MVVM."
            ),
            actions=[
                ft.TextButton(
                    "Entendido!", on_click=lambda evt: self.close_dialog(dialog, evt))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def navigate_to_cadastros(self, e):
        """Navega para a tela de Categorias (Sprint 3)."""
        logger.info("Navegando para Gestão de Categorias (/categories).")
        self.page.go("/categories")
