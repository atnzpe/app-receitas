# ARQUIVO: src/database/category_queries.py
import sqlite3
from typing import List, Optional, Dict  # <--- [CORREÇÃO] Adicionado Dict
from src.core.logger import get_logger
from src.core.exceptions import DatabaseError
from src.database.database import get_db_connection
from src.models.recipe_model import Category

logger = get_logger("src.database.category")

DEFAULT_CATEGORIES = [
    "Café da Manhã", "Almoço", "Jantar", "Sobremesas",
    "Lanches", "Bebidas", "Fitness", "Low Carb",
    "Vegano", "Massas", "Carnes", "Peixes"
]


class CategoryQueries:
    """Gerenciador de dados de Categorias."""

    def _get_conn(self):
        return get_db_connection()

    def init_default_categories(self):
        conn = self._get_conn()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM categories WHERE user_id IS NULL")
            if cursor.fetchone()[0] == 0:
                for cat_name in DEFAULT_CATEGORIES:
                    cursor.execute(
                        "INSERT INTO categories (name) VALUES (?)", (cat_name,))
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Erro seed: {e}")
        finally:
            conn.close()

    def get_all_categories_for_user(self, user_id: int) -> List[Category]:
        self.init_default_categories()
        conn = self._get_conn()
        try:
            cursor = conn.cursor()
            # Traz categorias e flag de favorito
            sql = """
                SELECT DISTINCT c.id, c.name, c.user_id,
                       CASE WHEN fc.user_id IS NOT NULL THEN 1 ELSE 0 END as is_fav
                FROM categories c
                LEFT JOIN favorite_categories fc ON c.id = fc.category_id AND fc.user_id = ?
                WHERE c.user_id IS NULL OR c.user_id = ? OR fc.user_id IS NOT NULL
                ORDER BY c.name ASC
            """
            cursor.execute(sql, (user_id, user_id))
            return [Category(id=r[0], name=r[1], user_id=r[2], is_favorite=bool(r[3])) for r in cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Erro get cats: {e}")
            return []
        finally:
            conn.close()

    def add_category(self, name: str, user_id: int) -> Optional[Category]:
        conn = self._get_conn()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO categories (name, user_id) VALUES (?, ?)", (name, user_id))
            conn.commit()
            return Category(id=cursor.lastrowid, name=name, user_id=user_id)
        except:
            return None
        finally:
            conn.close()

    def delete_category(self, cat_id: int, user_id: int) -> bool:
        conn = self._get_conn()
        try:
            c = conn.execute(
                "DELETE FROM categories WHERE id=? AND user_id=?", (cat_id, user_id))
            conn.commit()
            return c.rowcount > 0
        except:
            return False
        finally:
            conn.close()

    # --- LÓGICA DE FAVORITO CASCATA ---
    def toggle_favorite_cascade(self, cat_id: int, user_id: int) -> bool:
        """
        Favorita Categoria + Todas as Receitas dela.
        """
        conn = self._get_conn()
        try:
            cursor = conn.cursor()
            conn.execute("BEGIN")

            # Verifica estado
            cursor.execute(
                "SELECT 1 FROM favorite_categories WHERE user_id=? AND category_id=?", (user_id, cat_id))
            exists = cursor.fetchone()

            is_fav = False
            if exists:
                # Remove da Categoria
                cursor.execute(
                    "DELETE FROM favorite_categories WHERE user_id=? AND category_id=?", (user_id, cat_id))
                # Remove das Receitas
                cursor.execute("""
                    DELETE FROM favorite_recipes 
                    WHERE user_id=? AND recipe_id IN (SELECT id FROM recipes WHERE category_id=?)
                """, (user_id, cat_id))
                is_fav = False
            else:
                # Adiciona na Categoria
                cursor.execute(
                    "INSERT INTO favorite_categories (user_id, category_id) VALUES (?,?)", (user_id, cat_id))
                # Adiciona nas Receitas (INSERT OR IGNORE)
                cursor.execute("""
                    INSERT OR IGNORE INTO favorite_recipes (user_id, recipe_id)
                    SELECT ?, id FROM recipes WHERE category_id=?
                """, (user_id, cat_id))
                is_fav = True

            conn.commit()
            return is_fav
        except sqlite3.Error as e:
            conn.rollback()
            logger.error(f"Erro cascade: {e}")
            return False
        finally:
            conn.close()

    def get_user_categories(self, user_id: int) -> List[Dict]:
        """Retorna dicionários para Dropdown."""
        cats = self.get_all_categories_for_user(user_id)
        return [{'id': c.id, 'name': c.name} for c in cats]

    def update_category(self, cat_id: int, name: str, user_id: int) -> bool:
        conn = self._get_conn()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE categories SET name=? WHERE id=? AND user_id=?", (name, cat_id, user_id))
            conn.commit()
            return cursor.rowcount > 0
        except:
            return False
        finally:
            conn.close()
