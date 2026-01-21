# ARQUIVO: src/database/recipe_queries.py
# OBJETIVO: Centralizar operações de escrita/leitura de receitas com transações seguras.
import sqlite3
from src.core.logger import get_logger
from src.core.exceptions import DatabaseError
from src.database.database import get_db_connection
from src.models.recipe import RecipeCreate

logger = get_logger("src.database.recipe")


class RecipeQueries:
    def __init__(self, db_path: str = None):
        # Permite injeção de dependência para testes, se necessário
        pass

    def _get_connection(self):
        return get_db_connection()

    def create_recipe(self, recipe_data: RecipeCreate, user_id: int) -> bool:
        """
        Cria uma receita e seus ingredientes em uma TRANSAÇÃO ATÔMICA.
        Se falhar nos ingredientes, a receita não é salva.
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            # Inicia transação explicitamente para garantir atomicidade
            conn.execute("BEGIN TRANSACTION")

            # 1. Inserir Cabeçalho da Receita
            cursor.execute("""
                INSERT INTO recipes (
                    user_id, category_id, title, preparation_time, servings, 
                    instructions, additional_instructions, source, image_path
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id, recipe_data.category_id, recipe_data.title,
                recipe_data.preparation_time, recipe_data.servings,
                recipe_data.instructions, recipe_data.additional_instructions,
                recipe_data.source, recipe_data.image_path
            ))

            # Recupera o ID da receita recém-criada
            recipe_id = cursor.lastrowid

            # 2. Inserir Ingredientes (Lote)
            if recipe_data.ingredients:
                ingredients_data = [
                    (recipe_id, ing.name, ing.quantity, ing.unit)
                    for ing in recipe_data.ingredients
                ]
                # executemany é muito mais performático para inserts em lote
                cursor.executemany("""
                    INSERT INTO recipe_ingredients (recipe_id, name, quantity, unit)
                    VALUES (?, ?, ?, ?)
                """, ingredients_data)

            # Se chegou aqui sem erro, confirma tudo no disco
            conn.commit()
            logger.info(
                f"Receita '{recipe_data.title}' (ID: {recipe_id}) criada com sucesso.")
            return True

        except sqlite3.Error as e:
            # Em caso de qualquer erro, desfaz TUDO
            conn.rollback()
            logger.error(f"Transação falhou ao criar receita (Rollback): {e}")
            raise DatabaseError(f"Erro ao salvar receita no banco: {e}")
        finally:
            conn.close()

    def get_user_recipes(self, user_id: int) -> list:
        """
        Retorna todas as receitas criadas pelo usuário ou favoritadas por ele.
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            # Query Híbrida: Receitas do Dono OR Receitas Favoritadas
            sql = """
                SELECT DISTINCT r.*, 
                       CASE WHEN fr.user_id IS NOT NULL THEN 1 ELSE 0 END as is_favorite
                FROM recipes r
                LEFT JOIN favorite_recipes fr ON r.id = fr.recipe_id AND fr.user_id = ?
                WHERE r.user_id = ? OR fr.user_id IS NOT NULL
                ORDER BY r.created_at DESC
            """
            cursor.execute(sql, (user_id, user_id))
            rows = cursor.fetchall()

            # Retorna lista de dicionários (ou objetos Pydantic se preferir converter aqui)
            return [dict(row) for row in rows]

        except sqlite3.Error as e:
            logger.error(f"Erro ao buscar receitas: {e}")
            return []
        finally:
            conn.close()

    def toggle_recipe_favorite(self, recipe_id: int, user_id: int) -> bool:
        """Alterna favorito da receita."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM favorite_recipes WHERE user_id=? AND recipe_id=?", (user_id, recipe_id))
            if cursor.fetchone():
                cursor.execute(
                    "DELETE FROM favorite_recipes WHERE user_id=? AND recipe_id=?", (user_id, recipe_id))
                result = False  # Removeu
            else:
                cursor.execute(
                    "INSERT INTO favorite_recipes (user_id, recipe_id) VALUES (?, ?)", (user_id, recipe_id))
                result = True  # Adicionou
            conn.commit()
            return result
        except sqlite3.Error as e:
            logger.error(f"Erro no toggle favorite: {e}")
            return False
        finally:
            conn.close()
