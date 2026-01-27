# ARQUIVO: src/database/recipe_queries.py
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
            logger.info(f"Receita '{recipe_data.title}' (ID: {recipe_id}) criada.")
            return True

        except sqlite3.Error as e:
            conn.rollback()
            logger.error(f"Erro ao criar receita: {e}")
            raise DatabaseError(f"Erro ao salvar: {e}")
        finally:
            conn.close()

    def update_recipe(self, recipe_id: int, recipe_data: RecipeCreate, user_id: int) -> bool:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            conn.execute("BEGIN TRANSACTION")

            # Verifica propriedade
            cursor.execute("SELECT 1 FROM recipes WHERE id = ? AND user_id = ?", (recipe_id, user_id))
            if not cursor.fetchone():
                return False

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

            # Atualiza ingredientes (Remove antigos e insere novos)
            cursor.execute("DELETE FROM recipe_ingredients WHERE recipe_id = ?", (recipe_id,))
            
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

    def delete_recipe(self, recipe_id: int, user_id: int) -> bool:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM recipes WHERE id = ? AND user_id = ?", (recipe_id, user_id))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            logger.error(f"Erro ao deletar: {e}")
            return False
        finally:
            conn.close()

    def get_user_recipes(self, user_id: int) -> List[Dict[str, Any]]:
        """
        [MODO MINHAS RECEITAS]
        Retorna estritamente:
        1. Receitas criadas pelo usuário logado.
        2. Receitas favoritadas pelo usuário.
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            
            sql = """
                SELECT DISTINCT r.*, 
                       CASE WHEN fr.user_id IS NOT NULL THEN 1 ELSE 0 END as is_favorite
                FROM recipes r
                LEFT JOIN favorite_recipes fr ON r.id = fr.recipe_id AND fr.user_id = ?
                WHERE 
                    r.user_id = ?             
                    OR fr.user_id IS NOT NULL 
                ORDER BY r.created_at DESC
            """
            cursor.execute(sql, (user_id, user_id))
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Erro ao buscar minhas receitas: {e}")
            return []
        finally:
            conn.close()

    def get_all_recipes(self, user_id: int) -> List[Dict[str, Any]]:
        """
        [MODO DISCOVERY - LISTAGEM GERAL]
        Retorna TODAS as receitas do banco.
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            
            sql = """
                SELECT DISTINCT r.*, 
                       CASE WHEN fr.user_id IS NOT NULL THEN 1 ELSE 0 END as is_favorite
                FROM recipes r
                LEFT JOIN favorite_recipes fr ON r.id = fr.recipe_id AND fr.user_id = ?
                ORDER BY r.title ASC
            """
            cursor.execute(sql, (user_id,))
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Erro ao buscar discovery: {e}")
            return []
        finally:
            conn.close()

    def get_recipe_details(self, recipe_id: int) -> Optional[Dict[str, Any]]:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
            row = cursor.fetchone()
            if not row: return None
            
            recipe = dict(row)
            
            cursor.execute("SELECT name, quantity, unit FROM recipe_ingredients WHERE recipe_id = ?", (recipe_id,))
            ing_rows = cursor.fetchall()
            recipe['ingredients'] = [dict(row) for row in ing_rows]
            
            return recipe
        except sqlite3.Error as e:
            logger.error(f"Erro ao buscar detalhes: {e}")
            return None
        finally:
            conn.close()

    def toggle_favorite(self, recipe_id: int, user_id: int) -> bool:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM favorite_recipes WHERE user_id=? AND recipe_id=?", (user_id, recipe_id))
            if cursor.fetchone():
                cursor.execute("DELETE FROM favorite_recipes WHERE user_id=? AND recipe_id=?", (user_id, recipe_id))
                result = False 
            else:
                cursor.execute("INSERT INTO favorite_recipes (user_id, recipe_id) VALUES (?, ?)", (user_id, recipe_id))
                result = True 
            conn.commit()
            return result
        except sqlite3.Error as e:
            logger.error(f"Erro toggle favorite: {e}")
            return False
        finally:
            conn.close()

    # --- SPRINT 5: MOTORES DE BUSCA (DISCOVERY) ---

    def search_recipes_by_name(self, term: str, user_id: int) -> List[Dict[str, Any]]:
        """
        Busca receitas por título (Nome) ou categoria.
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            search_term = f"%{term}%"
            
            sql = """
                SELECT DISTINCT r.*, 
                       c.name as category_name,
                       CASE WHEN fr.user_id IS NOT NULL THEN 1 ELSE 0 END as is_favorite
                FROM recipes r
                LEFT JOIN categories c ON r.category_id = c.id
                LEFT JOIN favorite_recipes fr ON r.id = fr.recipe_id AND fr.user_id = ?
                WHERE r.title LIKE ? OR c.name LIKE ?
                ORDER BY r.title ASC
            """
            cursor.execute(sql, (user_id, search_term, search_term))
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Erro na busca por nome: {e}")
            return []
        finally:
            conn.close()

    def search_recipes_by_ingredients(self, ingredients: List[str], user_id: int) -> List[Dict[str, Any]]:
        """
        Modo Dispensa: Busca receitas que contenham os ingredientes informados.
        Retorna receitas ordenadas pela quantidade de ingredientes coincidentes (relevância).
        """
        if not ingredients:
            return []

        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            
            # Monta placeholders dinamicamente
            placeholders = ','.join(['?'] * len(ingredients))
            # Lista de parâmetros: user_id primeiro, depois os ingredientes limpos
            params = [user_id] + [ing.strip() for ing in ingredients]
            
            # Query Inteligente:
            # - Filtra ingredientes (IN)
            # - Agrupa por receita
            # - Conta quantos hits (match_count)
            # - Ordena por relevância
            sql = f"""
                SELECT r.*, 
                       COUNT(ri.id) as match_count,
                       CASE WHEN fr.user_id IS NOT NULL THEN 1 ELSE 0 END as is_favorite
                FROM recipes r
                JOIN recipe_ingredients ri ON r.id = ri.recipe_id
                LEFT JOIN favorite_recipes fr ON r.id = fr.recipe_id AND fr.user_id = ?
                WHERE ri.name IN ({placeholders})
                GROUP BY r.id
                ORDER BY match_count DESC, r.title ASC
            """
            
            cursor.execute(sql, params)
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Erro na busca por dispensa: {e}")
            return []
        finally:
            conn.close()