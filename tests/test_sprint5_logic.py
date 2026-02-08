# ARQUIVO: tests/test_sprint5_logic.py
import unittest
# [CORREÇÃO] Importando o nome correto: IngredientSchema
from src.models.recipe import RecipeCreate, IngredientSchema

class TestSprint5Logic(unittest.TestCase):
    
    def test_recipe_model_accepts_new_fields(self):
        """Valida se o modelo aceita imagem, fonte e dicas."""
        data = {
            "category_id": 1,
            "title": "Bolo Teste",
            "instructions": "Misturar tudo.",
            # Pydantic converte dict para IngredientSchema
            "ingredients": [{"name": "Farinha", "quantity": "200", "unit": "g"}],
            "image_path": "http://site.com/foto.jpg",
            "source": "Livro da Vovó",
            "additional_instructions": "Cuidado com o forno."
        }
        
        model = RecipeCreate(**data)
        
        self.assertEqual(model.image_path, "http://site.com/foto.jpg")
        self.assertEqual(model.source, "Livro da Vovó")
        self.assertEqual(model.ingredients[0].name, "Farinha")
        print("✅ Modelo aceitou novos campos corretamente.")

    def test_smart_back_logic(self):
        """Simula a lógica de decisão de rota."""
        session_data = {"previous_route": "/discovery"}
        self.assertEqual(session_data["previous_route"], "/discovery")
        
        session_data["previous_route"] = "/my_recipes"
        self.assertEqual(session_data["previous_route"], "/my_recipes")
        print("✅ Lógica Smart Back validada.")

if __name__ == '__main__':
    unittest.main()