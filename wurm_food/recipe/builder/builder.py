from typing import List

from wurm_food.knowledge import Cooker, Container, KnowledgeBase
from wurm_food.recipe.recipe import Recipe
from wurm_food.recipe.selector.filter import FILTER_REGISTRY
from wurm_food.recipe.selector.selector import Selector, SELECTOR_REGISTRY


class SelectorBuilder(object):
    def __init__(self, selector: Selector):
        self._selector = selector

    def build(self) -> Selector:
        return self._selector

    def filter(self, name: str, *args, **kwargs) -> 'SelectorBuilder':
        filter_cls = FILTER_REGISTRY.get(name)
        filter = filter_cls(child=self._selector, *args, **kwargs)
        self._selector = filter
        return self


class RecipeBuilder(object):
    def __init__(self, cooker: Cooker, container: Container, kb: KnowledgeBase):
        self._cooker = cooker
        self._container = container
        self._selectors = []
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

    def select(self, name: str, *args, **kwargs) -> SelectorBuilder:
        selector_cls = SELECTOR_REGISTRY.get(name)
        selector = selector_cls(*args, **kwargs)
        builder = SelectorBuilder(selector)
        self._selectors.append(builder)

        return builder


class RecipeBuildState(object):
    def __init__(self, recipe: Recipe):
        self._ingredient_count = 0
        self._recipe = None

    def ingredient_count(self):
        return self._ingredient_count
