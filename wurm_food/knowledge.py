"""
    knowledge.py

    Implements the base data models for the input reference data. This is static data originating from Wurm,
    not user data.
"""

from abc import abstractmethod, ABC
import json
import os
from typing import Dict, List, Type, TypeVar

T = TypeVar('T')


class ModelBase(ABC):
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def from_json(self, json_ob: Dict):
        raise NotImplementedError()

    @abstractmethod
    def to_json(self) -> str:
        raise NotImplementedError()

    def __str__(self) -> str:
        return self.name().title()


class NameValueModel(ModelBase):
    def __init__(self, name: str, value: int):
        self._name = name
        self._value = value

    def __eq__(self, other) -> bool:
        return self._name == other._name and self._value == other._value

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self._name, self._value))

    def name(self) -> str:
        return self._name

    def value(self) -> int:
        return self._value

    @classmethod
    def from_json(cls, json_obj: Dict):
        return cls(json_obj['name'], json_obj['value'])

    def to_json(self) -> str:
        return json.dumps({
            'name': self.name(),
            'value': self.value(),
        })


class Container(NameValueModel):
    """
    A model for a cooking container, eg a frying pan
    """
    def __init__(self, name, value):
        super().__init__(name, value)


class Cooker(NameValueModel):
    """
    A model for a cooker, eg an oven
    """
    def __init__(self, name, value):
        super().__init__(name, value)


class Category(ModelBase):
    """
    A model for the display categories for a UI.
    :param name: The category display and key name
    :param id: The display id, defining the order they should be displayed
    """
    def __init__(self, name: str, id: int):
        self._name = name
        self._id = id

    def name(self) -> str:
        return self._name

    def id(self) -> int:
        return self._id

    def to_json(self) -> str:
        return json.dumps({
            'name': self._name,
            'id': self._value,
        })

    @classmethod
    def from_json(cls, json_obj: Dict):
        return cls(json_obj['name'], json_obj['id'])


class Ingredient(ModelBase):
    MAX_INGREDIENT_ID = 138
    """
    Represents an base ingredient in a recipe, without considering preparedness such as "chopped".
    """

    def __init__(self, name: str, id: int, group_id: int, combine_id: int, categories: List[str]):
        self._name = name
        self._id = id
        self._group_id = group_id
        self._combine_id = combine_id
        self._categories = categories

    def __eq__(self, other) -> bool:
        return self._name == other._name and self._combine_id == other._combine_id

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self._name, self._combine_id))

    def name(self) -> str:
        return self._name

    def id(self) -> int:
        return self._id

    def group_id(self) -> int:
        return self._group_id

    def combine_id(self) -> int:
        return self._combine_id

    def categories(self) -> List[str]:
        return self._categories

    @classmethod
    def from_json(cls, json_obj: Dict):
        return cls(
            json_obj['name'],
            json_obj['id'],
            json_obj['group_id'],
            json_obj['comb_id'],
            json_obj['category'],
        )

    def to_json(self) -> str:
        return json.dumps({
            'name': self._name,
            'id': self._id,
            'group_id': self._group_id,
            'comb_id': self._combine_id,
            'category': self._categories,
        })


class PreparationMethod(NameValueModel):
    NULL_NAME = 'whole'
    def __init__(self, name: str, value: int):
        super().__init__(name, value)


class Rarity(NameValueModel):
    NORMAL_NAME = "normal"
    RARE_NAME = "rare"
    SUPREME_NAME = "supreme"
    FANTASTIC_NAME = "fantastic"

    def __init__(self, name: str, value: int):
        super().__init__(name, value)


class SkillAffinity(NameValueModel):
    def __init__(self, name: str, value: int):
        super().__init__(name, value)


class KnowledgeBase(object):
    def __init__(self):
        self._containers = {}
        self._cookers = {}
        self._categories = {}
        self._ingredients = {}
        self._preparation_methods = {}
        self._rarities = {}
        self._skill_affinities = {}

    @classmethod
    def load_from_json(cls,
                       base_dir: str,
                       container_file='container.json',
                       cooker_file='cooker.json',
                       category_file='category.json',
                       ingredient_file='ingredient.json',
                       preparation_file='preparation.json',
                       rarity_file='rarity.json',
                       skill_affinity_file='skill.json'):
        knowledge_base = KnowledgeBase()

        cls._load_to_dict(knowledge_base._containers, Container, os.path.join(base_dir, container_file), 'containers')
        cls._load_to_dict(knowledge_base._cookers, Cooker, os.path.join(base_dir, cooker_file), 'cookers')
        cls._load_to_dict(knowledge_base._categories, Category, os.path.join(base_dir, category_file), 'categories')
        cls._load_to_dict(knowledge_base._ingredients, Ingredient, os.path.join(base_dir, ingredient_file), 'ingredients')
        cls._load_to_dict(knowledge_base._preparation_methods, PreparationMethod,
                          os.path.join(base_dir, preparation_file), 'preparations')
        cls._load_to_dict(knowledge_base._rarities, Rarity, os.path.join(base_dir, rarity_file), 'rarities')
        cls._load_to_dict(knowledge_base._skill_affinities, SkillAffinity,
                          os.path.join(base_dir, skill_affinity_file), 'skills')

        return knowledge_base

    def containers(self) -> Dict[str, Container]:
        return self._containers

    def cookers(self) -> Dict[str, Cooker]:
        return self._cookers

    def categories(self) -> Dict[str, Category]:
        return self._categories

    def ingredients(self) -> Dict[str, Ingredient]:
        return self._ingredients

    def preparation_methods(self) -> Dict[str, PreparationMethod]:
        return self._preparation_methods

    def rarities(self) -> Dict[str, Rarity]:
        return self._rarities

    def skill_affinities(self) -> Dict[str, SkillAffinity]:
        return self._skill_affinities

    def get_container(self, name: str) -> Container:
        return self._containers[name]

    def get_cooker(self, name: str) -> Cooker:
        return self._cookers[name]

    def get_category(self, name: str) -> Category:
        return self._categories[name]

    def get_ingredient(self, name: str) -> Ingredient:
        return self._ingredients[name]

    def get_preparation_method(self, name: str) -> PreparationMethod:
        return self._preparation_methods[name]

    def get_rarity(self, name: str) -> Rarity:
        return self._rarities[name]

    def get_skill_affinity(self, name: str) -> SkillAffinity:
        return self._skill_affinities[name]

    @classmethod
    def _load_to_dict(cls, dict: Dict, builder_type: Type, container_filename: str, collection_key: str) -> Dict[str, T]:
        with open(container_filename, 'r') as fp:
            obj = json.load(fp)
            for k, v in obj[collection_key].items():
                dict[k] = builder_type.from_json(v)
