from typing import Callable

from was.application import app
from was.model import db
from was.model.config import Config
from was.model.manager import Manager


def main() -> None:
    importers: list[Callable[[], None]] = [
        _import_config,
        _import_manager,
    ]

    for importer in importers:
        with app.app_context():
            print(f'import {importer.__name__.removeprefix("_import_")} ...', flush=True, end='')
            importer()
            print('done')


def _import_config() -> None:
    c = Config()
    c.key = 'emergency'
    c.value = 'false'
    db.session.add(c)
    db.session.commit()

def _import_manager() -> None:
    m = Manager()
    m.id = 'test'
    m.password_hash = Manager.hash_password('1234')
    db.session.add(m)
    db.session.commit()

if __name__ == '__main__':
    main()
