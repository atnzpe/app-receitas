# ARQUIVO: src/database/category_queries.py
# CÓDIGO COMPLETO E BLINDADO
import sqlite3
from typing import List, Optional
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


def init_default_categories():
    """Garante que as categorias nativas existam."""
    conn = get_db_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM categories WHERE user_id IS NULL")
        if cursor.fetchone()[0] == 0:
            logger.info("Populando categorias nativas...")
            for cat_name in DEFAULT_CATEGORIES:
                cursor.execute(
                    "INSERT INTO categories (name) VALUES (?)", (cat_name,))
            conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Erro seed: {e}")
    finally:
        conn.close()


def get_all_categories_for_user(user_id: int) -> List[Category]:
    """
    Retorna uma lista unificada contendo:
    1. Categorias Nativas (user_id IS NULL)
    2. Categorias criadas pelo usuário (user_id = user_id)
    3. Categorias favoritadas pelo usuário (mesmo que de outros)
    """
    init_default_categories()
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        # Query Otimizada: Faz o Join com favoritos para preencher o campo 'is_favorite'
        # e filtra para mostrar apenas o que é relevante para o usuário.
        sql = """
            SELECT DISTINCT c.id, c.name, c.user_id,
                   CASE WHEN fc.user_id IS NOT NULL THEN 1 ELSE 0 END as is_fav
            FROM categories c
            LEFT JOIN favorite_categories fc ON c.id = fc.category_id AND fc.user_id = ?
            WHERE c.user_id IS NULL 
               OR c.user_id = ? 
               OR fc.user_id IS NOT NULL
            ORDER BY c.name ASC
        """
        cursor.execute(sql, (user_id, user_id))
        rows = cursor.fetchall()

        return [
            Category(
                id=row['id'],
                name=row['name'],
                user_id=row['user_id'],
                is_favorite=bool(row['is_fav'])
            ) for row in rows
        ]
    except sqlite3.Error as e:
        logger.error(f"Erro ao buscar categorias: {e}", exc_info=True)
        return []
    finally:
        conn.close()


def add_category(name: str, user_id: int) -> Optional[Category]:
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO categories (name, user_id) VALUES (?, ?)", (name, user_id))
        conn.commit()
        return Category(id=cursor.lastrowid, name=name, user_id=user_id)
    except sqlite3.IntegrityError:
        logger.warning(f"Tentativa de duplicidade: {name}")
        return None
    except sqlite3.Error as e:
        logger.error(f"Erro add: {e}")
        raise DatabaseError("Erro ao criar categoria", e)
    finally:
        conn.close()


def delete_category(cat_id: int, user_id: int) -> bool:
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # Blindagem: Só deleta se o usuário for o dono (user_id bate)
        cursor.execute(
            "DELETE FROM categories WHERE id = ? AND user_id = ?", (cat_id, user_id))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        logger.error(f"Erro delete: {e}")
        return False
    finally:
        conn.close()


def toggle_favorite(cat_id: int, user_id: int) -> bool:
    """Alterna o status de favorito (Like/Unlike)."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # Verifica se já existe
        cursor.execute(
            "SELECT 1 FROM favorite_categories WHERE user_id = ? AND category_id = ?", (user_id, cat_id))
        exists = cursor.fetchone()

        if exists:
            cursor.execute(
                "DELETE FROM favorite_categories WHERE user_id = ? AND category_id = ?", (user_id, cat_id))
            is_fav = False
        else:
            cursor.execute(
                "INSERT INTO favorite_categories (user_id, category_id) VALUES (?, ?)", (user_id, cat_id))
            is_fav = True

        conn.commit()
        return is_fav
    except sqlite3.Error as e:
        logger.error(f"Erro toggle favorite: {e}")
        return False
    finally:
        conn.close()

# Mantido para compatibilidade de testes antigos, se houver


def get_user_categories(user_id: int) -> List[Category]:
    return get_all_categories_for_user(user_id)


def update_category(cat_id: int, name: str, user_id: int) -> bool:
    conn = get_db_connection()
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
