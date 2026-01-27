# ARQUIVO: src/database/database.py
# OBJETIVO: Gerenciar a conexão e o esquema do banco de dados SQLite.
import sqlite3
import os
from src.core.logger import get_logger
from src.core.exceptions import DatabaseError

# Inicializa o logger específico para banco de dados
logger = get_logger("src.database")

# Definição de caminhos
DB_DIR = "data"
DB_NAME = "recipes.db"
DB_PATH = os.path.join(DB_DIR, DB_NAME)

def init_database():
    """
    Inicializa o banco de dados (Migrations Simplificadas).
    Cria tabelas se não existirem e garante integridade referencial.
    """
    logger.info("Iniciando verificação de esquema do Banco de Dados...")

    try:
        # Garante que a pasta de dados existe
        os.makedirs(DB_DIR, exist_ok=True)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Habilita Foreign Keys (SQLite padrão é OFF)
        cursor.execute("PRAGMA foreign_keys = ON;")

        # Lista de tabelas essenciais
        queries = [
            # 1. Usuários
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                hashed_password TEXT NOT NULL
            );
            """,
            # 2. Categorias
            """
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                user_id INTEGER,
                icon TEXT DEFAULT 'restaurant_menu',
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                UNIQUE(name, user_id)
            );
            """,
            # 3. Favoritos de Categorias
            """
            CREATE TABLE IF NOT EXISTS favorite_categories (
                user_id INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                PRIMARY KEY (user_id, category_id),
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
            );
            """,
            # 3.1 Favoritos de Receitas
            """
            CREATE TABLE IF NOT EXISTS favorite_recipes (
                user_id INTEGER NOT NULL,
                recipe_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, recipe_id),
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE
            );
            """,
            # 4. Receitas (Mestre) - Atualizado com novos campos da Sprint 4
            """
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category_id INTEGER,
                title TEXT NOT NULL,
                preparation_time INTEGER,
                servings TEXT,
                instructions TEXT NOT NULL,
                additional_instructions TEXT, -- Novo: Caldas, etc.
                source TEXT,                  -- Novo: Fonte
                image_path TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
            );
            """,
            # 5. Ingredientes (Detalhe) - Atualizado com unidade
            """
            CREATE TABLE IF NOT EXISTS recipe_ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                quantity TEXT,
                unit TEXT,
                FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
            );
            """
        ]

        # Executa a criação das tabelas
        for q in queries:
            cursor.execute(q)

        # Seed: Garante usuário SYSTEM para receitas nativas
        cursor.execute("""
            INSERT OR IGNORE INTO users (full_name, email, hashed_password) 
            VALUES ('System Admin', 'system@app.local', '$2b$12$SYSTEMUSERHASHPLACEHOLDERDO_NOT_USE_REAL_PWD');
        """)

        conn.commit()
        logger.info("Banco de dados atualizado com suporte a Core de Receitas.")

    except sqlite3.Error as e:
        logger.critical(f"Erro Crítico no Banco de Dados: {e}", exc_info=True)
        raise DatabaseError("Falha na inicialização do esquema do banco de dados.", e)
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def get_db_connection():
    """Retorna uma conexão segura com Row Factory ativado."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row # Permite acessar colunas por nome
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Falha de conexão SQLite: {e}")
        raise DatabaseError("Não foi possível conectar ao banco de dados.", e)