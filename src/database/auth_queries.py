# CÓDIGO COMPLETO E COMENTADO
"""
Camada de acesso a dados (Queries) exclusiva para autenticação e CRUD de usuários.
Usa bcrypt para hashing de senha seguro.
"""
import sqlite3
import bcrypt  # Usamos bcrypt para hashing seguro
import logging
from typing import Optional

from .database import get_db_connection
from src.models.user_model import User

logger = logging.getLogger(__name__)


def _hash_password(password: str) -> str:
    """
    Gera um hash seguro para uma senha usando bcrypt.
    O 'salt' é gerado automaticamente e armazenado dentro do hash.
    """
    try:
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_bytes = bcrypt.hashpw(password_bytes, salt)
        return hashed_bytes.decode('utf-8')
    except Exception as e:
        logger.error(f"Erro ao gerar hash bcrypt: {e}", exc_info=True)
        raise


def _verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se uma senha em texto plano corresponde a um hash bcrypt.
    """
    try:
        plain_password_bytes = plain_password.encode('utf-8')
        hashed_password_bytes = hashed_password.encode('utf-8')
        # bcrypt.checkpw faz a comparação segura
        return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)
    except (ValueError, TypeError) as e:
        logger.warning(
            f"Erro ao verificar senha (hash malformado ou inválido): {e}")
        return False


def register_user(full_name: str, email: str, password: str) -> Optional[User]:
    """
    Cria um novo usuário no banco de dados.
    Retorna o objeto User se for bem-sucedido, ou None se o email já existir.
    """
    logger.debug(f"Tentativa de registro para o email: {email}")
    password_hash = _hash_password(password)

    conn = get_db_connection()
    if not conn:
        logger.error("Não foi possível conectar ao DB para registrar usuário.")
        return None

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (full_name, email, hashed_password) VALUES (?, ?, ?)",
            (full_name, email, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid

        if user_id:
            logger.info(
                f"Usuário '{full_name}' (ID: {user_id}) registrado com sucesso.")
            return User(id=user_id, full_name=full_name, email=email)
        return None

    except sqlite3.IntegrityError:
        # Este erro ocorre se o email (UNIQUE) já existir
        logger.warning(f"Falha no registro: Email '{email}' já cadastrado.")
        return None
    except sqlite3.Error as e:
        logger.error(f"Erro SQLite ao registrar usuário: {e}", exc_info=True)
        return None
    finally:
        conn.close()


def get_user_by_email_and_password(email: str, password: str) -> Optional[User]:
    """
    Autentica um usuário.
    Retorna o objeto User se o email e a senha estiverem corretos, ou None caso contrário.
    """
    logger.debug(f"Tentativa de autenticação para o email: {email}")
    conn = get_db_connection()
    if not conn:
        logger.error(
            "Não foi possível conectar ao DB para autenticar usuário.")
        return None

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user_row = cursor.fetchone()  # Busca o usuário pelo email

        if not user_row:
            logger.warning(
                f"Falha no login: Usuário '{email}' não encontrado.")
            return None

        stored_hash = user_row['hashed_password']

        # Verifica a senha usando bcrypt
        if _verify_password(password, stored_hash):
            logger.info(f"Usuário '{email}' autenticado com sucesso.")
            # Sucesso! Retorna o objeto User (sem a senha)
            return User(
                id=user_row['id'],
                full_name=user_row['full_name'],
                email=user_row['email']
            )
        else:
            logger.warning(
                f"Falha no login: Senha incorreta para o usuário '{email}'.")
            return None

    except sqlite3.Error as e:
        logger.error(f"Erro SQLite ao logar: {e}", exc_info=True)
        return None
    finally:
        conn.close()
