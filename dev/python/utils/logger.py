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

##########################################################

class Logger:
    def __init__(self, log_filename, name='logger', log_level=logging.INFO):

        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%d-%m-%Y %H:%M:%S'
        )

        file_handler = logging.FileHandler(f'{debug_dir}/{log_filename}.log',mode='w', encoding='utf-8')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def debug(self, message):
        """Логирование отладочных сообщений"""
        self.logger.debug(message)

    def info(self, message):
        """Логирование информационных сообщений"""
        self.logger.info(message)

    def warning(self, message):
        """Логирование предупреждений"""
        self.logger.warning(message)

    def error(self, message, **kwargs):
        """Логирование ошибок"""
        self.logger.error(message, **kwargs)

    def critical(self, message):
        """Логирование критических ошибок"""
        self.logger.critical(message)

    def exception(self, message):
        """Логирование исключений с трассировкой стека"""
        self.logger.exception(message)