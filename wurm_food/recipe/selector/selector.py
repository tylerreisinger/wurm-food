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


class SelectorRegistry(object):
    def __init__(self):
        self._selectors = {}
        self._selector_to_name = {}

    def register_selector(self, name: str, selector: Selector):
        if name in self._selectors:
            raise KeyError("{} is already registered as a selector".format(name))

        self._selectors[name] = selector
        self._selector_to_name[selector] = name

    def get(self, name: str) -> Selector:
        if name not in self._selectors:
            raise KeyError('{} is not a valid selector'.format(name))
        return self._selectors[name]


SELECTOR_REGISTRY = SelectorRegistry()
SELECTOR_REGISTRY.register_selector('ingredient', ExactIngredientSelector)
SELECTOR_REGISTRY.register_selector('category', IngredientCategorySelector)
SELECTOR_REGISTRY.register_selector('combine', CombineSelector)