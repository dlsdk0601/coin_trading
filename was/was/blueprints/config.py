from was.blueprints import sf
from was.ex.api import Res, ok
from was.ex.pydantic_ex import BaseModel
from was.model import db
from was.model.config import Config


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


@sf.post('config-list')
def config_list(_: ConfigListRes) -> Res[ConfigListRes]:
    configs_q = db.select(Config)
    configs = db.session.execute(configs_q).scalars().all()

    return ok(ConfigListRes(
        items=list(map(lambda x: ConfigListResItem.from_model(x), configs)))
    )
