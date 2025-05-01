import os

from flask import Flask, request, url_for, jsonify, Response
from flask_cors import CORS
from sqlalchemy import text
from werkzeug.middleware.proxy_fix import ProxyFix

from was import config, model
from was.blueprints import sf
from was.ex.date_ex import now
from was.ex.flask_ex import initialize, load_submodules, remote_addr
from was.model import db

app = Flask(__name__)
app.config.from_object(config)
initialize(app)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)  # type: ignore

# DB 기능 초기화
model.db.init_app(app)
load_submodules(model)
app.register_blueprint(sf)

if app.debug:
    CORS(app, supports_credentials=True, resources=[
        '*',
    ])


@app.route('/dokku/checks')
def dokku_checks():
    answer = db.session.query(text('1 + 1')).scalar()

    res = {
        'answer': answer,
        'headers': {key: val for key, val in request.headers.items()},
        'external_url': url_for('dokku_checks', _external=True),
    }

    return jsonify(res)


@app.route('/health-check')
def health_check() -> Response:
    # 현재 시간 (OS)
    os_now = now().isoformat()
    # 현재 시간 (DB)
    db_now = db.session.execute(text('SELECT now()')).scalar_one()
    db_now = db_now.astimezone().isoformat()

    alembic_version = db.session.execute(
        text('SELECT version_num FROM alembic_version LIMIT 1')
    ).scalar_one_or_none()
    if alembic_version is None:
        alembic_version = 'N/A'

    ip_address: str | None = remote_addr()

    git_commit_hash = os.getenv('GIT_REV', 'N/A')

    return jsonify({
        'os_now': os_now,
        'db_now': db_now,
        'alembic_version': alembic_version,
        'ip_address': ip_address,
        'git_commit_hash': git_commit_hash,
    })
