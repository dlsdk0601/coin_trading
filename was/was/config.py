from os import environ

from sconfig import configure

PORT = 5001
DEBUG = False
SECRET_KEY = 'ec9e23cbe277615ab4fd38f09479d5630ac79078378bb4e74b98d72ebe3acbef'
SECRET_PASSWORD_BASE_SALT = SECRET_KEY

# DB -> 한글 정렬을 위해 남겨두는데 프로젝트 기본으로 설정해두고 사용할 경우 대비해준다.
DB_COLLNAME = 'und-x-icu'

# Flask-SQLAlchemy
SQLALCHEMY_DATABASE_URI = environ.get(
    'DATABASE_URL',
    f'postgres://postgres@{environ.get("DOCKER_HOST", "localhost")}:30323/coin-trading'
)

API_URL = 'https://api.upbit.com/v1'

BINANCE_API_KEY = ''
BINANCE_API_SECRET_KEY = ''

UPBIT_ACCESS_KEY = ''
UPBIT_SECRET_KEY = ''

BOLLINGER_BAND_PERIOD = 24 * 60 * 60

IS_LOOP = False

configure(__name__)

# SALT 는 Bytes 타입이어야 한다.
SECRET_PASSWORD_BASE_SALT = bytes.fromhex(SECRET_PASSWORD_BASE_SALT)
if SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
    SQLALCHEMY_DATABASE_URI = 'postgresql://' + SQLALCHEMY_DATABASE_URI.removeprefix('postgres://')
