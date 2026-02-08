# ARQUIVO: src/database/recipe_queries.py
import sqlite3
from typing import List, Dict, Any, Optional
from src.core.logger import get_logger
from src.database.database import get_db_connection
from src.models.recipe import RecipeCreate

logger = get_logger("src.database.recipe")


class RecipeQueries:
    def _get_conn(self):
        return get_db_connection()

    def _close_conn(self, conn):
        if conn:
            conn.close()

    # --- BUSCA AVANÇADA (ATUALIZADA) ---
    def search_advanced(self, uid: int, term: str = "", max_time: int = 0,
                        servings: str = "", category_id: int = 0) -> List[Dict]:
        """Busca com suporte a filtro por Categoria."""
        conn = self._get_conn()
        try:
            params = [uid]
            sql = """
                SELECT DISTINCT r.*, 
                       (SELECT COUNT(*) FROM favorite_recipes WHERE recipe_id=r.id AND user_id=?) as is_favorite
                FROM recipes r 
                WHERE 1=1
            """

            if term:
                sql += " AND (r.title LIKE ? OR r.instructions LIKE ?)"
                t = f"%{term}%"
                params.extend([t, t])

            if max_time > 0:
                sql += " AND r.preparation_time <= ?"
                params.append(max_time)

            if servings:
                sql += " AND r.servings LIKE ?"
                params.append(f"%{servings}%")

            # [NOVO] Filtro por Categoria
            if category_id > 0:
                sql += " AND r.category_id = ?"
                params.append(category_id)

            sql += " ORDER BY r.title ASC"

            cur = conn.cursor()
            cur.execute(sql, params)
            return [dict(row) for row in cur.fetchall()]
        except Exception as e:
            logger.error(f"Erro search_advanced: {e}")
            return []
        finally:
            conn.close()

    # --- MÉTODOS CRUD PADRÃO ---

    def create_recipe(self, data: RecipeCreate, user_id: int) -> bool:
        conn = self._get_conn()
        try:
            cur = conn.cursor()
            conn.execute("BEGIN")
            cur.execute("""
                INSERT INTO recipes (user_id, category_id, title, preparation_time, servings, instructions, additional_instructions, source, image_path) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, data.category_id, data.title, data.preparation_time, data.servings, data.instructions, data.additional_instructions, data.source, data.image_path))
            rid = cur.lastrowid
            if data.ingredients:
                ings = [(rid, i.name, i.quantity, i.unit)
                        for i in data.ingredients]
                cur.executemany(
                    "INSERT INTO recipe_ingredients (recipe_id, name, quantity, unit) VALUES (?, ?, ?, ?)", ings)
            conn.commit()
            return True
        except:
            conn.rollback()
            return False
        finally:
            conn.close()

    def update_recipe(self, rid: int, data: RecipeCreate, uid: int) -> bool:
        conn = self._get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT 1 FROM recipes WHERE id=? AND user_id=?", (rid, uid))
            if not cur.fetchone():
                return False
            conn.execute("BEGIN")
            cur.execute("""
                UPDATE recipes SET category_id=?, title=?, preparation_time=?, servings=?, instructions=?, additional_instructions=?, source=?, image_path=?, updated_at=CURRENT_TIMESTAMP
                WHERE id=?
            """, (data.category_id, data.title, data.preparation_time, data.servings, data.instructions, data.additional_instructions, data.source, data.image_path, rid))
            cur.execute(
                "DELETE FROM recipe_ingredients WHERE recipe_id=?", (rid,))
            if data.ingredients:
                ings = [(rid, i.name, i.quantity, i.unit)
                        for i in data.ingredients]
                cur.executemany(
                    "INSERT INTO recipe_ingredients (recipe_id, name, quantity, unit) VALUES (?, ?, ?, ?)", ings)
            conn.commit()
            return True
        except:
            conn.rollback()
            return False
        finally:
            conn.close()

    def get_recipe_details(self, rid: int) -> Optional[Dict]:
        conn = self._get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM recipes WHERE id=?", (rid,))
            row = cur.fetchone()
            if not row:
                return None
            rec = dict(row)
            cur.execute(
                "SELECT name, quantity, unit FROM recipe_ingredients WHERE recipe_id=?", (rid,))
            rec['ingredients'] = [dict(r) for r in cur.fetchall()]
            return rec
        finally:
            conn.close()

    def get_user_recipes(self, user_id: int) -> List[Dict]:
        conn = self._get_conn()
        try:
            cur = conn.cursor()
            sql = """
                SELECT DISTINCT r.*, CASE WHEN fr.user_id IS NOT NULL THEN 1 ELSE 0 END as is_favorite
                FROM recipes r
                LEFT JOIN favorite_recipes fr ON r.id = fr.recipe_id AND fr.user_id = ?
                WHERE r.user_id = ? OR fr.user_id IS NOT NULL
                ORDER BY r.created_at DESC
            """
            cur.execute(sql, (user_id, user_id))
            return [dict(row) for row in cur.fetchall()]
        finally:
            conn.close()

    def delete_recipe(self, recipe_id: int, user_id: int) -> bool:
        conn = self._get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM recipes WHERE id=? AND user_id=?", (recipe_id, user_id))
            conn.commit()
            return cur.rowcount > 0
        finally:
            conn.close()

    def toggle_favorite(self, rid: int, uid: int) -> bool:
        conn = self._get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT 1 FROM favorite_recipes WHERE user_id=? AND recipe_id=?", (uid, rid))
            if cur.fetchone():
                cur.execute(
                    "DELETE FROM favorite_recipes WHERE user_id=? AND recipe_id=?", (uid, rid))
                res = False
            else:
                cur.execute(
                    "INSERT INTO favorite_recipes (user_id, recipe_id) VALUES (?,?)", (uid, rid))
                res = True
            conn.commit()
            return res
        finally:
            conn.close()

    # Mantido para compatibilidade, mas o Discovery deve usar search_advanced
    def search_recipes_by_name(self, term: str, uid: int) -> List[Dict]:
        return self.search_advanced(uid, term=term)
