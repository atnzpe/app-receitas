# ARQUIVO: src/services/intelligence_service.py
import requests
import json
import re
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any
from src.core.logger import get_logger

logger = get_logger("src.services.intelligence")

# --- IMPORTAÇÕES DEFENSIVAS (Foco em Android) ---
# Em Android/Mobile, bibliotecas como Tesseract ou SpeechRecognition podem falhar
# na instalação ou execução por falta de binários do sistema.
# O try/except garante que o app ABRA mesmo sem elas.

HAS_OCR = False
try:
    import pytesseract
    from PIL import Image
    HAS_OCR = True
except ImportError:
    logger.warning("OCR indisponível: pytesseract ou Pillow não instalados.")

HAS_VOICE = False
try:
    import speech_recognition as sr
    HAS_VOICE = True
except ImportError:
    logger.warning("Voz indisponível: SpeechRecognition não instalado.")


class IntelligenceService:
    """
    Serviço central de Automação.
    Blinda o app contra falhas de dependência em ambiente Mobile.
    """

    # --- 1. WEB SCRAPING (Funciona em qualquer lugar com Internet) ---
    @staticmethod
    def fetch_recipe_data(url: str) -> tuple[Optional[str], Optional[Dict[str, Any]]]:
        if not url.startswith("http"):
            return "URL inválida. Inclua http:// ou https://", None

        headers = {'User-Agent': 'Mozilla/5.0 (Android 10; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0'}

        try:
            logger.info(f"Baixando URL: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            scripts = soup.find_all('script', type='application/ld+json')
            target_data = None

            # Busca JSON-LD (Schema.org)
            for script in scripts:
                if not script.string: continue
                try:
                    data = json.loads(script.string)
                    target_data = IntelligenceService._find_recipe_type(data)
                    if target_data: break
                except: continue

            if not target_data:
                return "Site não compatível (sem dados Schema.org/Recipe).", None

            return None, IntelligenceService._normalize_schema(target_data, url)

        except Exception as e:
            logger.error(f"Erro Scraping: {e}")
            return f"Erro de conexão: {str(e)}", None

    @staticmethod
    def _find_recipe_type(data: Any) -> Optional[Dict]:
        """Busca recursiva por @type: Recipe."""
        if isinstance(data, dict):
            if 'Recipe' in data.get('@type', ''): return data
            if '@graph' in data: return IntelligenceService._find_recipe_type(data['@graph'])
        elif isinstance(data, list):
            for item in data:
                res = IntelligenceService._find_recipe_type(item)
                if res: return res
        return None

    @staticmethod
    def _normalize_schema(data: Dict, url: str) -> Dict:
        """Limpa os dados brutos."""
        # Tempo
        prep_time = 0
        time_iso = data.get('totalTime') or data.get('prepTime') or data.get('cookTime')
        if time_iso:
            regex = re.compile(r'PT(?:(\d+)H)?(?:(\d+)M)?')
            match = regex.match(time_iso)
            if match:
                h, m = int(match.group(1) or 0), int(match.group(2) or 0)
                prep_time = (h * 60) + m

        # Ingredientes
        ingredients = []
        for ing in data.get('recipeIngredient', []):
            ingredients.append({"name": ing.strip(), "quantity": "", "unit": ""})

        # Instruções
        instr = []
        raw_inst = data.get('recipeInstructions', [])
        if isinstance(raw_inst, list):
            for step in raw_inst:
                if isinstance(step, dict): instr.append(step.get('text', ''))
                elif isinstance(step, str): instr.append(step)
        elif isinstance(raw_inst, str): instr.append(raw_inst)

        # Imagem
        img = data.get('image', '')
        if isinstance(img, dict): img = img.get('url', '')
        elif isinstance(img, list): img = img[0] if img else ''

        return {
            "title": data.get('name', 'Receita Importada'),
            "preparation_time": str(prep_time) if prep_time else "",
            "servings": str(data.get('recipeYield', '')).replace("servings", "").strip(),
            "instructions": "\n".join(instr),
            "ingredients": ingredients,
            "image_path": img,
            "source": url,
            "additional_instructions": f"Autor: {data.get('author', {}).get('name', 'Web')}"
        }

    # --- 2. OCR (Defensivo) ---
    @staticmethod
    def extract_text_from_image(image_path: str) -> str:
        if not HAS_OCR:
            return "ERRO: Biblioteca OCR indisponível neste dispositivo."
        try:
            return pytesseract.image_to_string(Image.open(image_path), lang='por').strip()
        except Exception as e:
            return f"Erro na leitura: {str(e)}"

    # --- 3. VOZ (Defensivo) ---
    @staticmethod
    def listen_dictation() -> str:
        if not HAS_VOICE:
            return "ERRO: Reconhecimento de voz indisponível."
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
            return r.recognize_google(audio, language='pt-BR')
        except Exception as e:
            return "" # Retorno vazio indica falha silenciosa ou cancelamento