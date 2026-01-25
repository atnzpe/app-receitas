# ARQUIVO: src/database/recipe_queries.py
# OBJETIVO: Centralizar operações de receitas (Create, Read, Update, Delete).
import sqlite3
from typing import List, Dict, Any, Optional
from src.core.logger import get_logger
from src.core.exceptions import DatabaseError
from src.database.database import get_db_connection
from src.models.recipe import RecipeCreate

logger = get_logger("src.database.recipe")


class RecipeQueries:
    def __init__(self, db_path: str = None):
        pass

    def _get_connection(self):
        return get_db_connection()

    def create_recipe(self, recipe_data: RecipeCreate, user_id: int) -> bool:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            conn.execute("BEGIN TRANSACTION")

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

            recipe_id = cursor.lastrowid

            if recipe_data.ingredients:
                ingredients_data = [
                    (recipe_id, ing.name, ing.quantity, ing.unit)
                    for ing in recipe_data.ingredients
                ]
                cursor.executemany("""
                    INSERT INTO recipe_ingredients (recipe_id, name, quantity, unit)
                    VALUES (?, ?, ?, ?)
                """, ingredients_data)

            conn.commit()
            logger.info(
                f"Receita '{recipe_data.title}' (ID: {recipe_id}) criada.")
            return True

        except sqlite3.Error as e:
            conn.rollback()
            logger.error(f"Erro ao criar receita: {e}")
            raise DatabaseError(f"Erro ao salvar: {e}")
        finally:
            conn.close()

    def get_user_recipes(self, user_id: int) -> List[Dict[str, Any]]:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
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
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            logger.error(f"Erro ao buscar receitas: {e}")
            return []
        finally:
            conn.close()

    def delete_recipe(self, recipe_id: int, user_id: int) -> bool:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM recipes WHERE id = ? AND user_id = ?", (recipe_id, user_id))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            logger.error(f"Erro ao deletar: {e}")
            return False
        finally:
            conn.close()

    def toggle_favorite(self, recipe_id: int, user_id: int) -> bool:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM favorite_recipes WHERE user_id=? AND recipe_id=?", (user_id, recipe_id))
            if cursor.fetchone():
                cursor.execute(
                    "DELETE FROM favorite_recipes WHERE user_id=? AND recipe_id=?", (user_id, recipe_id))
                result = False
            else:
                cursor.execute(
                    "INSERT INTO favorite_recipes (user_id, recipe_id) VALUES (?, ?)", (user_id, recipe_id))
                result = True
            conn.commit()
            return result
        except sqlite3.Error as e:
            logger.error(f"Erro toggle favorite: {e}")
            return False
        finally:
            conn.close()

    # --- MÉTODOS PARA EDIÇÃO (UPDATE) ---

    def get_recipe_details(self, recipe_id: int) -> Optional[Dict[str, Any]]:
        """Busca dados completos da receita para edição."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
            row = cursor.fetchone()
            if not row:
                return None

            recipe = dict(row)

            # Busca ingredientes
            cursor.execute(
                "SELECT name, quantity, unit FROM recipe_ingredients WHERE recipe_id = ?", (recipe_id,))
            ing_rows = cursor.fetchall()
            recipe['ingredients'] = [dict(row) for row in ing_rows]

            return recipe
        except sqlite3.Error as e:
            logger.error(f"Erro ao buscar detalhes: {e}")
            return None
        finally:
            conn.close()

    def update_recipe(self, recipe_id: int, recipe_data: RecipeCreate, user_id: int) -> bool:
        """Atualiza receita e recria ingredientes."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            conn.execute("BEGIN TRANSACTION")

            # Verifica propriedade
            cursor.execute(
                "SELECT 1 FROM recipes WHERE id = ? AND user_id = ?", (recipe_id, user_id))
            if not cursor.fetchone():
                logger.warning(
                    f"Tentativa de editar receita alheia: {recipe_id}")
                return False

            # Atualiza dados básicos
            cursor.execute("""
                UPDATE recipes SET 
                    category_id=?, title=?, preparation_time=?, servings=?, 
                    instructions=?, additional_instructions=?, source=?, updated_at=CURRENT_TIMESTAMP
                WHERE id=?
            """, (
                recipe_data.category_id, recipe_data.title,
                recipe_data.preparation_time, recipe_data.servings,
                recipe_data.instructions, recipe_data.additional_instructions,
                recipe_data.source, recipe_id
            ))

            # Atualiza Ingredientes (Delete + Insert)
            cursor.execute(
                "DELETE FROM recipe_ingredients WHERE recipe_id = ?", (recipe_id,))

            if recipe_data.ingredients:
                ingredients_data = [
                    (recipe_id, ing.name, ing.quantity, ing.unit)
                    for ing in recipe_data.ingredients
                ]
                cursor.executemany("""
                    INSERT INTO recipe_ingredients (recipe_id, name, quantity, unit)
                    VALUES (?, ?, ?, ?)
                """, ingredients_data)

            conn.commit()
            logger.info(f"Receita {recipe_id} atualizada.")
            return True

        except sqlite3.Error as e:
            conn.rollback()
            logger.error(f"Erro ao atualizar: {e}")
            raise DatabaseError("Falha na atualização.", e)
        finally:
            conn.close()
