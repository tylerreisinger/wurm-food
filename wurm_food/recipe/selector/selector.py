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

    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError()


class ExactIngredientSelector(Selector):
    """
    Select all of a fixed set of ingredients.
    :param ingredients: A list of all ingredients to select each time.
    :param repetitions: The number of times to duplicate each ingredient.

    ## Example

    `ExactIngredientSelector(RecipeIngredient.from_name_string("feta cheese", kb), repetitions=2)`
    will always select 2 feta cheese ingredients.
    """
    def __init__(self, ingredients: Union[RecipeIngredient, List[RecipeIngredient]], repetitions=1):
        if isinstance(ingredients, list):
            self._ingredients = ingredients
        else:
            self._ingredients = [ingredients]
        self._repetitions = repetitions

    def select(self, kb: KnowledgeBase) -> List[RecipeIngredient]:
        values = []
        for i in range(0, self._repetitions):
            values.extend([ingredient.clone() for ingredient in self._ingredients])
        return values

    def name(self) -> str:
        return 'ingredient'


class IngredientCategorySelector(Selector):
    def __init__(self, category: str):
        self._category = category

    def select(self, kb: KnowledgeBase) -> List[RecipeIngredient]:
        selected = []
        for ingredient in kb.ingredients().values():
            if self._category in ingredient.categories():
                selected.append(ingredient)

        return selected

    def name(self) -> str:
        return 'category'


class SelectorRegistry(object):
    def __init__(self):
        self._selectors = {}

    def register_selector(self, selector: Selector):
        name = selector.name()
        if name in self._selectors:
            raise KeyError("{} is already registered as a selector".format(name))

        self._selectors[name] = selector

    def get(self, name: str) -> Selector:
        if name not in self._selectors:
            raise KeyError('{} is not a valid selector'.format(name))
        return self._selectors[name]


SELECTOR_REGISTRY = SelectorRegistry()
SELECTOR_REGISTRY.register_selector(ExactIngredientSelector)
SELECTOR_REGISTRY.register_selector(IngredientCategorySelector)