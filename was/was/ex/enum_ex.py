from enum import unique, Enum
from typing import TYPE_CHECKING, TypeVar, Callable

if TYPE_CHECKING:
    from mypy.typeshed.stdlib.typing_extensions import Self

T = TypeVar('T')
U = TypeVar('U')

def enum_from_value(cons: Callable[[U], T], value: U) -> T | None:
    try:
        return cons(value)
    except ValueError:
        return None


@unique
class StringEnum(str, Enum):
    # noinspection PyMethodParameters
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __str__(self):
        return self.value