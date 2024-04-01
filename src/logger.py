import datetime
import logging
import os
from logging import handlers


def set_log(level, *args):
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

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = "|".join(str(arg) for arg in args)

    levels = ('TR', 'DG', 'WA')
    if level not in levels:
        logger.info(f'TR|{now}|Log Level Error')
    else:
        logger.info(f'{level}|{now}|{message}')
