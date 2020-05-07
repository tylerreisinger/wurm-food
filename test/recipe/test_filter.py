from wurm_food.knowledge import KnowledgeBase
from wurm_food.recipe.ingredient import RecipeIngredient
from wurm_food.recipe.selector.filter import UniformSampleFilter, PrepareIngredientFilter
from wurm_food.recipe.selector.selector import ExactIngredientSelector, IngredientCategorySelector


class TestFilter(object):
    @classmethod
    def setup_class(cls):
        cls._kb = KnowledgeBase.load_from_json('../data/knowledge')

    def test_uniform_sample_filter(self):
        SELECTORS = [
            UniformSampleFilter(
                ExactIngredientSelector(RecipeIngredient.from_name_string('potato', self._kb)),
                num_samples=1
            ),
        ]
        EXPECTED = [
            RecipeIngredient.from_name_string('potato', self._kb)
        ]

        for selector, expected in zip(SELECTORS, EXPECTED):
            assert selector.select(self._kb) == [expected]

        selector = UniformSampleFilter(
            IngredientCategorySelector(
                'fruit'
            ),
            num_samples=5
        )

        ingredients = [ingredient for ingredient in self._kb.ingredients().values() if 'fruit' in ingredient.categories()]
        selected = selector.select(self._kb)

        for ingredient in selector.select(self._kb):
            assert ingredient in ingredients
        assert len(selected) == 5

    def test_prepare_ingredient_filter(self):
        SELECTORS = [
            PrepareIngredientFilter(
                ExactIngredientSelector(RecipeIngredient.from_name_string('carrot', self._kb)),
                self._kb.get_preparation_method('chopped')
            )
        ]
        EXPECTED = [
            [RecipeIngredient.from_name_string('chopped carrot', self._kb)]
        ]

        for selector, expected in zip(SELECTORS, EXPECTED):
            ingredients = selector.select(self._kb)
            assert ingredients == expected