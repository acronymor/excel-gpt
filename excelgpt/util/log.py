import logging
import os
from logging import handlers


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warn': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self, level='info'):
        fmt = '%(asctime)s %(levelname)s %(pathname)s[%(lineno)d] %(funcName)s: %(message)s'
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        log_dir = os.path.join(base_dir, "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        filename: str = os.path.join(log_dir, "excel-gpt.log")

        self.logger = logging.getLogger(filename)
        self.logger.setLevel(self.level_relations.get(level))

        th = handlers.TimedRotatingFileHandler(filename=filename, when='D', backupCount=3, encoding='utf-8')
        th.setFormatter(logging.Formatter(fmt))

        self.logger.addHandler(th)


logger = Logger(level='debug').logger
