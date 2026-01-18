import sqlite3
import bcrypt
from typing import Optional
from src.core.logger import get_logger
from src.core.exceptions import DatabaseError, AuthenticationError
from src.database.database import get_db_connection
from src.models.user_model import User

logger = get_logger("src.database.auth")


def _hash_password(password: str) -> str:
    try:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    except Exception as e:
        logger.error("Erro ao gerar hash da senha.", exc_info=True)
        raise AuthenticationError(
            "Erro interno de segurança ao processar senha.", e)


def _verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        logger.warning(f"Erro na verificação de hash: {e}")
        return False


def register_user(full_name: str, email: str, password: str) -> Optional[User]:
    try:
        # Validação Pydantic ocorre aqui implicitamente se instanciássemos o User,
        # mas como estamos inserindo raw data, validamos via banco (Constraints).
        password_hash = _hash_password(password)
        conn = get_db_connection()

        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (full_name, email, hashed_password) VALUES (?, ?, ?)",
            (full_name, email, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid

        conn.close()
        logger.info(f"Usuário registrado: {email}")
        return User(id=user_id, full_name=full_name, email=email)

    except sqlite3.IntegrityError:
        logger.warning(f"Tentativa de registro duplicado: {email}")
        return None  # Email já existe (tratado pelo ViewModel)
    except (sqlite3.Error, DatabaseError) as e:
        logger.error(f"Erro de BD no registro: {e}")
        raise DatabaseError("Erro ao salvar novo usuário.", e)


def get_user_by_email_and_password(email: str, password: str) -> Optional[User]:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            logger.warning(f"Login falhou: Usuário não encontrado ({email})")
            return None

        if _verify_password(password, row['hashed_password']):
            logger.info(f"Login sucesso: {email}")
            return User(id=row['id'], full_name=row['full_name'], email=row['email'])
        else:
            logger.warning(f"Login falhou: Senha incorreta ({email})")
            return None

    except sqlite3.Error as e:
        logger.error(f"Erro de BD no login: {e}")
        raise DatabaseError("Erro ao buscar credenciais.", e)
