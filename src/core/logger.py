import logging
import os
import sys
from datetime import datetime

# Garante que a pasta de logs exista
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Nome do arquivo de log rotacionado por dia
log_filename = datetime.now().strftime(f"{LOG_DIR}/app_%Y-%m-%d.log")


def get_logger(name: str) -> logging.Logger:
    """
    Retorna um logger configurado com precisão cirúrgica.
    Logs são escritos no arquivo (persistência) E no console (dev).
    """
    logger = logging.getLogger(name)

    # Evita duplicar handlers se a função for chamada várias vezes para o mesmo nome
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.DEBUG)  # Em produção, pode-se mudar para INFO

    # Formato: [HORA] [NIVEL] [MODULO:LINHA] - MENSAGEM
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s',
        datefmt='%H:%M:%S'
    )

    # 1. Handler de Arquivo (Persistência completa)
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 2. Handler de Console (Feedback imediato)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
