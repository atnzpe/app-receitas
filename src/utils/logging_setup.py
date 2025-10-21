# CÓDIGO COMPLETO E COMENTADO
# Este arquivo é baseado no utils.py que você forneceu
import logging
import os
import flet as ft
# A importação de numpy foi mantida como no arquivo original
import numpy as np 

def setup_logging(page: ft.Page):
    """
    Configura o sistema de logging de forma adaptativa (Web vs. Desktop).
    Baseado no arquivo utils.py fornecido.

    Args:
        page (ft.Page): A página Flet principal, usada para verificar o ambiente.
    """
    if page.web:
        # Se for web (PWA), envia logs para o console do navegador.
        log_format = "%(asctime)s - PWA - %(levelname)s - %(message)s"
        logging.basicConfig(
            level=logging.INFO, # Nível INFO é suficiente para produção PWA.
            format=log_format,
            handlers=[
                logging.StreamHandler(),
            ],
        )
        logging.info("Logging configurado para ambiente WEB (PWA).")
    else:
        # Se for desktop, cria um arquivo de log local.
        log_dir = "logs"
        log_file = os.path.join(log_dir, "app.log")

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_format = "%(asctime)s - DESKTOP - %(levelname)-8s - [%(filename)s:%(lineno)d] - %(message)s"
        
        # Limpa handlers antigos para evitar duplicação de logs.
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        logging.basicConfig(
            level=logging.DEBUG, # Nível DEBUG é útil para desenvolvimento desktop.
            format=log_format,
            handlers=[
                logging.FileHandler(log_file, mode="w", encoding="utf-8"),
                logging.StreamHandler(),
            ],
        )
        logging.info(f"Logging configurado para ambiente DESKTOP. Arquivo em: {log_file}")


def get_logger(name: str):
    """
    Retorna uma instância de logger com o nome especificado.
    """
    return logging.getLogger(name)