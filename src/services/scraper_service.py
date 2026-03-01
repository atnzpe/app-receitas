# ARQUIVO: src/services/scraper_service.py
import requests
import json
import re
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any, List
from src.core.logger import get_logger

logger = get_logger("src.services.scraper")

class RecipeScraper:
    """
    NORMALIZADOR UNIVERSAL DE RECEITAS (Versão Heurística)
    Usa recursividade para encontrar texto humano em meio a metadados.
    """

    @staticmethod
    def fetch_recipe(url: str) -> tuple[Optional[str], Optional[Dict[str, Any]]]:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'https://www.google.com/'
        }

        try:
            if not url.startswith("http"):
                return "URL inválida.", None

            logger.info(f"--- EXTRAINDO: {url} ---")
            
            session = requests.Session()
            response = session.get(url, headers=headers, timeout=20)
            response.encoding = 'utf-8' 
            
            if response.status_code == 403:
                return "Site bloqueou o acesso (Proteção Anti-Bot).", None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            scripts = soup.find_all('script', type='application/ld+json')
            target_data = None

            for script in scripts:
                if not script.string: continue
                try:
                    data = json.loads(script.string)
                    if isinstance(data, dict): data = [data]
                    target_data = RecipeScraper._find_recipe_object(data)
                    if target_data: break
                except: continue

            if not target_data:
                return "Receita não encontrada.", None

            return None, RecipeScraper._normalize_for_database(target_data, url)

        except Exception as e:
            logger.error(f"Erro Scraper: {e}")
            return f"Erro técnico: {str(e)}", None

    @staticmethod
    def _find_recipe_object(data: Any) -> Optional[Dict]:
        """Busca recursiva pelo objeto Recipe."""
        if isinstance(data, dict):
            t = str(data.get('@type', ''))
            if 'Recipe' in t: return data
            if '@graph' in data: return RecipeScraper._find_recipe_object(data['@graph'])
            return None
        elif isinstance(data, list):
            for item in data:
                res = RecipeScraper._find_recipe_object(item)
                if res: return res
        return None

    @staticmethod
    def _extract_image_url(img_data: Any) -> str:
        """Extrai URL de qualquer estrutura."""
        if not img_data: return ""
        if isinstance(img_data, str): return img_data.strip()
        if isinstance(img_data, list) and img_data: return RecipeScraper._extract_image_url(img_data[0])
        if isinstance(img_data, dict): return img_data.get('url', '')
        return ""

    @staticmethod
    def _smart_text_extractor(data: Any, captured_texts: List[str]):
        """
        [INTELIGÊNCIA] Algoritmo Recursivo que ignora chaves de máquina (@type, HowToStep)
        e captura apenas texto humano relevante.
        """
        if isinstance(data, str):
            # Filtra lixo curto ou chaves conhecidas
            clean = data.strip()
            if len(clean) > 2 and not clean.startswith("@") and clean not in ["HowToStep", "HowToSection"]:
                # Remove HTML residual
                clean = re.sub('<[^<]+?>', '', clean)
                captured_texts.append(clean)
        
        elif isinstance(data, list):
            for item in data:
                RecipeScraper._smart_text_extractor(item, captured_texts)
        
        elif isinstance(data, dict):
            # Se for uma Seção, tenta pegar o nome para dar contexto
            if 'name' in data and 'itemListElement' in data:
                captured_texts.append(f"\n--- {data['name'].upper()} ---")

            # Prioriza chaves que contêm texto humano
            for key in ['text', 'name', 'itemListElement', 'description']:
                if key in data:
                    RecipeScraper._smart_text_extractor(data[key], captured_texts)

    @staticmethod
    def _extract_instructions(inst_data: Any) -> str:
        """Usa o extrator inteligente para limpar as instruções."""
        if not inst_data: return ""
        
        texts = []
        RecipeScraper._smart_text_extractor(inst_data, texts)
        
        # Remove duplicatas consecutivas (comum em alguns JSONs)
        final_lines = []
        last_line = ""
        for line in texts:
            if line != last_line:
                if line.startswith("---"): # Formatação de seção
                    final_lines.append(line)
                else:
                    final_lines.append(f"- {line}")
                last_line = line
                
        return "\n".join(final_lines)

    @staticmethod
    def _parse_ingredient(text: str) -> Dict[str, str]:
        text = text.replace('&nbsp;', ' ').strip()
        match = re.match(r'^([\d\.,/]+)\s*([a-zA-Zçãõ\(\)]+)?\s*(?:de )?(.*)$', text, re.IGNORECASE)
        
        if match:
            qty = match.group(1) or ""
            unit = match.group(2) or ""
            name = match.group(3) or ""
            if not name and unit:
                name = unit
                unit = ""
            return {"name": name.strip(), "quantity": qty.strip(), "unit": unit.strip()}
        
        return {"name": text, "quantity": "", "unit": ""}

    @staticmethod
    def _normalize_for_database(data: Dict, url: str) -> Dict[str, Any]:
        try:
            # Tempo (Padrão 0)
            prep_time = 0
            time_str = data.get('totalTime') or data.get('prepTime') or data.get('cookTime')
            if time_str:
                match = re.search(r'(?:(\d+)H)?(?:(\d+)M)?', time_str)
                if match:
                    h = int(match.group(1) or 0)
                    m = int(match.group(2) or 0)
                    prep_time = (h * 60) + m

            img_url = RecipeScraper._extract_image_url(data.get('image'))
            # [INTELIGÊNCIA APLICADA AQUI]
            instructions = RecipeScraper._extract_instructions(data.get('recipeInstructions'))

            ingredients = []
            for ing in data.get('recipeIngredient', []):
                ingredients.append(RecipeScraper._parse_ingredient(ing))

            author = data.get('author')
            author_name = "Web"
            if isinstance(author, dict): author_name = author.get('name', 'Web')
            elif isinstance(author, list) and author: 
                author_name = author[0].get('name', 'Web') if isinstance(author[0], dict) else str(author[0])

            return {
                "title": data.get('name', 'Receita Importada').strip(),
                "preparation_time": str(prep_time), 
                "servings": str(data.get('recipeYield', '')).replace('servings', '').strip(),
                "instructions": instructions,
                "image_path": img_url,
                "source": url,
                "additional_instructions": f"Autor: {author_name}",
                "ingredients": ingredients
            }

        except Exception as e:
            logger.error(f"Erro na normalização: {e}")
            return {}