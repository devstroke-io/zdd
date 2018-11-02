import logging

from .formatter import Formatter
from .formatter_cli import FormatterCLI


class Logger(logging.Logger):
    @classmethod
    def prepare(cls, name: str, level: int) -> logging.Logger:
        """Prepare and return a beautiful Logger instance ❀❀❀

        :param name: Name of the Logger instance
        :type name: str|int
        :param level: Logger level
        :type level: int
        :return: The Logger
        :rtype: logging.Logger
        """
        logger = logging.getLogger(name=name)
        logger.setLevel(level=level)
        # set file handler
        fmt = Formatter()
        file_log_handler = logging.FileHandler('logfile.log')
        file_log_handler.setFormatter(fmt)
        logger.addHandler(file_log_handler)
        # set stream handler
        fmt_cli = FormatterCLI()
        stream_log_handler = logging.StreamHandler()
        stream_log_handler.setFormatter(fmt_cli)
        logger.addHandler(stream_log_handler)

        # import warnings
        # warnings.filterwarnings('default')
        logging.captureWarnings(True)
        warn_logger = logging.getLogger('py.warnings')
        warn_logger.addHandler(stream_log_handler)
        warn_logger.addHandler(file_log_handler)

        return logger

    @classmethod
    def get(cls, name: str) -> logging.Logger:
        """Get a Logger instance by name

        :param name: Name of the Logger instance
        :type name: str
        :return: The Logger
        :rtype: logging.Logger
        """
        return logging.getLogger(name)
