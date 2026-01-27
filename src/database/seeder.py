# ARQUIVO: src/database/seeder.py
import json
import os
from src.core.logger import get_logger
from src.database.database import get_db_connection

logger = get_logger("src.database.seeder")

# Caminho relativo para o arquivo JSON
NATIVE_RECIPES_PATH = os.path.join("src", "assets", "native_recipes.json")


def seed_native_recipes(user_id: int = 1):
    """
    Lê o arquivo JSON de receitas nativas e popula o banco de dados.
    """
    if not os.path.exists(NATIVE_RECIPES_PATH):
        logger.warning(
            f"Arquivo de seed não encontrado: {NATIVE_RECIPES_PATH}")
        return

    try:
        # Lê o JSON com encoding utf-8 para suportar acentos
        with open(NATIVE_RECIPES_PATH, 'r', encoding='utf-8') as f:
            recipes_data = json.load(f)

        conn = get_db_connection()
        cursor = conn.cursor()

        # 1. Carrega categorias existentes para evitar duplicatas
        cursor.execute("SELECT id, name FROM categories")
        existing_cats = {row['name'].lower(): row['id']
                         for row in cursor.fetchall()}

        count_new = 0

        for r_data in recipes_data:
            # 2. Verifica se a receita já existe (pelo título e usuário)
            cursor.execute(
                "SELECT 1 FROM recipes WHERE title = ? AND user_id = ?", (r_data['title'], user_id))
            if cursor.fetchone():
                continue  # Pula se já existe

            # 3. Resolve a Categoria (Cria se não existir)
            cat_name = r_data.get('category', 'Outros')
            cat_id = existing_cats.get(cat_name.lower())

            if not cat_id:
                # Cria nova categoria dinamicamente (ex: 'Fitness', 'Vegano')
                cursor.execute(
                    "INSERT INTO categories (name, icon) VALUES (?, ?)", (cat_name, "restaurant_menu"))
                cat_id = cursor.lastrowid
                # Atualiza o mapa local
                existing_cats[cat_name.lower()] = cat_id
                logger.info(f"Nova categoria criada: {cat_name}")

            # 4. Insere a Receita
            cursor.execute("""
                INSERT INTO recipes (
                    user_id, category_id, title, preparation_time, servings, 
                    instructions, additional_instructions, source
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id, cat_id, r_data['title'], r_data['preparation_time'],
                r_data['servings'], r_data['instructions'],
                r_data.get('additional_instructions'), r_data['source']
            ))

            recipe_id = cursor.lastrowid

            # 5. Insere os Ingredientes
            ingredients_raw = r_data.get('ingredients', [])
            if ingredients_raw:
                ing_tuples = [(recipe_id, i['name'], i['quantity'], i['unit'])
                              for i in ingredients_raw]
                cursor.executemany("""
                    INSERT INTO recipe_ingredients (recipe_id, name, quantity, unit)
                    VALUES (?, ?, ?, ?)
                """, ing_tuples)

            count_new += 1

        conn.commit()
        conn.close()

        if count_new > 0:
            logger.info(
                f"SEEDER: {count_new} receitas nativas importadas com sucesso! 🚀")
        else:
            logger.info("SEEDER: Banco de dados já está atualizado.")

    except Exception as e:
        logger.error(f"Falha no Seeder de Receitas: {e}", exc_info=True)
