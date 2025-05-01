import importlib
import logging
import pkgutil
import sys
from pathlib import Path
from typing import TypeVar, Type

from flask import Flask, request, g
from werkzeug.local import LocalProxy


def initialize(app: Flask) -> None:
    app.logger.setLevel(app.config.get('LOG_LEVEL', logging.INFO))
    formatter = _Formatter(fmt=None, app=app)
    for handler in logging.root.handlers:
        handler.setFormatter(formatter)

    if app.debug:
        _initialize_debug(app)


class _Formatter(logging.Formatter):
    _source_root: Path
    FORMAT = "[%(asctime)s] %(levelname)s in %(pathname)s:%(lineno)s.%(funcName)s, %(message)s"

    def __init__(self, fmt: str | None, app: Flask):
        fmt = self.FORMAT if fmt is None else fmt
        super().__init__(fmt=fmt)

        self._source_root = Path(app.root_path).resolve().parent

    def format(self, record: logging.LogRecord):
        pathname = Path(record.pathname)
        if pathname.is_relative_to(self._source_root):
            record.pathname = str(pathname.relative_to(self._source_root))
        return super().format(record)


def _initialize_debug(app: Flask):
    # 별다른 설정이 없을 경우 env 는 개발로 정의한다.
    if app.config.get('ENV') == 'production':
        app.config['ENV'] = 'development'


def load_submodules(module) -> None:
    for finder, name, is_pkg in pkgutil.iter_modules(module.__path__):
        module_name = f'{module.__name__}.{name}'
        if module_name not in sys.modules:
            child_module = importlib.import_module(module_name)
        else:
            child_module = sys.modules[module_name]

        if is_pkg:
            load_submodules(child_module)


def remote_addr() -> str | None:
    if 'CF-Connecting-IP' in request.headers and 'X-Forwarded-For' in request.headers:
        ipv6 = request.headers['CF-Connecting-IP']  # Ipv6 가 리턴 된다.
        return request.headers['X-Forwarded-For'].split(',')[0].strip()
    elif 'X-Forwarded-For' in request.headers:
        return request.headers['X-Forwarded-For'].split(',')[-1].strip()
    elif 'X-Real-Ip' in request.headers:
        return request.headers['X-Real-Ip']
    else:
        return request.remote_addr


T = TypeVar('T')


def global_proxy(name: str, builder: Type[T]) -> T:
    def f():
        if not hasattr(g, name):
            setattr(g, name, builder())
        return getattr(g, name)

    return LocalProxy(f)  # type: ignore
