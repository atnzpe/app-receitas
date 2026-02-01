# ARQUIVO: src/viewmodels/discovery_viewmodel.py
import flet as ft
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
        self.load_initial_data()

    def load_initial_data(self):
        self.search()

    def search(self, term: str = "", max_time: str = "", servings: str = ""):
        """
        Executa a busca com filtros avançados.
        """
        try:
            # Tratamento de tipos
            time_limit = int(
                max_time) if max_time and max_time.isdigit() else 0
            term = term.strip() if term else ""
            servings = servings.strip() if servings else ""

            logger.info(
                f"Busca Filtros: Termo='{term}', Tempo<={time_limit}, Porções='{servings}'")

            # [CORREÇÃO] Chamada direta sem fallback para garantir o uso do filtro
            self.recipes = self.db.search_advanced(
                uid=self.user.id,
                term=term,
                max_time=time_limit,
                servings=servings
            )

            logger.info(f"Resultados encontrados: {len(self.recipes)}")

        except Exception as e:
            logger.error(f"Erro na busca: {e}")
            self.recipes = []

    def navigate_to_details(self, recipe_id: int):
        self.page.data["detail_recipe_id"] = recipe_id
        self.page.data["previous_route"] = "/discovery"
        self.page.go("/recipe_detail")

    def toggle_favorite(self, recipe_id: int):
        try:
            self.db.toggle_favorite(recipe_id, self.user.id)
            for r in self.recipes:
                if r['id'] == recipe_id:
                    r['is_favorite'] = 1 - int(r.get('is_favorite', 0))
        except Exception as e:
            logger.error(f"Erro ao favoritar: {e}")
