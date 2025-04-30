from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

db: SQLAlchemy = SQLAlchemy(
    session_options={'autoflush': False}
)

# https://github.com/sqlalchemy/sqlalchemy2-stubs/issues/54
# Base 만 올바르게 찾기 때문에, 기본 type 지정으로 미리한다.
Base = DeclarativeBase
Base = db.Model  # type: ignore


class Model(Base):
    __abstract__ = True
