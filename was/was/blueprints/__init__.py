from uuid import UUID

from flask import Response, request, jsonify, session, has_request_context
from flask.sansio.blueprints import Blueprint
from sqlalchemy import func

from was.application import app
from was.ex.api import Res, ResStatus
from was.ex.flask_ex import global_proxy
from was.model import db
from was.model.manager import ManagerAuthentication, Manager


class ManagerGlobal:
    _MANAGER_AUTHENTICATION_PK = 'MANAGER_AUTHENTICATION_PK'
    _manager_authentication: ManagerAuthentication | None

    def get_manager_authentication_pk(self) -> int | None:
        return session.get(self._MANAGER_AUTHENTICATION_PK)

    def set_manager_authentication_pk(self, access_token_pk):
        session[self._MANAGER_AUTHENTICATION_PK] = access_token_pk

    @property
    def manager_authentication(self) -> ManagerAuthentication | None:
        if hasattr(self, "_manager_authentication"):
            return self._manager_authentication

        self._manager_authentication = None
        access_token = request.headers.get('Authorization')
        if access_token:
            auth_q = db.select(ManagerAuthentication).filter(
                ManagerAuthentication.access_token == access_token,
                ManagerAuthentication.expired_at >= func.now()
            )
            auth = db.session.execute(auth_q).scalar_one_or_none()
            if auth:
                self._manager_authentication = auth
                return auth
            else:
                self.set_manager_authentication_pk(None)
        return None

    @property
    def manager_or_none(self) -> Manager | None:
        if not has_request_context():
            return None
        return self.manager_authentication.manager if self.manager_authentication else None

    @property
    def manager(self) -> Manager:
        assert self.manager_or_none, '현재 요청에는 manager 가 포함 되어 있지 않다.'
        return self.manager_or_none


bg = global_proxy('manager', ManagerGlobal)

sf = Blueprint('sf', __name__, url_prefix='/sf')


@app.before_request
def before_request() -> Response | None:
    raw_access_token = request.headers.get('Authorization')
    auth: ManagerAuthentication | None = None
    access_token: UUID | None = None

    if raw_access_token:
        try:
            access_token = UUID(raw_access_token)
        except ValueError:
            return jsonify(
                Res(errors=[], status=ResStatus.INVALID_ACCESS_TOKEN, validation_errors=[]))

    if access_token:
        auth_q = db.select(ManagerAuthentication).filter(
            ManagerAuthentication.access_token == access_token,
            ManagerAuthentication.expired_at >= func.now()
        )
        auth = db.session.execute(auth_q).scalar_one_or_none()
        if auth:
            auth.update_expired_at()
            db.session.commit()

    if not auth:
        require_access_token = True
        match ((request.endpoint or '').split('.', maxsplit=2)):
            case [_, endpoint]:
                if endpoint in ['sign_in']:
                    require_access_token = False
            case _:
                pass
        if require_access_token:
            return jsonify(Res(errors=[], status=ResStatus.INVALID_ACCESS_TOKEN, validation_errors=[]))

    return None
