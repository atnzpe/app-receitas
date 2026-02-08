# ARQUIVO: src/database/auth_queries.py
import sqlite3
import bcrypt
from typing import Optional
from src.core.logger import get_logger
from src.core.exceptions import DatabaseError, AuthenticationError
from src.database.database import get_db_connection
from src.models.user_model import User

logger = get_logger("src.database.auth")

def _hash_password(password: str) -> str:
    logger.debug("Iniciando hash da senha.")
    try:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        return hashed
    except Exception as e:
        logger.error(f"Erro hash senha: {e}")
        raise AuthenticationError("Erro de segurança.", e)

def _verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))
    except Exception as e:
        logger.warning(f"Erro verificação hash: {e}")
        return False

def register_user(full_name: str, email: str, password: str) -> Optional[User]:
    logger.info(f"Registro iniciado: {email}")
    conn = None
    try:
        pwd_hash = _hash_password(password)
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO users (full_name, email, hashed_password) VALUES (?, ?, ?)",
            (full_name, email, pwd_hash)
        )
        conn.commit()
        
        user_id = cursor.lastrowid
        logger.info(f"Usuário registrado com sucesso ID: {user_id}")
        return User(id=user_id, full_name=full_name, email=email)

    except sqlite3.IntegrityError:
        logger.warning(f"Tentativa de registro duplicado: {email}")
        return None # Retorna None para o ViewModel tratar
    except sqlite3.Error as e:
        logger.error(f"Erro BD Registro: {e}")
        raise DatabaseError("Erro ao salvar usuário.", e)
    finally:
        if conn: conn.close()

def get_user_by_email_and_password(email: str, password: str) -> Optional[User]:
    logger.info(f"Login iniciado: {email}")
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()

        if not row:
            logger.warning(f"Login falhou: Usuário não encontrado ({email})")
            return None

        if _verify_password(password, row['hashed_password']):
            logger.info(f"Login sucesso: {email}")
            return User(id=row['id'], full_name=row['full_name'], email=row['email'])
        else:
            logger.warning(f"Login falhou: Senha incorreta ({email})")
            return None
    except Exception as e:
        logger.error(f"Erro Login: {e}")
        return None
    finally:
        if conn: conn.close()