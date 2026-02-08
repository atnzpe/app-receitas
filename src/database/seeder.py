# ARQUIVO: src/database/seeder.py
import sqlite3
import json
import os
from src.core.logger import get_logger
from src.database.database import DB_PATH

logger = get_logger("src.database.seeder")

# Banco de Imagens Fictícias (URLs Estáveis do Unsplash)
# Usamos URLs diretos para garantir que funcionem sempre
IMAGE_MAP = {
    "bolo": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=600&q=80",
    "chocolate": "https://images.unsplash.com/photo-1606313564200-e75d5e30476d?auto=format&fit=crop&w=600&q=80",
    "pudim": "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?auto=format&fit=crop&w=600&q=80",
    "torta": "https://images.unsplash.com/photo-1574885014184-a4f59c82c61e?auto=format&fit=crop&w=600&q=80",
    "frango": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?auto=format&fit=crop&w=600&q=80",
    "carne": "https://images.unsplash.com/photo-1603048297172-c92544798d5e?auto=format&fit=crop&w=600&q=80",
    "peixe": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=600&q=80",
    "salada": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=600&q=80",
    "sopa": "https://images.unsplash.com/photo-1547592166-23acbe3a624b?auto=format&fit=crop&w=600&q=80",
    "pão": "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=600&q=80",
    "massa": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?auto=format&fit=crop&w=600&q=80",
    "arroz": "https://images.unsplash.com/photo-1536304993881-ff6e9eefa2a6?auto=format&fit=crop&w=600&q=80",
    "default": "https://images.unsplash.com/photo-1495521821758-ee18ece60918?auto=format&fit=crop&w=600&q=80" # Cozinha genérica
}

def _get_image_for_title(title: str) -> str:
    """Retorna uma imagem baseada em palavras-chave no título."""
    title_lower = title.lower()
    for key, url in IMAGE_MAP.items():
        if key in title_lower:
            return url
    return IMAGE_MAP["default"]

def seed_native_recipes():
    """
    Popula o banco de dados com receitas nativas a partir de um JSON.
    Injeta imagens automaticamente se não existirem.
    """
    json_path = os.path.join("src", "assets", "native_recipes.json")
    
    if not os.path.exists(json_path):
        logger.warning(f"Arquivo de seed não encontrado: {json_path}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Verifica se já existem receitas do sistema (user_id = 1 é o Admin/Sistema)
        cursor.execute("SELECT COUNT(*) FROM recipes WHERE user_id = 1")
        count = cursor.fetchone()[0]
        
        if count > 0:
            logger.info("SEEDER: Banco de dados já populado. Pulando seed.")
            return

        logger.info("SEEDER: Iniciando população de receitas nativas...")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            recipes = json.load(f)

        # Garante que o usuário Admin (ID 1) existe
        cursor.execute("INSERT OR IGNORE INTO users (id, full_name, email, hashed_password) VALUES (1, 'Admin', 'admin@system.local', 'system_hash')")

        for r in recipes:
            # 1. Resolve Categoria
            cursor.execute("SELECT id FROM categories WHERE name = ? AND user_id IS NULL", (r['category'],))
            cat_row = cursor.fetchone()
            if cat_row:
                cat_id = cat_row[0]
            else:
                cursor.execute("INSERT INTO categories (name, user_id, icon) VALUES (?, NULL, 'restaurant')", (r['category'],))
                cat_id = cursor.lastrowid

            # 2. Define Imagem (Se não tiver no JSON, usa a lógica automática)
            image_url = r.get('image_path')
            if not image_url:
                image_url = _get_image_for_title(r['title'])

            # 3. Insere Receita
            cursor.execute("""
                INSERT INTO recipes (user_id, category_id, title, preparation_time, servings, instructions, image_path)
                VALUES (1, ?, ?, ?, ?, ?, ?)
            """, (
                cat_id, 
                r['title'], 
                r.get('preparation_time'), 
                r.get('servings'), 
                r.get('instructions'),
                image_url # <--- Imagem Injetada
            ))
            
            recipe_id = cursor.lastrowid

            # 4. Insere Ingredientes
            for ing in r.get('ingredients', []):
                cursor.execute("""
                    INSERT INTO recipe_ingredients (recipe_id, name, quantity, unit)
                    VALUES (?, ?, ?, ?)
                """, (recipe_id, ing['name'], ing.get('quantity'), ing.get('unit')))

        conn.commit()
        logger.info(f"SEEDER: Sucesso! {len(recipes)} receitas nativas importadas com imagens.")

    except Exception as e:
        conn.rollback()
        logger.error(f"SEEDER: Falha crítica ao popular banco: {e}")
    finally:
        conn.close()