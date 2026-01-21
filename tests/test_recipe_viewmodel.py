import unittest
from src.viewmodels.recipe_viewmodel import RecipeViewModel

class TestRecipeViewModel(unittest.TestCase):
    def test_add_temp_ingredient_validation(self):
        """Testa se o ViewModel rejeita ingredientes inválidos antes de chegar na UI"""
        vm = RecipeViewModel()
        
        # Teste 1: Nome vazio (Deve falhar)
        error = vm.add_temp_ingredient("", "1", "kg")
        self.assertIsNotNone(error) # Espera erro
        
        # Teste 2: Nome curto (Deve falhar se a regra for >2)
        error = vm.add_temp_ingredient("A", "1", "kg")
        self.assertIsNotNone(error)
        
        # Teste 3: Válido
        error = vm.add_temp_ingredient("Arroz", "1", "kg")
        self.assertIsNone(error) # Não deve retornar erro
        self.assertEqual(len(vm.temp_ingredients), 1)

if __name__ == "__main__":
    unittest.main()