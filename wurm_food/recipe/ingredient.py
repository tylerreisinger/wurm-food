import copy

from wurm_food.knowledge import Ingredient, Rarity, PreparationMethod, KnowledgeBase
from wurm_food.util import AffinityValue


class RecipeIngredient(object):
    def __init__(self, ingredient: Ingredient, rarity: Rarity, preparation_method: PreparationMethod):
        assert ingredient is not None and rarity is not None and preparation_method is not None
        self._ingredient = ingredient
        self._rarity = rarity
        self._preparation_method = preparation_method

    def __str__(self) -> str:
        string = ""
        if self._rarity.name() != Rarity.NORMAL_NAME:
            string += self._rarity.name() + " "
        if self._preparation_method.name() != PreparationMethod.NULL_NAME:
            string += self._preparation_method.name() + " "
        string += self._ingredient.name()
        return string.title()

    def __eq__(self, other: 'RecipeIngredient') -> bool:
        return self._ingredient == other._ingredient and self._preparation_method == other._preparation_method \
            and self._rarity == other._rarity

    def __ne__(self, other: 'RecipeIngredient') -> bool:
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self._rarity, self._preparation_method, self._ingredient))

    @classmethod
    def from_name_string(cls, name_str: str, kb: KnowledgeBase) -> 'RecipeIngredient':
        parts = name_str.lower().split(' ')
        rarity = None
        preparation_method = None
        ingredient = None

        if parts[0].lower() in kb.rarities():
            rarity = kb.rarities()[parts[0].lower()]
            parts = parts[1:]
        else:
            rarity = kb.rarities()['normal']

        inner_parts = parts[:len(parts)-1]
        for i in range(1, len(inner_parts)+1):
            name = ' '.join(inner_parts[:i])
            if name.lower() in kb.preparation_methods():
                preparation_method = kb.preparation_methods()[name.lower()]
                break

        if preparation_method is None:
            i = 0
            preparation_method = kb.preparation_methods()[PreparationMethod.NULL_NAME]

        end = parts[i:]
        end_name = ' '.join(end).lower()

        if end_name in kb.ingredients():
            ingredient = kb.ingredients()[end_name]
        else:
            raise ValueError("Ingredient '{}' not found from name string '{}'".format(end_name, name_str))

        return RecipeIngredient(ingredient, rarity, preparation_method)

    def value(self):
        return AffinityValue(self._ingredient.value() + self._rarity.value() + self._preparation_method.value()).value()

    def ingredient(self) -> Ingredient:
        return self._ingredient

    def rarity(self) -> Rarity:
        return self._rarity

    def preparation_method(self) -> PreparationMethod:
        return self._preparation_methodf

    def clone(self) -> 'RecipeIngredient':
        return copy.copy(self)
