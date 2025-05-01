from uuid import uuid4, UUID

from sqlalchemy import func

from was.blueprints import bg, sf
from was.ex.api import Res, err, ok
from was.ex.pydantic_ex import BaseModel
from was.model import db
from was.model.manager import Manager, ManagerAuthentication


class SignInReq(BaseModel):
    id: str
    password: str


class SignInRes(BaseModel):
    token: UUID


@sf.post('/sign-in')
def sign_in(req: SignInReq) -> Res[SignInRes]:
    manager_q = db.select(Manager).filter(Manager.id == req.id)
    manager: Manager | None = db.session.execute(manager_q).scalar_one_or_none()

    if not manager:
        return err('계정이 존재하지 않습니다.')

    if manager.delete_at is not None:
        return err('계정이 삭제되었습니다.')

    if manager.password_hash != Manager.hash_password(req.password):
        return err('비밀번호가 잘못되었습니다.')

    access_token = uuid4()
    auth = ManagerAuthentication()
    auth.access_token = access_token
    auth.manager = manager
    auth.update_expired_at()
    db.session.add(auth)
    db.session.commit()
    bg.set_manager_authentication_pk(auth.pk)
    return ok(SignInRes(token=access_token))


class SignOutReq(BaseModel):
    pass


class SignOutRes(BaseModel):
    pass


@sf.post('/sign-out')
def sign_out(_: SignOutReq) -> Res[SignOutRes]:
    _sign_out()
    return ok(SignOutRes())


def _sign_out():
    pk = bg.get_manager_authentication_pk()

    if not pk:
        return

    bg.set_manager_authentication_pk(None)
    token_q = db.select(ManagerAuthentication).filter(
        ManagerAuthentication.pk == pk,
        ~ManagerAuthentication.expired
    )
    token = db.session.execute(token_q).scalar_one_or_none()

    if not token:
        return

    token.expired_at = func.now()
    db.session.commit()
