# ARQUIVO: src/viewmodels/discovery_viewmodel.py
import flet as ft
from typing import List
from src.database.recipe_queries import RecipeQueries
from src.models.user_model import User
from src.core.logger import get_logger

logger = get_logger("src.viewmodels.discovery")


class DiscoveryViewModel:
    def __init__(self, page: ft.Page):
        self.page = page
        self.db = RecipeQueries()
        self.user: User = self.page.data.get("logged_in_user")
        self.recipes = []
        self.search_mode = "name"  # 'name' ou 'pantry'

    def toggle_mode(self, mode: str):
        self.search_mode = mode
        self.recipes = []  # Limpa a lista ao trocar de aba para evitar confusão visual
        self.page.update()

    def search(self, query: str):
        """
        Executa a busca.
        Regra de UX: Se a query for muito curta (<2 chars), limpa a lista.
        """
        if not query or len(query.strip()) < 2:
            self.recipes = []
            self.page.update()
            return

        try:
            if self.search_mode == "name":
                self.recipes = self.db.search_recipes_by_name(
                    query, self.user.id)
            else:
                # Modo Dispensa: Separa por vírgula e remove vazios
                ingredients_list = [i.strip()
                                    for i in query.split(",") if i.strip()]
                if ingredients_list:
                    self.recipes = self.db.search_recipes_by_ingredients(
                        ingredients_list, self.user.id)
                else:
                    self.recipes = []

            logger.info(
                f"Busca '{query}' no modo {self.search_mode}: {len(self.recipes)} resultados.")
            self.page.update()

        except Exception as e:
            logger.error(f"Erro na busca: {e}")
            self.recipes = []
            self.page.update()

    def navigate_to_details(self, recipe_id: int):
        self.page.data["detail_recipe_id"] = recipe_id
        self.page.go("/recipe_detail")

    def toggle_favorite(self, recipe_id: int):
        try:
            self.db.toggle_favorite(recipe_id, self.user.id)
            # Atualização visual imediata (Otimista)
            for r in self.recipes:
                if r['id'] == recipe_id:
                    # Inverte 0 <-> 1
                    r['is_favorite'] = 1 - int(r.get('is_favorite', 0))
            self.page.update()
        except Exception as e:
            logger.error(f"Erro ao favoritar: {e}")
