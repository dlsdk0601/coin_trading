import datetime
import logging
import os
from enum import auto
from logging import handlers
from unittest import case

from was.ex.enum_ex import StringEnum
from was.service.slack import send_message

class LogLevel(StringEnum):
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()

    @property
    def label(self) -> str:
        match self:
            case LogLevel.DEBUG:
                return 'DEBUG'
            case LogLevel.INFO:
                return 'INFO'
            case LogLevel.WARNING:
                return 'WARNING'
            case LogLevel.ERROR:
                return 'ERROR'
            case _:
                return ''


class Log:
    def __init__(self):
        current_path = os.getcwd()
        log_dir = os.path.join(current_path, '..', '/tmp')
        file_name = 'coin_trading.log'

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

    def info(self, message: str):
        self.logger.info(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)


    def log_call(self, func):
        def wrapper(*args, **kwargs):
            params = ', '.join([str(arg) for arg in args])
            self.info(message=f'request | {func.__name__}{(params)}')
            return func(*args, **kwargs)

        return wrapper

    def log(self, level: LogLevel, text: str, slack_send: bool = False):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f'{level}|{now}|{text}'

        match level:
            case LogLevel.INFO:
                self.info(message=message)
            case LogLevel.DEBUG:
                self.debug(message=message)
            case LogLevel.WARNING:
                self.warning(message=message)
            case LogLevel.ERROR:
                self.error(message=message)

        if slack_send:
            send_message(message=message)


log = Log()
