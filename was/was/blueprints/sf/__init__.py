from flask import request, session, has_request_context
from sqlalchemy import func

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
