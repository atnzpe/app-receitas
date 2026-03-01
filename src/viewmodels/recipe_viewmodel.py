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
        self.temp_ingredients: List[IngredientSchema] = []
        self.user: User = self.page.data.get("logged_in_user")
        self.editing_recipe_id = self.page.data.get("editing_recipe_id")

    def load_editing_data(self) -> Optional[Dict]:
        if self.editing_recipe_id:
            return self.load_recipe_for_edit(self.editing_recipe_id)
        return None

    def add_temp_ingredient(self, name: str, qty: str, unit: str) -> bool:
        try:
            if not name or len(name.strip()) < 2:
                return False
            ing = IngredientSchema(name=name.strip(), quantity=qty.strip(), unit=unit.strip())
            self.temp_ingredients.append(ing)
            return True
        except Exception as e:
            logger.error(f"Erro add_temp: {e}")
            return False

    def remove_temp_ingredient(self, index: int):
        if 0 <= index < len(self.temp_ingredients):
            self.temp_ingredients.pop(index)

    def load_recipe_for_edit(self, rid: int):
        data = self.db.get_recipe_details(rid)
        if data:
            self.editing_recipe_id = data['id']
            self.temp_ingredients = [
                IngredientSchema(name=i['name'], quantity=i['quantity'] or "", unit=i['unit'] or "")
                for i in data.get('ingredients', [])
            ]
            return data
        return None

    def save_recipe(self, title: str, prep_time: str, servings: str,
                    instructions: str, add_instr: str, source: str,
                    image_path: str, category_id: str) -> Tuple[bool, str]:
        """Salva ou atualiza a receita com LOG DETALHADO."""
        try:
            if not self.user:
                return False, "Sessão expirada."

            logger.info("--- Iniciando Salvamento ---")
            logger.debug(f"Título: {title}")
            logger.debug(f"Img Path (Raw): {image_path} (Tipo: {type(image_path)})")

            p_time = int(prep_time) if prep_time and prep_time.isdigit() else None
            c_id = int(category_id) if category_id and category_id != "0" else 0

            if not title:
                return False, "O título é obrigatório."

            # Validação prévia
            if image_path and not isinstance(image_path, str):
                logger.error(f"ERRO CRÍTICO: image_path não é string! É {type(image_path)}")
                return False, "Erro interno: Formato de imagem inválido."

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
            
            logger.info("Modelo Pydantic criado com sucesso.")

            if self.editing_recipe_id:
                success = self.db.update_recipe(self.editing_recipe_id, recipe_data, self.user.id)
                msg = "Receita atualizada!"
            else:
                success = self.db.create_recipe(recipe_data, self.user.id)
                msg = "Receita criada!"

            if success:
                self.temp_ingredients = []
                self.editing_recipe_id = None
                return True, msg
            return False, "Erro no banco de dados."

        except Exception as e:
            logger.error(f"Erro FATAL ao salvar: {e}")
            # Log do que tentou ser salvo para debug
            return False, f"Erro de validação: {str(e)}"

    def import_from_url(self, url: str) -> Tuple[Optional[str], Optional[Dict]]:
        logger.info(f"Importando URL: {url}")
        error, data = RecipeScraper.fetch_recipe(url)
        
        if error:
            return error, None

        if data:
            logger.info("Dados recebidos do Scraper. Processando ingredientes...")
            self.temp_ingredients = []
            raw_ings = data.get('ingredients', [])
            for ing in raw_ings:
                self.add_temp_ingredient(
                    ing.get('name', ''), ing.get('quantity', ''), ing.get('unit', '')
                )
            
            if 'ingredients' in data:
                del data['ingredients']
                
        return None, data