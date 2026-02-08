# ARQUIVO: src/viewmodels/recipe_viewmodel.py
import flet as ft
from typing import List, Optional, Dict, Tuple
from src.core.logger import get_logger
from src.database.recipe_queries import RecipeQueries
from src.models.recipe import RecipeCreate, IngredientSchema
from src.models.user_model import User
from src.services.scraper_service import RecipeScraper

logger = get_logger("src.viewmodels.recipe")


class RecipeViewModel:
    def __init__(self, page: ft.Page):
        self.page = page
        self.db = RecipeQueries()
        # [CORREÇÃO] Tipagem correta para lista de schemas
        self.temp_ingredients: List[IngredientSchema] = []
        self.user: User = self.page.data.get("logged_in_user")
        self.editing_recipe_id = self.page.data.get("editing_recipe_id")

    def load_editing_data(self) -> Optional[Dict]:
        """Carrega dados se estiver editando (compatibilidade com código antigo)."""
        if self.editing_recipe_id:
            return self.load_recipe_for_edit(self.editing_recipe_id)
        return None

    def add_temp_ingredient(self, name: str, qty: str, unit: str) -> Optional[str]:
        try:
            # Validação simples
            if not name or len(name.strip()) < 2:
                return "Nome inválido (mínimo 2 letras)"

            # [CORREÇÃO] Uso consistente de IngredientSchema
            ing = IngredientSchema(
                name=name.strip(), quantity=qty.strip(), unit=unit.strip())
            self.temp_ingredients.append(ing)
            return None  # Sucesso retorna None (sem erro)
        except Exception as e:
            return str(e)

    def remove_temp_ingredient(self, index: int):
        if 0 <= index < len(self.temp_ingredients):
            self.temp_ingredients.pop(index)

    def load_recipe_for_edit(self, rid: int):
        data = self.db.get_recipe_details(rid)
        if data:
            self.editing_recipe_id = data['id']
            # Reconstrói a lista de ingredientes usando o Schema
            self.temp_ingredients = [
                IngredientSchema(
                    name=i['name'], quantity=i['quantity'] or "", unit=i['unit'] or ""
                )
                for i in data.get('ingredients', [])
            ]
            return data
        return None

    def save_recipe(self, title: str, prep_time: str, servings: str,
                    instructions: str, add_instr: str, source: str,
                    image_path: str, category_id: str) -> Tuple[bool, str]:
        """
        Salva ou atualiza a receita. Retorna (Sucesso, Mensagem).
        """
        try:
            if not self.user:
                return False, "Sessão expirada. Faça login novamente."

            # Conversão segura de tipos
            p_time = int(
                prep_time) if prep_time and prep_time.isdigit() else None
            c_id = int(category_id) if category_id else 0

            # Criação do Modelo Pydantic (Validação ocorre aqui)
            recipe_data = RecipeCreate(
                category_id=c_id,
                title=title,
                preparation_time=p_time,
                servings=servings,
                instructions=instructions,
                additional_instructions=add_instr,
                source=source,
                image_path=image_path,
                ingredients=self.temp_ingredients
            )

            # Decisão: Criar ou Atualizar?
            if self.editing_recipe_id:
                success = self.db.update_recipe(
                    self.editing_recipe_id, recipe_data, self.user.id)
                msg = "Receita atualizada com sucesso!"
            else:
                success = self.db.create_recipe(recipe_data, self.user.id)
                msg = "Receita criada com sucesso!"

            if success:
                # Limpa o estado após sucesso
                self.temp_ingredients = []
                self.editing_recipe_id = None
                return True, msg
            else:
                return False, "Erro no banco de dados ao salvar."

        except Exception as e:
            logger.error(f"Erro ao salvar receita no ViewModel: {e}")
            return False, f"Erro de validação: {str(e)}"

    # --- NOVO MÉTODO DE IMPORTAÇÃO (WEB SCRAPING) ---
    def import_from_url(self, url: str) -> Tuple[Optional[str], Optional[Dict]]:
        """Chama o serviço de scraper."""
        error, data = RecipeScraper.fetch_recipe(url)
        if error:
            return error, None

        # Popula ingredientes temporários automaticamente
        if data and 'ingredients' in data:
            self.temp_ingredients = []  # Limpa atuais
            for ing in data['ingredients']:
                self.add_temp_ingredient(
                    ing.get('name', ''),
                    ing.get('quantity', ''),
                    ing.get('unit', '')
                )
            # Remove do dict para não duplicar no retorno, pois já está no self.temp_ingredients
            del data['ingredients']

        return None, data
