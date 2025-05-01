from enum import auto
from typing import TypeVar, Generic, Any

from was.ex.enum_ex import StringEnum
from was.ex.pydantic_ex import BaseModel

RES_DATA = TypeVar('RES_DATA', bound=BaseModel)


class ResStatus(StringEnum):
    OK = auto()
    INVALID_ACCESS_TOKEN = auto()
    NO_PERMISSION = auto()
    NOT_FOUND = auto()
    LOGIN_REQUIRED = auto()


class Res(BaseModel, Generic[RES_DATA]):
    data: RES_DATA | None
    errors: list[str]
    validation_errors: list[dict[str, Any]]
    status: ResStatus


def ok(data: RES_DATA) -> Res[RES_DATA]:
    return Res(data=data, errors=[], validation_errors=[], status=ResStatus.OK)


def err(*errors: str) -> Res[RES_DATA]:
    return Res(errors=list(errors), validation_errors=[], status=ResStatus.OK)
