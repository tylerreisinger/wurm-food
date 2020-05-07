from abc import ABC
import random
from typing import List, Union

from wurm_food.knowledge import KnowledgeBase, PreparationMethod
from wurm_food.recipe.ingredient import RecipeIngredient
from wurm_food.recipe.selector.selector import Selector


class Filter(Selector, ABC):
    def __init__(self, child: Selector):
        self._child = child

    def child(self) -> List[Selector]:
        return self._child

    def get_child_ingredients(self, kb: KnowledgeBase) -> List[RecipeIngredient]:
        return [ingred for ingred in self._child.select(kb)]


class UniformSampleFilter(Filter):
    def __init__(self, child: Selector, num_samples: int = 1, allow_duplicates: bool = False):
        super().__init__(child)
        self._num_samples = num_samples
        self._allow_duplicates = allow_duplicates

    def select(self, kb: KnowledgeBase) -> List[RecipeIngredient]:
        child_ingredients = self.get_child_ingredients(kb)
        out_ingredients = []

        if self._allow_duplicates:
            out_ingredients = random.choices(child_ingredients, self._num_samples)
        else:
            out_ingredients = random.sample(child_ingredients, self._num_samples)

        return out_ingredients


class DedupFilter(Filter):
    def __init__(self, child: Selector):
        super().__init__(child)

    def select(self, kb: KnowledgeBase) -> List[RecipeIngredient]:
        unique_ingredients = set({})

        ingredients = self.get_child_ingredients(kb)
        for ingredient in ingredients:
            unique_ingredients.add(ingredient)

        return list(unique_ingredients)


class PrepareIngredientFilter(Filter):
    def __init__(self, child: Selector, preparation_methods: Union[PreparationMethod, List[PreparationMethod]]):
        super().__init__(child)
        if isinstance(preparation_methods, list):
            self._preparation_methods = preparation_methods
        else:
            self._preparation_methods = [preparation_methods]

    def select(self, kb: KnowledgeBase) -> List[RecipeIngredient]:
        out_ingredients = []
        child_ingredients = self.get_child_ingredients(kb)

        for ingredient in child_ingredients:
            prep_method = random.choice(self._preparation_methods)
            new_ingredient = RecipeIngredient(
                ingredient.ingredient(),
                ingredient.rarity(),
                prep_method,
            )
            out_ingredients.append(new_ingredient)

        return out_ingredients


class FilterRegistry(object):
    def __init__(self):
        self._filters = {}

    def register_filter(self, name: str, filter: Filter):
        if name in self._filters:
            raise KeyError("{} is already registered as a filter".format(name))

        self._filters[name] = filter

FILTER_REGISTRY = FilterRegistry()
FILTER_REGISTRY.register_filter('uniform_sample', UniformSampleFilter)
FILTER_REGISTRY.register_filter('prepare', PrepareIngredientFilter)
FILTER_REGISTRY.register_filter('dedup', DedupFilter)