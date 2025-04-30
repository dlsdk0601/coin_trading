from datetime import datetime

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from was.model import Model


class Config(Model):
    pk: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    key: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, comment='key')
    value: Mapped[str] = mapped_column(String(64), nullable=False, comment='value')

    create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    update_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        {'comment': '환경 변수'}
    )
