# CÓDIGO COMPLETO E BLINDADO
import sqlite3
import os
from src.core.logger import get_logger
from src.core.exceptions import DatabaseError

logger = get_logger("src.database")

DB_DIR = "data"
DB_NAME = "recipes.db"
DB_PATH = os.path.join(DB_DIR, DB_NAME)


def init_database():
    """
    Inicializa o banco de dados. 
    Define a estrutura com permissões de proprietário (user_id).
    """
    logger.info("Iniciando verificação de esquema do Banco de Dados...")

    try:
        os.makedirs(DB_DIR, exist_ok=True)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        # Scripts SQL Atualizados
        queries = [
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                hashed_password TEXT NOT NULL
            );
            """,
            # ALTERADO: Adicionado user_id (NULL = Nativa, ID = Usuário)
            """
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                user_id INTEGER, 
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                UNIQUE(name, user_id) -- Impede que o mesmo usuário tenha duas categorias iguais, mas permite repetição entre usuários diferentes
            );
            """,
            # NOVA TABELA: Favoritos (Many-to-Many)
            """
            CREATE TABLE IF NOT EXISTS favorite_categories (
                user_id INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                PRIMARY KEY (user_id, category_id),
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                instructions TEXT,
                prep_time_minutes INTEGER,
                source_url TEXT,
                image_path TEXT,
                category_id INTEGER,
                user_id INTEGER,
                FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE SET NULL,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity TEXT,
                recipe_id INTEGER NOT NULL,
                FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE
            );
            """
        ]

        for q in queries:
            cursor.execute(q)

        conn.commit()
        logger.info(
            "Banco de dados atualizado com suporte a permissões e favoritos.")

    except sqlite3.Error as e:
        logger.critical(f"Erro Crítico no Banco de Dados: {e}", exc_info=True)
        raise DatabaseError(
            "Falha na inicialização do esquema do banco de dados.", e)
    finally:
        if 'conn' in locals() and conn:
            conn.close()


def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Falha de conexão SQLite: {e}")
        raise DatabaseError("Não foi possível conectar ao banco de dados.", e)
