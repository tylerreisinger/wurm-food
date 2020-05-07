from test.recipe.test_base import TestBase
from wurm_food.knowledge import KnowledgeBase
from wurm_food.recipe.ingredient import RecipeIngredient
from wurm_food.recipe.selector.selector import ExactIngredientSelector, IngredientCategorySelector


class TestSelector(TestBase):
    def test_exact_ingredient_selector(self):
        selector = ExactIngredientSelector(RecipeIngredient.from_name_string('feta cheese', self._kb), repetitions=2)

        expected_results = [
            RecipeIngredient.from_name_string('feta cheese', self._kb),
            RecipeIngredient.from_name_string('feta cheese', self._kb),
        ]

        assert selector.select(self._kb) == expected_results

    def test_category_selector(self):
        category = 'meat'
        ingredients = [ingredient for ingredient in self._kb.ingredients().values() if category in ingredient.categories()]
        selector = IngredientCategorySelector(category)

        assert selector.select(self._kb) == ingredients