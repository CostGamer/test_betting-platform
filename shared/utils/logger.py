import logging
import sys

from pythonjsonlogger import jsonlogger

from shared.configs.settings import LoggingSettings

logger = logging.getLogger(__name__)


def init_logger(log_settings: LoggingSettings) -> None:
    """Initializes the logger with specified settings.

    This function configures the logger to output logs both to the console (stdout)
    and to a specified log file, with a custom JSON format. The log level, file path,
    and encoding are set according to the provided `log_settings`.

    Args:
        log_settings (LoggingSettings): Configuration settings for the logger,
                                         including log level, log file path,
                                         and log encoding.
    """
    log_level = log_settings.log_level.upper()
    log_file = log_settings.log_file
    log_encoding = log_settings.log_encoding
    log_format = "%(levelname)s %(asctime)s %(name)s %(funcName)s %(message)s"

    formatter = jsonlogger.JsonFormatter(log_format)
    stream_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler(log_file, encoding=log_encoding)
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logging.basicConfig(level=log_level, handlers=[stream_handler, file_handler])
