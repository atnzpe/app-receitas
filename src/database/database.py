# CÓDIGO COMPLETO E COMENTADO
import sqlite3
import os
import logging  # Para debug

logger = logging.getLogger(__name__)

# Define o caminho do banco de dados (offline-first)
DB_DIR = "data"
DB_NAME = "recipes.db"
DB_PATH = os.path.join(DB_DIR, DB_NAME)


def init_database():
    """
    Inicializa o banco de dados SQLite e cria as tabelas iniciais
    se elas ainda não existirem.
    """
    try:
        # Garante que o diretório 'data' (ignorado pelo .gitignore) exista
        os.makedirs(DB_DIR, exist_ok=True)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        logger.info(f"Banco de dados conectado em: {DB_PATH}")

        # Habilitar chaves estrangeiras é crucial para a integridade dos dados
        cursor.execute("PRAGMA foreign_keys = ON;")

        # Tabela de Usuários
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            hashed_password TEXT NOT NULL
        );
        """)

        # Tabela de Categorias
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
        """)

        # Tabela de Receitas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            instructions TEXT,
            prep_time_minutes INTEGER,
            source_url TEXT,
            image_path TEXT,
            category_id INTEGER,
            user_id INTEGER, -- Vincula receita ao usuário
            FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE SET NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        );
        """)

        # Tabela de Ingredientes
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity TEXT,
            recipe_id INTEGER NOT NULL,
            FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE
        );
        """)

        conn.commit()
        logger.info(
            "Tabelas 'users', 'categories', 'recipes', e 'ingredients' verificadas/criadas.")

    except sqlite3.Error as e:
        logger.error(
            f"Erro ao inicializar o banco de dados: {e}", exc_info=True)
    finally:
        if conn:
            conn.close()


def get_db_connection() -> sqlite3.Connection | None:
    """
    Retorna uma nova conexão com o banco de dados.
    Usar 'row_factory = sqlite3.Row' nos permite acessar dados por nome
    de coluna (como um dicionário), o que é muito mais limpo.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Permite acesso estilo dict
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Erro ao conectar ao banco de dados: {e}", exc_info=True)
        if conn:
            conn.close()
        return None
