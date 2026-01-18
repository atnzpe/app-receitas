# ARQUIVO: src/database/category_queries.py
# CÓDIGO COMPLETO E BLINDADO

import sqlite3
from typing import List, Optional

# Importações do nosso Core Blindado
from src.core.logger import get_logger
from src.core.exceptions import DatabaseError
from src.database.database import get_db_connection
from src.models.recipe_model import Category

# Logger específico para rastreabilidade
logger = get_logger("src.database.category")

# --- MISE EN PLACE: Categorias Nativas ---
# Estas são as categorias "Michelin" que já vêm com o app.
DEFAULT_CATEGORIES = [
    "Entradas & Petiscos", "Prato Principal", "Acompanhamentos",
    "Sobremesas", "Bebidas & Drinks", "Café da Manhã",
    "Fitness / Saudável", "Massas & Risotos", "Carnes",
    "Peixes & Frutos do Mar", "Vegetariano / Vegano", "Pães & Bolos"
]


def init_default_categories():
    """
    Verifica se a tabela de categorias está vazia. 
    Se estiver, popula com as categorias nativas (Seed).
    Isso garante que o usuário nunca veja uma tela vazia no primeiro uso.
    """
    conn = get_db_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        # Verifica quantas categorias existem
        cursor.execute("SELECT COUNT(*) FROM categories")
        count = cursor.fetchone()[0]

        if count == 0:
            logger.info(
                "Tabela vazia detectada. Iniciando 'Seed' de categorias nativas...")
            for cat_name in DEFAULT_CATEGORIES:
                # Inserção segura contra SQL Injection (?)
                cursor.execute(
                    "INSERT INTO categories (name) VALUES (?)", (cat_name,))
            conn.commit()
            logger.info(
                f"Sucesso: {len(DEFAULT_CATEGORIES)} categorias nativas inseridas.")

    except sqlite3.Error as e:
        # Não paramos o app por isso, mas logamos o erro crítico
        logger.error(
            f"Erro ao popular categorias iniciais: {e}", exc_info=True)
    finally:
        conn.close()


def get_all_categories() -> List[Category]:
    """
    Busca todas as categorias ordenadas alfabeticamente.
    Retorna: Lista de objetos Pydantic 'Category'.
    """
    # Garante o Seed antes de listar
    init_default_categories()

    logger.debug("Query: Buscando todas as categorias...")
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM categories ORDER BY name ASC")
        rows = cursor.fetchall()

        # Converte as tuplas do banco em Objetos Pydantic (Validação na saída)
        categories = [Category(id=row['id'], name=row['name']) for row in rows]
        return categories

    except sqlite3.Error as e:
        logger.error(f"Erro SQLite ao listar: {e}", exc_info=True)
        raise DatabaseError("Não foi possível carregar as categorias.", e)
    finally:
        conn.close()


def add_category(name: str) -> Optional[Category]:
    """
    Insere uma nova categoria customizada pelo usuário.
    """
    logger.debug(f"Query: Inserindo categoria '{name}'")
    conn = get_db_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        conn.commit()

        new_id = cursor.lastrowid
        logger.info(f"Categoria '{name}' criada com ID: {new_id}")
        return Category(id=new_id, name=name)

    except sqlite3.IntegrityError:
        logger.warning(f"Tentativa de duplicidade: '{name}' já existe.")
        return None  # Retorna None para o ViewModel tratar o aviso
    except sqlite3.Error as e:
        logger.error(f"Erro ao salvar: {e}", exc_info=True)
        raise DatabaseError("Falha crítica ao salvar categoria.", e)
    finally:
        conn.close()


def update_category(cat_id: int, new_name: str) -> bool:
    """Atualiza o nome de uma categoria existente."""
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE categories SET name = ? WHERE id = ?", (new_name, cat_id))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.IntegrityError:
        return False  # Nome já existe
    except sqlite3.Error as e:
        logger.error(f"Erro ao atualizar ID {cat_id}: {e}")
        raise DatabaseError("Falha ao atualizar registro.", e)
    finally:
        conn.close()


def delete_category(cat_id: int) -> bool:
    """Remove uma categoria."""
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        # Nota: Receitas vinculadas terão category_id = NULL (Regra ON DELETE SET NULL)
        cursor.execute("DELETE FROM categories WHERE id = ?", (cat_id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        logger.error(f"Erro ao deletar ID {cat_id}: {e}")
        raise DatabaseError("Falha ao excluir registro.", e)
    finally:
        conn.close()
