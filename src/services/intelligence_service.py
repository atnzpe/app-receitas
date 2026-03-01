# ARQUIVO: src/services/intelligence_service.py
import re
import os
import sys
from typing import Optional, Dict, Any, List
from src.core.logger import get_logger
from src.services.scraper_service import RecipeScraper

logger = get_logger("src.services.intelligence")

# --- 1. BLINDAGEM DE DEPENDÊNCIAS ---
# Tenta importar as bibliotecas pesadas. Se falhar (ex: no Android), define flags como False.
HAS_PDF_SUPPORT = False
HAS_OCR_SUPPORT = False

try:
    import pdfplumber
    HAS_PDF_SUPPORT = True
except ImportError:
    logger.warning("Biblioteca 'pdfplumber' não encontrada. Leitura de PDF desativada.")

try:
    import pytesseract
    from PIL import Image
    HAS_OCR_SUPPORT = True

    # Configuração Dinâmica do Tesseract para Windows
    if os.name == 'nt':
        # Tenta caminhos comuns ou variáveis de ambiente
        possible_paths = [
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
            os.path.join(os.getenv('LOCALAPPDATA', ''), 'Tesseract-OCR', 'tesseract.exe')
        ]
        tess_found = False
        for path in possible_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                tess_found = True
                break

        if not tess_found:
            # Se não achar o binário, desativa o OCR para não crashar na execução
            logger.warning("Binário do Tesseract não encontrado no Windows.")
            HAS_OCR_SUPPORT = False

except ImportError:
    logger.warning("Bibliotecas de OCR (pytesseract/Pillow) não encontradas.")


class IntelligenceService:
    """
    Serviço de Inteligência Híbrido (Web + Arquivos).
    Projetado para rodar em qualquer plataforma (Cross-Platform Safe).
    """

    # --- WEB SCRAPING (Funciona em tudo que tem internet) ---
    @staticmethod
    def fetch_recipe_data(url: str) -> tuple[Optional[str], Optional[Dict[str, Any]]]:
        try:
            return RecipeScraper.fetch_recipe(url)
        except Exception as e:
            logger.error(f"Erro no fetch_recipe_data: {e}")
            return str(e), None

    # --- LEITURA DE PDF (Segura) ---
    @staticmethod
    def read_pdf(file_path: str) -> str:
        if not HAS_PDF_SUPPORT:
            return "ERRO: O suporte a PDF não está disponível neste dispositivo."

        logger.info(f"Lendo PDF: {file_path}")
        full_text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        full_text += text + "\n"
            return full_text
        except Exception as e:
            logger.error(f"Erro ao ler PDF: {e}")
            return "Não foi possível extrair texto deste PDF. Ele pode ser uma imagem escaneada."

    # --- OCR / IMAGEM (Segura) ---
    @staticmethod
    def read_image(file_path: str) -> str:
        """
        Tenta ler imagem. Se estiver no Android ou sem Tesseract,
        retorna aviso amigável em vez de crashar.
        """
        if not HAS_OCR_SUPPORT:
            # Mensagem técnica para o usuário entender por que falhou
            if os.name == 'nt':
                return "ERRO: Tesseract OCR não instalado no Windows."
            else:
                # No Android, pytesseract não funciona nativamente sem receitas complexas do Buildozer
                return "OCR Indisponível: Esta função requer processamento local não suportado neste dispositivo móvel."

        logger.info(f"Lendo Imagem (OCR): {file_path}")
        try:
            img = Image.open(file_path)
            text = pytesseract.image_to_string(img, lang='por')
            return text
        except Exception as e:
            logger.error(f"Erro no OCR: {e}")
            return "Erro ao processar imagem."

    # --- PARSER DE TEXTO (Puro Python - Roda em tudo) ---
    @staticmethod
    def parse_raw_text(text: str) -> Dict[str, Any]:
        """
        Analisa o texto bruto extraído e tenta estruturar.
        """
        # Se o texto for uma mensagem de erro das funções acima, retorna vazio
        if text.startswith("ERRO") or text.startswith("OCR Indisponível"):
            return {}

        try:
            logger.info("Iniciando análise heurística...")
            lines = [line.strip() for line in text.split('\n') if line.strip()]

            data = {
                "title": "", "ingredients": [], "instructions": "",
                "preparation_time": "", "servings": "",
                "source": "Arquivo Importado", "image_path": ""
            }

            if not lines:
                return data

            # Tenta achar título (primeira linha válida)
            data["title"] = lines[0].title()

            # Estratégia simples: procurar palavras-chave
            ing_start = -1
            instr_start = -1

            for i, line in enumerate(lines):
                l = line.lower()
                if "ingrediente" in l:
                    ing_start = i
                elif "preparo" in l or "instruções" in l:
                    instr_start = i

            # Se achou seções, corta o texto
            raw_ings = []
            raw_instr = []

            if ing_start != -1:
                end = instr_start if instr_start > ing_start else len(lines)
                raw_ings = lines[ing_start + 1: end]

            if instr_start != -1:
                raw_instr = lines[instr_start + 1:]

            # Processa Ingredientes com o Scraper Service (Reuso de código)
            for line in raw_ings:
                if len(line) > 3:
                    try:
                        data["ingredients"].append(
                            RecipeScraper._parse_ingredient(line))
                    except Exception as e:
                        logger.error(f"Erro ao parsear ingrediente '{line}': {e}")

            # Processa Instruções
            data["instructions"] = "\n".join(
                [re.sub(r'^[\d\-\.]+\s*', '', l) for l in raw_instr])

            return data

        except Exception as e:
            logger.error(f"Erro no parse_raw_text: {e}")
            return {}