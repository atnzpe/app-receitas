# CÓDIGO COMPLETO E BLINDADO
from src.database import category_queries
from src.database.database import get_db_connection
import src.database.database as db_module
import unittest
import os
import sys
import uuid  # Garante unicidade do banco

# Ajusta path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


class TestCategoryQueries(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Configura um banco de teste ÚNICO por execução (Isolamento Total)."""
        # Gera um sufixo aleatório (ex: recipes_test_a1b2c3d4.db)
        random_id = str(uuid.uuid4())[:8]
        cls.TEST_DB_NAME = f"recipes_test_{random_id}.db"
        cls.original_db = db_module.DB_NAME

        # Patch: Aponta para o arquivo temporário exclusivo
        db_module.DB_NAME = cls.TEST_DB_NAME
        db_module.DB_PATH = os.path.join(db_module.DB_DIR, cls.TEST_DB_NAME)

        # Garante diretório
        if not os.path.exists(db_module.DB_DIR):
            os.makedirs(db_module.DB_DIR)

        db_module.init_database()
        cls.user_id = 1

    @classmethod
    def tearDownClass(cls):
        """Limpeza do arquivo temporário."""
        # Restaura configuração original
        db_module.DB_NAME = cls.original_db
        db_module.DB_PATH = os.path.join(db_module.DB_DIR, cls.original_db)

        # Tenta deletar o arquivo de teste criado
        try:
            target_file = os.path.join(db_module.DB_DIR, cls.TEST_DB_NAME)
            if os.path.exists(target_file):
                # Fecha conexões pendentes antes de deletar (força bruta)
                import gc
                gc.collect()
                os.remove(target_file)
        except Exception as e:
            print(
                f"Aviso: Não foi possível deletar o banco de teste {cls.TEST_DB_NAME}: {e}")

    def setUp(self):
        """Limpa dados via SQL antes de CADA teste."""
        conn = get_db_connection()
        try:
            conn.execute("DELETE FROM categories")
            conn.execute("DELETE FROM sqlite_sequence WHERE name='categories'")
            conn.commit()
        finally:
            conn.close()

        category_queries.init_default_categories()

    def test_01_defaults(self):
        cats = category_queries.get_user_categories(self.user_id)
        nativas = [c for c in cats if c.is_native]
        self.assertGreater(len(nativas), 0)

    def test_02_create_user_category(self):
        cat_name = "Minha Categoria Única"
        cat = category_queries.add_category(cat_name, self.user_id)

        self.assertIsNotNone(cat, "Erro: Retornou None. Banco sujo detectado.")
        self.assertEqual(cat.name, cat_name)
        self.assertEqual(cat.user_id, self.user_id)
        self.assertFalse(cat.is_native)

    def test_03_prevent_duplicates(self):
        cat_name = "Categoria Duplicada"
        category_queries.add_category(cat_name, self.user_id)
        cat_dup = category_queries.add_category(cat_name, self.user_id)
        self.assertIsNone(cat_dup)

    def test_04_security_update(self):
        cats = category_queries.get_user_categories(self.user_id)
        nativa = next(c for c in cats if c.is_native)
        result = category_queries.update_category(
            nativa.id, "Hacker", self.user_id)
        self.assertFalse(result)

    def test_05_security_delete(self):
        cats = category_queries.get_user_categories(self.user_id)
        nativa = next(c for c in cats if c.is_native)
        result = category_queries.delete_category(nativa.id, self.user_id)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
