# ARQUIVO: src/database/database.py
import sqlite3
import os
from src.core.logger import get_logger
from src.core.exceptions import DatabaseError

logger = get_logger("src.database")
DB_DIR = "data"
DB_NAME = "recipes.db"
DB_PATH = os.path.join(DB_DIR, DB_NAME)


def get_db_path():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    return DB_PATH


def get_db_connection():
    """Retorna uma conexão configurada com Row Factory."""
    try:
        conn = sqlite3.connect(get_db_path())
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Falha de conexão SQLite: {e}")
        raise DatabaseError("Não foi possível conectar ao banco de dados.", e)


def init_database():
    """Inicializa o esquema do banco de dados (Migrations Simplificadas)."""
    logger.info("Iniciando verificação de esquema do Banco de Dados...")
    conn = None
    try:
        conn = get_db_connection()
        # [CRÍTICO] Modo WAL evita travamentos de leitura/escrita simultânea
        conn.execute("PRAGMA journal_mode=WAL;")
        cursor = conn.cursor()

        tables = {
            "users": """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    hashed_password TEXT NOT NULL
                );
            """,
            "categories": """
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    user_id INTEGER,
                    icon TEXT DEFAULT 'restaurant_menu',
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                    UNIQUE(name, user_id)
                );
            """,
            "favorite_categories": """
                CREATE TABLE IF NOT EXISTS favorite_categories (
                    user_id INTEGER NOT NULL,
                    category_id INTEGER NOT NULL,
                    PRIMARY KEY (user_id, category_id),
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                    FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
                );
            """,
            "recipes": """
                CREATE TABLE IF NOT EXISTS recipes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    category_id INTEGER,
                    title TEXT NOT NULL,
                    preparation_time INTEGER,
                    servings TEXT,
                    instructions TEXT NOT NULL,
                    additional_instructions TEXT,
                    source TEXT,
                    image_path TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
                );
            """,
            "favorite_recipes": """
                CREATE TABLE IF NOT EXISTS favorite_recipes (
                    user_id INTEGER NOT NULL,
                    recipe_id INTEGER NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (user_id, recipe_id),
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                    FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE
                );
            """,
            "recipe_ingredients": """
                CREATE TABLE IF NOT EXISTS recipe_ingredients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recipe_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    quantity TEXT,
                    unit TEXT,
                    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
                );
            """
        }

        for table_name, query in tables.items():
            cursor.execute(query)
            logger.debug(f"Tabela verificada/criada: {table_name}")

        conn.commit()
        logger.info("Banco de dados atualizado e verificado com sucesso.")

    except sqlite3.Error as e:
        logger.critical(
            f"Erro Crítico Geral no Banco de Dados: {e}", exc_info=True)
        raise DatabaseError(
            "Falha na inicialização do esquema do banco de dados.", e)
    finally:
        if conn:
            conn.close()
