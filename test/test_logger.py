import unittest
from unittest.mock import MagicMock
from src.lib.logger import LogLevel, Logger

class TestLogger(unittest.TestCase):
    
    def setUp(self):
        self.logger = Logger(LogLevel.DEBUG, output=MagicMock(), width=80)
        self.logger._log = MagicMock()

    def test_info(self):
        self.logger.info("Test info message")
        self.logger._log.assert_called_with("Test info message", "blue", LogLevel.INFO)


    def test_error(self):
        self.logger.error("Test error message")
        self.logger._log.assert_called_with("Test error message", "red", LogLevel.ERROR)


    def test_debug(self):
        self.logger.debug("Test debug message")
        self.logger._log.assert_called_with("Test debug message", "cyan", LogLevel.DEBUG)
    
    def test_warn(self):
        self.logger.warn("Test warning message")
        self.logger._log.assert_called_with("Test warning message", "yellow", LogLevel.WARN)

    def test_critical(self):
        self.logger.critical("Test critical message")
        self.logger._log.assert_called_with("Test critical message", "magenta", LogLevel.CRITICAL)

    def test_add_separator(self):
        self.logger.add_seperator("green")
        self.logger._log.assert_called_with("-" * 80, "green")

if __name__ == "__main__":
    unittest.main()
