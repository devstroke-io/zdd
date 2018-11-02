import logging

from colorama import init, Fore, Style


class Formatter(logging.Formatter):
    """Beautiful formatter for Logging.logger â€â€â€

    :rtype: Formatter
    """
    fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    styles = {
        logging.CRITICAL: Fore.RED + Style.BRIGHT + fmt + Style.RESET_ALL,
        logging.ERROR: Fore.RED + fmt + Style.RESET_ALL,
        logging.WARNING: Fore.YELLOW + fmt + Style.RESET_ALL,
        logging.INFO: Fore.CYAN + fmt + Style.RESET_ALL,
        logging.DEBUG: fmt
    }

    def __init__(self) -> None:
        super().__init__(fmt="%(levelno)d: %(msg)s", datefmt=None, style='%')
        init()

    def format(self, record: logging.LogRecord) -> str:
        """Format and return a logging.LogRecord

        :param record: The record to format
        :type record: logging.Record
        :return: The LogRecord formatted
        :rtype: str
        """
        format_orig = self._style._fmt
        self._style._fmt = self.styles.get(record.levelno, format_orig)
        result = logging.Formatter.format(self, record)
        self._style._fmt = format_orig
        return result
