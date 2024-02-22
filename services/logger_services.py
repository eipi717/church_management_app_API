from enums.logging_enums import LogLevel
from utils.logging_utils import Logger
import os


def init_loggers(path_basename: str):
    debug_logger = Logger(name=path_basename, level=str(LogLevel.DEBUG)).create_logger()
    error_logger = Logger(name=path_basename, level=str(LogLevel.ERROR)).create_logger()

    return debug_logger, error_logger