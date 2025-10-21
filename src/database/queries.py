# CÓDIGO COMPLETO E COMENTADO
"""
Este arquivo centralizará todas as interações SQL com o banco de dados
que NÃO sejam de autenticação (Receitas, Categorias, Ingredientes).

Seguindo a arquitetura, o ViewModel (ex: CategoryViewModel) chamará funções
deste arquivo para buscar ou modificar dados.
"""

from .database import get_db_connection
import sqlite3
import logging

logger = logging.getLogger(__name__)

# Este arquivo está pronto para receber as funções da Sprint 3.
# Exemplo de como uma função será (não executar ainda):
#
# from src.models.recipe_model import Category
#
# def get_all_categories() -> list[Category]:
#     logger.debug("Buscando todas as categorias do banco de dados...")
#     conn = get_db_connection()
#     if not conn:
#         return []
#     try:
#         cursor = conn.cursor()
#         cursor.execute("SELECT id, name FROM categories ORDER BY name")
#         rows = cursor.fetchall()
#         return [Category(id=row['id'], name=row['name']) for row in rows]
#     except sqlite3.Error as e:
#         logger.error(f"Erro ao buscar categorias: {e}", exc_info=True)
#         return []
#     finally:
#         conn.close()