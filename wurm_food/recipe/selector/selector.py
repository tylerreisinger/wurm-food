from abc import abstractmethod, ABC
from typing import List, Union

from wurm_food.knowledge import KnowledgeBase
from wurm_food.recipe.ingredient import RecipeIngredient


class Selector(ABC):
    """
    A class which returns a list of ingredients to be included in a recipe.
    """
    @abstractmethod
    def select(self, kb: KnowledgeBase) -> List[RecipeIngredient]:
        raise NotImplementedError()


class ExactIngredientSelector(Selector):
    """
    Select all of a fixed set of ingredients.
    :param ingredients: A list of all ingredients to select each time.
    :param repetitions: The number of times to duplicate each ingredient.

    ## Example

    `ExactIngredientSelector(RecipeIngredient.from_name_string("feta cheese", kb))`
    will always select feta cheese.
    """
    def __init__(self, *args: List[RecipeIngredient]):
        self._ingredients = args

    def select(self, kb: KnowledgeBase) -> List[RecipeIngredient]:
        values = []
        values.extend([ingredient.clone() for ingredient in self._ingredients])
        return values


class IngredientCategorySelector(Selector):
    def __init__(self, category: str):
        self._category = category

    def select(self, kb: KnowledgeBase) -> List[RecipeIngredient]:
        selected = []
        for ingredient in kb.ingredients().values():
            if self._category in ingredient.categories():
                selected.append(ingredient)

        return selected


class CombineSelector(Selector):
    def __init__(self, selectors: List[Selector]):
        self._selectors = selectors

    def select(self, kb: KnowledgeBase) -> List[RecipeIngredient]:
        ingredients = []
        for selector in self._selectors:
            ingredients.extend(selector.select(kb))
        return ingredients


