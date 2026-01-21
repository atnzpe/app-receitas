from src.models.recipe import RecipeCreate, IngredientSchema
from src.database.recipe_queries import RecipeQueries
from src.database.database import get_db_connection
import src.database.database as db_module
import unittest
import os
import sys
import uuid
from datetime import datetime

# Ajusta path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


class TestRecipeQueries(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Configura banco de teste isolado."""
        random_id = str(uuid.uuid4())[:8]
        cls.TEST_DB_NAME = f"recipes_test_{random_id}.db"
        cls.original_db = db_module.DB_NAME

        # Patch do banco
        db_module.DB_NAME = cls.TEST_DB_NAME
        db_module.DB_PATH = os.path.join(db_module.DB_DIR, cls.TEST_DB_NAME)

        if not os.path.exists(db_module.DB_DIR):
            os.makedirs(db_module.DB_DIR)

        # Garante limpeza inicial
        if os.path.exists(db_module.DB_PATH):
            try:
                os.remove(db_module.DB_PATH)
            except:
                pass

        db_module.init_database()

        # Cria um usuário de teste
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO users (full_name, email, hashed_password) VALUES ('Chef Teste', 'chef@test.com', 'hash')")
        cls.user_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.commit()
        conn.close()

        cls.db = RecipeQueries()

    @classmethod
    def tearDownClass(cls):
        db_module.DB_NAME = cls.original_db
        db_module.DB_PATH = os.path.join(db_module.DB_DIR, cls.original_db)
        try:
            target = os.path.join(db_module.DB_DIR, cls.TEST_DB_NAME)
            if os.path.exists(target):
                os.remove(target)
        except:
            pass

    def test_create_full_recipe(self):
        """Testa a criação de uma receita completa com ingredientes."""

        # 1. Prepara os dados (DTO)
        ingredientes = [
            IngredientSchema(name="Farinha de Trigo",
                             quantity="500", unit="g"),
            IngredientSchema(name="Ovos", quantity="3", unit="unid"),
            IngredientSchema(name="Leite", quantity="200", unit="ml")
        ]

        recipe_data = RecipeCreate(
            title="Bolo de Teste",
            preparation_time=45,
            servings="8 fatias",
            instructions="Misture tudo e asse.",
            ingredients=ingredientes
        )

        # 2. Executa a criação
        success = self.db.create_recipe(recipe_data, self.user_id)
        self.assertTrue(success, "A criação da receita falhou.")

        # 3. Verifica no Banco (Validação Cruzada)
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verifica Receita
        cursor.execute("SELECT * FROM recipes WHERE title = ?",
                       ("Bolo de Teste",))
        recipe_row = cursor.fetchone()
        self.assertIsNotNone(recipe_row)
        recipe_id = recipe_row['id']

        # Verifica Ingredientes
        cursor.execute(
            "SELECT count(*) FROM recipe_ingredients WHERE recipe_id = ?", (recipe_id,))
        count = cursor.fetchone()[0]
        self.assertEqual(count, 3, "Deveria ter salvo 3 ingredientes.")

        conn.close()


if __name__ == '__main__':
    unittest.main()
