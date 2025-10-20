"""
Camada de acesso a dados exclusiva para autenticação e CRUD de usuários.
(REFATORADO) Usa bcrypt para hashing de senha seguro.
"""
import sqlite3
import bcrypt # (ALTERADO) Importa bcrypt
from typing import Optional

from .database import get_db_connection
from src.models.user_model import User

# (REMOVIDO) O SALT agora é gerenciado pelo bcrypt dentro do próprio hash.
# SALT = b'your_very_secret_salt_here' 

def _hash_password(password: str) -> str:
    """
    (REFATORADO) Gera um hash seguro para uma senha usando bcrypt.
    O salt é gerado e incluído automaticamente no hash.
    
    :param password: A senha em texto plano.
    :return: A string do hash da senha.
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode('utf-8')

def _verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    (REFATORADO) Verifica se uma senha em texto plano corresponde a um hash bcrypt.

    :param plain_password: A senha fornecida pelo usuário.
    :param hashed_password: O hash armazenado no banco de dados.
    :return: True se a senha corresponder, False caso contrário.
    """
    try:
        plain_password_bytes = plain_password.encode('utf-8')
        hashed_password_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)
    except (ValueError, TypeError):
        # Ocorre se o hashed_password não for um hash bcrypt válido.
        print("Erro ao verificar senha: hash malformado ou inválido.")
        return False

def register_user(full_name: str, email: str, password: str) -> Optional[User]:
    """
    Cria um novo usuário no banco de dados.
    (ALTERADO) Agora usa _hash_password com bcrypt.
    """
    conn = get_db_connection()
    if not conn:
        return None
        
    password_hash = _hash_password(password)
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (full_name, email, hashed_password) VALUES (?, ?, ?)",
            (full_name, email, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        if user_id:
            return User(id=user_id, full_name=full_name, email=email)
        return None
        
    except sqlite3.IntegrityError:
        print(f"Erro: Email '{email}' já cadastrado.")
        return None
    except sqlite3.Error as e:
        print(f"Erro ao registrar usuário: {e}")
        return None
    finally:
        conn.close()

def get_user_by_email_and_password(email: str, password: str) -> Optional[User]:
    """
    Autentica um usuário.
    (ALTERADO) Agora usa _verify_password com bcrypt.
    """
    conn = get_db_connection()
    if not conn:
        return None
        
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user_row = cursor.fetchone()
        
        if not user_row:
            print("Usuário não encontrado.")
            return None
            
        stored_hash = user_row['hashed_password']
        
        if _verify_password(password, stored_hash):
            # Sucesso! Retorna o objeto User
            return User(
                id=user_row['id'],
                full_name=user_row['full_name'],
                email=user_row['email']
            )
        else:
            print("Senha incorreta.")
            return None
            
    except sqlite3.Error as e:
        print(f"Erro ao logar: {e}")
        return None
    finally:
        conn.close()