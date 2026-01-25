import unittest
from unittest.mock import MagicMock
from src.viewmodels.recipe_list_viewmodel import RecipeListViewModel

class TestRecipeListVM(unittest.TestCase):
    def test_initial_state(self):
        page_mock = MagicMock()
        vm = RecipeListViewModel(page_mock)
        self.assertEqual(vm.get_recipes_count(), 0)

if __name__ == "__main__":
    unittest.main()