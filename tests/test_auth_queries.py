# CÓDIGO ALTERADO E COMENTADO
import unittest
import os
import sqlite3

# Ajusta o path para que 'src' seja encontrado
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.database import init_database
from src.database import auth_queries
from src.database.database import DB_PATH, DB_DIR

class TestAuthQueries(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Configura o ambiente de teste. Roda uma vez."""
        os.makedirs(DB_DIR, exist_ok=True)
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        
        init_database()
        print("Banco de dados de teste inicializado para AuthQueries.")

    def test_01_hash_and_verify_password(self):
        """(ALTERADO) Testa se o hashing e a verificação com bcrypt funcionam."""
        print("Executando: test_01_hash_and_verify_password")
        password = "MinhaSenha@123"
        hashed = auth_queries._hash_password(password)
        
        self.assertIsInstance(hashed, str)
        self.assertTrue(hashed.startswith('$2b$')) # Verifica se é um hash bcrypt
        
        # Teste de verificação (sucesso)
        self.assertTrue(auth_queries._verify_password(password, hashed))
        
        # Teste de verificação (falha)
        self.assertFalse(auth_queries._verify_password("SenhaErrada", hashed))

    def test_02_register_user_success(self):
        """Testa o registro de um novo usuário com sucesso."""
        print("Executando: test_02_register_user_success")
        user = auth_queries.register_user(
            full_name="Usuário Bcrypt",
            email="bcrypt@email.com",
            password="senha123"
        )
        self.assertIsNotNone(user)
        self.assertEqual(user.full_name, "Usuário Bcrypt")
        self.assertEqual(user.email, "bcrypt@email.com")
        self.assertIsNotNone(user.id)

    def test_03_register_user_fail_duplicate_email(self):
        """Testa a falha ao registrar um email duplicado."""
        print("Executando: test_03_register_user_fail_duplicate_email")
        # Tenta registrar o mesmo email novamente
        user = auth_queries.register_user(
            full_name="Outro Usuário",
            email="bcrypt@email.com", # Email duplicado
            password="outrasenha"
        )
        self.assertIsNone(user, "Deveria retornar None para email duplicado.")

    def test_04_get_user_login_success(self):
        """Testa o login (get_user) com credenciais corretas."""
        print("Executando: test_04_get_user_login_success")
        # (Usuário 'bcrypt@email.com' foi criado no test_02)
        user = auth_queries.get_user_by_email_and_password(
            email="bcrypt@email.com",
            password="senha123"
        )
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "bcrypt@email.com")

    def test_05_get_user_login_fail_wrong_password(self):
        """Testa o login com senha incorreta."""
        print("Executando: test_05_get_user_login_fail_wrong_password")
        user = auth_queries.get_user_by_email_and_password(
            email="bcrypt@email.com",
            password="senha_errada"
        )
        self.assertIsNone(user)

    def test_06_get_user_login_fail_no_user(self):
        """Testa o login com um email que não existe."""
        print("Executando: test_06_get_user_login_fail_no_user")
        user = auth_queries.get_user_by_email_and_password(
            email="naoexiste@email.com",
            password="senha123"
        )
        self.assertIsNone(user)

if __name__ == '__main__':
    unittest.main()