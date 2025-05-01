from datetime import datetime, timedelta
from hashlib import sha3_512
from uuid import UUID

from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from was import config
from was.ex.date_ex import now
from was.model import Model


class Manager(Model):
    pk: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    id: Mapped[str] = mapped_column(String(32), nullable=False, comment='로그인 아이디')
    password_hash: Mapped[str] = mapped_column(String(512), nullable=False, comment='로그인 비밀번호 해쉬')

    create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(),
                                                comment='생성 일자')
    update_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now(), comment='수정 일자')
    delete_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), comment='삭제 일자')

    authentication = relationship('ManagerAuthentication', uselist=True, back_populates='manager')

    @staticmethod
    def hash_password(password: str) -> str:
        m = sha3_512()
        m.update(config.SECRET_PASSWORD_BASE_SALT)
        m.update(password.encode('utf-8'))
        m.update(config.SECRET_PASSWORD_BASE_SALT)
        return m.hexdigest()

    __table_args__ = (
        {'comment': '관리자'}
    )


class ManagerAuthentication(Model):
    pk: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(),
                                                comment='생성 일자')
    update_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now(), comment='수정 일자')
    manager_pk: Mapped[int] = mapped_column(ForeignKey(Manager.pk))
    manager: Mapped[Manager] = relationship(Manager, back_populates='authentication')

    access_token: Mapped[UUID] = mapped_column(postgresql.UUID(), unique=True, nullable=False, comment='토큰')
    expired_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), comment='만료 일자')

    @hybrid_property
    def expired(self) -> bool:
        return now() > self.expired_at

    def update_expired_at(self) -> None:
        self.expired_at = now() + timedelta(days=7)

    __table_args__ = (
        {'comment': '관리자 - Authentication'}
    )
