from enum import Enum


class LogLevel(Enum):
    DEBUG = "DEBUG"
    ERROR = "ERROR"

    def __str__(self):
        return self.value
