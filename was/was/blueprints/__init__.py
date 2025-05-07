from uuid import UUID

from flask import Blueprint, Response, request
from sqlalchemy import func

from was.blueprints.sf.config import config
from was.blueprints.sf.sign import auth
from was.ex.api import Res, ResStatus
from was.ex.flask_ex import res_jsonify
from was.model import db
from was.model.manager import ManagerAuthentication

bp = Blueprint('blueprint', __name__, url_prefix='/sf')
bp.register_blueprint(auth)
bp.register_blueprint(config)


@bp.before_request
def before_request() -> Response | None:
    raw_access_token = request.headers.get('Authorization')
    manager_auth: ManagerAuthentication | None = None
    access_token: UUID | None = None

    if raw_access_token:
        try:
            access_token = UUID(raw_access_token)
        except ValueError:
            return res_jsonify(
                Res(data=None, errors=[], status=ResStatus.INVALID_ACCESS_TOKEN, validation_errors=[]))

    if access_token:
        auth_q = db.select(ManagerAuthentication).filter(
            ManagerAuthentication.access_token == access_token,
            ManagerAuthentication.expired_at >= func.now()
        )
        manager_auth = db.session.execute(auth_q).scalar_one_or_none()
        if manager_auth:
            manager_auth.update_expired_at()
            db.session.commit()

    if not manager_auth:
        require_access_token = True
        match ((request.endpoint or '').split('.', maxsplit=2)):
            case [_, endpoint]:
                if endpoint in ['sign_in']:
                    require_access_token = False
            case _:
                pass
        if require_access_token:
            return res_jsonify(
                Res(data=None, errors=[], status=ResStatus.INVALID_ACCESS_TOKEN, validation_errors=[]))

    return None
