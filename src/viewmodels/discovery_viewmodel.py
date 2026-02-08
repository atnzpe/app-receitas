# ARQUIVO: src/viewmodels/discovery_viewmodel.py
import flet as ft
from src.database.recipe_queries import RecipeQueries
from src.database.category_queries import CategoryQueries
from src.models.user_model import User
from src.core.logger import get_logger

logger = get_logger("src.viewmodels.discovery")


class DiscoveryViewModel:
    def __init__(self, page: ft.Page):
        self.page = page
        self.db = RecipeQueries()
        self.cat_db = CategoryQueries()

        self.user: User = self.page.data.get("logged_in_user")
        self.recipes = []
        self.categories_options = []

        # Estado dos Filtros
        self.active_category_id = 0

        # Inicialização
        self.load_categories()
        self.load_initial_context()

    def load_categories(self):
        """Carrega lista de categorias para o Dropdown."""
        try:
            cats = self.cat_db.get_user_categories(self.user.id)
            # Opção '0' representa 'Todas'
            self.categories_options = [
                ft.dropdown.Option("0", "Todas as Categorias")]
            self.categories_options.extend(
                [ft.dropdown.Option(str(c['id']), c['name']) for c in cats]
            )
        except Exception as e:
            logger.error(f"Erro ao carregar categorias: {e}")
            self.categories_options = [ft.dropdown.Option("0", "Padrão")]

    def load_initial_context(self):
        """Verifica filtro vindo da navegação (Tela de Categorias)."""
        cat_id = self.page.data.get("filter_category_id")

        if cat_id:
            logger.info(f"Contexto Detectado: Categoria ID {cat_id}")
            self.active_category_id = int(cat_id)

            # Limpa sessão
            self.page.data["filter_category_id"] = None
            self.page.data["filter_category_name"] = None

        self.search()

    def search(self, term: str = "", max_time: str = "", servings: str = "", category_val: str = None):
        """Busca blindada."""
        try:
            # Conversão segura de tipos
            # Aceita float do slider
            time_limit = int(float(max_time)) if max_time else 0
            term = term.strip() if term else ""
            servings = servings.strip() if servings else ""

            if category_val:
                self.active_category_id = int(category_val)

            logger.info(
                f"Busca: '{term}', Time<={time_limit}, CatID={self.active_category_id}")

            self.recipes = self.db.search_advanced(
                uid=self.user.id,
                term=term,
                max_time=time_limit,
                servings=servings,
                category_id=self.active_category_id
            )
            logger.info(f"Resultados: {len(self.recipes)}")

        except Exception as e:
            logger.error(f"Erro na busca: {e}", exc_info=True)
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
