# ARQUIVO: src/viewmodels/recipe_viewmodel.py
# OBJETIVO: Gerenciar o estado da criação de receita e intermediar UI e Database.
from typing import List
from pydantic import ValidationError
from src.core.logger import get_logger
from src.database.recipe_queries import RecipeQueries
from src.models.recipe import RecipeCreate, IngredientSchema
from src.database.database import DB_PATH

logger = get_logger("src.viewmodels.recipe")


class RecipeViewModel:
    def __init__(self):
        self.db = RecipeQueries(DB_PATH)
        # Estado Local: Lista de ingredientes que o usuário está adicionando na tela
        # Eles só vão para o banco quando clicar em "Salvar Receita"
        self.temp_ingredients: List[IngredientSchema] = []

    def add_temp_ingredient(self, name: str, qty: str, unit: str) -> str:
        """
        Valida e adiciona um ingrediente à lista temporária em memória.
        Retorna string de erro ou None se sucesso.
        """
        try:
            # Normalização simples
            name = name.strip() if name else ""
            qty = qty.strip() if qty else None
            unit = unit.strip() if unit else None

            # Validação via Pydantic
            ing = IngredientSchema(name=name, quantity=qty, unit=unit)

            # Adiciona à lista local
            self.temp_ingredients.append(ing)
            logger.debug(f"Ingrediente temporário adicionado: {name}")
            return None  # Sem erro

        except ValidationError as e:
            # Extrai a primeira mensagem de erro amigável
            msg = e.errors()[0]['msg']
            logger.warning(f"Erro de validação de ingrediente: {msg}")
            return str(msg)
        except Exception as e:
            logger.error(f"Erro inesperado ao adicionar ingrediente: {e}")
            return "Erro ao adicionar ingrediente."

    def remove_temp_ingredient(self, index: int):
        """Remove ingrediente da lista temporária pelo índice."""
        if 0 <= index < len(self.temp_ingredients):
            removed = self.temp_ingredients.pop(index)
            logger.debug(f"Ingrediente removido: {removed.name}")

    def save_recipe(self, user_id: int, title: str, instructions: str,
                    category_id: str, prep_time: str, servings: str,
                    add_instr: str, source: str) -> bool:
        """
        Compila todos os dados do formulário e tenta persistir no banco.
        """
        logger.info("Iniciando salvamento de receita...")
        try:
            # Conversão e Tratamento de Tipos
            # Se string vazia ou inválida, vira None
            p_time = int(
                prep_time) if prep_time and prep_time.isdigit() else None
            cat_id = int(
                category_id) if category_id and category_id.isdigit() else None

            # Criação do Objeto Mestre (Validação Pydantic Final)
            recipe_data = RecipeCreate(
                title=title,
                category_id=cat_id,
                preparation_time=p_time,
                servings=servings or None,
                instructions=instructions,
                additional_instructions=add_instr or None,
                source=source or None,
                # Injeta a lista que estava em memória
                ingredients=self.temp_ingredients
            )

            # Chama camada de persistência
            success = self.db.create_recipe(recipe_data, user_id)

            if success:
                # Limpa estado apenas se salvou com sucesso
                self.temp_ingredients = []
                logger.info("Receita salva e estado limpo.")

            return success

        except ValidationError as ve:
            # Erro de validação dos campos da receita (ex: título curto)
            error_msg = ve.errors()[0]['msg']
            logger.warning(f"Erro de validação ao salvar receita: {error_msg}")
            raise Exception(f"Dados inválidos: {error_msg}")
        except Exception as e:
            # Erro genérico ou de banco
            logger.error(
                f"Erro crítico no ViewModel ao salvar: {e}", exc_info=True)
            raise e
