import sys
import os
from termcolor import colored
from enum import Enum

class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3
    CRITICAL = 4

class Logger:
    def __init__(self, level: LogLevel = LogLevel.DEBUG, output=sys.stdout, width=None):
        self.output = output
        self.level = level
        try:
            self.width = width if width is not None else os.get_terminal_size().columns
        except OSError:
            self.width = 80
    
    def info(self, message):
        self._log(message, 'blue', LogLevel.INFO)
    
    def warn(self, message):
        self._log(message, 'yellow', LogLevel.WARN)
    
    def error(self, message):
        self._log(message, 'red', LogLevel.ERROR)
    
    def debug(self, message):
        self._log(message, 'cyan', LogLevel.DEBUG)        

    def critical(self, message):
        self._log(message, 'magenta', LogLevel.CRITICAL)

    def add_seperator(self, color='white'):
        self._log("-" * self.width, color)

    def _log(self, message, color = "white", level = LogLevel.DEBUG ):
        if level.value >= self.level.value:
            print(colored(message, color), file=self.output)