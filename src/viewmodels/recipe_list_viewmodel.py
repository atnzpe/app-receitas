# ARQUIVO: src/viewmodels/recipe_list_viewmodel.py
import flet as ft
from typing import List, Dict
from src.core.logger import get_logger
from src.database.recipe_queries import RecipeQueries
from src.models.user_model import User

logger = get_logger("src.viewmodels.recipe_list")


class RecipeListViewModel:
    def __init__(self, page: ft.Page):
        self.page = page
        self.db = RecipeQueries()
        self.recipes: List[Dict] = []  # Lista crua ou Models
        self.user: User = self.page.data.get("logged_in_user")

    def load_recipes(self):
        """Carrega receitas do banco."""
        if not self.user:
            return

        try:
            self.recipes = self.db.get_user_recipes(self.user.id)
            logger.info(
                f"Carregadas {len(self.recipes)} receitas para o usuário {self.user.id}")
        except Exception as e:
            logger.error(f"Erro ao carregar receitas: {e}", exc_info=True)
            self.recipes = []

    def get_recipes_count(self) -> int:
        return len(self.recipes)

    def navigate_to_create(self, e):
        self.page.go("/create_recipe")

    def navigate_to_details(self, recipe_id):
        # Futuro: self.page.go(f"/recipe/{recipe_id}")
        logger.info(f"Navegar para detalhes: {recipe_id}")
        pass
