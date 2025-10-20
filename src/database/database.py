# CÓDIGO COMPLETO E COMENTADO
import sqlite3
import os

# Define o caminho do banco de dados (offline-first)
DB_DIR = "data"
DB_NAME = "recipes.db"
DB_PATH = os.path.join(DB_DIR, DB_NAME)

def init_database():
    """
    Inicializa o banco de dados SQLite e cria as tabelas iniciais
    se elas ainda não existirem.
    
    Esta função deve ser chamada na inicialização do app (main.py).
    """
    # Garante que o diretório 'data' exista
    os.makedirs(DB_DIR, exist_ok=True)
    
    conn = None
    try:
        # Conecta (ou cria) o banco de dados
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        print(f"Banco de dados conectado em: {DB_PATH}")
        
        # --- CRIAÇÃO DAS TABELAS ---
        # Habilitar chaves estrangeiras
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        # Tabela de Categorias
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            hashed_password TEXT NOT NULL
        );
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
        """)
        
        # Tabela de Receitas (Recipe)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            instructions TEXT,
            prep_time_minutes INTEGER,
            source_url TEXT,
            image_path TEXT,
            category_id INTEGER,
            user_id INTEGER, -- (NOVA COLUNA) Vincula receita ao usuário
            FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE SET NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        );
        """)

        # Tabela de Ingredientes (Ingredient)
        # Relação N-para-1: Muitos ingredientes pertencem a UMA receita.
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
        print("Tabelas 'users', 'categories', 'recipes', e 'ingredients' verificadas/criadas.")
        
    except sqlite3.Error as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
    finally:
        if conn:
            conn.close()

def get_db_connection():
    """
    Retorna uma nova conexão com o banco de dados.
    Utiliza row_factory para facilitar o acesso aos dados por nome de coluna.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        if conn:
            conn.close()
        return None