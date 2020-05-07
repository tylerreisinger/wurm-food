from typing import List

from wurm_food.knowledge import Cooker, Container
from wurm_food.recipe.ingredient import RecipeIngredient


class Recipe(object):
    def __init__(self, cooker: Cooker, container: Container, ingredients: List[RecipeIngredient]):
        self._cooker = cooker
        self._container = container
        self._ingredients = ingredients

    def cooker(self) -> Cooker:
        return self._cooker

    def container(self) -> Container:
        return self._container

    def ingredients(self) -> List[RecipeIngredient]:
        return self._ingredients

    def add_ingredient(self, ingredient: RecipeIngredient):
        self._ingredients.append(ingredient)

    def __len__(self):
        return len(self._ingredients)

    def __iter__(self):
        return iter(self._ingredients)

    def __str__(self):
        template = \
"""
Cooked in a(n) {cooker} {container}:
{ingredients}
"""
        container = ''
        if self._container.name() != 'none':
            container = 'using a(n) ' + str(self._container)
        else:
            container = 'directly'

        ing_strs = []
        for ingredient in self._ingredients:
            ing_strs.append(str(ingredient))

        return template.format(self._cooker, self._container, '\n\t'.join(ing_strs))
