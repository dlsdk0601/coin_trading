from enum import auto
from typing import TypeVar, Generic, Any, Type

from flask import request, Response, current_app

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


def res_jsonify(res: Res) -> Response:
    return current_app.response_class(res.model_dump_json(by_alias=True))

def ok(data: RES_DATA):
    return res_jsonify(
        Res(data=data, errors=[], validation_errors=[], status=ResStatus.OK)
    )


def err(*errors: str):
    return res_jsonify(
        Res(data=None, errors=list(errors), validation_errors=[], status=ResStatus.OK)
    )

def get_req(req_type: Type[BaseModel]):
    return req_type.model_validate(request.get_json(force=True))