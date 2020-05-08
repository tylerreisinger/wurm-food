from abc import ABC, abstractmethod
from typing import Any, List, NamedTuple, Union, Dict, Optional

from wurm_food.knowledge import KnowledgeBase
from wurm_food.recipe.ingredient import RecipeIngredient
from wurm_food.recipe.selector.filter import UniformSampleFilter, PrepareIngredientFilter, DedupFilter
from wurm_food.recipe.selector.selector import IngredientCategorySelector, ExactIngredientSelector, CombineSelector, \
    Selector


class RegistryArg(ABC):
    @abstractmethod
    def parse_arg(self, arg: Any, kb: KnowledgeBase) -> Any:
        raise NotImplementedError()


class SelectorRegistryArgDescriptor(object):
    def __init__(self, arg_parsers: Dict[Union[int, str], 'RecipeIngredientArg'] = {}, num_args: Optional[int] = None,
                 allow_missing: bool = True, variadic_parser: Optional[RegistryArg] = None):
        self._positional_args = {}
        self._named_args = {}
        self._num_args = num_args
        self._allow_missing = allow_missing
        if arg_parsers and '..' in arg_parsers:
            self._variadic_parser = arg_parsers['..']
        else:
            self._variadic_parser = variadic_parser

        if arg_parsers:
            for key, value in arg_parsers.items():
                if isinstance(key, int):
                    self._positional_args[key] = value
                else:
                    self._named_args[key] = value

    def parse_args(self, kb: KnowledgeBase, *args, **kwargs) -> (List[Any], Dict[str, Any]):
        out_args = [arg for arg in args]
        out_kw_args = dict(kwargs)

        if self._num_args and self._num_args != len(args) and self._variadic_parser is None:
            raise ValueError('Got {} args but expected {}'.format(len(args), self._num_args))

        for idx, arg in enumerate(args):
            if idx in self._positional_args:
                out_args[idx] = self._positional_args[idx].parse_arg(arg, kb)
            elif self._variadic_parser:
                out_args[idx] = self._variadic_parser.parse_arg(arg, kb)
            elif not self._allow_missing:
                raise KeyError('Argument #{} is not specified and is required'.format(idx))

        for name, arg in kwargs:
            if name in self._positional_args:
                out_kw_args[name] = self._named_args[name].parse_arg(arg, kb)
            elif not self._allow_missing:
                raise KeyError('Argument \'{}\' is not specified and is required'.format(name))

        return out_args, out_kw_args

    def num_args(self):
        return self._num_args

    def positional_args(self):
        return self._positional_args

    def named_args(self):
        return self._named_args


class SelectorRegistryEntry(NamedTuple):
    cls: Selector
    args: SelectorRegistryArgDescriptor


class SelectorRegistry(object):
    def __init__(self):
        self._selectors = {}
        self._selector_to_name = {}

    def register_selector(self, name: str, selector_cls: type,
                          reg_args: Optional[Dict[Union[int, str], RegistryArg]] = None, *args: Any, **kwargs: Any):
        if name in self._selectors:
            raise KeyError("{} is already registered as a selector".format(name))

        self._selectors[name] = SelectorRegistryEntry(cls=selector_cls, args=SelectorRegistryArgDescriptor(reg_args, *args, **kwargs))
        self._selector_to_name[selector_cls] = name

    def get(self, name: str) -> SelectorRegistryEntry:
        if name not in self._selectors:
            raise KeyError('{} is not a valid selector'.format(name))
        return self._selectors[name]


class FilterRegistry(SelectorRegistry):
    def register_filter(self, name: str, selector_cls: type, args: SelectorRegistryArgDescriptor = None):
        self.register_selector(name, selector_cls, args)


class RecipeIngredientArg(RegistryArg):
    def parse_arg(self, name: str, kb: KnowledgeBase) -> RecipeIngredient:
        return RecipeIngredient.from_name_string(name, kb)


class LiteralArg(RegistryArg):
    def parse_arg(self, arg: Any, kb: KnowledgeBase) -> Any:
        return arg


SELECTOR_REGISTRY: SelectorRegistry = SelectorRegistry()
SELECTOR_REGISTRY.register_selector('ingredient', ExactIngredientSelector, {
    '..': RecipeIngredientArg(),
}, allow_missing=False)
SELECTOR_REGISTRY.register_selector('category', IngredientCategorySelector)
SELECTOR_REGISTRY.register_selector('combine', CombineSelector)

FILTER_REGISTRY: FilterRegistry = FilterRegistry()
FILTER_REGISTRY.register_filter('uniform_sample', UniformSampleFilter)
FILTER_REGISTRY.register_filter('prepare', PrepareIngredientFilter)
FILTER_REGISTRY.register_filter('dedup', DedupFilter)