# System imports
from datetime import datetime
import os
import sys
from enum import IntEnum
import traceback
import logging

# External imports

# User imports
from consts import debug_dir
from .singleton import singleton

##########################################################

class Logger:
    logger: logging.Logger
    log_filename: str
    name: str
    log_level: int

    def __init__(self, log_filename, name='logger', log_level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.log_filename = log_filename
        self.name = name
        self.log_level = log_level

        self._initialize_logger()

    def _initialize_logger(self):
        """ Настройка логгера """
        self.logger.setLevel(self.log_level)

        log_file = f'{debug_dir}/{self.log_filename}.log'

        if os.path.exists(log_file):
            new_filename = f'{log_file}.bkp'

            if os.path.exists(new_filename):
                os.remove(new_filename)

            os.rename(log_file, new_filename)

        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s: %(message)s',
            datefmt='%d-%m-%Y %H:%M:%S'
        )

        file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def debug(self, message: str):
        """Логирование отладочных сообщений"""
        self.logger.debug(message)

    def info(self, message: str):
        """Логирование информационных сообщений"""
        self.logger.info(message)

    def warning(self, message: str):
        """Логирование предупреждений"""
        self.logger.warning(message)

    def error(self, message: str, **kwargs):
        """Логирование ошибок"""
        self.logger.error(message, **kwargs)

    def critical(self, message: str):
        """Логирование критических ошибок"""
        self.logger.critical(message)

    def exception(self, message: str):
        """Логирование исключений с трассировкой стека"""
        self.logger.exception(message, exc_info=True)

# --------------------------------------

@singleton
class AppLogger(Logger):
    def __init__(self):
        log_filename = 'app_logger'
        name = 'app_logger'
        log_level = logging.DEBUG

        super().__init__(log_filename, name, log_level)

# --------------------------------------
