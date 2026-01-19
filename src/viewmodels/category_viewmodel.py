# ARQUIVO: src/viewmodels/category_viewmodel.py
# CÓDIGO ATUALIZADO (ESTRATÉGIA OVERLAY)
import flet as ft
from typing import List, Optional
from src.core.logger import get_logger
from src.database import category_queries
from src.models.recipe_model import Category
from src.models.user_model import User

logger = get_logger("src.viewmodels.category")


class CategoryViewModel:
    def __init__(self, page: ft.Page):
        self.page = page
        self.categories: List[Category] = []
        self.user: User = self.page.data.get("logged_in_user")

        self.list_view: Optional[ft.ListView] = None
        self.dialog: Optional[ft.AlertDialog] = None
        self.name_field: Optional[ft.TextField] = None

    def initialize(self):
        self.load_data(update_ui=False)

    def load_data(self, update_ui=True):
        if not self.user:
            return
        try:
            self.categories = category_queries.get_all_categories_for_user(
                self.user.id)
            self._populate_list_controls()
            if update_ui and self.list_view:
                self.list_view.update()
        except Exception as e:
            logger.error(f"Erro load: {e}", exc_info=True)
            if update_ui:
                self._show_snack("Erro ao carregar lista.", True)

    def _populate_list_controls(self):
        if not self.list_view:
            return
        self.list_view.controls.clear()

        if not self.categories:
            self.list_view.controls.append(
                ft.Container(
                    content=ft.Text("Nenhuma categoria encontrada.",
                                    color=ft.Colors.GREY_500),
                    alignment=ft.Alignment(0, 0),
                    padding=20
                )
            )
            return

        for cat in self.categories:
            self.list_view.controls.append(self._create_list_item(cat))

    def _create_list_item(self, cat: Category):
        is_mine = cat.user_id == self.user.id
        is_native = cat.is_native

        if is_native:
            icon, icon_color, subtitle = ft.Icons.VERIFIED, ft.Colors.BLUE, "Sistema"
        elif is_mine:
            icon, icon_color, subtitle = ft.Icons.LABEL, ft.Colors.ORANGE, "Minha Categoria"
        else:
            icon, icon_color, subtitle = ft.Icons.PUBLIC, ft.Colors.GREY, "Comunidade"

        fav_icon = ft.Icons.STAR if cat.is_favorite else ft.Icons.STAR_BORDER
        fav_color = ft.Colors.AMBER if cat.is_favorite else ft.Colors.GREY_400

        return ft.ListTile(
            leading=ft.Icon(icon, color=icon_color),
            title=ft.Text(cat.name, weight=ft.FontWeight.W_500),
            subtitle=ft.Text(subtitle, size=12),
            trailing=ft.Row(
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    ft.IconButton(
                        icon=fav_icon,
                        icon_color=fav_color,
                        tooltip="Favoritar",
                        on_click=lambda e, c=cat: self.toggle_favorite(c)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color=ft.Colors.RED_400,
                        tooltip="Excluir",
                        visible=is_mine,
                        on_click=lambda e, id=cat.id: self.delete_category(id)
                    ) if is_mine else ft.Container()
                ],
                width=120
            )
        )

    def toggle_favorite(self, cat: Category):
        try:
            new_status = category_queries.toggle_favorite(cat.id, self.user.id)
            self._show_snack(
                "Favoritado!" if new_status else "Removido dos favoritos.")
            self.load_data(update_ui=True)
        except Exception as e:
            logger.error(f"Erro fav: {e}")

    # --- CONTROLE DE DIÁLOGO (ESTRATÉGIA OVERLAY) ---
    def open_dialog(self, e):
        """Força a abertura do diálogo via Overlay."""
        logger.debug("Abrindo modal de nova categoria.")

        if self.name_field:
            self.name_field.value = ""
            self.name_field.error_text = None

        if self.dialog:
            self.dialog.open = True
            # Adiciona explicitamente ao overlay para garantir visibilidade
            if self.dialog not in self.page.overlay:
                self.page.overlay.append(self.dialog)
            self.page.update()

    def close_dialog(self, e=None):
        """Fecha e limpa o modal."""
        logger.debug("Fechando modal.")
        if self.dialog:
            self.dialog.open = False
            self.page.update()
            # Opcional: Remover do overlay para limpar, mas manter também funciona

    def save_category(self, e):
        logger.info("Botão 'Salvar' clicado.")

        if not self.user:
            self._show_snack("Sessão inválida.", True)
            return

        try:
            raw_val = self.name_field.value if self.name_field else ""
            name = (raw_val or "").strip()

            if len(name) < 3:
                if self.name_field:
                    self.name_field.error_text = "Mínimo 3 caracteres."
                    self.name_field.update()
                return

            if category_queries.add_category(name, self.user.id):
                self._show_snack("Categoria criada!")
                self.close_dialog()
                self.load_data(update_ui=True)
            else:
                if self.name_field:
                    self.name_field.error_text = "Categoria já existe."
                    self.name_field.update()

        except Exception as ex:
            logger.critical(f"ERRO save_category: {ex}", exc_info=True)
            self._show_snack(f"Erro: {ex}", True)

    def delete_category(self, cat_id: int):
        try:
            if category_queries.delete_category(cat_id, self.user.id):
                self._show_snack("Categoria excluída.")
                self.load_data(update_ui=True)
            else:
                self._show_snack("Erro ao excluir.", True)
        except Exception:
            self._show_snack("Erro crítico.", True)

    def _show_snack(self, text, is_error=False):
        color = ft.Colors.RED if is_error else ft.Colors.GREEN
        self.page.snack_bar = ft.SnackBar(content=ft.Text(text), bgcolor=color)
        self.page.snack_bar.open = True
        self.page.update()
