from typing import List

from wurm_food.knowledge import Cooker, Container, KnowledgeBase
from wurm_food.recipe.recipe import Recipe
from wurm_food.recipe.selector.selector import Selector, SELECTOR_REGISTRY


class RecipeBuilder(object):
    def __init__(self, cooker: Cooker, container: Container, kb: KnowledgeBase, selectors: List[Selector] = []):
        self._cooker = cooker
        self._container = container
        self._selectors = selectors
        self._kb = kb

    def build_random_recipe(self) -> Recipe:
        ingredients = []
        for selector in self._selectors:
            selected = selector.select(self._kb)
            ingredients.extend(selected)

        return Recipe(
            cooker=self._cooker,
            container=self._container,
            ingredients=ingredients,
        )

    def select(self, name: str, *args, **kwargs) -> Selector:
        selector_cls = SELECTOR_REGISTRY.get(name)
        selector = selector_cls(*args, **kwargs)
        self._selectors.append(selector)

        return selector


class RecipeBuildState(object):
    def __init__(self, recipe: Recipe):
        self._ingredient_count = 0
        self._recipe = None

    def ingredient_count(self):
        return self._ingredient_count
