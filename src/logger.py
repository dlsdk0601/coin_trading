import datetime
import logging
import os
from logging import handlers


class Log:
    def __init__(self):
        current_path = os.getcwd()
        log_dir = os.path.join(current_path, '..', '/tmp')
        file_name = 'upbit_log'

        log_formatter = logging.Formatter('%(message)s')
        log_handler = handlers.TimedRotatingFileHandler(
            filename=os.path.join(log_dir, file_name),
            when='midnight',
            interval=1,
            encoding='utf-8'
        )
        log_handler.setFormatter(log_formatter)
        log_handler.suffix = '%Y%m%d'

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(log_handler)

        self.logger = logger

    def log(self, level, *args):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = "|".join(str(arg) for arg in args)

        levels = ('TR', 'DG', 'WA')
        if level not in levels:
            self.logger.info(f'TR|{now}|Log Level Error')
        else:
            self.logger.info(f'{level}|{now}|{message}')

    def log_call(self, func):
        def wrapper(*args, **kwargs):
            params = ', '.join([str(arg) for arg in args])
            self.log('DG', 'request', f'{func.__name__}{(params)}')
            return func(*args, **kwargs)

        return wrapper


log = Log()
