from __future__ import annotations
from functools import total_ordering, singledispatchmethod
from typing import TypeVar, Union, Callable

from wurm_food.knowledge import Ingredient


@total_ordering
class AffinityValue(object):
    def __init__(self, value, modulo=Ingredient.MAX_INGREDIENT_ID):
        self._modulo = modulo
        if type(value) == 'int':
            self._value = abs(value % self._modulo)
        elif type(value) == AffinityValue:
            self._value = value.value()
        else:
            raise TypeError("AffinityValue.__init__ dose not accept a {} for value".format(type(value)))

    def __str__(self):
        return str(self.value())

    def __eq__(self, other: Union[AffinityValue, int]):
        if isinstance(other, AffinityValue):
            return self.value() == other.value()
        elif isinstance(other, int):
            return self.value() == other
        else:
            raise TypeError("AffinityValue can only compare to an int or an AffinityValue")

    def __lt__(self, other):
        if isinstance(other, AffinityValue):
            return self.value() < other.value()
        elif isinstance(other, int):
            return self.value() < other
        else:
            raise TypeError("AffinityValue can only compare to an int or an AffinityValue")

    def __add__(self, other: Union[AffinityValue, int]) -> AffinityValue:
        return self._perform_operation_on_value(other, lambda x, y: x+y)

    def __sub__(self, other: Union[AffinityValue, int]) -> AffinityValue:
        return self._perform_operation_on_value(other, lambda x, y: x-y)

    def __mul__(self, other: int) -> AffinityValue:
        return self._perform_operation_on_value(other, lambda x, y: x*y)

    def __radd__(self, other: Union[AffinityValue, int]) -> AffinityValue:
        return self.__add__(other)

    def __rsub__(self, other: Union[AffinityValue, int]) -> AffinityValue:
        return -self.__sub__(other)

    def __rmul__(self, other: int) -> AffinityValue:
        return self.__mul__(other)

    def __iadd__(self, other: Union[AffinityValue, int]) -> AffinityValue:
        self._value = self.__add__(other).value()

    def __isub__(self, other: Union[AffinityValue, int]) -> AffinityValue:
        self._value = self.__sub__(other).value()

    def __imul__(self, other: int) -> AffinityValue:
        self._value = self.__mul__(other).value()

    def value(self) -> int:
        return self._value

    def _perform_operation_on_value(self, value: Union[AffinityValue, int], fn: Callable[[int, int], int]) -> AffinityValue:
        if isinstance(value, AffinityValue):
            return AffinityValue(fn(self.value(), value.value()))
        elif isinstance(value, int):
            return AffinityValue(fn(self.value(), value))
        else:
            raise TypeError("Operation only accepts objects of type AffinityValue or int")