from enum import Enum
from datetime import datetime
import sys
from typing import TextIO, Optional
import os

from daedalus.logger.log_level import LogLevel

class Logger:
    name: str = ""
    level: LogLevel = LogLevel.INFO
    log_file: Optional[str] = None
    max_file_size: int = 1024 * 1024  # 1MB default
    backup_count: int = 3
    _file_handler: Optional[TextIO] = None

    @staticmethod
    def initialize(
            name: str,
            level: LogLevel = LogLevel.INFO,
            log_file: Optional[str] = None,
            max_file_size: int = 1024 * 1024,  # 1MB default
            backup_count: int = 3
    ):
        Logger.name = name
        Logger.level = level
        Logger.log_file = log_file
        Logger.max_file_size = max_file_size
        Logger.backup_count = backup_count

        if log_file:
            Logger._setup_file_handler()

    @staticmethod
    def _setup_file_handler() -> None:
        """Set up the file handler and perform log rotation if needed."""
        if Logger.log_file:
            if os.path.exists(Logger.log_file) and os.path.getsize(Logger.log_file) >= Logger.max_file_size:
                Logger._rotate_logs()
            Logger._file_handler = open(Logger.log_file, 'a')

    @staticmethod
    def _rotate_logs() -> None:
        """Rotate log files, maintaining a specified number of backups."""
        if not Logger.log_file:
            return

        for i in range(Logger.backup_count - 1, 0, -1):
            src = f"{Logger.log_file}.{i}"
            dst = f"{Logger.log_file}.{i + 1}"
            if os.path.exists(src):
                os.rename(src, dst)

        if os.path.exists(Logger.log_file):
            os.rename(Logger.log_file, f"{Logger.log_file}.1")

    @staticmethod
    def _format_message(level: LogLevel, message: str) -> str:
        """Format the log message with timestamp and level."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        return f"[{timestamp}] [{Logger.name}] [{level.name}] {message}"

    @staticmethod
    def _log(level: LogLevel, message: str) -> None:
        """Internal method to handle the actual logging."""
        if level.value < Logger.level.value:
            return

        formatted_message = Logger._format_message(level, message)

        # Console output
        print(formatted_message)

        # File output
        if Logger._file_handler:
            Logger._file_handler.write(formatted_message + '\n')
            Logger._file_handler.flush()

            # Check file size and rotate if necessary
            if os.path.getsize(Logger.log_file) >= Logger.max_file_size:
                Logger._file_handler.close()
                Logger._rotate_logs()
                Logger._setup_file_handler()

    @staticmethod
    def debug(message: str) -> None:
        """Log a debug message."""
        Logger._log(LogLevel.DEBUG, message)

    @staticmethod
    def info(message: str) -> None:
        """Log an info message."""
        Logger._log(LogLevel.INFO, message)

    @staticmethod
    def warning(message: str) -> None:
        """Log a warning message."""
        Logger._log(LogLevel.WARNING, message)

    @staticmethod
    def error(message: str) -> None:
        """Log an error message."""
        Logger._log(LogLevel.ERROR, message)

    @staticmethod
    def critical(message: str) -> None:
        """Log a critical message."""
        Logger._log(LogLevel.CRITICAL, message)

    @staticmethod
    def set_level(level: LogLevel) -> None:
        """Change the logging level."""
        Logger.level = level

    @staticmethod
    def __del__() -> None:
        """Cleanup method to ensure file handler is properly closed."""
        if Logger._file_handler:
            Logger._file_handler.close()
