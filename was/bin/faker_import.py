from typing import Callable

from was.application import app
from was.model import db
from was.model.config import Config


def main() -> None:
    importers: list[Callable[[], None]] = [
        _import_config,
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


if __name__ == '__main__':
    main()
