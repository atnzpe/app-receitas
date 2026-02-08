# ARQUIVO: src/services/scraper_service.py
import requests
import json
import re
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any
from src.core.logger import get_logger

logger = get_logger("src.services.scraper")


class RecipeScraper:
    """
    Serviço de inteligência para extração de dados estruturados (Schema.org/Recipe).
    Focado em robustez: lê o JSON-LD que os sites entregam para o Google.
    """

    @staticmethod
    def fetch_recipe(url: str) -> tuple[Optional[str], Optional[Dict[str, Any]]]:
        """
        Retorna: (Mensagem de Erro, Dicionário de Dados)
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        try:
            if not url.startswith("http"):
                return "URL inválida. Comece com http:// ou https://", None

            logger.info(f"Iniciando scraping tático de: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Estratégia Principal: Buscar JSON-LD (Padrão Ouro)
            scripts = soup.find_all('script', type='application/ld+json')
            target_data = None

            for script in scripts:
                try:
                    if not script.string:
                        continue
                    data = json.loads(script.string)

                    # Normaliza para lista para processar igual
                    if isinstance(data, dict):
                        data = [data]

                    # Busca recursiva por @type: Recipe
                    target_data = RecipeScraper._find_recipe_in_json(data)
                    if target_data:
                        break
                except:
                    continue

            if not target_data:
                return "Não foi possível extrair dados estruturados deste site.", None

            return None, RecipeScraper._parse_schema(target_data, url)

        except Exception as e:
            logger.error(f"Erro ao importar receita: {e}")
            return f"Erro de conexão: {str(e)}", None

    @staticmethod
    def _find_recipe_in_json(data: Any) -> Optional[Dict]:
        """Busca profunda pelo objeto Recipe dentro do JSON-LD (pode estar aninhado ou em grafo)."""
        if isinstance(data, dict):
            if 'Recipe' in data.get('@type', ''):
                return data
            if '@graph' in data:
                return RecipeScraper._find_recipe_in_json(data['@graph'])
            return None
        elif isinstance(data, list):
            for item in data:
                res = RecipeScraper._find_recipe_in_json(item)
                if res:
                    return res
        return None

    @staticmethod
    def _parse_schema(data: Dict, url: str) -> Dict[str, Any]:
        """Normaliza os dados brutos do site para o formato do App."""
        try:
            # 1. Tempo (ISO 8601 PT40M -> 40)
            prep_time = 0
            # Tenta pegar totalTime, se não, soma prep + cook
            time_iso = data.get('totalTime') or data.get(
                'prepTime') or data.get('cookTime')
            if time_iso:
                # Regex simples para extrair minutos totais
                regex = re.compile(r'PT(?:(\d+)H)?(?:(\d+)M)?')
                match = regex.match(time_iso)
                if match:
                    h = int(match.group(1) or 0)
                    m = int(match.group(2) or 0)
                    prep_time = (h * 60) + m

            # 2. Imagem
            image = ""
            img_data = data.get('image')
            if isinstance(img_data, list):
                image = img_data[0] if img_data else ""
            elif isinstance(img_data, dict):
                image = img_data.get('url', '')
            elif isinstance(img_data, str):
                image = img_data

            # 3. Ingredientes
            ingredients = []
            raw_ings = data.get('recipeIngredient', [])
            for ing_str in raw_ings:
                # Limpeza básica
                clean_str = ing_str.replace('&nbsp;', ' ').strip()
                ingredients.append({
                    "name": clean_str,  # O parser complexo de qtd/unidade ficaria para a v2
                    "quantity": "",
                    "unit": ""
                })

            # 4. Instruções
            instructions = []
            raw_inst = data.get('recipeInstructions', [])
            if isinstance(raw_inst, str):
                instructions.append(raw_inst)
            elif isinstance(raw_inst, list):
                for step in raw_inst:
                    if isinstance(step, dict):
                        instructions.append(step.get('text', ''))
                    elif isinstance(step, str):
                        instructions.append(step)

            return {
                "title": data.get('name', 'Receita Importada').strip(),
                "preparation_time": str(prep_time) if prep_time else "",
                "servings": str(data.get('recipeYield', '')).replace('servings', '').replace('porções', '').strip(),
                "instructions": "\n".join(instructions),
                "image_path": image,
                "source": url,
                "additional_instructions": f"Autor: {data.get('author', {}).get('name', 'Desconhecido')}",
                "ingredients": ingredients
            }

        except Exception as e:
            logger.error(f"Erro no parsing dos dados: {e}")
            return {}
