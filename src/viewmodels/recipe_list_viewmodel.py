# ARQUIVO: src/viewmodels/recipe_list_viewmodel.py
import flet as ft
from typing import Optional
from src.core.logger import get_logger
from src.database.recipe_queries import RecipeQueries
from src.models.user_model import User

logger = get_logger("src.viewmodels.recipe_list")

class RecipeListViewModel:
    """
    Gerencia o estado da tela de listagem (Minhas Receitas).
    """
    def __init__(self, page: ft.Page):
        self.page = page
        self.db = RecipeQueries()
        self.recipes = []
        self.user: User = self.page.data.get("logged_in_user")
        self.current_dialog: Optional[ft.AlertDialog] = None
        self.current_mode = "my"

    def _close_dialog(self, e):
        if self.current_dialog:
            self.current_dialog.open = False
            self.page.update()

    def _show_feedback_modal(self, title: str, message: str, is_error: bool = False):
        icon = ft.Icons.ERROR_OUTLINE if is_error else ft.Icons.CHECK_CIRCLE_OUTLINE
        color = ft.Colors.RED if is_error else ft.Colors.GREEN

        dlg = ft.AlertDialog(
            title=ft.Row([ft.Icon(icon, color=color, size=30), ft.Text(title)], alignment=ft.MainAxisAlignment.START),
            content=ft.Text(message, size=16),
            actions=[ft.TextButton("OK", on_click=self._close_dialog)],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.current_dialog = dlg
        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.update()

    def toggle_mode(self, mode: str):
        if mode != self.current_mode:
            logger.info(f"Alternando modo de lista para: {mode}")
            self.current_mode = mode
            self.load_recipes()

    def load_recipes(self):
        if not self.user: return
        try:
            # Na view "Minhas Receitas", usamos sempre get_user_recipes
            self.recipes = self.db.get_user_recipes(self.user.id)
            logger.info(f"Lista carregada ({self.current_mode}): {len(self.recipes)} itens.")
            self.page.update()
        except Exception as e:
            logger.error(f"Erro load: {e}")
            self._show_feedback_modal("Erro", "Falha ao carregar lista.", is_error=True)

    def delete_recipe(self, recipe_id: int):
        try:
            if self.db.delete_recipe(recipe_id, self.user.id):
                self.load_recipes()
                self._show_feedback_modal("Sucesso", "Receita excluída com sucesso!")
            else:
                self._show_feedback_modal("Erro", "Você não tem permissão para excluir esta receita.", is_error=True)
        except Exception as e:
            self._show_feedback_modal("Erro", str(e), is_error=True)

    def toggle_favorite(self, recipe_id: int):
        try:
            status = self.db.toggle_favorite(recipe_id, self.user.id)
            # Recarrega a lista para atualizar o ícone visualmente se necessário, 
            # ou apenas exibe mensagem. O ideal é atualizar o estado local.
            msg = "Adicionado aos Favoritos!" if status else "Removido dos Favoritos."
            self.load_recipes() 
            self._show_feedback_modal("Favoritos", msg, is_error=False)
        except Exception:
            self._show_feedback_modal("Erro", "Falha ao atualizar favorito.", is_error=True)

    def navigate_to_create(self, e):
        if "editing_recipe_id" in self.page.data:
            del self.page.data["editing_recipe_id"]
        self.page.go("/create_recipe")

    def navigate_to_edit(self, recipe_id: int):
        self.page.data["editing_recipe_id"] = recipe_id
        self.page.go("/create_recipe")

    def navigate_to_details(self, recipe_id: int):
        self.page.data["detail_recipe_id"] = recipe_id
        self.page.data["previous_route"] = "/my_recipes" 
        self.page.go("/recipe_detail")