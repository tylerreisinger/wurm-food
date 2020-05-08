from test.recipe.test_base import TestBase
from wurm_food.recipe.builder.builder import RecipeBuilder
from wurm_food.recipe.ingredient import RecipeIngredient


class TestBuilder(TestBase):
    def test_select_builder(self):
        builder = RecipeBuilder(
            self._kb.get_cooker('oven'),
            self._kb.get_container('pottery bowl'),
            self._kb,
        )

        selector = builder.select('ingredient', 'corn').build()

        assert selector.select(self._kb) == [RecipeIngredient.from_name_string('corn', self._kb)]