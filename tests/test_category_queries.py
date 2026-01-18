# ARQUIVO: tests/test_category_queries.py
# CÓDIGO COMPLETO

from src.database import category_queries
from src.database.database import init_database, DB_PATH
import unittest
import os
import sys

# Ajusta path para encontrar o src
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


class TestCategoryQueries(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Ambiente limpo para teste
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        init_database()

    def test_01_seed_data(self):
        """Verifica se as categorias Michelin (Seed) foram criadas."""
        cats = category_queries.get_all_categories()
        self.assertGreater(
            len(cats), 0, "A lista não deveria estar vazia (Seed falhou).")
        names = [c.name for c in cats]
        self.assertIn("Prato Principal", names)
        self.assertIn("Sobremesas", names)

    def test_02_create_custom_category(self):
        """Testa criação de categoria do usuário."""
        cat = category_queries.add_category("Minha Receita de Vó")
        self.assertIsNotNone(cat)
        self.assertEqual(cat.name, "Minha Receita de Vó")

    def test_03_prevent_duplicates(self):
        """Testa blindagem contra duplicidade."""
        # Tenta criar uma que já existe no Seed
        cat = category_queries.add_category("Sobremesas")
        self.assertIsNone(cat, "Deveria retornar None para duplicata.")

    def test_04_update_category(self):
        """Testa atualização."""
        cat = category_queries.add_category("Teste Update")
        result = category_queries.update_category(cat.id, "Teste Atualizado")
        self.assertTrue(result)

        # Validação
        all_cats = category_queries.get_all_categories()
        updated = next((c for c in all_cats if c.id == cat.id), None)
        self.assertEqual(updated.name, "Teste Atualizado")

    def test_05_delete_category(self):
        """Testa exclusão."""
        cat = category_queries.add_category("Para Deletar")
        result = category_queries.delete_category(cat.id)
        self.assertTrue(result)

        all_cats = category_queries.get_all_categories()
        deleted = next((c for c in all_cats if c.id == cat.id), None)
        self.assertIsNone(deleted)


if __name__ == '__main__':
    unittest.main()
