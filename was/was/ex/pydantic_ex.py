import pydantic
from stringcase import camelcase


class BaseModel(pydantic.BaseModel):
    class Config:
        alias_generator = camelcase
        populate_by_name = True
        arbitrary_types_allowed = True
        by_alias = True


class GenericModel(pydantic.BaseModel):
    class Config:
        alias_generator = camelcase
        populate_by_name = True
        arbitrary_types_allowed = True
        by_alias = True
