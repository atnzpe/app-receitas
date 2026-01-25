# ARQUIVO: src/viewmodels/recipe_viewmodel.py
# OBJETIVO: Gerenciar estado de Criação e Edição de receitas.
from typing import List, Optional
from pydantic import ValidationError
from src.core.logger import get_logger
from src.database.recipe_queries import RecipeQueries
from src.models.recipe import RecipeCreate, IngredientSchema
from src.database.database import DB_PATH

logger = get_logger("src.viewmodels.recipe")


class RecipeViewModel:
    def __init__(self):
        self.db = RecipeQueries(DB_PATH)
        self.temp_ingredients: List[IngredientSchema] = []

        # Estado de Edição: Se preenchido, estamos editando. Se None, criando.
        self.editing_recipe_id: Optional[int] = None

    def add_temp_ingredient(self, name: str, qty: str, unit: str) -> str:
        """Adiciona ingrediente à lista temporária."""
        try:
            name = name.strip() if name else ""
            qty = qty.strip() if qty else None
            unit = unit.strip() if unit else None

            ing = IngredientSchema(name=name, quantity=qty, unit=unit)
            self.temp_ingredients.append(ing)
            return None
        except ValidationError as e:
            return str(e.errors()[0]['msg'])
        except Exception as e:
            return "Erro ao adicionar ingrediente."

    def remove_temp_ingredient(self, index: int):
        if 0 <= index < len(self.temp_ingredients):
            self.temp_ingredients.pop(index)

    def load_recipe_for_edit(self, recipe_id: int) -> dict:
        """Carrega dados do banco para o modo de edição."""
        logger.info(f"Carregando receita {recipe_id} para edição.")
        data = self.db.get_recipe_details(recipe_id)

        if data:
            self.editing_recipe_id = data['id']
            # Converte dicionários do banco para objetos Pydantic na memória
            self.temp_ingredients = []
            if data.get('ingredients'):
                for item in data['ingredients']:
                    try:
                        ing = IngredientSchema(
                            name=item['name'],
                            quantity=item['quantity'],
                            unit=item['unit']
                        )
                        self.temp_ingredients.append(ing)
                    except:
                        pass
            return data
        return None

    def save_recipe(self, user_id: int, title: str, instructions: str,
                    category_id: str, prep_time: str, servings: str,
                    add_instr: str, source: str) -> bool:

        mode = 'ATUALIZAÇÃO' if self.editing_recipe_id else 'CRIAÇÃO'
        logger.info(f"Iniciando {mode} de receita...")

        try:
            p_time = int(
                prep_time) if prep_time and prep_time.isdigit() else None
            cat_id = int(
                category_id) if category_id and category_id.isdigit() else None

            recipe_data = RecipeCreate(
                title=title,
                category_id=cat_id,
                preparation_time=p_time,
                servings=servings or None,
                instructions=instructions,
                additional_instructions=add_instr or None,
                source=source or None,
                ingredients=self.temp_ingredients
            )

            # Decisão: Insert ou Update?
            if self.editing_recipe_id:
                success = self.db.update_recipe(
                    self.editing_recipe_id, recipe_data, user_id)
            else:
                success = self.db.create_recipe(recipe_data, user_id)

            if success:
                self.temp_ingredients = []
                self.editing_recipe_id = None  # Reseta estado

            return success

        except ValidationError as ve:
            msg = ve.errors()[0]['msg']
            logger.warning(f"Validação falhou: {msg}")
            raise Exception(f"Dados inválidos: {msg}")
        except Exception as e:
            logger.error(f"Erro ao salvar: {e}", exc_info=True)
            raise e
