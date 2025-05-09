from flask import Blueprint

from was.ex.api import ok, get_req, err
from was.ex.pydantic_ex import BaseModel
from was.model import db
from was.model.config import Config

config = Blueprint('config', __name__)


class ConfigListReq(BaseModel):
    pass


class ConfigListResItem(BaseModel):
    pk: int
    key: str
    value: str

    @classmethod
    def from_model(cls, model: Config) -> 'ConfigListResItem':
        return cls(pk=model.pk, key=model.key, value=model.value)


class ConfigListRes(BaseModel):
    items: list[ConfigListResItem]


@config.post('config-list')
def config_list():
    _ = get_req(ConfigListReq)
    configs_q = db.select(Config)
    configs = db.session.execute(configs_q).scalars().all()

    return ok(ConfigListRes(
        items=list(map(lambda x: ConfigListResItem.from_model(x), configs)))
    )


class ConfigShowReq(BaseModel):
    pk: int


class ConfigShowRes(BaseModel):
    pk: int
    key: str
    value: str


@config.post('config-show')
def config_show():
    req = get_req(ConfigShowReq)
    config_q = db.select(Config).filter(Config.pk == req.pk)
    c = db.session.execute(config_q).scalar_one_or_none()

    if c is None:
        return err('데이터가 조회되지 않습니다.')

    return ok(ConfigShowRes(pk=c.pk, key=c.key, value=c.value))
