# ARQUIVO: src/viewmodels/recipe_viewmodel.py
from typing import List, Optional
from src.core.logger import get_logger
from src.database.recipe_queries import RecipeQueries
from src.models.recipe import RecipeCreate, IngredientSchema

logger = get_logger("src.viewmodels.recipe")


class RecipeViewModel:
    def __init__(self):
        self.db = RecipeQueries()
        self.temp_ingredients: List[IngredientSchema] = []
        self.editing_recipe_id: Optional[int] = None

    def add_temp_ingredient(self, name: str, qty: str, unit: str) -> Optional[str]:
        try:
            # Validação simples
            if not name or len(name) < 2:
                return "Nome inválido"
            ing = IngredientSchema(name=name, quantity=qty, unit=unit)
            self.temp_ingredients.append(ing)
            return None
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
                    name=i['name'], quantity=i['quantity'], unit=i['unit'])
                for i in data.get('ingredients', [])
            ]
            return data
        return None

    def save_recipe(self, user_id: int, title: str, category_id: str, instructions: str,
                    prep_time: str, servings: str,
                    add_instr: str, source: str, image_path: str) -> bool:
        try:
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
                    self.editing_recipe_id, recipe_data, user_id)
            else:
                success = self.db.create_recipe(recipe_data, user_id)

            if success:
                # Limpa o estado após sucesso
                self.temp_ingredients = []
                self.editing_recipe_id = None

            return success
        except Exception as e:
            logger.error(f"Erro ao salvar receita no ViewModel: {e}")
            return False
